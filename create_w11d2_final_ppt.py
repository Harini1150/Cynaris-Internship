
from pathlib import Path
import pandas as pd
from pptx import Presentation
from pptx.util import Inches, Pt

# Load business dataset
df = pd.read_csv("data/indian_business_orders.csv")

total_sales = df["Amount"].sum()
total_profit = df["Profit"].sum()
profit_margin = (total_profit / total_sales) * 100
total_orders = df["Order ID"].nunique()

category = df.groupby("Category")[["Amount", "Profit"]].sum()

# Create PowerPoint
prs = Presentation()

def add_text_slide(title, lines):
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = title

    text_frame = slide.placeholders[1].text_frame
    text_frame.clear()

    for i, line in enumerate(lines):
        p = text_frame.paragraphs[0] if i == 0 else text_frame.add_paragraph()
        p.text = line
        p.font.size = Pt(20)

def add_chart_slide(title, filename):
    image_path = Path("outputs") / filename

    if not image_path.exists():
        raise FileNotFoundError(image_path)

    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = title

    slide.shapes.add_picture(
        str(image_path),
        Inches(0.5),
        Inches(1.2),
        width=Inches(9)
    )

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[0])
slide.shapes.title.text = "Indian Business Executive Report"
slide.placeholders[1].text = "Cynaris Internship | Week 11 Day 2"

# Slide 2: Executive summary
add_text_slide("Executive Business Summary", [
    f"Total Sales: INR {total_sales:,.0f}",
    f"Total Profit: INR {total_profit:,.0f}",
    f"Profit Margin: {profit_margin:.2f}%",
    f"Unique Orders: {total_orders}"
])

# Slide 3: Category performance
add_text_slide("Category Performance", [
    f"{name}: Sales INR {row['Amount']:,.0f} | Profit INR {row['Profit']:,.0f}"
    for name, row in category.iterrows()
])

# Slide 4: Recommendations
add_text_slide("Executive Recommendations", [
    "Electronics leads in total sales.",
    "Clothing generates the highest profit.",
    "Furniture has the lowest profit margin.",
    "Review Furniture costs and pricing.",
    "Monitor category margins monthly."
])

# Slides 5-7: Existing PNG charts
add_chart_slide(
    "Monthly Sales Trend",
    "w11d2_monthly_sales.png"
)

add_chart_slide(
    "Category Sales vs Profit",
    "w11d2_category_sales_profit.png"
)

add_chart_slide(
    "Category Profit Margins",
    "w11d2_category_profit_margin.png"
)

# Save final presentation
output_path = Path("reports/W11D2_Executive_Business_Report_Final.pptx")
output_path.parent.mkdir(parents=True, exist_ok=True)

prs.save(output_path)

print("PowerPoint created:", output_path)
print("Total slides:", len(prs.slides))

