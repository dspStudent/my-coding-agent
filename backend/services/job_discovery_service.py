from sqlalchemy.orm import Session
from backend.db import crud
from backend.connectors import JobBoardScraperConnector, SerpAPIConnector
from datetime import datetime, timedelta

def get_discovery_connectors(db: Session, user_id: int):
    connectors = []
    # Correctly reference the function through the `crud` namespace
    user_data_sources = crud.get_user_data_sources_by_user_id_and_type(db, user_id, "job_discovery")

    for user_data_source in user_data_sources:
        if user_data_source.data_source.key == "job_board_scraper":
            connectors.append(JobBoardScraperConnector())
        elif user_data_source.data_source.key == "serpapi":
            connectors.append(SerpAPIConnector(api_key=user_data_source.encrypted_credentials))

    return connectors

async def run_discovery(db: Session, user_id: int, query: dict):
    since = datetime.now() - timedelta(days=1)
    connectors = get_discovery_connectors(db, user_id)

    all_jobs = []
    for connector in connectors:
        jobs = await connector.search_recent_jobs(query, since)
        all_jobs.extend(jobs)

    # In a real application, you would save the jobs to the database here
    # and de-duplicate them.

    return all_jobs
