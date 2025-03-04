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
   ```
   
2. **Virtual Environment and dependency installation**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Creating an the env file**
   ```bash
      cp sampleenv.txt .env
   ```

4. **Creating and updating the api keys in .env file**
 ```
      Open .env file
      register to Groq dev console and langchain community
      Completely free to use apis available here
      use the angchain api and groq api keys here

5.**Running**
```bash
   python -m streamlit run app.py
```
Usage 🛠️

    Upload a CSV: Drag and drop a CSV file (e.g., from Kaggle) into the uploader.
    Select a Table: Choose the table you want to query from the dropdown.
    Ask Away: Type a question like "How many items cost more than $50?" in the text area.
    See Results: The app generates the SQL query and displays the results instantly.

Example Queries

    "Show all entries where category is 'Electronics'"
    "How many records are there?"
    "List items with stock less than 10"

Tech Stack 🧰

    Frontend: Streamlit
    Backend: Python, SQLite3
    AI: LangChain, Groq (deepseek-r1-distill-llama-70b)
    Data Handling: Pandas
    Environment: dotenv

Contributions are welcome! Here’s how to get involved:

    Fork the repo.
    Create a feature branch (git checkout -b feature/awesome-thing).
    Commit your changes (git commit -m "Add awesome thing").
    Push to the branch (git push origin feature/awesome-thing).
    Open a Pull Request.

For more help, open an issue.
Roadmap 🛤️

    Add support for multiple file formats (Excel, JSON)
    Implement query history
    Add export results feature
    Support for complex JOIN queries
    Enhance UI with custom theme

    Built with ❤️ by Siv4kumaru
    Thanks to xAI for Groq and LangChain for the awesome framework!
    Inspired by the power of asking questions in plain English.

Star this repo if you find it useful! ⭐

Questions? Reach out at [sktriple777@gmail.com] or open an issue.
