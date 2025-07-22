import streamlit as st
import asyncio
import sys

from chains import Chain
from portfolio import Portfolio
from utils import clean_text

from playwright.async_api import async_playwright

# Limit tokens to stay within Groq's on-demand tier (6000 TPM)
MAX_TOKENS = 5000  # 6000 tokens limit, with buffer

def truncate_text(text, max_tokens=MAX_TOKENS):
    return text[:max_tokens * 4]  # Roughly 1 token ≈ 4 characters

# ✅ JavaScript rendering using Playwright
async def fetch_html_playwright(url):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, timeout=60000)
            html = await page.content()
            await browser.close()
            return html
    except Exception as e:
        return f"ERROR::{e}"

def get_dynamic_content(url):
    try:
        html = asyncio.run(fetch_html_playwright(url))
        if isinstance(html, str) and html.startswith("ERROR::"):
            st.error(f"Render failed: {html[7:]}")
            return None
        return html
    except Exception as e:
        st.error(f"Event loop error: {e}")
        return None

# ✅ Main Streamlit App
def create_streamlit_app(chain, portfolio, clean_text):
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    st.title("📧 Cold Mail Generator")

    st.caption(f"🧠 Using Python interpreter: `{sys.executable}`")

    url_input = st.text_input("Enter the URL of the job description:", value="https://apply.workable.com/reebok/j/7E296806CB/")
    submit_button = st.button("Submit")

    if submit_button:
        with st.spinner("🔍 Extracting job info and generating cold email..."):
            try:
                html_text = get_dynamic_content(url_input)
                if not html_text:
                    st.error("Failed to load or render page content.")
                    return

                data = clean_text(html_text)
                truncated_data = truncate_text(data)
                portfolio.load_portfolio()

                jobs = chain.extract_jobs(truncated_data)

                if not jobs:
                    st.warning("No jobs extracted from the page. Try a different URL.")
                    return

                for i, job in enumerate(jobs, 1):
                    skills = job.get('skills', [])
                    if not skills:
                        st.warning(f"No skills found for job #{i}. Skipping.")
                        continue

                    links = portfolio.query_links(skills)
                    email = chain.write_mail(job, links)

                    with st.expander(f"✉️ Cold Email #{i}"):
                        st.markdown(email, unsafe_allow_html=True)

                st.success("✅ Cold email(s) generated successfully!")

            except Exception as e:
                st.error(f"An error occurred: {e}")

# ✅ Entry Point
if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    create_streamlit_app(chain, portfolio, clean_text)