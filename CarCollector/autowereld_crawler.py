# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from CarCollector.models import Car

__author__ = 'rian'


def get_car_page(brand_id, min_price, max_price):
    return 'http://www.autowereld.nl/zoeken.html?mrk=' + brand_id + '&prvan=' + min_price + '&prtot=' + max_price


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll('tr', class_='item')
    return listing_tags


def parse_car_listing(listing_tag, brand_name):
    car = Car()
    link = listing_tag.find('h3').find('a')
    if link is not None:
        car.title = link.text

    car.brand = brand_name
    price_string = ''
    price_tag = listing_tag.find('td', class_='prijs').find('strong')

    if price_tag is not None:
        price_string = price_tag.text.encode('utf-8')
    try:
        price_extracted = re.search('€ (.+)', price_string).group(1)
    except AttributeError:
        price_extracted = ''

    try:
        price_converted = price_extracted.replace('.', '')
        price = Decimal(price_converted)
    except:
        price = 0

    car.price = price

    description = listing_tag.find('td', class_='omschrijving').find('span', class_='kenmerken')
    car.description = description.text.encode('utf-8')

    if link is not None:
        car.url = 'http://www.autowereld.nl' + link['href']

    image_tag = listing_tag.find('td', class_='foto').find('img')
    if image_tag is not None:
        car.image_url = 'http://www.autowereld.nl' + image_tag['src']

    return car


def collect_cars(brand_id, brand_name, min_price, max_price):
    print('start autowereld')
    brand_page = get_car_page(brand_id, min_price, max_price)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand_name)
        result.append(car)
    print('end autowereld')
    return result


def crawl_car_brand_tags():
    headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
    response = requests.post('http://www.autowereld.nl/zoeken.html?rs-meer=merken&rs-meer-init=1', headers=headers)
    print(response.status_code)
    json = response.json()
    options = json['zoekbalk']['filters']['mrk']
    soup = BeautifulSoup(options, 'html5lib')
    brand_tags = soup.findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags):
    results = {}
    for car_brand_tag in car_brand_tags:
        car_brand_string = car_brand_tag.text
        car_brand_name = ' '.join(car_brand_string.split())
        car_brand_id = car_brand_tag['value']
        results[car_brand_name] = car_brand_id
    return results
