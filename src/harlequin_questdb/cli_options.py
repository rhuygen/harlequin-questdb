from harlequin.options import (
    HarlequinAdapterOption,  # noqa
    ListOption,  # noqa
    PathOption,  # noqa
    SelectOption,  # noqa
    TextOption,
)

QuestDBAdapter_OPTIONS: list[HarlequinAdapterOption] = [
    TextOption(
        name="host",
        description="The QuestDB host name or IP address.",
        short_decls=["-h"],
        default="localhost",
    ),
    TextOption(
        name="port",
        description="The port for QuestDB's PostgreSQL wire protocol.",
        short_decls=["-p"],
        default="8812",
    ),
    TextOption(
        name="username",
        description="The QuestDB username.",
        short_decls=["-u"],
        default="admin",
    ),
    TextOption(
        name="password",
        description="The QuestDB password.",
        default="quest",
    ),
]
