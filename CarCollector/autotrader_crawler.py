# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from CarCollector.models import Car

__author__ = 'rian'


def get_car_page(brand_id):
    return 'http://www.autotrader.nl/auto/' + brand_id + '/'


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll('section', class_='result')
    return listing_tags


def parse_car_listing(listing_tag, brand_name):
    car = Car()
    link = listing_tag.find('h2').find('a')
    if link is not None:
        car.title = link['title']

    car.brand = brand_name
    price_string = ''
    price_div = listing_tag.find('div', class_='result-price-label')

    if price_div is not None:
        price_string = price_div.text.encode('utf-8')
    try:
        price_extracted = re.search('€ (.+),-', price_string).group(1)
    except AttributeError:
        price_extracted = ''

    try:
        price_converted = price_extracted.replace('.', '')
        price = Decimal(price_converted)
    except:
        price = 0

    car.price = price

    if link is not None:
        car.url = 'http://www.autotrader.nl' + link['href']

    image_tag = listing_tag.find('img', class_='img-rounded')
    if image_tag is not None:
        car.image_url = image_tag['data-src']

    return car


def collect_cars(brand_id, brand_name):
    brand_page = get_car_page(brand_id)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand_name)
        result.append(car)
    return result


def crawl_car_brand_tags():
    response = requests.get('http://www.autotrader.nl/auto/')
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    brand_tags = soup.find('select', {'id': 'merk'}).findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags):
    results = {}
    for car_brand_tag in car_brand_tags:
        search = re.search('^(.+) \(\d*\)', car_brand_tag.text.encode('utf-8'))
        if search is None:
            continue
        car_brand_string = search.group(1)
        car_brand_name = ' '.join(car_brand_string.split())
        car_brand_id = car_brand_tag['value']
        results[car_brand_name] = car_brand_id
    return results