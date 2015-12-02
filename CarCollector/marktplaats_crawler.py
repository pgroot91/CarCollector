# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from CarCollector.models import Car

__author__ = 'rian'


def get_car_page(car_id):
    return 'http://www.marktplaats.nl/z.html?categoryId=' + car_id


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll(class_='listing-aurora')
    return listing_tags


def parse_car_listing(listing_tag, brand_name):
    car = Car()
    car.title = listing_tag.find('span', class_='mp-listing-title').text
    car.brand = brand_name
    price_string = listing_tag.find('div', class_='price').text.encode('utf-8')
    try:
        price_extracted = re.search('€ (.+)', price_string).group(1)
    except AttributeError:
        price_extracted = ''
    try:
        price_converted = price_extracted.replace('.', '').replace(',', '.')
        price = Decimal(price_converted)
    except:
        price = 0
    car.price = price
    description = listing_tag.find('span', class_='mp-listing-description')
    extended_description = listing_tag.find('span', class_='mp-listing-description-extended')
    car.description = description.text.encode('utf-8')
    if extended_description:
        car.description += extended_description.text.encode('utf-8')
    car.url = listing_tag.find('h2', class_='heading').find('a')['href']
    car.image_url = listing_tag.find('div', class_='listing-image').find('img')['src']
    return car


def collect_cars(brand_id, brand_name):
    print('start marktplaats')
    brand_page = get_car_page(brand_id)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand_name)
        result.append(car)
    print('end marktplaats')
    return result


def crawl_car_brand_tags():
    response = requests.get('http://www.marktplaats.nl/c/auto-s/c91.html')
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    brand_tags = soup.find('select', {'name': 'categoryId'}).find('optgroup', label='Alle merken').findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags):
    results = {}
    for car_brand_tag in car_brand_tags:
        car_brand_name = ' '.join(car_brand_tag.string.split())
        car_brand_id = car_brand_tag['value']
        results[car_brand_name] = car_brand_id
    return results