from pathlib import Path
import logging
import html

import pandas as pd
from autoviz.AutoViz_Class import AutoViz_Class
from ydata_profiling import ProfileReport
import sweetviz as sv


# ---------- Paths and logging ----------

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "merged_orders_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "reports"
AUTOVIZ_DIR = OUTPUT_DIR / "autoviz"

OUTPUT_DIR.mkdir(exist_ok=True)
AUTOVIZ_DIR.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    filename=OUTPUT_DIR / "w7d2_errors.log",
    level=logging.ERROR,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def write_autoviz_index():
    """Create an index linking to generated AutoViz HTML charts."""
    files = sorted(AUTOVIZ_DIR.rglob("*.html"))

    links = "\n".join(
        "<li><a href='autoviz/{}'>{}</a></li>".format(
            html.escape(path.relative_to(AUTOVIZ_DIR).as_posix()),
            html.escape(path.name),
        )
        for path in files
        if path.name.lower() != "index.html"
    )

    if not links:
        links = "<li>No AutoViz HTML charts were found. Check the error log.</li>"

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>W7D2 AutoViz Report</title>
<style>
body {{ font-family: Arial, sans-serif; max-width: 900px;
       margin: 40px auto; line-height: 1.6; }}
h1 {{ color: #17365d; }}
</style>
</head>
<body>
<h1>W7D2: AutoViz Exploratory Data Analysis</h1>
<p>Dataset: merged_orders_cleaned.csv</p>
<p>Rows: 1,500 | Columns: 17</p>
<h2>Generated interactive charts</h2>
<ul>{links}</ul>
</body>
</html>"""

    (OUTPUT_DIR / "autoviz_report.html").write_text(
        page, encoding="utf-8"
    )
    print(f"AutoViz index saved: {OUTPUT_DIR / 'autoviz_report.html'}")


def write_insights(df):
    """Calculate business insights independently with Pandas."""
    category_sales = (
        df.groupby("Category")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )
    category_profit = df.groupby("Category")["Profit"].sum()
    total_sales = float(df["Amount"].sum())
    total_profit = float(df["Profit"].sum())

    city_sales = (
        df.groupby("City")["Amount"]
        .sum()
        .sort_values(ascending=False)
        .head(5)
    )

    negative_count = int((df["Profit"] < 0).sum())
    negative_pct = negative_count / len(df) * 100

    # Check for unnecessary leading/trailing whitespace in text fields.
    whitespace_counts = {}
    for column in df.select_dtypes(include="object").columns:
        values = df[column].dropna().astype(str)
        count = int((values != values.str.strip()).sum())
        if count:
            whitespace_counts[column] = count

    best_sales_category = category_sales.index[0]
    best_profit_category = category_profit.idxmax()
    lowest_profit_category = category_profit.idxmin()

    best_profit_margin = (
        category_profit[best_profit_category]
        / category_sales[best_profit_category] * 100
    )
    lowest_profit_margin = (
        category_profit[lowest_profit_category]
        / category_sales[lowest_profit_category] * 100
    )

    lines = [
        "# W7D2 — Automated EDA: Business Insights",
        "",
        "## Dataset overview",
        f"- Rows: {len(df):,}",
        f"- Columns: {len(df.columns)}",
        f"- Total sales amount: {total_sales:,.2f}",
        f"- Total profit: {total_profit:,.2f}",
        "",
        "## Three business insights",
        "",
        f"### 1. {best_sales_category} leads sales",
        (
            f"{best_sales_category} has the highest category sales at "
            f"{category_sales[best_sales_category]:,.2f}, representing "
            f"{category_sales[best_sales_category] / total_sales * 100:.1f}% "
            "of total sales."
        ),
        "",
        f"### 2. {best_profit_category} leads total profit",
        (
            f"{best_profit_category} generates the highest category profit "
            f"({category_profit[best_profit_category]:,.2f}) with a "
            f"profit-to-sales ratio of {best_profit_margin:.1f}%. "
            f"{lowest_profit_category} generates only "
            f"{category_profit[lowest_profit_category]:,.2f} profit "
            f"({lowest_profit_margin:.1f}% of its sales), so its costs, "
            "pricing, and discounting deserve further review."
        ),
        "",
        "### 3. Negative-profit records need attention",
        (
            f"{negative_count:,} of {len(df):,} rows "
            f"({negative_pct:.1f}%) have negative profit. Investigate the "
            "loss-making transactions by category, sub-category, and city "
            "before making pricing or supplier decisions."
        ),
        "",
        "## Top five cities by sales",
        "",
        "| City | Sales amount |",
        "|---|---:|",
    ]

    for city, value in city_sales.items():
        lines.append(f"| {city} | {value:,.2f} |")

    lines += ["", "## Text data quality checks", ""]

    if whitespace_counts:
        lines.append(
            "Leading/trailing whitespace was detected in these text columns:"
        )
        for column, count in whitespace_counts.items():
            lines.append(f"- `{column}`: {count} value(s)")
        lines.append(
            "\nStandardize whitespace before grouping or comparing these fields."
        )
    else:
        lines.append("No leading/trailing whitespace was detected in text fields.")

    lines += [
        "",
        "## Method",
        (
            "These figures were calculated using Pandas groupby and aggregation. "
            "The HTML profiling tools are used to explore distributions and "
            "data-quality patterns; key business totals should still be "
            "validated independently."
        ),
        "",
    ]

    (OUTPUT_DIR / "w7d2_insights.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )
    print(f"Insights saved: {OUTPUT_DIR / 'w7d2_insights.md'}")


def write_comparison():
    """Write a 100-word AutoViz vs SweetViz comparison."""
    comparison = (
        "AutoViz automatically generates a broad set of charts with little "
        "setup and is useful for analysts who want to quickly scan numeric "
        "and categorical relationships. Its interactive HTML output is "
        "convenient to explore but can produce several separate files and "
        "may need interpretation. SweetViz packages distributions, "
        "associations, and variable summaries into a polished, single HTML "
        "report that is easier to share with non-technical stakeholders. "
        "SweetViz is more presentation-friendly, while AutoViz offers "
        "flexible chart generation for exploratory work. Neither replaces "
        "data validation or business context. For this dataset, I recommend "
        "SweetViz for stakeholder review and AutoViz for analyst-led follow-up "
        "and investigation."
    )

    recommendation = (
        "\n\n## Recommendation\n\n"
        "Recommend SweetViz for the initial business-stakeholder review "
        "because its single HTML report is straightforward to share. Use "
        "AutoViz for analyst-led exploration and ydata-profiling for a "
        "more detailed check of distributions, correlations, and data quality. "
        "Validate all important findings with Pandas before presenting them."
    )

    content = (
        "# W7D2 — AutoViz vs SweetViz\n\n"
        "## Comparison (100 words)\n\n"
        + comparison
        + "\n"
        + recommendation
        + "\n"
    )

    (OUTPUT_DIR / "w7d2_tool_comparison.md").write_text(
        content, encoding="utf-8"
    )
    print(f"Comparison saved: {OUTPUT_DIR / 'w7d2_tool_comparison.md'}")


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    df = pd.read_csv(DATA_FILE)
    print(f"Loaded dataset: {df.shape[0]} rows × {df.shape[1]} columns")

    # Save insights and comparison independently of report generation.
    write_insights(df)
    write_comparison()

    # 1. AutoViz interactive HTML charts.
    print("\n[1/3] Running AutoViz. This may take a few minutes...")
    try:
        visualizer = AutoViz_Class()
        visualizer.AutoViz(
            filename=str(DATA_FILE),
            sep=",",
            depVar="",
            dfte=None,
            header=0,
            verbose=2,
            lowess=False,
            chart_format="html",
            max_rows_analyzed=150000,
            max_cols_analyzed=30,
            save_plot_dir=str(AUTOVIZ_DIR),
        )
        print("AutoViz finished.")
    except Exception:
        logging.exception("AutoViz report generation failed.")
        print("AutoViz failed. See reports/w7d2_errors.log.")
    finally:
        write_autoviz_index()

    # 2. ydata-profiling HTML report.
    print("\n[2/3] Running ydata-profiling...")
    try:
        profile = ProfileReport(
            df,
            title="W7D2 Indian Retail Dataset - ydata-profiling",
            explorative=True,
        )
        profile.to_file(OUTPUT_DIR / "ydata_profiling_report.html")
        print("ydata-profiling report saved.")
    except Exception:
        logging.exception("ydata-profiling report generation failed.")
        print("ydata-profiling failed. See reports/w7d2_errors.log.")

    # 3. SweetViz HTML report.
    print("\n[3/3] Running SweetViz...")
    try:
        report = sv.analyze(df)
        report.show_html(
            filepath=str(OUTPUT_DIR / "sweetviz_report.html"),
            open_browser=False,
        )
        print("SweetViz report saved.")
    except Exception:
        logging.exception("SweetViz report generation failed.")
        print("SweetViz failed. See reports/w7d2_errors.log.")

    print("\nW7D2 report generation finished.")
    print(f"Open the reports here: {OUTPUT_DIR}")
    print("Check the error log if any tool failed.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logging.exception("W7D2 script stopped unexpectedly.")
        raise
