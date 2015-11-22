# -*- coding: utf-8 -*-
import requests
import string
from decimal import Decimal
import re

from bs4 import BeautifulSoup
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from SearchEngine.marktplaats_crawler import get_car_page, get_car_tags, parse_car_listing
from SearchEngine.models import Car


def is_car_class(tag):
    tag_get = tag.get('class')
    if tag_get is None:
        return False
    return tag_get == 'thumb-placeholder-centered juiceless-link'


def parse_car_summary(listing_tag):
    result = [listing_tag['data-url']]
    return result


def parse_car_page(car_link, brand_name):
    print('car link: ' + car_link)
    response = requests.get(car_link)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    car = parse_car(soup, brand_name, car_link)
    return car


def parse_car(soup, brand, car_link):
    car = Car()
    car.title = soup.find(id='title')
    car.brand = brand
    find = soup.find(id='car-attributes')
    find_find = find.find(text='Merk &amp; Model:')
    print(find_find)
    brand_model = find_find.findNext('span').text
    try:
        model = re.search(brand.name + ' (.+)', brand_model).group(1)
    except AttributeError:
        model = ''
    car.model = string.capwords(model)
    license_plate = soup.find(text='Kenteken:').findNext('span').text
    car.license = license_plate
    price_string = soup.find(id='vip-ad-price-container').find('span').text
    try:
        price_extracted = re.search('.+ (.+)', price_string).group(1)
    except AttributeError:
        price_extracted = ''
    try:
        price_converted = price_extracted.replace('.', '').replace(',', '.')
        price = Decimal(price_converted)
    except:
        price = 0
    print(price)
    car.price = price
    description = soup.find(id='vip-ad-description').text
    car.description = description
    car.url = car_link
    print(car.brand, car.model, car.license, car.price)
    return car

def search(request):
    c = {}
    c.update(csrf(request))
    if request.POST:
        brands = get_car_brands_and_ids(crawl_car_brand_tags())
        print(brands)
        brand_name = request.POST['term']
        brand_id = brands[brand_name]
        print(brand_id)
        brand_page = get_car_page(brand_id)
        print(brand_page)
        car_tags = get_car_tags(brand_page)
        print(car_tags)
        cars = []
        for listing_tag in car_tags:
            car = parse_car_listing(listing_tag, brand_name)
            print(car)
            cars.append(car)

        return render_to_response('search.html', context=c, context_instance=RequestContext(request),
                                  dictionary={'result': cars})
                                  # dictionary={'result': google(request.POST['term'], 10)})
    # return HttpResponseRedirect("/")
    else:
        return render_to_response('search.html', c, context_instance=RequestContext(request))


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