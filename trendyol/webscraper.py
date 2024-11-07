from bs4 import BeautifulSoup
import requests
import json
import os
import time

# Define the categories as a list of keywords, including "Other" as a fallback category
categories_list = [
    "Sweatshirt", "Pantolon", "Gömlek", "Kazak&Hırka", "Elbise",
    "Bluz&Tunik&Büstiyer", "Tayt", "İç Giyim", "Etek", "T-Shirt",
    "Ceket & Yelek", "Jeans", "Tesettür Giyim", "Pardösü & Trençkot",
    "Body", "Alt - Üst Takım", "Kaban & Mont", "Yağmurluk & Rüzgarlık",
    "Polar", "Çorap", "Takım Elbise", "Abiye Elbise", "Mezuniyet Elbiseleri",
    "Polo Yaka T-shirt", "Büyük Beden", "Plaj Giyim", "Kapri & Bermuda",
    "Şort", "Tulum&Salopet", "Kimono & Kaftan", "Other"
]

# Define the colors list
color_list = [
    "Altın", "Bej", "Beyaz", "Bordo", "Ekru", "Gri", "Gümüş", "Haki",
    "Kahverengi", "Kırmızı", "Lacivert", "Mavi", "Metalik", "Mor",
    "Pembe", "Sarı", "Siyah", "Turkuaz", "Turuncu", "Yeşil", "Çok Renkli"
]

categories = {category: [] for category in categories_list}


for page_num in range(1, 501):
    url = f'https://www.trendyol.com/kadin-giyim-x-g1-c82?pi={page_num}'
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')

    for item in soup.find_all('div', class_='p-card-wrppr'):
        name = item.find('span', class_='prdct-desc-cntnr-name').text.strip() if item.find('span',
                                                                                           'prdct-desc-cntnr-name') else 'N/A'
        price = item.find('div', class_='prc-box-dscntd').text.strip() if item.find('div', 'prc-box-dscntd') else 'N/A'
        link = 'https://www.trendyol.com' + item.find('a')['href'] if item.find('a') else 'N/A'

        color = next((col for col in color_list if col.lower() in name.lower()), 'N/A')

        rating = item.find('span', class_='rating-score').text.strip() if item.find('span',
                                                                                    class_='rating-score') else 'N/A'


        size = item.find('span', class_='size-class-name').text.strip() if item.find('span',
                                                                                     'size-class-name') else 'N/A'

        category = next((cat for cat in categories_list if cat.lower() in name.lower()), "Other")


        product_data = {
            'name': name,
            'price': price,
            'link': link,
            'color': color,
            'size': size,
            'rating': rating,
            'category': category
        }

        categories[category].append(product_data)

    time.sleep(1)

for category, products in categories.items():
    if products:
        filename = f'trendyol_products_{category.replace(" ", "_").replace("&", "and")}.json'
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(products, json_file, ensure_ascii=False, indent=4)

print("Data saved to category-specific JSON files")
