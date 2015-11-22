# -*- coding: utf-8 -*-
import requests

from bs4 import BeautifulSoup
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from CarCollector.marktplaats_crawler import collect_cars


def search(request):
    c = {}
    c.update(csrf(request))
    if request.POST:
        brands = get_car_brands_and_ids(crawl_car_brand_tags())
        print(brands)
        brand_name = request.POST['term']
        brand_id = brands[brand_name]
        print(brand_id)
        cars = []
        cars.extend(collect_cars(brand_id, brand_name))

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