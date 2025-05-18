# Natural Language to SQL Converter

The Natural Language to SQL Converter is an intuitive web application that transforms plain English questions into SQL queries. Built with Streamlit and powered by the Together AI API, this tool enables users with no SQL knowledge to query databases using natural language.

Simply enter a question like "Show me the top 5 customers by total orders," and the application will generate the appropriate SQL query by analyzing your database schema. The clean, modern interface displays your database structure and produces only the SQL code you need without any explanations or reasoning steps.

This tool bridges the gap between business users and database information, making data access more democratic and efficient across organizations.

A Streamlit web application that converts natural language questions into SQL queries using AI.

![NL to SQL Converter Screenshot](https://github.com/user-attachments/assets/01a24fe5-a0e0-47a6-bc85-289ee157d738)

## 🖥️ Output
![NL to SQL Converter Screenshot](https://github.com/user-attachments/assets/f630967f-4ee9-490f-a65b-53340b210b86)

## 🌟 Features

* **Natural Language Processing**: Convert plain English questions into SQL queries
* **Database Schema Detection**: Automatically extracts and displays your database schema
* **Clean SQL Output**: Displays only the SQL query without explanations or thinking steps
* **Copy to Clipboard**: Easy copying of generated SQL for use in your database tools
* **Dark Theme UI**: Modern dark blue interface for comfortable viewing
* **Responsive Layout**: Works well on various screen sizes

## 🚀 Getting Started

### Prerequisites

* Python 3.8 or higher
* A Together AI API key (get one at [together.ai](https://together.ai))
* SQLite database (or modify the code for your database)

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/yourusername/nl-to-sql-converter.git
   cd nl-to-sql-converter
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add your API key:

   ```
   TOGETHER_API_KEY=your_api_key_here
   ```

4. Make sure your SQLite database is in the project folder or update the path in the code.

### Running the Application

Start the Streamlit app:

```bash
streamlit run app.py
```

The application should now be running at [http://localhost:8501](http://localhost:8501).

## 💡 Usage

1. **Enter Your Question**: Type a natural language question about your data in the text area.
2. **View Your Schema**: The right panel shows your database tables and columns.
3. **Generate SQL**: Click the "Generate SQL" button to convert your question.
4. **Review and Use**: Copy the generated SQL to use in your database tools.

### Example Questions

* "Show me all customers who made purchases in the last month"
* "What are the top 5 most expensive products in our inventory?"
* "How many orders were placed by each customer in 2024?"
* "Find all users who have spent more than \$1000 total"
* "Which products have never been ordered?"

## 🔧 Customization

### Changing the Database

To use a different database, update the `db_url` variable:

```python
# For PostgreSQL
db_url = "postgresql://user:password@localhost:5432/database"

# For MySQL
db_url = "mysql://user:password@localhost:3306/database"
```

You'll need to install the appropriate drivers (like `psycopg2` for PostgreSQL).

### Modifying the AI Model

This project uses the DeepSeek-R1-Distill-Llama-70B model. To use a different model, change the model parameter:

```python
response = client.chat.completions.create(
    model="your-preferred-model",
    # other parameters
)
```

## 📝 How It Works

1. The application extracts your database schema.
2. When you submit a question, it creates a prompt combining your schema and question.
3. This prompt is sent to the Together AI API with the DeepSeek model.
4. The response is processed to extract only the SQL query.
5. The clean SQL is displayed in the interface.

[Click here to watch the demo video](https://github.com/user-attachments/assets/7d3c6698-7aa2-4d91-84f5-1c758d0e7b13)

## 🔒 Security Notes

* Your API key is stored in a `.env` file which should never be committed to version control.
* Database credentials should be handled securely.
* Consider implementing additional security measures for production deployments.

## 📊 Requirements

```
streamlit
together
sqlalchemy
python-dotenv
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgements

* [Together AI](https://together.ai) for the API
* [DeepSeek AI](https://deepseek.ai) for the language model
* [Streamlit](https://streamlit.io) for the web framework
* [SQLAlchemy](https://www.sqlalchemy.org) for database interactions
