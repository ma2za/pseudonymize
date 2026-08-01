# Compatibility policy

`0.1.0b1` freezes the dependency-free core API for the first stable release. The supported public
surface is the set of names exported by `pseudonymize.__all__`, their documented constructors and
methods, the `pseudonymize` command-line interface, and the documented token formats.

## Beta to stable

From `0.1.0b1` through `0.1.0`, releases preserve documented behavior and accepted inputs. A change
that would require application code to be rewritten returns the project to a new beta series.
Release candidates accept only release-blocking fixes.

Security fixes may reject input that was previously accepted when accepting it would violate a
documented safety invariant. Such changes are called out prominently in release notes.

## Stable `0.1` line

After `0.1.0`, patch releases preserve the public API and token format. New optional parameters,
methods, entity types, file formats, and additive report fields may appear in a minor release.
Removing or renaming public names, changing defaults, weakening safety guarantees, or changing a
deterministic token for the same normalized input requires a later incompatible release.

Private modules, names beginning with an underscore, exception message wording, formatting of
object representations, normalized JSON/JSONL/CSV whitespace, and undocumented detector
implementation details are not compatibility contracts.

## Supported environments

The stable line supports the Python versions declared in package metadata and tested in CI. When a
Python version reaches end of life, a future minor release may stop supporting it. The base wheel
remains typed, dependency-free, and free of import-time network or model activity throughout the
`0.1` line.
