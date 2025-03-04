# SQLAI 🤖

**Interact with your database using natural language queries powered by AI!**

SQLAI is a Streamlit-based web application that lets you upload CSV files, store them in a SQLite database, and query them using plain English. Leveraging the power of xAI's Grok and LangChain, it converts your questions into SQL queries and displays the results—all in a sleek, user-friendly interface.

---

## Features ✨

- **Natural Language Queries**: Ask questions like "Show me all entries where price > 100" and get SQL results.
- **CSV Upload**: Upload CSV files (up to 200MB) and automatically convert them into database tables.
- **Dynamic Schema**: View your database schema and select tables to query.
- **Robust Error Handling**: Handles empty files, encoding issues, and SQL execution errors gracefully.
- **Real-Time Feedback**: See generated SQL queries and their results side-by-side.
- **Powered by AI**: Uses `deepseek-r1-distill-llama-70b` via LangChain for smart query generation.

---

## Demo 🎥

Check out the live demo here: [SQLAI Demo](https://siv4kumar-sqlai.streamlit.app/)  
*Hosted on Streamlit Community Cloud—try it out!*

---

## Installation 🚀

Get SQLAI running locally with these steps:

### Prerequisites
- Python 3.8+
- Git

### Steps
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/sqlai.git
   cd sqlai
   
2. **Virtual Environment and dependency installation**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt


