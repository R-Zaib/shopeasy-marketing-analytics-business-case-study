import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# Initialize VADER SentimentIntensityAnalyzer
sia = SentimentIntensityAnalyzer()

# Define a function for fetching data from SQL database 
def fetch_data_from_sql():
    # Define the connection
    conn_str = (
        "Driver={SQL Server};"  # Specify the driver for SQL server
        "Server=DESKTOP-AWD\\SQLEXPRESS;"  # Specify your SQL server instance 
        "Database=PortfolioProject_MarketingAnalytics;" # Specify database name
        "Trusted_Connection=yes;"   # Use Windows Authentication for the connection
    )
    # Establish the connection to the database
    conn = pyodbc.connect(conn_str)

    # Define the SQL query to fetch customer reviews data
    query = "SELECT ReviewID, CustomerID, ProductID, ReviewDate, Rating, ReviewText FROM dbo.customer_reviews"
    
    # Execute the query and fetch the data into a df
    df = pd.read_sql(query, conn)

    # Close the connection to free up resources
    conn.close()

    # Return the fetched data as a DataFrame
    return df

# Define a function to calculate sentiment scores using VADER
def calculate_sentiment(review):
    # Get the sentiment scores for the review text
    sentiment = sia.polarity_scores(review)
    return sentiment['compound'] # Returns a score between -1 (negative) and 1 (positive)

# Fetch the customer reviews data from the SQL database 
customer_reviews_df = fetch_data_from_sql()
# print(customer_reviews_df)

# Calculate sentiment score for each review and add it to the dataframe
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Print the dataframe with sentiment scores
print(customer_reviews_df)