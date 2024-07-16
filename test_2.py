import requests
from bs4 import BeautifulSoup
import json


class EbayScraper:
    def __init__(self, url):
        self.url = url
        self.data = {}

    def fetch_page(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return None

    def parse_data(self, html):
        soup = BeautifulSoup(html, 'lxml')

        # Назва товару
        title = soup.find('h1', class_='x-item-title__mainTitle').text.strip()

        # Фото товару
        image = soup.find('div', class_='ux-image-carousel zoom img-transition-medium').find('img')['data-zoom-src']

        # Ціна товару
        price = soup.find('div', class_='x-price-primary').text

        # Продавець
        link_for_seller_foun = soup.find('div', class_='vim x-sellercard-atf').next_element['href']
        start_index = link_for_seller_foun.find('ssn=') + 4
        end_index = link_for_seller_foun.find('&')
        seller_link = 'https://www.ebay.com/str/' + link_for_seller_foun[start_index:end_index]

        # Ціна доставки
        shipping = soup.find('div', class_='ux-labels-values col-12 ux-labels-values--shipping').find('div',
                                                                                                      class_='ux-labels-values__values col-9').find(
            'span').text

        # Заповнення даних
        self.data = {
            "title": title,
            "image": image,
            "url": self.url,
            "price": price,
            "seller_link": seller_link,
            "shipping": shipping
        }

    def save_to_json(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def display_data(self):
        print(json.dumps(self.data, ensure_ascii=False, indent=4))


# Використання класу
url = ("https://www.ebay.com/itm/365013757827?itmmeta=01J2XBSMA017RGP73TK8BHVWK3&hash=item54fc83ef83:g:LAoAAOSwzEJmleJh&amdata=enc%3AAQAJAAAA0PdwGOCxVKYIvMd7QwmAMjd8mB30PnGdwghtIj2M0yZ%2BEd29PR7uXhoU9J5hoSNvEytZ3eqLqlLgR59I4%2F52jCG9KlYDWUBpaUSg3gZb%2F1ALiggS9try5LT4dpWV8VXYhj4phap7D6rL%2Fa0KMehATsOA59SWgaZF1Fn0EhfbiTbFpxVwPrHbI8mpAtVopxZow%2BOE%2FDwhZNfQXC3lSBWeWczfuL8%2B0VHBjvyFJDinXXKxeBHni7KZMuGk4tOHBVNdsG5xj0dW1nYbAOCgXPFcyNc%3D%7Ctkp%3ABFBMkMXmq5dk")
scraper = EbayScraper(url)
html = scraper.fetch_page()
if html:
    scraper.parse_data(html)
    scraper.display_data()
scraper.save_to_json('ebay_product_data.json')
