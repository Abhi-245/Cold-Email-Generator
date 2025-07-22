import os
import re
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

# Load environment variables from .env
load_dotenv()

# Token Limit Constants
MAX_TOKENS = 3000  # reduced to stay safer under Groq’s 6000 TPM limit

def truncate_text(text, max_tokens=MAX_TOKENS):
    return text[:max_tokens * 4]  # 1 token ≈ 4 chars


class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama3-70b-8192"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the careers page of a website.
            Your job is to extract the job postings and return them in JSON format containing the
            following keys: `role`, `experience`, `location`, `job id`, `skills`, and `description`.
            Make sure the `skills` field is **never empty**. If skills are not directly listed, infer them based on job responsibilities or common sense.
            Only return the valid JSON.
             ### VALID JSON (NO PREAMBLE):
            """
        )

        truncated_text = truncate_text(cleaned_text)
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": truncated_text})

        try:
            json_parser = JsonOutputParser()
            parsed = json_parser.parse(res.content)
        except OutputParserException as e:
            print("❌ Parsing failed:", res.content[:1000])  # print first 1000 chars for debugging
            raise OutputParserException("Context too big. Unable to parse jobs.") from e

        return parsed if isinstance(parsed, list) else [parsed]

    def extract_job_id(self, text):
        match = re.search(
            r"(?:job[\s\-:]?id|job[\s\-:]?ref(?:erence)?|req(?:uisition)?)[:#\-\s]*([A-Za-z0-9\-]+)",
            text,
            re.IGNORECASE
        )
        return match.group(1) if match else "Not Found"

    def write_mail(self, job, links):
        job_str = str(job)
        job_id = self.extract_job_id(job_str)

        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description}

            ### INSTRUCTION:
            You are Abhi, a business development executive at Multiverse. Multiverse is an AI & Software Consulting company dedicated to facilitating
            the seamless integration of business processes through automated tools. 
            Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
            process optimization, cost reduction, and heightened overall efficiency. 
            Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Multiverse
            in fulfilling their needs, and make sure to include the job id: {job_id}
            Also add the most relevant ones from the following links to showcase Multiverse's portfolio: {link_list}
            Remember you are Abhi, BDE at Multiverse. 
            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):
            """
        )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": job_str,
            "job_id": job_id,
            "link_list": links
        })
        return res.content