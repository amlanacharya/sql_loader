import streamlit as st
import sqlite3
import pandas as pd
from pathlib import Path
import requests
import io

# Constants
DB_URL = "https://raw.githubusercontent.com/amlanacharya/Ineuron/main/sakila.db"
DB_PATH = "sakila.db"

@st.cache_resource
def load_database():
    """Download SQLite database from GitHub if not exists"""
    if not Path(DB_PATH).exists():
        response = requests.get(DB_URL)
        with open(DB_PATH, 'wb') as f:
            f.write(response.content)
    return DB_PATH  # Return path instead of connection

# Initialize Streamlit app
st.title("Sakila Database Explorer")

try:
    # Get database path
    db_path = load_database()
    
    # Add notice about SQLite vs MySQL
    st.info("""
        ⚠️ **Note to Students**: 
        - This demo uses SQLite for cloud compatibility
        - Some SQL syntax might differ from MySQL
        - For full MySQL functionality, please install MySQL locally on your machine
        - Refer to MySQL documentation for exact syntax in your local setup
    """)
    
    # Create a text area for SQL query input
    query = st.text_area("Enter your SQL query:", height=150)

    # Execute button
    if st.button("Execute Query"):
        try:
            # Create new connection for each query
            with sqlite3.connect(db_path) as conn:
                # Execute query and fetch results
                df = pd.read_sql_query(query, conn)
                
                # Display results
                st.write("Query Results:")
                st.dataframe(df)
            
        except Exception as e:
            st.error(f"Error executing query: {str(e)}")

    # Add some example queries
    st.sidebar.header("Example Queries")
    example_queries = {
        "List all actors": "SELECT * FROM actor LIMIT 10",
        "Top 10 rented films": """
            SELECT f.title, COUNT(*) as rental_count
            FROM rental r
            JOIN inventory i ON r.inventory_id = i.inventory_id
            JOIN film f ON i.film_id = f.film_id
            GROUP BY f.title
            ORDER BY rental_count DESC
            LIMIT 10
        """,
        "Active customers": "SELECT * FROM customer WHERE active = 1 LIMIT 10"
    }

    # Add example query buttons
    st.sidebar.subheader("Click to load example queries:")
    for query_name, query_text in example_queries.items():
        if st.sidebar.button(query_name):
            st.text_area("Enter your SQL query:", value=query_text, height=150)

    # Add footer with attribution
    st.markdown("""
    ---
    Made with ❤️ by Amlan for GripData Analytics
    
    [GitHub](https://github.com/amlanacharya) | [LinkedIn](https://www.linkedin.com/in/amlan-acharya/)
    """)

except Exception as e:
    st.error(f"Error connecting to database: {str(e)}")