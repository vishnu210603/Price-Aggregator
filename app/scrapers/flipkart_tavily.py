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

async def extract_price_from_flipkart(url: str) -> float:
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            res = await client.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "lxml")

        # Try best selectors
        selectors = [
            "._30jeq3",                # Regular product price
            "._16Jk6d",                # Alternate layout
            "._25b18c ._30jeq3",       # Within container
            "._1VZFMf ._30jeq3",       # New layout
        ]
        for sel in selectors:
            tag = soup.select_one(sel)
            if tag:
                return normalize_price(tag.text)

        # Fallback: ₹ prefix and skip offers
        for text in soup.stripped_strings:
            if "₹" in text and all(x not in text.lower() for x in ["off", "%", "discount", "cashback", "save"]):
                try:
                    value = normalize_price(text)
                    if value > 100:
                        return value
                except:
                    continue
    except Exception as e:
        print(f"❌ Flipkart price extraction failed from {url}: {e}")
    return 0.0

async def scrape(query: str):
    try:
        res = tc.search(query=f"{query} site:flipkart.com")
        raw_results = res.get("results", [])[:5]

        items = []
        for r in raw_results:
            title = r.get("title", "")
            url = r.get("url", "")
            if not url or not title:
                continue

            if is_match(query, title):
                price = await extract_price_from_flipkart(url)
                items.append({
                    "productName": title,
                    "link": url,
                    "price": price,
                    "currency": "INR",
                    "source": "Flipkart"
                })

        return items
    except Exception as e:
        print(f"❌ Flipkart Tavily scraping failed: {e}")
        return []
