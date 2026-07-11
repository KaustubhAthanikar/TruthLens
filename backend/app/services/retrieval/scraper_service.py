import requests

from bs4 import BeautifulSoup



def scrape_article(url):


    try:

        response = requests.get(
            url,
            timeout=100,
            headers={"User-Agent":"Mozilla/5.0"})


        soup = BeautifulSoup(response.text,"lxml")



        for tag in soup(["script","style","nav", "footer"]):
            tag.extract()

        paragraphs = soup.find_all("p")

        text = ""

        for p in paragraphs:
            text += p.get_text()+ " "
            
        return text.strip()


    except Exception as e:


        print("Scraping failed:",e)


        return ""