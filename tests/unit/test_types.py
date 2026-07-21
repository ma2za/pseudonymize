import pytest

from pseudonymize import Detection, EntityType


def test_detection_validates_offsets_and_confidence() -> None:
    with pytest.raises(ValueError, match="non-empty"):
        Detection(EntityType.EMAIL, 1, 1, 0.9, "email")
    with pytest.raises(ValueError, match="confidence"):
        Detection(EntityType.EMAIL, 0, 1, 1.1, "email")
