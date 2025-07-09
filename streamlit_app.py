import streamlit as st
import requests

st.set_page_config(page_title="Price Aggregator", layout="centered")
st.title("🛍️ Global Price Aggregator")

country = st.selectbox("Select Country", ["IN", "US"])
query = st.text_input("Enter Product Query", "iPhone 16 Pro, 128GB")

if st.button("🔍 Search"):
    if not query:
        st.warning("Please enter a product name to search.")
    else:
        with st.spinner("Fetching prices..."):
            try:
                response = requests.post(
                    "http://localhost:8000/search",
                    json={"country": country, "query": query},
                    timeout=60
                )
                if response.status_code == 200:
                    results = response.json()
                    if not results:
                        st.info("No products found.")
                    else:
                        st.success(f"Found {len(results)} result(s):")
                        for product in results:
                            st.write("---")
                            st.markdown(f"**{product['productName']}**")
                            st.markdown(f"💰 Price: `{product['price']} {product['currency']}`")
                            st.markdown(f"🔗 [View Product]({product['link']})")
                            st.markdown(f"🛒 Source: {product['source']}")
                else:
                    st.error(f"❌ API error: {response.status_code} - {response.text}")
            except Exception as e:
                st.error(f"🚨 Request failed: {e}")
