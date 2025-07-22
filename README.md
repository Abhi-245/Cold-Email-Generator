# 📧 Cold Email Generator for Job Outreach

This project is a smart **Cold Email Generator** that extracts job descriptions from dynamic websites, understands the content using LLMs, and generates a tailored cold email showcasing your company’s capabilities — all in one click using Streamlit.

---

## 🚀 Features

- ✅ **Web scraping** with JavaScript rendering using Playwright
- ✅ **LLM-powered job data extraction** using Groq's LLaMA3 70B model
- ✅ **Cold email generation** tailored to each job post
- ✅ **Portfolio matching**: Links your past work to the job's required skills
- ✅ **Streamlit web app** for an easy-to-use UI

---

## 🧠 How It Works

1. You paste a job URL into the app
2. Playwright renders and extracts the webpage content
3. The LLM:
   - Parses and extracts structured job info: role, skills, job ID, description, etc.
   - Crafts a personalized email using your company pitch and portfolio
4. The email is displayed on screen, ready to send

---

## 🛠️ Tech Stack

| Tool        | Purpose |
|-------------|---------|
| 🐍 Python   | Core programming |
| 🦙 Groq (LLaMA3 70B) | LLM API for job extraction & email writing |
| 🦊 Playwright | JS rendering & dynamic scraping |
| 🌐 Streamlit | Front-end UI |
| 🧬 LangChain | Prompt chaining |
| 📦 dotenv   | API key management |
| 📚 ChromaDB | Portfolio link similarity search |

---

## 📁 Folder Structure

App/
├── chains.py            # Handles extraction and email writing chains
├── main.py              # Streamlit app entry point
├── portfolio.py         # Portfolio search logic
├── utils.py             # HTML cleaning & text utilities
├── .env                 # (ignored) Your Groq API Key


## ⚙️ Setup Instructions

Run the app

streamlit run main.py

🌍 Example Usage

Job link : https://careers.nike.com/specialist-ii-marketing-streetwear-jordan-emea/job/R-65158

<img width="1319" height="386" alt="Screenshot 2025-07-22 at 11 27 17 PM" src="https://github.com/user-attachments/assets/6fa7aa9f-a09a-49f3-99db-fb3d8424867f" />

<img width="1424" height="750" alt="Screenshot 2025-07-22 at 11 30 34 PM" src="https://github.com/user-attachments/assets/26c66279-f513-47ba-a124-5c06f999c92f" />

🧠 Limitations
	•	May not extract jobs from poorly structured or heavily obfuscated websites
	•	Groq’s API has token limits (~6000 TPM on free tier)
	•	Not production-ready for spam-free email delivery

📈 Future Improvements
	•	Add support for batch job link input
	•	Enhance error handling for edge cases
	•	Auto-send emails via SMTP integration
	•	Dockerize the whole app

Abhishek Dhakne
Data Scientist | IIT Madras 💼🤖
GitHub: @Abhi-245
LinkedIn: linkedin.com/in/abhishekdhakne


