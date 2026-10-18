
import csv
import json
from collections import defaultdict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "merged_orders_cleaned.csv"
OUTPUT_FILE = BASE_DIR / "w7d3_dashboard.html"


def main():
    if not DATA_FILE.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_FILE}")

    category_sales = defaultdict(float)
    category_profit = defaultdict(float)
    city_sales = defaultdict(float)
    monthly_sales = defaultdict(float)
    total_sales = 0.0
    total_profit = 0.0
    total_quantity = 0
    loss_rows = 0
    row_count = 0
    customers = set()

    with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {
            "Amount", "Profit", "Quantity", "Category",
            "City", "Order Date", "CustomerName"
        }
        missing = required - set(reader.fieldnames or [])
        if missing:
            raise ValueError(f"Missing required columns: {sorted(missing)}")

        for row in reader:
            amount = float(row["Amount"] or 0)
            profit = float(row["Profit"] or 0)
            quantity = int(float(row["Quantity"] or 0))

            category = (row["Category"] or "Unknown").strip()
            city = (row["City"] or "Unknown").strip()
            customer = (row["CustomerName"] or "").strip()
            order_date = (row["Order Date"] or "").strip()

            category_sales[category] += amount
            category_profit[category] += profit
            city_sales[city] += amount

            if len(order_date) >= 7:
                monthly_sales[order_date[:7]] += amount

            total_sales += amount
            total_profit += profit
            total_quantity += quantity
            row_count += 1

            if profit < 0:
                loss_rows += 1
            if customer:
                customers.add(customer)

    data = {
        "categorySales": [
            {"name": key, "value": round(value, 2)}
            for key, value in sorted(
                category_sales.items(), key=lambda item: item[1], reverse=True
            )
        ],
        "categoryProfit": [
            {"name": key, "value": round(value, 2)}
            for key, value in sorted(
                category_profit.items(), key=lambda item: item[1], reverse=True
            )
        ],
        "citySales": [
            {"name": key, "value": round(value, 2)}
            for key, value in sorted(
                city_sales.items(), key=lambda item: item[1], reverse=True
            )[:10]
        ],
        "monthlySales": [
            {"name": key, "value": round(value, 2)}
            for key, value in sorted(monthly_sales.items())
        ],
    }

    # Embed JSON safely inside the HTML script.
    data_json = json.dumps(data, ensure_ascii=False)
    data_json = (
        data_json.replace("<", "\\u003c")
        .replace(">", "\\u003e")
        .replace("&", "\\u0026")
    )

    template = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>W7D3 | Indian Retail Analytics Dashboard</title>
<script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/echarts@5.5.1/dist/echarts.min.js"></script>
<style>
* { box-sizing: border-box; }
body {
  margin: 0; padding: 24px;
  background: #f3f6fb; color: #182230;
  font-family: "Segoe UI", Arial, sans-serif;
}
header { margin: 0 auto 24px; max-width: 1400px; }
h1 { margin-bottom: 6px; }
.subtitle { color: #637083; }
.kpis {
  display: grid; grid-template-columns: repeat(4, minmax(150px, 1fr));
  gap: 16px; max-width: 1400px; margin: auto auto 20px;
}
.kpi, .chart-card {
  background: white; border: 1px solid #e3e8f0;
  border-radius: 12px; box-shadow: 0 3px 12px #14243a0a;
}
.kpi { padding: 20px; }
.kpi span { display: block; color: #637083; font-size: 14px; }
.kpi strong { display: block; margin-top: 8px; font-size: 26px; }
.grid {
  max-width: 1400px; margin: auto;
  display: grid; grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 18px;
}
.chart-card { padding: 16px; min-width: 0; }
.chart-card h2 { margin: 4px 0 8px; font-size: 18px; }
.chart { height: 360px; width: 100%; }
.status { max-width: 1400px; margin: 10px auto; color: #637083; }
footer { max-width: 1400px; margin: 20px auto; color: #637083; font-size: 13px; }
@media (max-width: 800px) {
  body { padding: 12px; }
  .kpis { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .grid { grid-template-columns: 1fr; }
}
</style>
</head>
<body>
<header>
  <h1>Indian Retail Analytics</h1>
  <div class="subtitle">W7D3 — Interactive charts with Plotly and ECharts</div>
</header>

<section class="kpis">
  <div class="kpi"><span>Total Sales</span><strong>₹__TOTAL_SALES__</strong></div>
  <div class="kpi"><span>Total Profit</span><strong>₹__TOTAL_PROFIT__</strong></div>
  <div class="kpi"><span>Quantity Sold</span><strong>__TOTAL_QUANTITY__</strong></div>
  <div class="kpi"><span>Rows With Negative Profit</span><strong>__LOSS_ROWS__ / __ROW_COUNT__</strong></div>
</section>

<div id="status" class="status">
  Loading interactive charts. An internet connection is needed for the chart libraries.
</div>

<main class="grid">
  <section class="chart-card">
    <h2>Sales by Category · Plotly</h2>
    <div id="categorySales" class="chart"></div>
  </section>
  <section class="chart-card">
    <h2>Profit by Category · Plotly</h2>
    <div id="categoryProfit" class="chart"></div>
  </section>
  <section class="chart-card">
    <h2>Top 10 Cities by Sales · ECharts</h2>
    <div id="citySales" class="chart"></div>
  </section>
  <section class="chart-card">
    <h2>Monthly Sales · ECharts</h2>
    <div id="monthlySales" class="chart"></div>
  </section>
</main>

<footer>
  Source: merged_orders_cleaned.csv. Hover over chart marks for values.
  Totals are calculated in Python from the input data.
</footer>

<script>
const DATA = __DATA_JSON__;

function money(value) {
  return "₹" + Number(value).toLocaleString("en-IN", {
    maximumFractionDigits: 0
  });
}

function drawCharts() {
  if (typeof Plotly === "undefined" || typeof echarts === "undefined") {
    document.getElementById("status").textContent =
      "Chart libraries could not load. Check your internet connection and refresh this page.";
    return;
  }

  const plotLayout = {
    autosize: true,
    margin: {l: 55, r: 20, t: 18, b: 60},
    paper_bgcolor: "white",
    plot_bgcolor: "white",
    font: {family: "Segoe UI, Arial", color: "#334155"},
    yaxis: {gridcolor: "#e9eef5", tickprefix: "₹"},
    xaxis: {tickangle: -15, automargin: true}
  };

  Plotly.newPlot("categorySales", [{
    x: DATA.categorySales.map(d => d.name),
    y: DATA.categorySales.map(d => d.value),
    type: "bar",
    marker: {color: "#4976d0"},
    hovertemplate: "%{x}<br>Sales: %{y:,.0f}<extra></extra>"
  }], {
    ...plotLayout,
    yaxis: {...plotLayout.yaxis, title: "Sales"}
  }, {responsive: true, displaylogo: false});

  Plotly.newPlot("categoryProfit", [{
    x: DATA.categoryProfit.map(d => d.name),
    y: DATA.categoryProfit.map(d => d.value),
    type: "bar",
    marker: {color: "#249b79"},
    hovertemplate: "%{x}<br>Profit: %{y:,.0f}<extra></extra>"
  }], {
    ...plotLayout,
    yaxis: {...plotLayout.yaxis, title: "Profit", tickprefix: "₹"}
  }, {responsive: true, displaylogo: false});

  const cityChart = echarts.init(document.getElementById("citySales"));
  const cities = [...DATA.citySales].reverse();
  cityChart.setOption({
    tooltip: {trigger: "axis", axisPointer: {type: "shadow"},
      valueFormatter: value => money(value)},
    grid: {left: 95, right: 28, top: 20, bottom: 30},
    xAxis: {type: "value", axisLabel: {formatter: value => "₹" + value.toLocaleString("en-IN")}},
    yAxis: {type: "category", data: cities.map(d => d.name)},
    dataZoom: [{type: "inside", yAxisIndex: 0}],
    series: [{
      name: "Sales", type: "bar",
      data: cities.map(d => d.value),
      itemStyle: {color: "#e5a33d", borderRadius: [0, 5, 5, 0]}
    }]
  });

  const monthlyChart = echarts.init(document.getElementById("monthlySales"));
  monthlyChart.setOption({
    tooltip: {trigger: "axis", valueFormatter: value => money(value)},
    grid: {left: 68, right: 25, top: 25, bottom: 55},
    xAxis: {
      type: "category", boundaryGap: false,
      data: DATA.monthlySales.map(d => d.name),
      axisLabel: {rotate: 35}
    },
    yAxis: {type: "value", axisLabel: {formatter: value => "₹" + value.toLocaleString("en-IN")}},
    dataZoom: [{type: "inside"}, {type: "slider", bottom: 5, height: 16}],
    series: [{
      name: "Monthly Sales", type: "line", smooth: true,
      data: DATA.monthlySales.map(d => d.value),
      showSymbol: true,
      lineStyle: {width: 3, color: "#7b61b5"},
      itemStyle: {color: "#7b61b5"},
      areaStyle: {opacity: 0.12, color: "#7b61b5"}
    }]
  });

  window.addEventListener("resize", () => {
    Plotly.Plots.resize("categorySales");
    Plotly.Plots.resize("categoryProfit");
    cityChart.resize();
    monthlyChart.resize();
  });

  document.getElementById("status").textContent =
    "Charts loaded. Hover over bars and points; use zoom controls where available.";
}

drawCharts();
</script>
</body>
</html>
"""

    replacements = {
        "__DATA_JSON__": data_json,
        "__TOTAL_SALES__": f"{total_sales:,.0f}",
        "__TOTAL_PROFIT__": f"{total_profit:,.0f}",
        "__TOTAL_QUANTITY__": f"{total_quantity:,}",
        "__LOSS_ROWS__": f"{loss_rows:,}",
        "__ROW_COUNT__": f"{row_count:,}",
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)

    OUTPUT_FILE.write_text(template, encoding="utf-8")
    print(f"Loaded {row_count:,} rows from {DATA_FILE.name}")
    print(f"Total sales: ₹{total_sales:,.2f}")
    print(f"Total profit: ₹{total_profit:,.2f}")
    print(f"Quantity sold: {total_quantity:,}")
    print(f"Rows with negative profit: {loss_rows:,}")
    print(f"Dashboard created: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
