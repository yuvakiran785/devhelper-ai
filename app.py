"""
DevHelper AI - Main Streamlit Application
A lightweight, beginner-friendly developer toolkit powered by Gemini 2.5 and Streamlit.
"""

import os
import streamlit as st
from dotenv import load_dotenv

from utils.gemini_client import (
    DEFAULT_MODEL,
    GeminiClientError,
    explain_python_error,
    generate_git_commit,
    explain_regex_pattern,
    explain_sql_query,
    get_active_api_key,
)

# Load environment variables use below code
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="DevHelper AI - Developer Toolkit",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for polished developer-centric aesthetics
st.markdown(
    """
    <style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
        background: linear-gradient(90deg, #3b82f6, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #64748b;
        margin-bottom: 1.5rem;
    }
    .status-badge {
        display: inline-block;
        padding: 0.2rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    .status-active {
        background-color: #dcfce7;
        color: #166534;
    }
    .status-missing {
        background-color: #fee2e2;
        color: #991b1b;
    }
    .result-container {
        border-radius: 0.5rem;
        border: 1px solid #e2e8f0;
        padding: 1.5rem;
        margin-top: 1rem;
        background-color: #ffffff;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------
# Sidebar Navigation & Settings
# -------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🛠️ **DevHelper AI**")
    st.caption("Lightweight developer toolkit powered by Google Gemini.")
    st.divider()

    st.markdown("### 🔑 API Configuration")
    env_api_key = os.getenv("GEMINI_API_KEY", "")
    user_api_key = st.text_input(
        "Gemini API Key",
        value=env_api_key,
        type="password",
        placeholder="Enter your Gemini API key...",
        help="Get a free key from Google AI Studio: https://aistudio.google.com/app/apikey",
    )

    # API key status indicator
    active_key = get_active_api_key(user_api_key)
    if active_key:
        st.markdown(
            '<span class="status-badge status-active">● API Key Connected</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="status-badge status-missing">○ No API Key Found</span>',
            unsafe_allow_html=True,
        )
        st.caption("👉 [Get a free API key here](https://aistudio.google.com/app/apikey)")

    st.divider()

    # Tool Navigation
    st.markdown("### 🧭 Choose Tool")
    tool = st.radio(
        label="Select a tool",
        options=[
            "🐛 Python Error Explainer",
            "📝 Git Commit Generator",
            "🔍 Regex Explainer",
            "🗄️ SQL Explainer",
        ],
        label_visibility="collapsed",
    )

    st.divider()
    st.markdown("### ⚙️ Engine Specs")
    st.markdown(f"**Model:** `{DEFAULT_MODEL}`")
    st.caption("Fast, cost-efficient, and optimized for code tasks without heavy frameworks.")


# -------------------------------------------------------------
# Tool 1: Python Error Explainer
# -------------------------------------------------------------
if tool == "🐛 Python Error Explainer":
    st.markdown('<div class="main-header">🐛 Python Error Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Paste a Python error or traceback to get a plain-English diagnosis and a minimal working code fix.</div>',
        unsafe_allow_html=True,
    )

    # Example loader button
    col_ex, _ = st.columns([1, 4])
    with col_ex:
        if st.button("📋 Load Example Error", key="btn_err_example"):
            st.session_state["err_traceback"] = (
                "Traceback (most recent call last):\n"
                '  File "app.py", line 12, in calculate_average\n'
                "    total = sum(data)\n"
                "TypeError: unsupported operand type(s) for +: 'int' and 'str'"
            )
            st.session_state["err_code"] = (
                "def calculate_average(data):\n"
                "    total = sum(data)\n"
                "    return total / len(data)\n\n"
                "results = calculate_average([10, 20, '30', 40])"
            )

    traceback_input = st.text_area(
        "Traceback or Error Message *",
        value=st.session_state.get("err_traceback", ""),
        height=140,
        placeholder="Paste your Python traceback or error output here...",
    )

    code_input = st.text_area(
        "Relevant Code Snippet (Optional)",
        value=st.session_state.get("err_code", ""),
        height=140,
        placeholder="Paste the function or code block that caused the error (optional)...",
    )

    if st.button("🔍 Diagnose & Fix Error", type="primary", use_container_width=False):
        if not traceback_input.strip():
            st.warning("Please provide a traceback or error message to diagnose.")
        else:
            with st.spinner("Analyzing traceback with Gemini..."):
                try:
                    result = explain_python_error(
                        traceback_text=traceback_input,
                        code_snippet=code_input,
                        api_key=active_key,
                    )
                    st.success("Analysis Complete!")
                    st.markdown(result)
                except GeminiClientError as gce:
                    st.error(f"⚠️ {str(gce)}")
                except Exception as ex:
                    st.error(f"⚠️ Unexpected error: {str(ex)}")


# -------------------------------------------------------------
# Tool 2: Git Commit Generator
# -------------------------------------------------------------
elif tool == "📝 Git Commit Generator":
    st.markdown('<div class="main-header">📝 Git Commit Generator</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Describe your code changes in casual language to generate clean, Conventional Commit messages.</div>',
        unsafe_allow_html=True,
    )

    col_ex, _ = st.columns([1, 4])
    with col_ex:
        if st.button("📋 Load Example Changes", key="btn_commit_example"):
            st.session_state["commit_desc"] = (
                "Added bcrypt hashing for user passwords during signup and login, "
                "and created unit tests to verify invalid password rejections."
            )
            st.session_state["commit_scope"] = "auth"

    col_desc, col_scope = st.columns([3, 1])
    with col_desc:
        desc_input = st.text_area(
            "What did you change? *",
            value=st.session_state.get("commit_desc", ""),
            height=130,
            placeholder="e.g. Fixed the navbar dropdown not closing when clicking outside on mobile devices...",
        )
    with col_scope:
        scope_input = st.text_input(
            "Scope / Module (Optional)",
            value=st.session_state.get("commit_scope", ""),
            placeholder="e.g. auth, ui, api, db",
            help="Optional module name enclosed in commit parenthesis.",
        )

    if st.button("✨ Generate Commit Message", type="primary"):
        if not desc_input.strip():
            st.warning("Please describe what changes you made.")
        else:
            with st.spinner("Drafting conventional commit message..."):
                try:
                    result = generate_git_commit(
                        description=desc_input,
                        scope=scope_input,
                        api_key=active_key,
                    )
                    st.success("Generated Commit Messages!")
                    st.markdown(result)
                except GeminiClientError as gce:
                    st.error(f"⚠️ {str(gce)}")
                except Exception as ex:
                    st.error(f"⚠️ Unexpected error: {str(ex)}")


# -------------------------------------------------------------
# Tool 3: Regex Explainer
# -------------------------------------------------------------
elif tool == "🔍 Regex Explainer":
    st.markdown('<div class="main-header">🔍 Regex Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Paste any regular expression pattern to get an intuitive token-by-token breakdown and test examples.</div>',
        unsafe_allow_html=True,
    )

    col_ex, _ = st.columns([1, 4])
    with col_ex:
        if st.button("📋 Load Example Regex", key="btn_regex_example"):
            st.session_state["regex_pattern"] = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
            st.session_state["regex_flags"] = "i"

    col_pat, col_flg = st.columns([3, 1])
    with col_pat:
        pattern_input = st.text_input(
            "Regular Expression Pattern *",
            value=st.session_state.get("regex_pattern", ""),
            placeholder=r"^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$",
        )
    with col_flg:
        flags_input = st.text_input(
            "Flags (Optional)",
            value=st.session_state.get("regex_flags", ""),
            placeholder="e.g. g, i, m",
        )

    if st.button("🔍 Explain Regular Expression", type="primary"):
        if not pattern_input.strip():
            st.warning("Please enter a regular expression pattern to explain.")
        else:
            with st.spinner("Deconstructing regex pattern..."):
                try:
                    result = explain_regex_pattern(
                        regex_pattern=pattern_input,
                        flags=flags_input,
                        api_key=active_key,
                    )
                    st.success("Explanation Ready!")
                    st.markdown(result)
                except GeminiClientError as gce:
                    st.error(f"⚠️ {str(gce)}")
                except Exception as ex:
                    st.error(f"⚠️ Unexpected error: {str(ex)}")


# -------------------------------------------------------------
# Tool 4: SQL Explainer
# -------------------------------------------------------------
elif tool == "🗄️ SQL Explainer":
    st.markdown('<div class="main-header">🗄️ SQL Explainer</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="sub-header">Understand complex queries with plain-English summaries, clause breakdowns, and performance notes.</div>',
        unsafe_allow_html=True,
    )

    col_ex, _ = st.columns([1, 4])
    with col_ex:
        if st.button("📋 Load Example SQL", key="btn_sql_example"):
            st.session_state["sql_query"] = (
                "SELECT u.id, u.email, COUNT(o.id) AS total_orders, SUM(o.amount) AS total_spent\n"
                "FROM users u\n"
                "LEFT JOIN orders o ON u.id = o.user_id\n"
                "WHERE u.is_active = TRUE AND o.created_at >= NOW() - INTERVAL '30 days'\n"
                "GROUP BY u.id, u.email\n"
                "HAVING COUNT(o.id) > 5\n"
                "ORDER BY total_spent DESC\n"
                "LIMIT 10;"
            )
            st.session_state["sql_dialect"] = "PostgreSQL"

    col_dialect, _ = st.columns([1, 2])
    with col_dialect:
        dialect_options = ["Standard SQL", "PostgreSQL", "MySQL", "SQLite", "Snowflake", "BigQuery", "SQL Server"]
        selected_dialect = st.selectbox(
            "SQL Dialect",
            options=dialect_options,
            index=dialect_options.index(st.session_state.get("sql_dialect", "PostgreSQL"))
            if st.session_state.get("sql_dialect") in dialect_options else 0,
        )

    sql_input = st.text_area(
        "SQL Query *",
        value=st.session_state.get("sql_query", ""),
        height=180,
        placeholder="Paste your SQL statement here...",
    )

    if st.button("🗄️ Explain SQL Query", type="primary"):
        if not sql_input.strip():
            st.warning("Please provide a SQL query to explain.")
        else:
            with st.spinner("Analyzing SQL logic and query plan..."):
                try:
                    result = explain_sql_query(
                        sql_query=sql_input,
                        dialect=selected_dialect,
                        api_key=active_key,
                    )
                    st.success("Query Breakdown Complete!")
                    st.markdown(result)
                except GeminiClientError as gce:
                    st.error(f"⚠️ {str(gce)}")
                except Exception as ex:
                    st.error(f"⚠️ Unexpected error: {str(ex)}")
