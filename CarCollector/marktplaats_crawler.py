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
    section = soup.findAll('section')
    print section
    listing_tags = soup.findAll(class_='listing-aurora')
    print(listing_tags.__len__())
    return listing_tags


def parse_car_listing(listing_tag, brand_name):
    print(listing_tag)
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
    print('car.image_url: ' + car.image_url)
    return car


def collect_cars(brand_id, brand_name):
    brand_page = get_car_page(brand_id)
    print(brand_page)
    car_tags = get_car_tags(brand_page)
    print(car_tags)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand_name)
        print(car)
        result.append(car)
    return result