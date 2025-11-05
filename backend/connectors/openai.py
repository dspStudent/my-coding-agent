from .base import ResumeParsingConnector
from openai import OpenAI
import json

class OpenAIConnector(ResumeParsingConnector):
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)

    def parse_resume(self, resume_text: str) -> dict:
        prompt = f"""
        Please parse the following resume text and extract the following information in a JSON format:
        - name (string)
        - email (string)
        - phone (string)
        - skills (list of strings)
        - experience (list of objects, each with 'title', 'company', and 'duration' strings)

        Resume Text:
        {resume_text}
        """

        response = self.client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that parses resumes and returns JSON."},
                {"role": "user", "content": prompt}
            ]
        )

        try:
            return json.loads(response.choices[0].message.content)
        except (json.JSONDecodeError, IndexError):
            return {}
