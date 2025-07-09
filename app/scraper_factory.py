from app.scrapers import amazon_tavily, flipkart_tavily, amazon_us_tavily

def get_scrapers(country: str):
    return {
        "IN": [amazon_tavily, flipkart_tavily],
        "US": [amazon_us_tavily],
    }.get(country.upper(), [])
