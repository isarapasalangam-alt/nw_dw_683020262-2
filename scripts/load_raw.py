"""Load the source CSV files into the DuckDB raw schema."""

from pathlib import Path

import duckdb


ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "northwind_dw.duckdb"

SOURCES = {
    "customer": "raw/customer.csv",
    "employees": "raw/employees.csv",
    "order_details": "raw/order_details.csv",
    "orders": "raw/orders.csv",
    "products": "raw/products.csv",
    "shippers": "raw/shippers.csv",
    "suppliers": "raw/suppliers.csv",
    "legacy_orders": "legacy/orders.csv",
    "legacy_order_details": "legacy/order_details.csv",
}


def main() -> None:
    con = duckdb.connect(str(DB_PATH))

    try:
        con.execute("CREATE SCHEMA IF NOT EXISTS raw")

        print(f"Loading data into {DB_PATH.name}")

        for table, relative_path in SOURCES.items():
            csv_path = ROOT / relative_path

            if not csv_path.is_file():
                raise FileNotFoundError(
                    f"CSV file not found: {csv_path}"
                )

            csv_path_sql = csv_path.as_posix().replace("'", "''")

            if table == "orders":
                types_sql = (
                    "{'order_date': 'DATE', "
                    "'shipped_date': 'DATE'}"
                )

                sql = f"""
                    CREATE OR REPLACE TABLE raw.{table} AS
                    SELECT *
                    FROM read_csv(
                        '{csv_path_sql}',
                        header = true,
                        types = {types_sql}
                    )
                """
            else:
                sql = f"""
                    CREATE OR REPLACE TABLE raw.{table} AS
                    SELECT *
                    FROM read_csv(
                        '{csv_path_sql}',
                        header = true
                    )
                """

            con.execute(sql)

            count = con.execute(
                f"SELECT COUNT(*) FROM raw.{table}"
            ).fetchone()[0]

            print(f"  raw.{table:<22} {count:>6,} rows")

        print("Loading completed successfully!")

    finally:
        con.close()


if __name__ == "__main__":
    main()