# 0002: Token format

Status: accepted.

Use `<PZ1:ENTITY:ALIAS>`, where `ALIAS` is the first 16 Base32 HMAC-SHA256 characters. Version,
namespace, entity type, and normalized value are NUL-separated MAC fields.
