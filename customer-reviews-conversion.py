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

# Define a function to categorize sentiment using both the sentiment score and the review rating
def categorize_sentiment(score, rating):
    # Define sentiment categories based on score and rating
    if score > 0.05:
        # Positive sentiment score
        return 'Positive' if rating >= 4 else 'Mixed Positive' if rating == 3 else 'Mixed Negative'

    elif score < -0.05:
        # Negative sentiment score
        return 'Negative' if rating <= 2 else 'Mixed Negative' if rating == 3 else 'Mixed Positive'
    
    else:
        # Neutral sentiment score
        return 'Positive' if rating >= 4 else 'Negative' if rating <= 2 else 'Neutral'

# Define a function to bucket sentiment scores into text ranges
def sentiment_bucket(score):
    # Bucket sentiment score ranges
    if score >= 0.5:
        return '0.5 to 1.0'  # Strongly positive sentiment
    elif score >= 0.0:
        return '0.0 to 0.49'  # Mildly positive sentiment
    elif score >= -0.5:
        return '-0.49 to 0.0'  # Mildly negative sentiment
    else:
        return '-1.0 to -0.5'  # Strongly negative sentiment


# Fetch the customer reviews data from the SQL database 
customer_reviews_df = fetch_data_from_sql()
# print(customer_reviews_df)

# Calculate sentiment score for each review and add it to the dataframe
customer_reviews_df['SentimentScore'] = customer_reviews_df['ReviewText'].apply(calculate_sentiment)

# Apply sentiment categorization using both text and rating
customer_reviews_df['SentimentCategory'] = customer_reviews_df.apply(
    lambda row: categorize_sentiment(row['SentimentScore'], row['Rating']), axis=1)

# Apply sentiment bucketing to categorize scores into defined ranges
customer_reviews_df['SentimentBucket'] = customer_reviews_df['SentimentScore'].apply(sentiment_bucket)

# Display the first few rows of the dataframe with sentiment scores, categories, and buckets
print(customer_reviews_df.head())

# Save the DataFrame to a new CSV file
customer_reviews_df.to_csv('fact_customer_reviews_with_sentiment.csv', index=False)
