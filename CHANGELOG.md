# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.3.0] - 2026-06-29

### Fixed

- Automatic reconnection when QuestDB closes an idle connection. `QuestDBConnection` now stores the DSN and transparently reconnects on `OperationalError` before retrying the query.

## [0.2.0] - 2026-06-29

### Added

- `connection_id` property on `QuestDBAdapter` for stable catalog and history caching.

## [0.1.0] - 2026-06-27

### Added

- Initial adapter implementation connecting to QuestDB via the PostgreSQL wire protocol (`psycopg`).
- CLI options: `--host`, `--port`, `--username`, `--password` with QuestDB defaults.
- Catalog browser populated via QuestDB's `tables()` and `table_columns()` SQL functions.
- Type label mappings for QuestDB-native types (catalog) and PostgreSQL wire protocol OIDs (query results).

[Unreleased]: https://github.com/tRik/harlequin-questdb/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/tRik/harlequin-questdb/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/tRik/harlequin-questdb/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/tRik/harlequin-questdb/releases/tag/v0.1.0
