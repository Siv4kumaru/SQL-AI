import streamlit as st
import sqlite3
from langchain_groq import ChatGroq
import os
import time
import pandas as pd
import re
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database file path
DATABASE_PATH = 'test.db'

def initialize_database():
    """Create database file if it doesn't exist"""
    if not os.path.exists(DATABASE_PATH):
        conn = sqlite3.connect(DATABASE_PATH)
        conn.close()
        print(f"Created new database file: {DATABASE_PATH}")

def get_all_table_names(database_path):
    """Get all table names from the database"""
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0]: tablehead(row[0], database_path) for row in cursor.fetchall()}
        conn.close()
        return tables
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return {}

def tablehead(table_name, database_path):
    """Get column information for a specific table"""
    try:
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()
        query = f"PRAGMA table_info({table_name})"
        cursor.execute(query)
        data = cursor.fetchall()
        info = [(i[1], i[2]) for i in data]
        conn.close()
        return info
    except sqlite3.Error as e:
        st.error(f"Database error: {e}")
        return []

def fetch_table_data(sql, table):
    """Execute SQL query and return results"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(sql)
        
        if "SELECT" not in sql.upper():
            conn.commit()
            conn.close()
            st.success("Query executed successfully!")
            st.rerun()
            return None
            
        data = cursor.fetchall()
        column_names = [description[0] for description in cursor.description]
        conn.close()
        return pd.DataFrame(data, columns=column_names)
    except sqlite3.Error as e:
        st.error(f"SQL execution error: {e}")
        return None

# Initialize database and get schema
initialize_database()
db_schema = get_all_table_names(DATABASE_PATH)

# Chat configuration
chat = ChatGroq(model_name="deepseek-r1-distill-llama-70b")
prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an expert in converting English questions to SQL queries!
        You will be given a question in English, and you have to convert it to an SQL query.
        The schema of the database is as follows: {dbSchema}

        The schema format is a dictionary where:
        - The keys are table names.
        - The values are lists of tuples representing the column names and their data types.

        Your task:
        - Only write the SQL query as output; do not include explanations or comments.
        - Use the provided table name in the query where applicable.
        """
    ),
    ("user", "sql query for: {user_input} on table {table_name}")
])

output_parser = StrOutputParser()
chain = prompt | chat | output_parser

# Streamlit configuration
st.set_page_config(page_title="SQLAI", page_icon="🤖", layout="centered")
st.title("SQLAI")
st.write("Interact with your database using natural language queries.")

# File uploader
csv_file = st.file_uploader("Upload a CSV file", type=["csv"], accept_multiple_files=False)
if csv_file:
    status = st.empty()
    try:
        df = pd.read_csv(csv_file,encoding="Latin1")
        table_name = re.sub(r"[^\w]", "", csv_file.name.split(".")[0])
        df.to_sql(table_name, sqlite3.connect(DATABASE_PATH), if_exists='replace', index=False)
        status.success(f"File uploaded successfully as table '{table_name}'!")
        time.sleep(2)
        status.empty()
        db_schema = get_all_table_names(DATABASE_PATH)
    except Exception as e:
        status.error(f"Error uploading file: {e}")

# Main interface
if db_schema:
    col1, col2 = st.columns([1, 1])
    with col1:
        with st.form("query_form"):
            selected_table = st.selectbox('Select a table', list(db_schema.keys()))
            user_input = st.text_area('Enter your query', 
                                    placeholder="e.g., Show all entries where cost > 100")
            submit_button = st.form_submit_button("Execute Query")
            
        if submit_button:
            if not user_input or user_input.isspace():
                st.error("Please enter a valid query.")
            else:
                with st.spinner("Generating SQL query..."):
                    try:
                        sql_query = chain.invoke({
                            "user_input": user_input,
                            "dbSchema": db_schema,
                            "table_name": selected_table
                        })
                        sql_query = re.sub(r"<think>.*?</think>\s*", "", sql_query, flags=re.DOTALL)
                        
                        st.subheader("Generated SQL Query:")
                        st.code(sql_query)
                        
                        with col2:
                            st.subheader("Query Results:")
                            result_df = fetch_table_data(sql_query, selected_table)
                            if result_df is not None and not result_df.empty:
                                st.dataframe(result_df)
                            elif result_df is not None:
                                st.info("No results found.")
                                
                    except Exception as e:
                        st.error(f"An error occurred: {e}")
else:
    st.info("Upload a CSV file to begin or ensure your database has tables.")

# Display schema (optional, for debugging)
with st.expander("View Database Schema"):
    st.json(db_schema)
