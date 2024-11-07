import requests
from bs4 import BeautifulSoup
import json
import time

product_urls = []
max_retries = 3
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

for page_num in range(1, 2):
    url = f'https://www.koton.com/erkek-giyim/?page={page_num}'

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    else:
        print(f"Failed to fetch page {page_num} after multiple attempts.")
        continue

    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all product links using the class "js-product-link product-link"
    for item in soup.find_all('a', class_='js-product-link product-link'):
        link = 'https://www.koton.com' + item['href']
        product_urls.append(link)

    time.sleep(1)

# Save the URLs to a JSON file
with open('koton_products_urls.json', 'w', encoding='utf-8') as json_file:
    json.dump(product_urls, json_file, ensure_ascii=False, indent=4)

print("URLs saved to koton_products_urls.json")
