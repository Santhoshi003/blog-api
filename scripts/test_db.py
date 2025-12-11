import asyncio
from app.db.session import engine

async def test_connect():
    async with engine.begin() as conn:
        # simple no-op to ensure we can connect
        await conn.run_sync(lambda sync_conn: None)
    print("DB connection OK")

asyncio.run(test_connect())
