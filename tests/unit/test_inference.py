from pseudonymize.document import ContentBlock, CSVCellLocation, Document
from pseudonymize.engine import Pseudonymizer
from pseudonymize.inference import TabularInferenceLayout
from pseudonymize.result import EntityType


def test_csv_tabular_inference() -> None:
    blocks = (
        ContentBlock("r0c0", "ssn", CSVCellLocation(0, 0)),
        ContentBlock("r0c1", "name", CSVCellLocation(0, 1)),
        ContentBlock("r1c0", "999-99-9999", CSVCellLocation(1, 0)),
        ContentBlock("r1c1", "John Doe", CSVCellLocation(1, 1)),
    )
    document = Document("test", blocks, {})
    layout = TabularInferenceLayout(document)

    assert layout.csv_semantics[0] == EntityType.NATIONAL_ID
    assert layout.csv_semantics[1] == EntityType.PERSON

    d0 = layout.extract_csv_detections(blocks[2])
    assert len(d0) == 1
    assert d0[0].entity_type == EntityType.NATIONAL_ID
    assert d0[0].start == 0
    assert d0[0].end == 11

    d1 = layout.extract_csv_detections(blocks[3])
    assert len(d1) == 1
    assert d1[0].entity_type == EntityType.PERSON


def test_engine_csv_tabular_inference() -> None:
    engine = Pseudonymizer()
    blocks = (
        ContentBlock("r0c0", "phone_number", CSVCellLocation(0, 0)),
        ContentBlock("r1c0", "555-0199", CSVCellLocation(1, 0)),
    )
    document = Document("test", blocks, {})
    result = engine.process_document(document)

    # Check detections
    phone_detections = [d for d in result.detections if d.entity_type == EntityType.PHONE]
    assert len(phone_detections) >= 1
    assert any(d.detector == "tabular" for d in phone_detections)
