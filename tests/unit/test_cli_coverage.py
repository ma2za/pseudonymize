import argparse
import stat
from unittest import mock

import pytest

from pseudonymize.cli import _location_payload, _read_key
from pseudonymize.document import CoordinateLocation, StructuralLocation
from pseudonymize.processing import DetectionReport
from pseudonymize.result import EntityType


def test_cli_read_key_file_permissions() -> None:
    with mock.patch("os.name", "posix"), mock.patch("pathlib.Path.stat") as mock_stat:
        # S_IMODE(st_mode) & 0o077 will be non-zero
        mock_stat.return_value.st_mode = stat.S_IRUSR | stat.S_IWUSR | stat.S_IROTH | stat.S_IWOTH
        arguments = argparse.Namespace(
            key_env=None,
            key_file=mock.Mock(),
            key_fd=None,
            text=None,
        )
        arguments.key_file.stat = mock_stat
        with pytest.raises(
            ValueError, match="key file must not be accessible by group or other users"
        ):
            _read_key(arguments)


def test_cli_unsupported_report_location() -> None:
    # Need to trigger the raise TypeError("unsupported report location")
    class FakeLocation:
        pass

    report = DetectionReport(
        entity_type=EntityType.EMAIL,
        block_id="1",
        start=0,
        end=5,
        location=FakeLocation(),  # type: ignore
        backend="rules",
        detector="email",
        confidence=1.0,
    )
    with pytest.raises(TypeError, match="unsupported report location"):
        _location_payload(report)


@pytest.mark.parametrize(
    ("location", "expected"),
    [
        (
            CoordinateLocation(page=2, x0=1.0, y0=2.0, x1=3.0, y1=4.0),
            {
                "kind": "coordinate",
                "page": 2,
                "x0": 1.0,
                "y0": 2.0,
                "x1": 3.0,
                "y1": 4.0,
            },
        ),
        (
            StructuralLocation(("slides", 1, "paragraphs", 2)),
            {"kind": "structural", "path": ("slides", 1, "paragraphs", 2)},
        ),
    ],
)
def test_cli_serializes_inspection_only_locations(
    location: CoordinateLocation | StructuralLocation, expected: dict[str, object]
) -> None:
    report = DetectionReport(
        entity_type=EntityType.EMAIL,
        block_id="block-1",
        start=0,
        end=5,
        location=location,
        backend="rules",
        detector="email",
        confidence=1.0,
    )

    assert _location_payload(report) == expected
