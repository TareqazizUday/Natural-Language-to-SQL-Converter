import json
import re
import os
import streamlit as st
from together import Together
from sqlalchemy import create_engine, inspect
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(
    page_title="NL to SQL Converter",
    page_icon="🔮",
    layout="wide",
)

st.markdown("""
<style>
    .main {
        background-color: #0A1929;
        color: white;
    }
    .stTextInput, .stTextArea {
        color: white;
    }
    .stButton>button {
        background-color: #3A86FF;
        color: white;
        border-radius: 10px;
        padding: 10px 24px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #4A96FF;
    }
    div[data-testid="stDecoration"] {
        background-image: linear-gradient(90deg, #0A1929, #0A3060);
    }
    .stAlert {
        background-color: #15355F;
        color: white;
    }
    .success-message {
        background-color: #1E634E;
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 15px;
    }
    .container {
        background-color: #15355F;
        padding: 4px;
        border-radius: 15px;
        margin-bottom: 20px;
    }
    h1, h2, h3 {
        color: #3A86FF;
    }
    .metadata {
        font-size: 0.8em;
        color: #8EB1C7;
    }
    .footer {
        text-align: center;
        color: #8EB1C7;
        padding: 20px;
    }
</style>
""", unsafe_allow_html=True)

api_key = os.getenv("TOGETHER_API_KEY")
if not api_key:
    st.error("API key not found! Please set TOGETHER_API_KEY in your .env file.")
    client = None
else:
    client = Together(api_key=api_key)

# SQLite DB connection string
db_url = "sqlite:///testdb.sqlite"

def extract_schema(db_url):
    """Extract database schema as JSON string"""
    try:
        engine = create_engine(db_url)
        inspector = inspect(engine)
        schema = {}

        for table in inspector.get_table_names():
            columns = inspector.get_columns(table)
            schema[table] = [{'name': col['name'], 'type': str(col['type'])} for col in columns]

        return json.dumps(schema, indent=2)
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return "{}"

def clean_text(text: str):
    """Clean output text if needed"""

    think_pattern = re.compile(r'<think>.*?</think>', re.DOTALL)
    text = think_pattern.sub('', text)

    sql_pattern = re.compile(r'```sql(.*?)```', re.DOTALL)
    match = sql_pattern.search(text)
    if match:
        return match.group(1).strip()

    select_pattern = re.compile(r'(SELECT.*?;)', re.DOTALL | re.IGNORECASE)
    match = select_pattern.search(text)
    if match:
        return match.group(1).strip()

    lines = text.strip().split("\n")
    sql_lines = []
    for line in lines:
        if not line.startswith("--") and not line.lower().startswith("here") and not line.lower().startswith("this"):

            if "<think>" in line or "</think>" in line or "Alright" in line or "First" in line or "Let me" in line:
                continue
            sql_lines.append(line)
    
    return "\n".join(sql_lines).strip()

def to_sql_query(schema, user_query):
    """Send prompt to Together API and get SQL query"""
    global client

    if not client:
        st.error("API client not initialized. Check your API key.")
        return ""
        
    prompt = f"""
You are a SQL generator. When given a database schema and a user question, generate only the SQL statement.

Schema:
{schema}

User question:
{user_query}

Output SQL query only, with no explanations, no markdown formatting, no think blocks, and no reasoning:
"""
    with st.spinner(""):
        try:
            response = client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2
            )
            sql = response.choices[0].message.content
            return clean_text(sql)
        except Exception as e:
            st.error(f"API Error: {str(e)}")
            return ""

st.markdown("<h1 style='text-align: center;'>🔮 Natural Language to SQL Converter</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("### 💬 Describe your data need")
    query = st.text_area(
        "Type your question in natural language:",
        placeholder="Example: Show me the top 5 customers by total orders",
        height=150
    )

    if st.button("🔄 Refresh Database Schema", use_container_width=True):
        with st.spinner("Refreshing schema..."):
            schema = extract_schema(db_url)
            st.session_state['schema'] = schema
            st.success("Schema refreshed successfully!")

    if st.button("✨ Generate SQL", type="primary", use_container_width=True):
        if not query:
            st.warning("Please enter a question first")
        elif not client:
            st.error("API client not initialized. Please check your .env file and restart the app.")
        else:
            try:
                schema = st.session_state.get('schema', extract_schema(db_url))
                sql = to_sql_query(schema, query)
                
                if sql:
                    st.session_state['sql_result'] = sql
                    st.session_state['last_query'] = query

            except Exception as e:
                st.error(f"⚠️ Error generating SQL: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("### 📊 Database Schema")
    with st.expander("View Schema", expanded=True):
        schema = st.session_state.get('schema', extract_schema(db_url))
        if schema != "{}":
            try:
                schema_dict = json.loads(schema)
                for table, columns in schema_dict.items():
                    st.markdown(f"**Table: `{table}`**")
                    for col in columns:
                        st.markdown(f"- `{col['name']}` ({col['type']})")
            except:
                st.code(schema)
        else:
            st.info("No schema available or database connection error")
    
    st.markdown("</div>", unsafe_allow_html=True)

if 'sql_result' in st.session_state:
    st.markdown("<div class='container'>", unsafe_allow_html=True)
    st.markdown("### 🚀 Generated SQL")
    st.markdown(f"<div class='metadata'>Based on: \"{st.session_state.get('last_query', '')}\"</div>", unsafe_allow_html=True)
    st.code(st.session_state['sql_result'], language="sql")

    if st.button("📋 Copy to Clipboard", use_container_width=True):
        st.markdown(f"""
        <script>
        navigator.clipboard.writeText('{st.session_state['sql_result']}');
        </script>
        """, unsafe_allow_html=True)
        st.success("SQL copied to clipboard!")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Add extra info at the bottom
st.markdown("<div class='container'>", unsafe_allow_html=True)
st.markdown("### 💡 Tips for better queries")
st.markdown("""
- Be specific about the tables and columns you want to query
- Mention any filters, sorting, or grouping clearly
- For complex queries, break down your requirements step by step
""")
st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("<div class='footer'>Powered by Together API & DeepSeek-R1 model</div>", unsafe_allow_html=True)