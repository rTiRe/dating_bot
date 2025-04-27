import asyncio
import clickhouse_connect

async def main():
    client = await clickhouse_connect.get_async_client(
        host="localhost",
        port=8123,
        username="default",
        password="default"
    )

    # 1. Use `query()`, not the summary API
    result = await client.query("SELECT * FROM dating.interactions LIMIT 10")
    # result is a QueryResult object

    # 2. Inspect rows and columns
    print("Columns:", result.column_names)    # e.g. ['event_time','liker_id','liked_id','interaction_type']
    for row in result.result_set:              # result_set is a list of tuples
        print(row)

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())
