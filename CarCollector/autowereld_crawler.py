# -*- coding: utf-8 -*-
from decimal import Decimal
import re
import requests
from bs4 import BeautifulSoup
from CarCollector.models import Car
from CarCollector.models import Site
from CarCollector.models import Brand
from CarCollector.models import SiteBrand
from CarCollector.models import SiteModel
from CarCollector.models import Model

__author__ = 'rian'


def get_car_page(brand_id, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):
    url = 'http://www.autowereld.nl/' + brand_id.lower() + '/?mdl=' + model_name.lower() + '&prvan=' + min_price + '&prtot=' + max_price + '&bjvan=' + min_year + '&bjtot=' + max_year + '&kmvan=' + min_milage + '&kmtot=' + max_milage
    return url


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll('tr', class_='item')
    return listing_tags


def parse_car_listing(listing_tag, brand, model_name):
    car = Car()
    link = listing_tag.find('h3').find('a')
    if link is not None:
        car.title = link.text

    car.brand = brand
    model = Model()
    model.name = model_name
    car.model = model
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


def collect_cars(brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):
    print('start autowereld')
    if model_name is None:
         model_name = ''
    brand_page = get_car_page(brand.name, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand, model_name)
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


def get_car_brands_and_ids(car_brand_tags, site):
    results = []
    for car_brand_tag in car_brand_tags:
        car_brand_string = car_brand_tag.text
        car_brand_name = ' '.join(car_brand_string.split())
        car_brand_id = car_brand_tag['value']
	brand, created = Brand.objects.get_or_create(name=car_brand_name)
        site_brand = SiteBrand()
	site_brand.site = site
	site_brand.brand = brand
	site_brand.identifier = car_brand_id
	site_brand.save()
        results.append(site_brand)
    return results

def crawl_car_model_tags(site):
    models = []
    site_brands = Site.objects.filter(site__pk=site.id)
    for site_brand in site_brands:
        headers = {'Accept': 'application/json', 'X-Requested-With': 'XMLHttpRequest'}
        response = requests.post('http://www.autowereld.nl/zoeken.html?mrk=' + site_brand.identifier + '&rs-meer=modellen&rs-meer-init=1', headers=headers)
        print(response.status_code)
        json = response.json()
        options = json['zoekbalk']['filters']['mdl']
        soup = BeautifulSoup(options, 'html5lib')
	models.extend(get_car_models_and_ids(soup.findAll('option'), site, site_brand.brand))
    return models


def get_car_models_and_ids(car_model_tags, site, brand):
    results = []
    for car_model_tag in car_model_tags:
        car_model_string = car_model_tag.text
        car_model_name = ' '.join(car_model_string.split())
        car_model_id = car_model_tag['value']
	model, created = Model.objects.get_or_create(name=car_model_name, brand=brand)
        site_model = SiteModel()
	site_model.site = site
	site_model.model = model
	site_model.identifier = car_model_id
	site_model.save()
        results.append(site_model)
    return results
