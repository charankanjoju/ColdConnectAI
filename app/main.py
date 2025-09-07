import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import os

os.environ["USER_AGENT"] = "cold-email-generator/1.0"

# Inject custom dashboard CSS
def add_dashboard_css():
    st.markdown(
        """
        <style>
        /* Background */
        body {
            background: #0d0d0d;
            font-family: 'Segoe UI', sans-serif;
        }

        /* App container */
        .stApp {
            background-color: #0d0d0d;
            padding: 0;
        }

        /* Top navigation bar */
        .top-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background: #1a1a1a;
            padding: 1rem 2rem;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .top-bar h2 {
            color: white;
            margin: 0;
            font-size: 1.2rem;
            letter-spacing: 1px;
        }
        .nav-links {
            display: flex;
            gap: 1.5rem;
        }
        .nav-links a {
            color: #ccc;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }
        .nav-links a:hover {
            color: #fff;
        }

        /* Dashboard cards */
        .card {
            background: #1a1a1a;
            border-radius: 18px;
            padding: 1.5rem;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5);
            color: #eee;
            margin-bottom: 1.5rem;
        }
        .card h3 {
            color: #fff;
            margin-bottom: 1rem;
        }

        /* Input styling */
        input[type="text"] {
            background: #262626 !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            color: #fff !important;
            border-radius: 10px;
            padding: 0.6rem 1rem !important;
        }

        input[type="text"]::placeholder {
            color: #888 !important;
        }

        /* Button */
        button {
            background: linear-gradient(135deg, #00c6ff, #0072ff) !important;
            border: none !important;
            border-radius: 12px !important;
            color: #fff !important;
            padding: 0.6rem 1.5rem !important;
            font-weight: bold !important;
            transition: transform 0.2s ease-in-out;
        }
        button:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        }

        /* Code block for email */
        pre {
            background: #0f0f0f !important;
            border-radius: 12px !important;
            padding: 1rem !important;
            color: #00ffcc !important;
            font-size: 0.9rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def create_streamlit_app(llm, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    add_dashboard_css()

    # Top nav bar
    st.markdown(
        """
       <div class="top-bar">
    <h1>Cold Email Generator</h1>
</div>

<style>
.top-bar {
    display: flex;
    justify-content: center;  /* Centers horizontally */
    align-items: center;      /* Centers vertically */
    padding: 1.5rem 0;
    background: transparent;  /* or use a dark bar if you want */
}

.top-bar h1 {
    color: white;
    font-size: 2.5rem;
    font-weight: 700;
    margin: 0;
    text-align: center;
}
</style>

        """,
        unsafe_allow_html=True,
    )

    # Layout: Left input | Right output
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown('')
        st.markdown("### 🔍 Job Input")
        url_input = st.text_input(
            "Enter Job URL",
            value="",
            placeholder="Paste the job listing URL here..."
        )
        submit_button = st.button("🚀 Generate Email")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('')
        st.markdown("### 📩 Generated Cold Email")

        if submit_button:
            try:
                loader = WebBaseLoader([url_input])
                data = clean_text(loader.load().pop().page_content)
                portfolio.load_portfolio()
                jobs = llm.extract_jobs(data)
                for job in jobs:
                    skills = job.get('skills', [])
                    links = portfolio.query_links(skills)
                    email = llm.write_mail(job, links)
                    st.code(email, language='markdown')
            except Exception as e:
                st.error(f"⚠️ An Error Occurred: {e}")
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)
