import requests
from bs4 import BeautifulSoup
import json
import time

# Base URL for the main category page
base_url = "https://www.trendyol.com/kadin-giyim-x-g1-c82"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
}

# Initialize a list to store product data
product_data = []

# Step 1: Request the main category page
response = requests.get(base_url, headers=headers)
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    # Step 2: Find all product links on the main page
    products = soup.select('a[href^="/"]')  # Use 'a[href^="/"]' to find links starting with '/'
    if not products:
        print("No products found on the main page. Check the selector or webpage content.")

    # Step 3: Loop through each product link
    for product in products:
        product_url = "https://www.trendyol.com" + product['href']

        # Additional filtering if necessary
        if "/p-" not in product_url:
            continue

        print(f"Scraping product at {product_url}")

        # Request the product page
        product_response = requests.get(product_url, headers=headers)
        if product_response.status_code == 200:
            product_soup = BeautifulSoup(product_response.text, 'html.parser')

            try:
                # Extract product title
                title = product_soup.select_one('h1.prdct-desc-cntnr-ttl').get_text(strip=True)

                # Extract product rating if available
                rating = product_soup.select_one('span.rating-score')
                rating = rating.get_text(strip=True) if rating else "No rating"

                # Extract number of favorites if available
                favorites = product_soup.select_one('.social-proof-text .focused-text')
                favorites = favorites.get_text(strip=True) if favorites else "No favorites"

                # Extract product details from the detail-attr-container list
                attributes = {}
                details_section = product_soup.select('ul.detail-attr-container li.detail-attr-item')

                for item in details_section:
                    key = item.select_one('span.attr-name.attr-key-name-w').get_text(strip=True)
                    value = item.select_one('div.attr-name.attr-value-name-w').get_text(strip=True)
                    attributes[key] = value  # Add key-value pair to the attributes dictionary

                # Append product data (URL, title, rating, favorites, attributes) to the main list
                product_data.append({
                    "url": product_url,
                    "title": title,
                    "rating": rating,
                    "favorites": favorites,
                    "attributes": attributes
                })
                print(f"Scraped data for {product_url}")

            except Exception as e:
                print(f"Error fetching data from {product_url}: {e}")
        else:
            print(f"Failed to load product page: {product_url}")

        # Optional: Pause to avoid overloading the server
        time.sleep(1)
else:
    print("Failed to load main page. Check the URL or network connection.")

# Save the extracted data to a JSON file
with open("trendyol_product_data.json", "w", encoding="utf-8") as f:
    json.dump(product_data, f, ensure_ascii=False, indent=4)

print("Data has been saved to trendyol_product_data.json")
