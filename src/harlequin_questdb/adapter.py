from __future__ import annotations

from typing import Any, Sequence

import psycopg
from harlequin import HarlequinAdapter, HarlequinConnection, HarlequinCursor
from harlequin.catalog import Catalog, CatalogItem
from harlequin.exception import HarlequinConnectionError, HarlequinQueryError
from .cli_options import QuestDBAdapter_OPTIONS

# QuestDB native type names (returned by table_columns()) → short display labels
QUESTDB_TYPE_LABELS: dict[str, str] = {
    "BOOLEAN": "t/f",
    "BYTE": "#",
    "SHORT": "#",
    "INT": "##",
    "LONG": "##",
    "LONG128": "##",
    "LONG256": "##",
    "FLOAT": "#.#",
    "DOUBLE": "#.#",
    "CHAR": "s",
    "STRING": "s",
    "VARCHAR": "s",
    "SYMBOL": "sym",
    "DATE": "dt",
    "TIMESTAMP": "ts",
    "BINARY": "bin",
    "UUID": "uid",
    "GEOHASH": "geo",
    "IPv4": "ip",
}

# PostgreSQL wire protocol OIDs → short display labels (used in cursor results)
OID_TYPE_LABELS: dict[int, str] = {
    16: "t/f",  # bool
    21: "#",  # int2
    23: "##",  # int4
    20: "##",  # int8
    700: "#.#",  # float4
    701: "#.#",  # float8
    1700: "#.#",  # numeric
    25: "s",  # text
    1043: "s",  # varchar
    18: "s",  # char
    1082: "dt",  # date
    1114: "ts",  # timestamp
    1184: "tstz",  # timestamptz
    2950: "uid",  # uuid
    17: "bin",  # bytea
    114: "{}",  # json
    3802: "{}",  # jsonb
}


class QuestDBCursor(HarlequinCursor):
    def __init__(self, cur: psycopg.Cursor) -> None:  # type: ignore[type-arg]
        self._cur = cur
        self._limit: int | None = None

    def columns(self) -> list[tuple[str, str]]:
        assert self._cur.description is not None
        return [(col.name, OID_TYPE_LABELS.get(col.type_code, "?")) for col in self._cur.description]

    def set_limit(self, limit: int) -> QuestDBCursor:
        self._limit = limit
        return self

    def fetchall(self) -> list[tuple]:  # type: ignore[type-arg]
        if self._limit is not None:
            return self._cur.fetchmany(self._limit)
        return self._cur.fetchall()


class QuestDBConnection(HarlequinConnection):
    def __init__(
        self,
        conn: psycopg.Connection,  # type: ignore[type-arg]
        init_message: str = "",
    ) -> None:
        self.conn = conn
        self.init_message = init_message

    def execute(self, query: str) -> QuestDBCursor | None:
        try:
            cur = self.conn.cursor()
            cur.execute(query, prepare=False)  # type: ignore[arg-type]  # simple query protocol → text results
            if cur.description is not None:
                return QuestDBCursor(cur)
            return None
        except psycopg.Error as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="QuestDB raised an error on this query.",
            ) from e

    def get_catalog(self) -> Catalog:
        table_items: list[CatalogItem] = []
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT table_name FROM tables() ORDER BY table_name")
                table_names = [row[0] for row in cur.fetchall()]

            for table_name in table_names:
                with self.conn.cursor() as cur:
                    cur.execute(f'SELECT "column", "type" FROM table_columns(\'{table_name}\')')  # type: ignore[arg-type]
                    col_items = [
                        CatalogItem(
                            qualified_identifier=f'"{table_name}"."{col_name}"',
                            query_name=f'"{col_name}"',
                            label=col_name,
                            type_label=QUESTDB_TYPE_LABELS.get(col_type, str(col_type)[:3].lower()),
                        )
                        for col_name, col_type in cur.fetchall()
                    ]
                table_items.append(
                    CatalogItem(
                        qualified_identifier=f'"{table_name}"',
                        query_name=f'"{table_name}"',
                        label=table_name,
                        type_label="table",
                        children=col_items,
                    )
                )
        except psycopg.Error as e:
            raise HarlequinQueryError(
                msg=str(e),
                title="QuestDB raised an error loading the catalog.",
            ) from e

        return Catalog(items=table_items)

    def close(self) -> None:
        self.conn.close()


class QuestDBAdapter(HarlequinAdapter):
    ADAPTER_OPTIONS = QuestDBAdapter_OPTIONS

    def __init__(
        self,
        conn_str: Sequence[str],
        host: str = "localhost",
        port: str = "8812",
        username: str = "admin",
        password: str = "quest",
        **_: Any,
    ) -> None:
        self.conn_str = conn_str
        self.host = host
        self.port = int(port)
        self.username = username
        self.password = password

    def connect(self) -> QuestDBConnection:
        dsn = (
            self.conn_str[0]
            if self.conn_str
            else (f"host={self.host} port={self.port} user={self.username} password={self.password} dbname=qdb")
        )
        try:
            conn = psycopg.connect(dsn, autocommit=True)
        except psycopg.Error as e:
            raise HarlequinConnectionError(
                msg=str(e),
                title="QuestDB adapter could not connect.",
            ) from e
        return QuestDBConnection(
            conn,
            init_message=f"Connected to QuestDB at {self.host}:{self.port}.",
        )
