# Data Cleaning Log

## Dataset
Sales transaction dataset

## Cleaning Steps

### 1. Missing Values
- Checked missing values using `isnull().sum()`.
- The `discount` column had 3 missing values.
- Missing discount values were replaced using the mean of the available discount values.

### 2. Duplicate Records
- Checked duplicate rows using `duplicated().sum()`.
- Found 0 duplicate rows.
- No duplicate records were removed.

### 3. Outliers
- Used the IQR method to detect outliers in the `price` column.
- Extreme price values were capped using the IQR lower and upper limits.

### 4. Text Standardization
- Removed extra whitespace from text columns.
- Standardized text using title case for:
  - Customer name
  - Product
  - Category
  - City

## Before vs After

| Quality Check | Before Cleaning | After Cleaning |
|---|---:|---:|
| Missing values | 3 | 0 |
| Duplicate rows | 0 | 0 |
| Total rows | 9 | 9 |

## Conclusion
The dataset was cleaned by handling missing values, checking duplicates, treating price outliers, and standardizing text values. The final dataset contains 9 records with no missing values or duplicate rows.