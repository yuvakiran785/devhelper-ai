# 🛠️ DevHelper AI (V1)

A lightweight, beginner-friendly developer toolkit powered by the **Google Gemini API** (`gemini-3.8-flash`) and **Streamlit**.

No LangChain, no vector databases, no complex agents—just clean, readable Python, the official `google-genai` SDK, and a responsive UI.

---

## ✨ Features

1. 🐛 **Python Error Explainer**
   - Paste a Python traceback or error message (with optional code context).
   - Gemini returns a plain-English root-cause analysis and a copy-pasteable minimal working fix.
2. 📝 **Git Commit Generator**
   - Describe code changes in casual language (e.g., *"fixed login redirect loop and added unit tests"*).
   - Generates Conventional Commits (e.g., `fix(auth): resolve login redirect loop`) with bulleted body descriptions and variations.
3. 🔍 **Regex Explainer**
   - Enter any regular expression pattern and optional flags.
   - Breaks down regex tokens into an easy-to-read table alongside matching and non-matching test examples.
4. 🗄️ **SQL Explainer**
   - Paste a SQL query and choose your dialect (PostgreSQL, MySQL, SQLite, Snowflake, etc.).
   - Outputs a plain-English high-level summary, clause-by-clause analysis (`SELECT`, `JOIN`, `WHERE`, `GROUP BY`), and performance tips.

---

## 📁 Project Structure

```text
ai project/
├── .env.example              # Template for environment variables
├── .gitignore                # Safeguards secrets (.env) and Python build files
├── requirements.txt          # Minimal Python dependencies
├── app.py                    # Streamlit UI with sidebar navigation & 4 tools
├── utils/
│   ├── __init__.py           # Package marker
│   ├── gemini_client.py      # Official google-genai client & API caller
│   └── prompts.py            # Optimized, token-efficient system instructions & templates
└── README.md                 # Project documentation & quickstart
```

---

## 🚀 Quickstart Guide

### 1. Prerequisites
- Python 3.10+ installed ([python.org](https://www.python.org/downloads/))

### 2. Clone or Open the Project
Open a terminal in the project directory:
```bash
cd "c:\Users\yuvak\OneDrive\Desktop\All-My-Codes\python\ai project"
```

### 3. Create and Activate a Virtual Environment (Recommended)
```bash
# Windows (PowerShell)
python -m venv .venv # to create virtual env
.\.venv\Scripts\Activate.ps1 #to run virtual env

# Windows (Command Prompt)
# .venv\Scripts\activate.bat

# macOS / Linux
# python3 -m venv .venv
# source .venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Get a Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Sign in with your Google account.
3. Click **"Create API Key"** and copy your key.

### 6. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
# Windows PowerShell:
Copy-Item .env.example .env

# Bash / Zsh:
# cp .env.example .env
```
Open `.env` and paste your key:
```env
GEMINI_API_KEY=AIzaSyYourActualKeyHere
```

*(Alternatively, you can skip editing `.env` and enter your API key directly into the Streamlit sidebar input when the app is running!)*

### 7. Run the Application
```bash
streamlit run app.py
```
Streamlit will automatically open your browser at `http://localhost:8501`.

---

## ⚡ Token Efficiency & Design Decisions

- **Fast & Inexpensive Model**: Uses `gemini-3.8-flash` for low latency, near-zero cost, and strong code reasoning.
- **Strict System Instructions**: System instructions in `utils/prompts.py` demand direct markdown tables and code blocks without conversational filler ("Certainly! Here is your answer:"), saving 20–40% on output tokens per prompt.
- **Deterministic Temperatures**: Low temperature settings (`0.1`–`0.3`) ensure consistent, reproducible explanations for code, SQL, and regex syntax.
- **Graceful Error Handling**: Detects quota limits (HTTP 429), invalid keys, and network timeouts, presenting helpful notifications directly in the Streamlit UI.



Created by yuva kiran