"""Run a SQL query against the project DuckDB database."""

import argparse
from pathlib import Path

import duckdb
from tabulate import tabulate


DB_PATH = Path(__file__).resolve().parent.parent / "northwind_dw.duckdb"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("sql", help="SQL statement to execute")
    args = parser.parse_args()

    con = duckdb.connect(str(DB_PATH), read_only=True)
    try:
        result = con.execute(args.sql)
        if result.description is None:
            return

        columns = [column[0] for column in result.description]
        rows = result.fetchall()
        print(tabulate(rows, headers=columns, tablefmt="plain", missingval=""))
        print(f"({len(rows)} rows)")
    finally:
        con.close()


if __name__ == "__main__":
    main()
