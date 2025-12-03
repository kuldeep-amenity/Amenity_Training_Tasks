# Pandas Data Analysis Guide

## Table of Contents
1. [Loading & Initial Inspection](#loading--initial-inspection)
2. [Data Selection & Indexing](#data-selection--indexing)
3. [Filtering Data](#filtering-data)
4. [Data Cleaning & Manipulation](#data-cleaning--manipulation)
5. [Grouping & Aggregation](#grouping--aggregation)
6. [Sorting & Ranking](#sorting--ranking)
7. [Combining DataFrames](#combining-dataframes)

---

## Loading & Initial Inspection

### Import Library
```python
import pandas as pd
```

### Load Dataset
```python
df = pd.read_csv('sales_data.csv')
```

### Basic Inspection Commands
```python
# View first 7 rows
df.head(7)

# View last 7 rows
df.tail(7)

# Get DataFrame dimensions
df.shape

# Get column names
df.columns

# Get data types
df.dtypes

# Statistical summary (numeric columns)
df.describe()

# Statistical summary (all columns)
df.describe(include='all')

# Count unique values per column
df.nunique()
```

---

## Data Selection & Indexing

### Select Single Column
```python
df['Product']
```

### Select Multiple Columns
```python
df[['Product', 'Price', 'Quantity']]
```

### Select Row by Position
```python
df.iloc[3]
```

### Select Multiple Rows by Position
```python
df.iloc[5:11]
```

### Set Index
```python
df.set_index('OrderID', inplace=True)
```

### Select Row by Index Label
```python
df.loc['ORD019']
```

### Select Specific Rows and Columns by Label
```python
df.loc[['ORD002', 'ORD005'], ['Product', 'Region']]
```

### Select Specific Rows and Columns by Position
```python
df.iloc[[0, 2, 4], [1, 3]]
```

---

## Filtering Data

### Filter by Numerical Condition
```python
# Quantity greater than 10
filtered_row = df[df['Quantity'] > 10]
```

### Filter by Categorical Condition
```python
# Category equals 'Electronics'
df.loc[df['Category'] == 'Electronics']
```

### Filter by Multiple Conditions (AND)
```python
# Region is 'West' AND Price is less than 50
df.loc[(df['Region'] == 'West') & (df['Price'] < 50)]
```

### Filter by Multiple Values (OR)
```python
# Product is 'Laptop', 'Mouse', or 'Keyboard'
df.loc[(df['Product'] == 'Laptop') | (df['Product'] == 'Mouse') | (df['Product'] == 'Keyboard')]
```

### Filter Rows with Missing Values
```python
df[df['Quantity'].isna()]
```

---

## Data Cleaning & Manipulation

### Identify Columns with Missing Values
```python
df.columns[df.isna().any()]
```

### Count Missing Values per Column
```python
df.isnull().sum()
```

### Fill Missing Values (Numerical)
```python
# Fill with mean
value = df['Price'].mean()
df['Price'] = df['Price'].fillna(value)
```

### Fill Missing Values (Categorical)
```python
# Fill with placeholder
df['Category'] = df['Category'].fillna("Unknown")
```

### Drop Rows with Missing Values
```python
df.dropna()
```

### Drop Column
```python
df.drop(columns=['Region'], inplace=True)
```

### Create New Column from Arithmetic Operation
```python
df['TotalPrice'] = df['Quantity'] * df['Price']
```

### Convert Column to Datetime
```python
df['OrderDate'] = pd.to_datetime(df['OrderDate'])
```

### Extract Month from Datetime
```python
df['OrderMonth'] = df['OrderDate'].dt.month
```

### Rename Columns
```python
df.rename(columns={'Price': 'UnitPrice', 'Quantity': 'UnitsSold'}, inplace=True)
```

### Change Data Type
```python
df['UnitPrice'] = df['UnitPrice'].astype(int)
```

### Remove Duplicates
```python
df.drop_duplicates(inplace=True)
```

### Apply Custom Function
```python
# Convert to uppercase
df['Product'] = df['Product'].apply(lambda x: x.upper())
```

---

## Grouping & Aggregation

### Group by Single Column and Sum
```python
df.groupby('Category')['UnitPrice'].sum()
```

### Group by Single Column and Calculate Mean
```python
df.groupby('Category')['UnitPrice'].mean()
```

### Group by Multiple Columns and Count
```python
df.groupby(['Category', 'UnitPrice']).size()
```

### Find Min and Max per Group
```python
df.groupby(['Category', 'UnitPrice']).agg(['min', 'max'])
```

### Count Unique Items per Group
```python
df.groupby('Category')['Product'].nunique()
```

### Get Group Sizes
```python
df.groupby('Category').size()
```

### Apply Multiple Aggregations
```python
df.groupby('Category').agg({'UnitPrice': 'mean', 'TotalPrice': 'max'})
```

---

## Sorting & Ranking

### Sort by Single Column (Ascending)
```python
df.sort_values('UnitPrice')
```

### Sort by Single Column (Descending)
```python
df.sort_values('UnitsSold', ascending=False)
```

### Sort by Multiple Columns
```python
df.sort_values(by=['UnitPrice', 'UnitsSold'], ascending=True)
```

---

## Combining DataFrames

### Concatenate Horizontally (Side by Side)
```python
df1 = pd.DataFrame({'ID': [1, 2], 'Name': ['A', 'B']})
df2 = pd.DataFrame({'ID': [3, 4], 'Name': ['C', 'D']})
dsc = pd.concat([df1, df2], axis=1)
```

### Concatenate Vertically (Stacking)
```python
df3 = pd.DataFrame({'ID': [5, 6], 'Name': ['E', 'F']})
df4 = pd.DataFrame({'ID': [7, 8], 'Name': ['G', 'H']})
df5 = pd.concat([df3, df4], axis=0)
```

### Merge DataFrames (Inner Join)
```python
df_a = pd.DataFrame({'ID': [1, 2, 3], 'ValueA': ['X', 'Y', 'Z']})
df_b = pd.DataFrame({'ID': [2, 3, 4], 'ValueB': ['P', 'Q', 'R']})
df_c = pd.merge(df_a, df_b, on='ID', how='inner')
```

---

## Common Parameters

### `inplace` Parameter
- `inplace=True`: Modifies the DataFrame directly
- `inplace=False`: Returns a new DataFrame (default)

### `axis` Parameter
- `axis=0`: Operations along rows (vertical)
- `axis=1`: Operations along columns (horizontal)

### Merge `how` Parameter
- `how='inner'`: Returns only matching rows
- `how='outer'`: Returns all rows from both DataFrames
- `how='left'`: Returns all rows from left DataFrame
- `how='right'`: Returns all rows from right DataFrame