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
    url = 'http://www.marktplaats.nl/z.html?'
    if brand_id:
        url += 'categoryId=' + brand_id
        if model_name:
            url += '&attributes=model%2C' + model_name
    if min_price:
        url += '&priceFrom=' + min_price
    if max_price:
        url += '&priceTo=' + max_price
    if min_year:
        url += '&yearFrom=' + min_year
    if max_year:
        url += '&yearTo=' + max_year
    if min_milage:
        url += '&mileageFrom=' + min_milage
    if max_milage:
        url +=  '&mileageTo=' + max_milage
    print(url)
    return url


def get_car_tags(brand_page):
    response = requests.get(brand_page)
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    listing_tags = soup.findAll(class_='listing-aurora')
    return listing_tags


def parse_car_listing(listing_tag, brand, model_name):
    car = Car()
    car.title = listing_tag.find('span', class_='mp-listing-title').text
    car.brand = brand
    model = Model()
    model.name = model_name
    car.model = model
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


def collect_cars(brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):
    print('start marktplaats')
    if model_name is None:
         model_name = ''
    brand_page = get_car_page(brand_id, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage)
    car_tags = get_car_tags(brand_page)
    result = []
    for listing_tag in car_tags:
        car = parse_car_listing(listing_tag, brand, model_name)
        result.append(car)
    print('end marktplaats')
    return result


def crawl_car_brand_tags():
    response = requests.get('http://www.marktplaats.nl/c/auto-s/c91.html')
    print(response.status_code)
    soup = BeautifulSoup(response.content, 'html5lib')
    brand_tags = soup.find('select', {'name': 'categoryId'}).find('optgroup', label='Alle merken').findAll('option')
    return brand_tags


def get_car_brands_and_ids(car_brand_tags, site):
    results = []
    for car_brand_tag in car_brand_tags:
        car_brand_name = ' '.join(car_brand_tag.string.split())
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
        print (site_brand.brand.name)
        response = requests.get('http://www.marktplaats.nl/h/auto-s/' + site_brand.brand.name.lower().replace(' ', '-').replace('\'', '-') + '.html')
        print(response.status_code)
        soup = BeautifulSoup(response.content, 'html5lib')
	tags = soup.find('div', {'id': 'cars-search-models'})
	if (tags is not None):
            tags = tags.find('ul', class_='item-frame')
            tags = tags.findAll('li')
	    models.extend(get_car_models_and_ids(tags, site, site_brand.brand))
    return models


def get_car_models_and_ids(car_model_tags, site, brand):
    results = []
    for car_model_tag in car_model_tags:
        car_model_name = ' '.join(car_model_tag.string.split())
	print(car_model_name)
        car_model_id = car_model_tag['data-val']
	model, created = Model.objects.get_or_create(name=car_model_name, brand=brand)
        site_model = SiteModel()
	site_model.site = site
	site_model.model = model
	site_model.identifier = car_model_id
	site_model.save()
        results.append(site_model)
    return results
