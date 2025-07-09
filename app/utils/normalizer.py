def normalize_price(price_text):
    return float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
