import pandas as pd
import pyodbc
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download the VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

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

# Fetch the customer reviews data from the SQL database 
customer_reviews_df = fetch_data_from_sql()
print(customer_reviews_df)
