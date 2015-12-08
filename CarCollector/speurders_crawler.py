# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from CarCollector.models import Car

__author__ = 'rian'


def get_car_page(brand_id, min_price, max_price):
    return 'http://www.speurders.nl/overzicht/autos/?subcategory=' + brand_id + '&min_prijs=' + min_price + '&max_prijs=' + max_price


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = list(listing_tag for listing_tag in soup.findAll('div', class_='row position-list-item') if
                        listing_tag.find('div', class_='position-list-price-column greyout') is None)
    return listing_tags


def parse_car_listing(listing_tag, brand_name):
    car = Car()
    header_and_description_div = listing_tag.find('div', class_='position-header-and-description')

    if header_and_description_div is not None:
        title_header = header_and_description_div.find('h2')
        description_paragraph = header_and_description_div.find('p')
        if title_header is not None:
            car.title = title_header.text
        if description_paragraph is not None:
            car.description = description_paragraph.text.encode('utf-8')

    car.brand = brand_name
    price_string = ''
    price_div = listing_tag.find('div', class_='block half-top-padding')

    if price_div is not None:
        price_string = price_div.find('h2').text.encode('utf-8')
    try:
        price_extracted = re.search('€ (.+),-', price_string).group(1)
    except AttributeError:
        price_extracted = ''

    try:
        price_converted = price_extracted.replace('.', '')
        price = Decimal(price_converted)
    except:
        price = 0

    car.price = price
    url_div = listing_tag.find('div', class_='position-list-item-description')

    if url_div is not None:
        car.url = 'http://www.speurders.nl' + url_div.find('a')['href']

    image_div = listing_tag.find('div', class_='list-item-img')
    if image_div is not None:
        style_text = image_div['style']

        if style_text is not None:
            car.image_url = 'http://' + re.search("background-image: url\('//(.+)'\);", style_text).group(1)

    return car


def collect_cars(brand_id, brand_name, min_price, max_price):
    print('start speurders')
    brand_page = get_car_page(brand_id, min_price, max_price)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand_name)
        result.append(car)
    print('end speurders')
    return result


def crawl_car_brand_tags():
    response = requests.get('http://www.speurders.nl/overzicht/autos/')
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    brand_tags = soup.find('select', {'id': 'subcategory'}).findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags):
    results = {}
    for car_brand_tag in car_brand_tags:
        car_brand_name = ' '.join(car_brand_tag.string.split())
        car_brand_id = car_brand_tag['value']
        results[car_brand_name] = car_brand_id
    return results
