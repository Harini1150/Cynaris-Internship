import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from w7d4_vanna_sql_analyst import ReadOnlyMySQLRunner
from vanna.capabilities.sql_runner.models import RunSqlToolArgs
from w7d4_sql_safety import UnsafeSQLQuery

async def main():
    runner = object.__new__(ReadOnlyMySQLRunner)

    try:
        await runner.run_sql(
            RunSqlToolArgs(sql="DELETE FROM customers"),
            None,
        )
    except UnsafeSQLQuery:
        print("PASS: unsafe SQL blocked before database execution")
    else:
        raise AssertionError("Unsafe SQL was not blocked")

if __name__ == "__main__":
    asyncio.run(main())
