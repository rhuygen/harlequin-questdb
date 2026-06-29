# harlequin-questdb

A [Harlequin](https://harlequin.sh) adapter for [QuestDB](https://questdb.io), connecting via QuestDB's PostgreSQL wire protocol.

## Installation

```bash
uv tool install harlequin --with harlequin-questdb
```

Or with pip:

```bash
pip install harlequin-questdb
```

## Upgrading

To upgrade Harlequin, the adapter, or both, run:

```bash
uv tool upgrade harlequin --with harlequin-questdb
```

This upgrades `harlequin` to the latest compatible version and refreshes `harlequin-questdb` at the same time. Run the same command regardless of which package was bumped.

## Usage

Connect to a local QuestDB instance using the defaults (host `localhost`, port `8812`, user `admin`, password `quest`):

```bash
harlequin -a questdb
```

Pass individual connection options to override the defaults:

```bash
harlequin -a questdb --host myserver --port 8812 -u myuser --password mypassword
```

Or pass a libpq-style connection string as a positional argument:

```bash
harlequin -a questdb "host=myserver port=8812 user=myuser password=mypassword dbname=qdb"
```

## Connection Options

| Option | Short | Default | Description |
|---|---|---|---|
| `--host` | `-h` | `localhost` | QuestDB host name or IP address |
| `--port` | `-p` | `8812` | PostgreSQL wire protocol port |
| `--username` | `-u` | `admin` | QuestDB username |
| `--password` | | `quest` | QuestDB password |

> **Note:** QuestDB only supports a single database named `qdb`. The `dbname` field in a connection string must be `qdb` (or omitted).
