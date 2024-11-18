import requests
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("SCRAPER_API_KEY")

def query_scraper_api(query):
    print(API_KEY)
    google_search_url = f"https://www.google.com/search?q={query}"
    print(google_search_url)
    url = f"http://api.scraperapi.com?api_key={API_KEY}&url={google_search_url}"
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        return extract_google_results(html_content) 
    else:
        raise Exception(f"Error with ScraperAPI: {response.status_code}")
    
def query_scraper_apiq():
    status_code=200
    
    if status_code == 200:
        html_content = response.text
        return extract_google_results(html_content) 
    else:
        raise Exception(f"Error with ScraperAPI: {response.status_code}")
        
def extract_google_results(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    results = []
    
    for result in soup.select("div#search div.g"):
        title = result.select_one("h3").get_text() if result.select_one("h3") else None
        link = result.select_one("a")["href"] if result.select_one("a") else None
        
        # Try to get the snippet from the div or span (more meaningful content)
        snippet = None
        
        # Check for snippet in the common span/div containing description
        if result.select_one(".IsZvec"):
            snippet = result.select_one(".IsZvec").get_text()  # This might be one of the snippet divs
        elif result.select_one("span.st"):
            snippet = result.select_one("span.st").get_text()  # Another common tag for snippets
        elif result.select_one("div.VwiC3b"):
            snippet = result.select_one("div.VwiC3b").get_text()  # Sometimes snippets are inside VwiC3b divs
        elif result.select_one("div.BVG0Nb"):  # Additional check for another common snippet div
            snippet = result.select_one("div.BVG0Nb").get_text()

        # If no snippet is found, add placeholder text
        if not snippet:
            snippet = "No meaningful snippet available"
        
        # Append the result to the list
        results.append({
            "title": title,
            "link": link,
            "snippet": snippet
        })

        # Now handle the additional content outside of the search results under div.jsname="PLkx0b"
        additional_info = soup.select_one('div[jsname="PLkx0b"]')

        # If div.jsname="PLkx0b" exists, append it as an additional result
        if additional_info:
            results.append({
                "title": "Additional Information",  # Title for this extra content
                "link": "",  # Empty link, as it's not a search result link
                "snippet": additional_info.get_text()  # Extract text from div.jsname="PLkx0b"
            })
    
    return results

def process_local_html(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            html_content = file.read()
            results = extract_google_results(html_content)
            return results
    except Exception as e:
        return str(e)

# Example Usage
if __name__ == "__main__":
    file_path = "./email of jpmorgan - Google Search.html"  # Path to your stored HTML file
    search_results = process_local_html(file_path)
    print(search_results)
