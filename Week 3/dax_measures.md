# Week 3 Day 2 – DAX Basics

## 1. Total Sales Measure

```DAX
Total Sales =
SUMX(
    cleaned_dataset,
    cleaned_dataset[quantity] * cleaned_dataset[price]
)
Electronics Sales =
CALCULATE(
    [Total Sales],
    cleaned_dataset[category] = "Electronics"
)
YTD Sales =
CALCULATE(
    [Total Sales],
    DATESYTD(cleaned_dataset[sale_date])
)
Running Total =
CALCULATE(
    SUMX(
        cleaned_dataset,
        cleaned_dataset[quantity] * cleaned_dataset[price]
    ),
    FILTER(
        ALL(cleaned_dataset),
        cleaned_dataset[sale_date]
            <= EARLIER(cleaned_dataset[sale_date])
    )
)
Profit Margin % =
DIVIDE(
    cleaned_dataset[price] *
        (1 - cleaned_dataset[discount] / 100),
    cleaned_dataset[price]
) * 100