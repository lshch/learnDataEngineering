import pandas as pd
import matplotlib.pyplot as plt

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
  print(df)

# Load the dataset
# Reads the CSV file into a Pandas DataFrame named airbnb_df.
df = pd.read_csv('AB_NYC_2019.csv')

# 1. Advanced Data Manipulation
# 1.1 Analyze Pricing Trends Across Neighborhoods and Room Types
# Create a pivot table to analyze average price by neighborhood_group and room_type
price_pivot = df.pivot_table(values='price', index='neighbourhood_group', columns='room_type', aggfunc='mean')
print_dataframe_info(price_pivot, "A pivot table to analyze average price by neighborhood_group and room_type: ")

# 1.2 Prepare Data for In-Depth Metric Analysis
# Melt the dataset to long format for price and minimum_nights
melted_df = df.melt(id_vars=['id', 'name', 'host_id', 'neighbourhood_group', 'room_type'],
                  value_vars=['price', 'minimum_nights'],
                  var_name='metric', value_name='value')
print_dataframe_info(melted_df.head(),"Melt the dataset to long format for price and minimum_nights:")

# 1.3 Classify Listings by Availability
def classify_availability(availability):
  if availability < 50:
    return 'Rarely Available'
  elif availability <= 200:
    return 'Occasionally Available'
  else:
    return 'Highly Available'

df['availability_status'] = df['availability_365'].apply(classify_availability)
print_dataframe_info(df.head(), "Classify Listings by Availability")

# 2. Descriptive Statistics
# Perform descriptive statistics on numeric columns
numeric_cols = ['price', 'minimum_nights', 'number_of_reviews']
descriptive_stats = df[numeric_cols].describe()

# Print the results
print_dataframe_info(descriptive_stats, "Descriptive statistics on numeric columns: ")

# 3. Time Series Analysis
# 3.1 Convert and Index Time Data
df['last_review'] = pd.to_datetime(df['last_review'])
df.set_index('last_review', inplace=True)


# 3.2 Identify Monthly Trends
# Resample to monthly frequency and calculate the mean of 'number_of_reviews' and 'average_price'

monthly_reviews = df['number_of_reviews'].resample('ME').sum()
average_monthly_prices = df['price'].resample('ME').mean()
monthly_trends = pd.DataFrame({'Number_of_Reviews': monthly_reviews, 'Average_Price': average_monthly_prices})

# Print the results
print_dataframe_info(monthly_trends, "Monthly trends in number of reviews and average price:")

# Plot the number of reviews
monthly_trends['Number_of_Reviews'].plot(figsize=(6, 6), title='Monthly Number of Reviews')
plt.ylabel('Number of Reviews')
plt.show()

# Plot the average price
monthly_trends['Average_Price'].plot(figsize=(12, 6), title='Monthly Average Price')
plt.ylabel('Average Price')
plt.show()

import matplotlib.pyplot as plt

# Assuming monthly_trends DataFrame is created as shown in the previous response

# Plot the number of reviews and average price on the same figure
fig, ax1 = plt.subplots(figsize=(12, 6))

color = 'tab:blue'
ax1.set_xlabel('Date')
ax1.set_ylabel('Number of Reviews', color=color)
ax1.plot(monthly_trends['Number_of_Reviews'], color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:red'
ax2.set_ylabel('Average Price', color=color)
ax2.plot(monthly_trends['Average_Price'], color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
#plt.show()


# 3.3 Analyze Seasonal Patterns
# Group by month and calculate mean

# Extract month from 'last_review'
df['month'] = df.index.month
month_names = {1: 'January', 2: 'February', 3: 'March', 4: 'April',
              5: 'May', 6: 'June', 7: 'July', 8: 'August',
              9: 'September', 10: 'October', 11: 'November', 12: 'December'}

# Create a new DataFrame with month names as index and average prices as values
# Group by month and calculate average price
monthly_averages = df.groupby('month')['price'].mean()
monthly_averages_df = pd.DataFrame({'Average Price': monthly_averages}).reset_index()
monthly_averages_df['Month'] = monthly_averages_df['month'].map(month_names)
monthly_averages_df.set_index('Month', inplace=True)
# Remove the column 'month'
monthly_averages_df = monthly_averages_df.drop('month', axis=1)

print(monthly_averages_df)
monthly_averages_df.to_csv('time_series_airbnb_data.csv', index=True)


