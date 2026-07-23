# 0004: Optional NER backend

Status: accepted.

The core exposes a block-aware `DetectionBackend` protocol but selects and downloads no model. A
future backend must document licence, revision, checksum, multilingual quality, memory, and cold
and warm latency.
