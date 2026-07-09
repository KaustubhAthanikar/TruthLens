from ddgs import DDGS
def search_web(query:str):
    results=[]

    with DDGS() as ddgs:
        for r in ddgs.text(query,max_results=5):
            results.append({

                "title": r["title"],

                "url": r["href"]

            })
    
    return results