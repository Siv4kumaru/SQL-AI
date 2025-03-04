import streamlit as st
import sqlite3
from langchain_groq import ChatGroq
import os
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import pandas as pd
import re
load_dotenv()

import sqlite3


def get_all_table_names(database_path):
    # Connect to the SQLite database
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Query to get all table names
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = {row[0]:[tablehead(row[0],database_path)] for row in cursor.fetchall()}

    conn.close()
    return tables

def tablehead(table_name,database_path):
    conn=sqlite3.connect(database_path)
    cursor=conn.cursor()
    
    query = f"PRAGMA table_info({table_name})"
    cursor.execute(query)
    data=cursor.fetchall()
    info=[(i[1],i[2]) for i in data]
    conn.close()
    return info

database_path = 'test.db'
dbSchema = get_all_table_names(database_path)
print("DB schema:", dbSchema)

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

        For example:
        {{'test': [('Cost_Show', 'TEXT'), ('OrderFmt', 'INTEGER')]}}
        - Here, 'test' is the table name.
        - 'Cost_Show' and 'OrderFmt' are column names with data types 'TEXT' and 'INTEGER,' respectively.

        Your task:
        - Only write the SQL query as output; do not include explanations, comments, or formatting such as ``` or 'sql'.

        Examples:
        1. How many entries of records are present?
           SQL: SELECT COUNT(*) FROM table;
        2. Tell me all the entries which have CostEleType as FIXED COST?
           SQL: SELECT * FROM table WHERE CostEleType = 'FIXED COST';
        3. Delete this table.
              SQL: delete from table;
        4. Show me the entries where the OrderFmt is greater than 100.
              SQL: SELECT * FROM table WHERE OrderFmt > 100;
        5. drop the table.
                SQL: DROP TABLE table;
        """
    ),
    ("user", "sql query for :{user_input}")
])

def cleanres(response):
    return response.replace("sql query for :","")

def fetchtable(sql,table):
    conn=sqlite3.connect('test.db')
    cursor=conn.cursor()
    cursor.execute(sql)
    if "SELECT" not in (sql).upper():
        conn.commit()
        st.success("Query executed successfully!")
        conn.close()
        st.rerun()
        return
    data=cursor.fetchall()
    column_names = [description[0] for description in cursor.description]
    conn.close()
    df=pd.DataFrame(data,columns=column_names,encoding="utf-8", errors="ignore")
    st.write(df)

output_parser=StrOutputParser()
chain = prompt | chat | output_parser

st.set_page_config(page_title="SQLAI", page_icon="🤖", layout="centered")
st.title("SQLAI")
st.write("Interact with the SQLAI model via this simple interface.")

csvfile=st.file_uploader("Upload a CSV file", type=["csv"], accept_multiple_files=False)
if csvfile:
    ss=st.empty()
    try:
        df=pd.read_csv(csvfile,encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(csvfile, encoding="ISO-8859-1")
    name=csvfile.name.split(".")[0]
    name= re.sub(r"[^\w]", "", name)
    df.to_sql(name, sqlite3.connect('test.db'), if_exists='replace', index=False)
    ss.success("File uploaded successfully!")
    ss.empty()  # Clear the placeholder after 3 seconds
    dbSchema = get_all_table_names(database_path)
if csvfile or dbSchema:
    col1, col2 = st.columns(2)
    with col1:
        with st.form("modelForm"):  
            dropdowntable = st.selectbox('Select a table', list(dbSchema.keys()))
            user_input = st.text_area('Enter your query', placeholder="Type your query here...")
            button = st.form_submit_button("Send Request")
        if button:
            if not user_input or user_input.isspace():
                st.error("Please enter a valid query.")
                st.stop()
            try:
                response = chain.invoke({"user_input": user_input,"dbSchema":dbSchema})
                st.success("Response received:")
                cleanres(response)
                with st.spinner("Loading..."):
                    st.write(response)
                with col2:
                    fetchtable(response,dropdowntable)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    

