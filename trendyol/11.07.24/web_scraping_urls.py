import requests
from bs4 import BeautifulSoup
import json

def scrape_item_attributes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    attributes = {}
    detail_attr_items = soup.select('ul.detail-attr-container li.detail-attr-item')

    for item in detail_attr_items:
        key_element = item.select_one('.attr-key-name-w')
        value_element = item.select_one('.attr-value-name-w')

        if key_element and value_element:
            key = key_element.text.strip()
            value = value_element.text.strip()
            attributes[key] = value

    return attributes

with open('trendyol_products_urls.json', 'r') as file:
    urls = json.load(file)

scraped_data = []

for url in urls:
    attributes = scrape_item_attributes(url)
    scraped_data.append({
        "url": url,
        "attributes": attributes
    })

with open('scraped_product_data.json', 'w', encoding='utf-8') as json_file:
    json.dump(scraped_data, json_file, ensure_ascii=False, indent=4)

print("Scraped data saved to scraped_product_data.json")
