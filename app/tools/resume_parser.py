from pathlib import Path
import json

import fitz
from docx import Document

from app.schema.candidate import Candidate
from app.core.gemini import ask_gemini



class PDFTool:


    def extract_text(
        self,
        file_path:str
    ) -> str:


        document = fitz.open(file_path)

        text=""


        for page in document:

            text += page.get_text()


        document.close()


        return text



class DocxTool:

    def extract_text(
        self,
        file_path:str
    ) -> str:


        document = Document(file_path)

        return "\n".join(
            p.text
            for p in document.paragraphs
        )

class GeminiResumeParser:


    def extract_candidate(
        self,
        resume_text:str
    ) -> Candidate:


        prompt=f"""

You are an expert technical recruiter.

Extract candidate information from the resume.

Return ONLY valid JSON.

Follow this EXACT structure:


{{
"name": null,

"email": null,

"phone": null,


"skills": [],


"experience": null,


"education": [
    {{
        "degree": null,
        "university": null,
        "year": null
    }}
],


"certifications": [],


"projects": [
    {{
        "name": null,
        "description": null,
        "technologies": [],
        "github": null,
        "live_url": null
    }}
],


"linkedin": null,

"github": null

}}



IMPORTANT RULES:

1. skills must be a list of strings.

Example:

[
"Python",
"FastAPI",
"PostgreSQL"
]


2. education must be a list of objects.

Correct:

[
{{
"degree":"BS Computer Science",
"university":"ABC University",
"year":"2024"
}}
]


3. projects must ALWAYS be a list of objects.

Correct:

[
{{
"name":"Advanced Laptop Agent",
"description":"AI agent that controls laptop tasks",
"technologies":[
"Python",
"Gemini API"
],
"github":"https://github.com/example",
"live_url":null
}}
]


Wrong:

[
"Advanced Laptop Agent"
]


4. If information is missing:
- strings → null
- lists → []


Resume:

{resume_text}

"""


        response = ask_gemini(prompt)


        response = (
            response
            .replace("```json","")
            .replace("```","")
            .strip()
        )


        try:

            data=json.loads(response)

        except json.JSONDecodeError:

            raise ValueError(
                f"Gemini returned invalid JSON:\n{response}"
            )


        return Candidate(**data)



class ResumeParserAgent:


    def __init__(self):

        self.pdf_tool=PDFTool()

        self.docx_tool=DocxTool()

        self.gemini=GeminiResumeParser()


    def run(
        self,
        file_path:str
    )->Candidate:


        extension=Path(file_path).suffix.lower()



        if extension==".pdf":

            text=self.pdf_tool.extract_text(
                file_path
            )


        elif extension==".docx":

            text=self.docx_tool.extract_text(
                file_path
            )


        else:

            raise ValueError(
                "Unsupported file type"
            )

        candidate=self.gemini.extract_candidate(
            text
        )

        return candidate