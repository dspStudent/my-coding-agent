from abc import ABC, abstractmethod

class ResumeParsingConnector(ABC):
    @abstractmethod
    def parse_resume(self, resume_text: str) -> dict:
        pass
