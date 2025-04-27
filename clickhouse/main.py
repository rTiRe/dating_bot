import clickhouse_connect
import asyncio


async def main():
    client = await clickhouse_connect.get_async_client(host="localhost", port=8123, username="default", password="")
    await client.command("CREATE TABLE IF NOT EXISTS test (id UInt64, name String) ENGINE = MergeTree() ORDER BY id")
    await client.command("INSERT INTO test (id, name) VALUES (1, 'John')")


if __name__ == "__main__":
    asyncio.run(main())
