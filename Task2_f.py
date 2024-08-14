import pandas as pd

def print_dataframe_info(df, message=None):
  """Prints basic information about a DataFrame.

  Args:
    df: The DataFrame to inspect.
    message: An optional message to print before the DataFrame information.
  """

  if message:
    print(message)

  print("Shape:", df.shape)
  print("Columns:", df.columns)
  print("Data types:", df.dtypes)
  print("Missing values:\n", df.isnull().sum())

# Load the dataset
# Reads the CSV file into a Pandas DataFrame named airbnb_df.
df = pd.read_csv('AB_NYC_2019.csv')

def categorize_price(price):
  if price < price_low_threshold:
    return 'Low'
  elif price < price_high_threshold:
    return 'Medium'
  else:
    return 'High'

def categorize_length_of_stay(min_nights):
  if min_nights <= min_nights_short_term:
    return 'Short-term'
  elif min_nights <= min_nights_medium_term:
    return 'Medium-term'
  else:
    return 'Long-term'


# Define price thresholds
price_low_threshold = 100 # $
price_high_threshold = 300 # $

# Define minimum nights thresholds
min_nights_short_term = 3
min_nights_medium_term = 14

# Create new columns
df['price_category'] = df['price'].apply(categorize_price)
df['length_of_stay_category'] = df['minimum_nights'].apply(categorize_length_of_stay)


# Selecting Rows and Columns
# Using .iloc:
# Select the first 5 rows and columns 1 to 3 (inclusive)
first_five_rows = df.iloc[:5, 1:4]

# Using .loc:
df = df.set_index('id')
df.index = df.index.astype(str)
# print(df.index)
# Select rows with index labels '2539' and '5178' and columns 'name' and 'price'
# Index named 'index_name'
selected_data = df.loc[['2539', '5178'], ['name', 'price']]
print(selected_data)

# Filtering Data
# Filter for listings in Manhattan and Brooklyn
manhattan_brooklyn_df = df[df['neighbourhood_group'].isin(['Manhattan', 'Brooklyn'])]

# Filter for listings with price > 100 and number_of_reviews > 10
filtered_df = manhattan_brooklyn_df[(manhattan_brooklyn_df['price'] > 100) &
                                   (manhattan_brooklyn_df['number_of_reviews'] > 10)]

# Select desired columns
selected_columns = filtered_df[['neighbourhood_group', 'price', 'minimum_nights',
                               'number_of_reviews', 'availability_365']]

print_dataframe_info(selected_columns, "Filtered and selected columns: ")
print(selected_columns.head())

# filtered DataFrame named 'filtered_and_selected_columns' with columns:
# 'neighbourhood_group', 'price_category', 'price', 'minimum_nights', 'number_of_reviews', 'availability_365'
filtered_and_selected_columns = filtered_df[['neighbourhood_group', 'price_category', 'price', 'minimum_nights',
                               'number_of_reviews', 'availability_365']]

# Group by neighbourhood_group and price_category
grouped_df = filtered_and_selected_columns.groupby(['neighbourhood_group', 'price_category'])

# Calculate aggregate statistics
agg_results = grouped_df[['price', 'minimum_nights', 'number_of_reviews', 'availability_365']].agg(['mean'])

print_dataframe_info(agg_results, "Aggregate statistics:")
print(agg_results)

# Sort by price in descending order and then by number_of_reviews in ascending order
df_sorted = df.sort_values(by=['price', 'number_of_reviews'], ascending=[False, True])
print(df_sorted)


# Group by neighbourhood_group and calculate total listings and average price

df2 = pd.read_csv('AB_NYC_2019.csv')

grouped_df = df2.groupby('neighbourhood_group').agg({
    'id': 'count',  # Count the number of listings in each group
    'price': 'mean'   # Calculate the average price for each group
})
# Rename columns
grouped_df = grouped_df.rename(columns={'id': 'total_listings', 'price': 'average_price'})


# Create a ranking based on total listings and average price
# Calculate ranking directly using the aggregated values
#grouped_df['ranking'] = grouped_df['id'] * 0.5 + grouped_df['price'] * 0.5

# 1. Create a new column named 'ranking' in the grouped_df DataFrame.
# 2. It uses the apply method with a lambda function.
# 3. The lambda function takes a single argument x, which represents each row in the grouped DataFrame.
# 4. Inside the function, it accesses values from columns named 'total_listings' and 'average_price'.
grouped_df['ranking'] = grouped_df.apply(lambda x: (( x['average_price']+ x['total_listings']) / 2), axis=1)
grouped_df = grouped_df.sort_values(by='ranking', ascending=False)
# Calculating ranks:
# .rank(ascending=False, method='dense') applies the rank function to the selected column
grouped_df['rank'] = grouped_df['ranking'].rank(ascending=False, method='dense')

print_dataframe_info(grouped_df, "Group by neighbourhood_group and calculate total listings and average price:")
print(grouped_df)
grouped_df.to_csv('aggregated_airbnb_data.csv', index=True)



