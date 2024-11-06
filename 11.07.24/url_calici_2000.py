import requests
from bs4 import BeautifulSoup
import json
import time

product_urls = []

for page_num in range(1, 501):
    url = f'https://www.trendyol.com/kadin-giyim-x-g1-c82?pi={page_num}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for item in soup.find_all('div', class_='p-card-wrppr'):
        link = 'https://www.trendyol.com' + item.find('a')['href'] if item.find('a') else None
        if link:
            product_urls.append(link)

    time.sleep(1)

with open('trendyol_products_urls.json', 'w', encoding='utf-8') as json_file:
    json.dump(product_urls, json_file, ensure_ascii=False, indent=4)

print("All product URLs saved to trendyol_products_urls.json")
