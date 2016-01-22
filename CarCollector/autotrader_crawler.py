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
    url = 'http://www.autotrader.nl/auto/'
    if brand_id:
        url += brand_id.lower()
	if model_name:
            url += '-' + model_name.lower()
    if min_price and max_price:
        url += '/?zoekopdracht=prijs-van-' + min_price + '-tot-' + max_price
    if min_year and max_year:
        url += '%2Fbouwjaar-van-' + min_year + '-tot-' + max_year
    if min_milage and max_milage:
        url += '%2Fkilometerstand-van-' + min_milage + '-tot-' + max_milage
    print(url)
    return url


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll('section', class_='result')
    return listing_tags


def parse_car_listing(listing_tag, brand, model_name):
    car = Car()
    link = listing_tag.find('h2').find('a')
    if link is not None:
        car.title = link['title']

    car.brand = brand
    model = Model()
    model.name = model_name
    car.model = model
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


def collect_cars(brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):
    print('start autotrader')
    if model_name is None:
         model_name = ''
    brand_page = get_car_page(brand.name, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand, model_name)
        result.append(car)
    print('end autotrader')
    return result


def crawl_car_brand_tags():
    response = requests.get('http://www.autotrader.nl/auto/')
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    brand_tags = soup.find('select', {'id': 'merk'}).findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags, site):
    results = []
    for car_brand_tag in car_brand_tags:
        search = re.search('^(.+) \(\d*\)', car_brand_tag.text.encode('utf-8'))
        if search is None:
            continue
        car_brand_string = search.group(1)
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
    site_brands = SiteBrand.objects.filter(site__pk=site.id)
    for site_brand in site_brands:
	print(site_brand.identifier)
        data = { 'merk': site_brand.identifier }
        response = requests.post('http://www.autotrader.nl/auto/searchbox/searchpanesimplex', data=data)
        print(response.status_code)
        print(response.text)
        soup = BeautifulSoup(response.content, 'html5lib')
	models.extend(get_car_models_and_ids(soup.find('select', {'id': 'model'}).findAll('option'), site, site_brand.brand))
    return models


def get_car_models_and_ids(car_model_tags, site, brand):
    results = []
    for car_model_tag in car_model_tags:
        search = re.search('^(.+) \(\d*\)', car_model_tag.text.encode('utf-8'))
        if search is None:
            continue
        car_model_string = search.group(1)
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
