from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

class ResumeParsingConnector(ABC):
    @abstractmethod
    def parse_resume(self, resume_text: str) -> dict:
        pass

class JobDiscoveryConnector(ABC):
    key: str

    @abstractmethod
    async def search_recent_jobs(self, query: Dict[str, Any], since: datetime) -> List[Dict[str, Any]]:
        pass
