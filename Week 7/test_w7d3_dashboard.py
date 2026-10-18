
import csv
import unittest
from decimal import Decimal
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "merged_orders_cleaned.csv"
HTML_FILE = BASE_DIR / "w7d3_dashboard.html"


class W7D3DashboardTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with DATA_FILE.open("r", newline="", encoding="utf-8-sig") as file:
            cls.rows = list(csv.DictReader(file))
        cls.html = HTML_FILE.read_text(encoding="utf-8")

    def test_dataset_shape(self):
        self.assertEqual(len(self.rows), 1500)
        self.assertEqual(len(self.rows[0]), 17)

    def test_business_metrics(self):
        total_sales = sum(Decimal(row["Amount"]) for row in self.rows)
        total_profit = sum(Decimal(row["Profit"]) for row in self.rows)
        total_quantity = sum(int(float(row["Quantity"])) for row in self.rows)
        loss_rows = sum(Decimal(row["Profit"]) < 0 for row in self.rows)

        self.assertEqual(total_sales, Decimal("431502.0"))
        self.assertEqual(total_profit, Decimal("23955.0"))
        self.assertEqual(total_quantity, 5615)
        self.assertEqual(loss_rows, 503)

    def test_plotly_charts_present(self):
        self.assertIn('Plotly.newPlot("categorySales"', self.html)
        self.assertIn('Plotly.newPlot("categoryProfit"', self.html)

    def test_echarts_present(self):
        self.assertIn('echarts.init(document.getElementById("citySales"))', self.html)
        self.assertIn('echarts.init(document.getElementById("monthlySales"))', self.html)

    def test_all_chart_containers_present(self):
        for chart_id in (
            "categorySales",
            "categoryProfit",
            "citySales",
            "monthlySales",
        ):
            self.assertIn(f'id="{chart_id}"', self.html)


if __name__ == "__main__":
    unittest.main(verbosity=2)

