import os
import shutil
import tarfile
import tempfile
import zipfile
from dataclasses import replace
from pathlib import Path

from pseudonymize.document import ContentBlock, Document
from pseudonymize.engine import _extract_document, _processing_adapters
from pseudonymize.exceptions import AdapterExecutionError, UnsupportedFormatError
from pseudonymize.formats import FileFormat


def _is_safe_member(name: str) -> bool:
    return not (name.startswith(("/", "\\")) or ".." in name)


class ArchiveAdapter:
    def __init__(self, format: FileFormat) -> None:
        self.format = format
        self._temp_dir: tempfile.TemporaryDirectory[str] | None = None
        self._work_dir: Path | None = None
        self._sub_docs: dict[str, Document] = {}

    def extract(self, source: Path) -> Document:
        self._temp_dir = tempfile.TemporaryDirectory()
        self._work_dir = Path(self._temp_dir.name)

        blocks: list[ContentBlock] = []

        if self.format is FileFormat.ZIP:
            try:
                with zipfile.ZipFile(source, "r") as zf:
                    for member in zf.namelist():
                        if not _is_safe_member(member):
                            continue

                        target_path = self._work_dir / member
                        target_path.parent.mkdir(parents=True, exist_ok=True)

                        if not member.endswith("/"):
                            with zf.open(member) as f_in, open(target_path, "wb") as f_out:
                                shutil.copyfileobj(f_in, f_out)

                            self._extract_sub_doc(member, target_path, blocks)
            except zipfile.BadZipFile as e:
                raise AdapterExecutionError("failed to extract zip archive") from e
        elif self.format is FileFormat.TAR:
            try:
                with tarfile.open(source, "r:*") as tf:
                    for member_info in tf.getmembers():
                        if not _is_safe_member(member_info.name):
                            continue

                        target_path = self._work_dir / member_info.name

                        if member_info.isdir():
                            target_path.mkdir(parents=True, exist_ok=True)
                        elif member_info.isfile():
                            target_path.parent.mkdir(parents=True, exist_ok=True)
                            f_in = tf.extractfile(member_info)
                            if f_in:
                                with open(target_path, "wb") as f_out:
                                    shutil.copyfileobj(f_in, f_out)
                                f_in.close()

                                self._extract_sub_doc(member_info.name, target_path, blocks)
            except tarfile.TarError as e:
                raise AdapterExecutionError("failed to extract tar archive") from e

        return Document(str(source), tuple(blocks), {"source_path": str(source)})

    def _extract_sub_doc(
        self, member_name: str, target_path: Path, blocks: list[ContentBlock]
    ) -> None:
        try:
            in_adapter, _ = _processing_adapters(
                target_path, format=None, encoding=None, input_adapter=None, output_adapter=None
            )
            sub_doc = _extract_document(in_adapter, target_path)
            self._sub_docs[member_name] = sub_doc

            for b in sub_doc.blocks:
                new_id = f"{member_name}::{b.id}"
                blocks.append(replace(b, id=new_id))

        except (UnsupportedFormatError, AdapterExecutionError, ValueError):
            pass  # Skip unsupported or corrupt inner files

    def render(self, document: Document) -> bytes:
        if not self._work_dir:
            raise AdapterExecutionError("render called before extract")

        doc_id = document.metadata.get("source_path")
        if not isinstance(doc_id, str):
            raise AdapterExecutionError("document provenance lost")

        source = Path(doc_id)

        out_temp_dir = tempfile.TemporaryDirectory()
        out_work_dir = Path(out_temp_dir.name)

        updated_blocks = {b.id: b.text for b in document.blocks}

        def process_member(member_name: str) -> None:
            if member_name in self._sub_docs:
                assert self._work_dir is not None
                target_path = self._work_dir / member_name

                # We need to run extract again during render so the out_adapter builds its internal state
                in_adapter, out_adapter = _processing_adapters(
                    target_path, format=None, encoding=None, input_adapter=None, output_adapter=None
                )
                sub_doc = _extract_document(in_adapter, target_path)

                new_sub_blocks = []
                for b in sub_doc.blocks:
                    ident = f"{member_name}::{b.id}"
                    new_text = updated_blocks.get(ident, b.text)
                    new_sub_blocks.append(replace(b, text=new_text))

                new_sub_doc = replace(sub_doc, blocks=tuple(new_sub_blocks))

                rendered_bytes = out_adapter.render(new_sub_doc)

                out_path = out_work_dir / member_name
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(rendered_bytes)
            else:
                assert self._work_dir is not None
                old_path = self._work_dir / member_name
                out_path = out_work_dir / member_name
                out_path.parent.mkdir(parents=True, exist_ok=True)
                if old_path.exists() and old_path.is_file():
                    shutil.copy2(old_path, out_path)

        out_archive_path = out_work_dir / f"archive.{self.format.value}"
        res = b""

        if self.format is FileFormat.ZIP:
            with zipfile.ZipFile(source, "r") as zf:
                for member in zf.namelist():
                    if not _is_safe_member(member):
                        continue
                    if not member.endswith("/"):
                        process_member(member)

            with zipfile.ZipFile(out_archive_path, "w", zipfile.ZIP_DEFLATED) as zf_out:
                for root, _, files in os.walk(out_work_dir):
                    for file in files:
                        f_path = Path(root) / file
                        if f_path == out_archive_path:
                            continue
                        arcname = str(f_path.relative_to(out_work_dir)).replace("\\", "/")
                        zf_out.write(f_path, arcname)

            res = out_archive_path.read_bytes()

        elif self.format is FileFormat.TAR:
            with tarfile.open(source, "r:*") as tf:
                for member_info in tf.getmembers():
                    if not _is_safe_member(member_info.name):
                        continue
                    if member_info.isfile():
                        process_member(member_info.name)

            mode = "w"
            if source.suffix == ".gz" or source.suffix == ".tgz":
                mode = "w:gz"
            elif source.suffix == ".bz2":
                mode = "w:bz2"

            with tarfile.open(str(out_archive_path), mode) as tf_out:
                for root, _, files in os.walk(out_work_dir):
                    for file in files:
                        f_path = Path(root) / file
                        if f_path == out_archive_path:
                            continue
                        arcname = str(f_path.relative_to(out_work_dir)).replace("\\", "/")
                        tf_out.add(f_path, arcname=arcname)
            res = out_archive_path.read_bytes()

        out_temp_dir.cleanup()
        if self._temp_dir:
            self._temp_dir.cleanup()
            self._work_dir = None
            self._sub_docs = {}

        return res
