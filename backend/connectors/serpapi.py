from .base import JobDiscoveryConnector
from typing import List, Dict, Any
from datetime import datetime
from serpapi import GoogleSearch

class SerpAPIConnector(JobDiscoveryConnector):
    key = "serpapi"

    def __init__(self, api_key: str):
        self.api_key = api_key

    async def search_recent_jobs(self, query: Dict[str, Any], since: datetime) -> List[Dict[str, Any]]:
        search = GoogleSearch({
            "q": " ".join(query.get("keywords", [])),
            "engine": "google_jobs",
            "api_key": self.api_key,
        })

        results = search.get_dict()
        jobs = []

        if "jobs_results" in results:
            for result in results["jobs_results"]:
                jobs.append({
                    "external_id": result.get("job_id"),
                    "job_title": result.get("title"),
                    "company": result.get("company_name"),
                    "location": result.get("location"),
                    "posting_url": result.get("related_links", [{}])[0].get("link"),
                    "posting_date": None, # SerpAPI does not provide a posting date
                    "raw": result,
                })

        return jobs
