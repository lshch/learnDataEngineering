import pandas as pd

def print_dataframe_info(df, message=None):
  """Prints basic information about a DataFrame.

  Args:
      df (pd.DataFrame): The DataFrame to inspect.
      message (str, optional): An optional message to print before the DataFrame information.
  """
  if message:
    print(message)

  print(f"Shape: {df.shape}")
  print(f"Columns: {df.columns}")
  print(f"Data types: {df.dtypes}")
  print("Missing values:\n", df.isnull().sum())

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

# Define thresholds and minimum nights
price_low_threshold = 100  # $
price_high_threshold = 300  # $
min_nights_short_term = 3
min_nights_medium_term = 14

# Load the dataset
airbnb_df = pd.read_csv('AB_NYC_2019.csv')

# Inspect the first few rows
print(airbnb_df.head())

# Get basic information about the dataset
print_dataframe_info(airbnb_df, "DataFrame before cleaning:")

# Check for missing values
print_dataframe_info(airbnb_df[airbnb_df.isnull().any(axis=1)], "Rows with missing values:")

# Handling Missing Values in Specific Columns
# Fill missing values in 'name' and 'host_name' with 'Unknown'
airbnb_df.loc[:, 'name'] = airbnb_df['name'].fillna('Unknown')
airbnb_df.loc[:, 'host_name'] = airbnb_df['host_name'].fillna('Unknown')

# Fill missing values in 'last_review' with pd.NaT
# Convert to datetime, handling potential errors
airbnb_df['last_review'] = pd.to_datetime(airbnb_df['last_review'], errors='coerce')
airbnb_df.loc[:, 'last_review'] = airbnb_df['last_review'].fillna(pd.NaT)

print(airbnb_df['last_review'].isnull().sum())

# Check for missing values
print_dataframe_info(airbnb_df[airbnb_df.isnull().any(axis=1)], "Rows with missing values after handling:")

# Create new columns
airbnb_df['price_category'] = airbnb_df['price'].apply(categorize_price)
airbnb_df['length_of_stay_category'] = airbnb_df['minimum_nights'].apply(categorize_length_of_stay)

# Check the first few rows
print(airbnb_df.head())

# Check the data types
print_dataframe_info(airbnb_df, "DataFrame after cleaning:")

# Check the distribution of categorical columns
print(airbnb_df['price_category'].value_counts())
print(airbnb_df['length_of_stay_category'].value_counts())

# Check for missing values in specific columns
print_dataframe_info(airbnb_df[['name', 'host_name', 'price', 'last_review']][airbnb_df[['name', 'host_name', 'price', 'last_review']].isnull().any(axis=1)], "Missing values in specific columns:")

# Remove rows with price equal to 0
airbnb_df = airbnb_df[airbnb_df['price'] > 0]

airbnb_origin_df = pd.read_csv('AB_NYC_2019.csv')
print_dataframe_info(airbnb_origin_df, "DataFrame before cleaning:")
print_dataframe_info(airbnb_df, "DataFrame after cleaning:")
