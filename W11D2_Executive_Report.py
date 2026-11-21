
import pandas as pd
import plotly.express as px
from pathlib import Path

# Load the Indian Business Dataset
df = pd.read_csv("data/indian_business_orders.csv")
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Calculate monthly sales
monthly_sales = (
    df.groupby(df["Order Date"].dt.to_period("M"))["Amount"]
    .sum()
    .reset_index()
)

monthly_sales["Order Date"] = (
    monthly_sales["Order Date"].dt.to_timestamp()
)

# Create an interactive Plotly chart
fig = px.line(
    monthly_sales,
    x="Order Date",
    y="Amount",
    markers=True,
    title="Monthly Sales Trend â€” Indian Business",
    labels={
        "Order Date": "Month",
        "Amount": "Sales (INR)"
    }
)

fig.update_layout(
    template="plotly_white",
    hovermode="x unified"
)

# Save the chart
Path("outputs").mkdir(exist_ok=True)
fig.write_html("outputs/w11d2_monthly_sales.html")

print("Interactive monthly sales chart created successfully!")
print("Saved to: outputs/w11d2_monthly_sales.html")


# -----------------------------------------
# Chart 2: Category-wise Sales and Profit
# -----------------------------------------

category_summary = (
    df.groupby("Category", as_index=False)
    .agg(
        Sales=("Amount", "sum"),
        Profit=("Profit", "sum")
    )
)

# Convert to long format for grouped bars
category_long = category_summary.melt(
    id_vars="Category",
    value_vars=["Sales", "Profit"],
    var_name="Metric",
    value_name="Amount"
)

fig_category = px.bar(
    category_long,
    x="Category",
    y="Amount",
    color="Metric",
    barmode="group",
    title="Category-wise Sales vs Profit",
    labels={
        "Category": "Business Category",
        "Amount": "Amount (INR)"
    },
    text_auto=".2s"
)

fig_category.update_layout(
    template="plotly_white"
)

fig_category.write_html(
    "outputs/w11d2_category_sales_profit.html"
)

print("Category-wise sales and profit chart created!")
print("Saved to: outputs/w11d2_category_sales_profit.html")
print("\nCategory performance:")
print(category_summary.to_string(index=False))


# -----------------------------------------
# Chart 3: Category-wise Profit Margin
# -----------------------------------------

category_summary["Profit Margin (%)"] = (
    category_summary["Profit"]
    / category_summary["Sales"]
    * 100
)

fig_margin = px.bar(
    category_summary,
    x="Category",
    y="Profit Margin (%)",
    color="Category",
    text="Profit Margin (%)",
    title="Profit Margin by Business Category",
    labels={
        "Profit Margin (%)": "Profit Margin (%)"
    }
)

fig_margin.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig_margin.update_layout(
    template="plotly_white",
    showlegend=False
)

fig_margin.write_html(
    "outputs/w11d2_category_profit_margin.html"
)

print("Category profit margin chart created!")
print("Saved to: outputs/w11d2_category_profit_margin.html")

print("\nCategory profit margins:")
print(
    category_summary[
        ["Category", "Profit Margin (%)"]
    ].to_string(index=False)
)


# -----------------------------------------
# Automated Executive PowerPoint Report
# -----------------------------------------

from pptx import Presentation
from pptx.util import Inches, Pt

prs = Presentation()

# Business KPIs
total_sales = df["Amount"].sum()
total_profit = df["Profit"].sum()
overall_margin = total_profit / total_sales * 100
total_orders = df["Order ID"].nunique()

# Helper function to create slides
def add_report_slide(title, lines):
    slide = prs.slides.add_slide(
        prs.slide_layouts[1]
    )
    slide.shapes.title.text = title

    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()

    for i, line in enumerate(lines):
        paragraph = (
            text_frame.paragraphs[0]
            if i == 0
            else text_frame.add_paragraph()
        )
        paragraph.text = line
        paragraph.font.size = Pt(22)

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Indian Business Executive Report"
slide.placeholders[1].text = (
    "Week 11 Day 2 | Data Analytics Internship"
)

# Slide 2: Business Summary
add_report_slide(
    "Executive Business Summary",
    [
        f"Total Sales: INR {total_sales:,.0f}",
        f"Total Profit: INR {total_profit:,.0f}",
        f"Overall Profit Margin: {overall_margin:.2f}%",
        f"Unique Orders: {total_orders}"
    ]
)

# Slide 3: Category Performance
category_lines = [
    f"{row['Category']}: "
    f"Sales INR {row['Sales']:,.0f}, "
    f"Profit INR {row['Profit']:,.0f}"
    for _, row in category_summary.iterrows()
]

add_report_slide(
    "Category-wise Business Performance",
    category_lines
)

# Slide 4: Recommendations
add_report_slide(
    "Executive Insights and Recommendations",
    [
        "Electronics generates the highest sales.",
        "Clothing generates the highest profit.",
        "Furniture has the lowest profit margin.",
        "Investigate Furniture pricing and costs.",
        "Monitor category margins monthly."
    ]
)

# Export Plotly Charts for PowerPoint

fig.write_image(
    "outputs/w11d2_monthly_sales.png",
    width=1200,
    height=650,
    scale=2
)

fig_category.write_image(
    "outputs/w11d2_category_sales_profit.png",
    width=1200,
    height=650,
    scale=2
)

fig_margin.write_image(
    "outputs/w11d2_category_profit_margin.png",
    width=1200,
    height=650,
    scale=2
)

print("\nAll three PowerPoint chart images created!")


# Add Plotly Chart Slides to PowerPoint

def add_chart_slide(title, image_path):
    slide = prs.slides.add_slide(
        prs.slide_layouts[5]
    )

    slide.shapes.title.text = title

    slide.shapes.add_picture(
        image_path,
        Inches(0.5),
        Inches(1.2),
        width=Inches(9)
    )

# Slide 5: Monthly Sales Trend
add_chart_slide(
    "Monthly Sales Trend",
    "outputs/w11d2_monthly_sales.png"
)

# Slide 6: Category Sales vs Profit
add_chart_slide(
    "Category-wise Sales and Profit",
    "outputs/w11d2_category_sales_profit.png"
)

# Slide 7: Profit Margin Comparison
add_chart_slide(
    "Category Profit Margin Analysis",
    "outputs/w11d2_category_profit_margin.png"
)

print("Three chart slides added successfully!")



# Save final PowerPoint
Path("reports").mkdir(exist_ok=True)
pptx_path = "reports/W11D2_Executive_Business_Report_v2.pptx"
prs.save(pptx_path)

print("Executive PowerPoint created successfully!")
print("Saved to:", pptx_path)
print("Total slides:", len(prs.slides))
