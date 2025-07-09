import os
from dotenv import load_dotenv
from tavily import TavilyClient
from app.utils.matcher import is_match
from app.utils.normalizer import normalize_price
import httpx
from bs4 import BeautifulSoup

load_dotenv()
API_KEY = os.getenv("TAVILY_API_KEY")
tc = TavilyClient(api_key=API_KEY)

async def extract_price_from_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")

        # Try multiple selectors for Amazon US
        selectors = [
            ".a-price .a-offscreen",                # Standard price
            "#corePrice_feature_div .a-offscreen",  # Featured price
            "#priceblock_ourprice",                 # Old selector
            "#priceblock_dealprice"                 # Deal price
        ]
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                return normalize_price(tag.text)

        # Fallback: Parse any $-prefixed value
        for text in soup.stripped_strings:
            if "$" in text:
                try:
                    value = normalize_price(text)
                    if value > 10:
                        return value
                except:
                    continue
    except Exception as e:
        print(f"❌ Amazon US price extraction failed from {url}: {e}")
    return 0.0

async def scrape(query):
    res = tc.search(query=f"{query} site:amazon.com")
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
                "currency": "USD",
                "source": "Amazon US"
            })
    return items
