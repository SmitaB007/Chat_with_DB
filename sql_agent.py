import os
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv('GROQ_API_KEY')
import streamlit as st 
from pathlib import Path
from langchain.agents import create_sql_agent
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_types import AgentType
from langchain.callbacks import StreamlitCallbackHandler 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from sqlalchemy import create_engine #sqlalchemy helps to map output coming from sql db
import sqlite3
from langchain_groq import ChatGroq 
import os
import urllib.parse


st.set_page_config(page_title="Chat with your DB") #there is a parameter of page icon , optional
st.title("Chat with your SQL DB")

LOCALDB = "USE_LOCALDB"
MYSQL = "USE_MYSQL"

radio_op = ["Use SQLite db - student.db","Connect to your SQL Database"]

selection = st.sidebar.radio(label="Choose option from below",options=radio_op)
if radio_op.index(selection) == 1:
    db_uri = MYSQL
    mysql_host=st.sidebar.text_input("Provide Host name:")
    mysql_user = st.sidebar.text_input("MySQL Username")
    mysql_pass = st.sidebar.text_input("Password",type="password")
    mysql_db=st.sidebar.text_input("Database name")
else:
    db_uri=LOCALDB


if not db_uri:
    st.info("Please enter the DB information")

llm=ChatGroq(groq_api_key=api_key,model_name="gemma2-9b-it")

@st.cache_resource(ttl="2h")  #to keep choice in the cache for 2hrs
def configure_db(db_uri,mysql_host=None,mysql_user=None,mysql_pass=None,mysql_db=None):
    if db_uri == LOCALDB:
        filepath=(Path(__file__).parent/"student.db").absolute()
        print(filepath)
        creator = lambda: sqlite3.connect(f"file:{filepath}?mode=ro",uri=True)
        return SQLDatabase(create_engine("sqlite:///",creator=creator))
    elif db_uri == MYSQL:
        if not (mysql_host and mysql_user and mysql_pass and mysql_db):
            st.error("Pls provide connection details")
            st.stop()
        print(mysql_host)

        user = urllib.parse.quote_plus(mysql_user)
        password = urllib.parse.quote_plus(mysql_pass)
        return SQLDatabase(create_engine(f"mysql+mysqlconnector://{user}:{password}@{mysql_host}/{mysql_db}"))


if db_uri == MYSQL:
    db=configure_db(db_uri,mysql_host,mysql_user,mysql_pass,mysql_db)
else:
    db=configure_db(db_uri)


toolkit = SQLDatabaseToolkit(db=db,llm=llm)
agent = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True,
        agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION   #reasoning before taking any action   It repeats this Thought → Action → Observation cycle until it reaches a Final Answer. It generates reasoning steps (Thought) internally, describing why it is choosing an action.
    )

if "message" not in st.session_state or st.sidebar.button("clear message history"):
          st.session_state["message"] = [{"role":"assistant","content":"How can I help you?"}]

          for m in st.session_state.message:
             st.chat_message(m["role"]).write(m["content"])

query = st.chat_input(placeholder="Ask anything from the database")

if query:
    st.session_state.message.append({"role":"user","content":query})

    with st.chat_message("assistant"):
        callback = StreamlitCallbackHandler(st.container())
        res = agent.run(query,callbacks=[callback])
        st.session_state.message.append({"role":"assistant","content":res})
        st.write(res)