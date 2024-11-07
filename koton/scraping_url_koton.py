import requests
from bs4 import BeautifulSoup
import json
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

max_retries = 3

def scrape_item_attributes(url):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            attributes = {}
            product_details_section = soup.find_all('div', class_='product-info__list-item')

            for detail in product_details_section:
                p_tag = detail.find('p')
                if p_tag:
                    text = p_tag.get_text(separator=" ", strip=True)

                    if "Model Bilgileri" not in text:
                        parts = text.split('\n')
                        for part in parts:
                            if ':' in part:
                                key, value = part.split(':', 1)
                                attributes[key.strip()] = value.strip()

            return attributes
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}. Retrying ({attempt + 1}/{max_retries})...")
            time.sleep(1)
    print(f"Failed to fetch {url} after {max_retries} attempts.")
    return {}

with open('koton_products_urls.json', 'r') as file:
    urls = json.load(file)

scraped_data = []

start_time = time.time()

for i, url in enumerate(urls, start=1):
    attributes = scrape_item_attributes(url)
    scraped_data.append({
        "url": url,
        "attributes": attributes
    })

    elapsed_time = time.time() - start_time
    avg_time_per_url = elapsed_time / i
    remaining_urls = len(urls) - i
    estimated_remaining_time = avg_time_per_url * remaining_urls

    print(f"Scraped {i}/{len(urls)}. Estimated time remaining: {estimated_remaining_time:.2f} seconds.")

    time.sleep(1)

total_time = time.time() - start_time

with open('scraped_product_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

print("Scraped data saved to scraped_product_data.json")
print(f"Total scraping time: {total_time:.2f} seconds")
