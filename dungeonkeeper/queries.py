"""Helper methods for querying player data."""

from typing import Any

import asyncpg

from dungeonkeeper.constants import Postgres


async def get_field(field: str, user_id: int) -> Any:
    """Get a field from the specified player record."""
    conn = await asyncpg.connect(dsn=Postgres.DSN)
    try:
        result = await conn.fetchval(
            f'SELECT {field} FROM dashboard_player WHERE discord_id=$1',
            user_id
        )
    finally:
        await conn.close()
    return result


async def set_field(field: str, user_id: int, value: Any) -> None:
    """Set a field on the specified player record."""
    conn = await asyncpg.connect(dsn=Postgres.DSN)
    try:
        await conn.execute(
            f'UPDATE dashboard_player SET {field}=$1 WHERE discord_id=$2',
            value, user_id
        )
    finally:
        await conn.close()


async def user_exists(user_id: int) -> bool:
    """Check if a user exists."""
    conn = await asyncpg.connect(dsn=Postgres.DSN)
    try:
        result = await conn.fetchval(
            "SELECT discord_id FROM dashboard_player WHERE discord_id=$1",
            user_id
        )
    finally:
        await conn.close()
    return result == user_id
