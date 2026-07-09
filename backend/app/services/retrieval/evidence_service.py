from app.services.retrieval.search_service import search_web
from app.services.retrieval.scraper_service import scrape_article
from urllib.parse import urlparse
from datetime import datetime

def get_domain(url):
    return urlparse(url).netloc

def retrieve_evidence(query:str):
    search_results=search_web(query)
    evidence=[]

    for result in search_results:
        content = scrape_article(result["url"])

        if len(content)<100:
            continue
        evidence.append({
            "title":result["title"],
            "url":result["url"],
            "source":get_domain(result["url"]),
            "content":content,
            "retrieved_at":datetime.now(),
            "credibility_score":None,
            "similarity_score":None
        })

    return evidence