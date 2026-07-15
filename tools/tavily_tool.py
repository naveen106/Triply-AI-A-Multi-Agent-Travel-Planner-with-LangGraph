from tavily import TavilyClient
from exa_py import Exa
import os
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
exa_client = Exa(api_key=os.environ.get("EXA_API_KEY"))

def tavily_search(query):
    response = client.search(query=query, max_results=5)
    results = []
    
    for i,r in enumerate(response['results']):
        title = r.get("title", "No Title")
        url = r.get("url", "")
        snippet = r.get("content", "").strip()

        #Keep only first 300 chars to avoid wall-of-text
        if len(snippet) > 300:
            snippet = snippet[:300].rsplit(" ",1)[0] + "..."
        results.append(f"{i}. **{title}**\n {url}\n {snippet}\n")
    return "\n\n".join(results)
        

def exa_search(query):

    response = exa_client.search(query=query, num_results=5)
    results = response.results if hasattr(response, 'results') else []
    final = []
    for result in results:
        title = result.title if hasattr(result, 'title') else "No title"
        url = result.url if hasattr(result, 'url') else ""
        published_date = result.published_date if hasattr(result, 'publishedDate') else ""
       
        image = result.image if hasattr(result, 'image') else None
        text = result.text if hasattr(result, 'text') else None
        #Keep only first 300 chars to avoid wall-of-text
        if len(text) > 1000:
            text = text[:400].rsplit(" ",1)[0] + "..."
        final.append(f"**{title}**\n {published_date}\n {url}\n {image}\n {text}\n")
    return "\n\n".join(final)