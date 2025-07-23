# Chat with Your SQL Database
A Streamlit-based web app that lets you query and interact with SQL databases using natural language. Built using LangChain and Groq’s Gemma2-9B-it LLM, it can connect to either a local SQLite database or a remote MySQL database.

### Features
Dual Database Support

Local SQLite (student.db)

Remote MySQL (via credentials)

Natural Language to SQL

Ask questions like:
"Show me all students with grades above 80"

ReAct Agent

Uses ZERO_SHOT_REACT_DESCRIPTION for reasoning before executing queries

Streamlit Chat UI

Sidebar options and persistent chat history

Secure Inputs

API keys and passwords managed via .env

### Tech Stack

Streamlit (frontend)

LangChain (agent + SQL toolkit)

Groq API (Gemma2-9B-it model)

SQLite / MySQL

SQLAlchemy




Start chatting with your database!

