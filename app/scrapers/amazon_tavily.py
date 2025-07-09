import os
from dotenv import load_dotenv
from tavily import TavilyClient
from app.utils.matcher import is_match
from app.utils.normalizer import normalize_price
import httpx
from bs4 import BeautifulSoup

load_dotenv()
tc = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

async def extract_price_from_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=15) as client:
            res = await client.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")
        price_tag = soup.select_one(".a-price .a-offscreen")
        if price_tag:
            return normalize_price(price_tag.text)
    except Exception as e:
        print(f"Error extracting price from {url}: {e}")
    return 0.0

async def scrape(query):
    res = tc.search(query=f"{query} site:amazon.in")
    items = []
    for r in res.get("results", [])[:5]:
        title = r.get("title", "")
        url = r.get("url", "")
        if is_match(query, title):
            price = await extract_price_from_page(url)
            items.append({
                "productName": title,
                "link": url,
                "price": price,
                "currency": "INR",
                "source": "Amazon India"
            })
    return items
