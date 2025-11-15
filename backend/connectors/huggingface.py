from .base import ResumeParsingConnector
from transformers import pipeline
import json

class HuggingFaceConnector(ResumeParsingConnector):
    def __init__(self):
        self.pipe = pipeline("question-answering", model="deepset/roberta-base-squad2")

    def parse_resume(self, resume_text: str) -> dict:
        questions = {
            "name": "What is the name of the candidate?",
            "email": "What is the email of the candidate?",
            "phone": "What is the phone number of the candidate?",
            "skills": "What are the skills of the candidate?",
        }

        results = {}
        for key, question in questions.items():
            result = self.pipe(question=question, context=resume_text)
            results[key] = result["answer"]

        return results
