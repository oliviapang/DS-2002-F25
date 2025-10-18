import os
import sys
import pandas as pd

import update_portfolio
import generate_summary

def run_production_pipeline():
    """
    Run the full production pipeline:
    1) ETL via update_portfolio.main()
    2) Reporting via generate_summary.main()
    """
    print("Starting production pipeline...", file=sys.stderr)

    print("ETL Step: running update_portfolio.main()", file=sys.stderr)
    update_portfolio.main()

    print("Running generate_summary.main()", file=sys.stderr)
    generate_summary.main()

    print("Production pipeline completed.", file=sys.stderr)


if __name__ == "__main__":
    run_production_pipeline()
