# -*- coding: utf-8 -*-
from multiprocessing import Pool

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from CarCollector import speurders_crawler
from CarCollector import marktplaats_crawler
from CarCollector import autotrader_crawler
from CarCollector import autowereld_crawler


def get_marktplaats_brands_and_ids():
    return marktplaats_crawler.get_car_brands_and_ids(marktplaats_crawler.crawl_car_brand_tags())


def get_speurders_car_brands_and_ids():
    return speurders_crawler.get_car_brands_and_ids(speurders_crawler.crawl_car_brand_tags())


def get_autotrader_car_brands_and_ids():
    return autotrader_crawler.get_car_brands_and_ids(autotrader_crawler.crawl_car_brand_tags())


def get_autowereld_car_brands_and_ids():
    return autowereld_crawler.get_car_brands_and_ids(autowereld_crawler.crawl_car_brand_tags())


def get_cars_from_pages(autotrader_brand_id, autowereld_brand_id, brand_name, marktplaats_brand_id,
                        speurders_brand_id):
    cars = []

    pool = Pool(processes=4)
    collect_marktplaats_cars = pool.apply_async(marktplaats_crawler.collect_cars, (marktplaats_brand_id, brand_name))
    collect_speurders_cars = pool.apply_async(speurders_crawler.collect_cars, (speurders_brand_id, brand_name))
    collect_autotrader_cars = pool.apply_async(autotrader_crawler.collect_cars, (autotrader_brand_id, brand_name))
    collect_autowereld_cars = pool.apply_async(autowereld_crawler.collect_cars, (autowereld_brand_id, brand_name))

    cars.extend(collect_marktplaats_cars.get())
    cars.extend(collect_speurders_cars.get())
    cars.extend(collect_autotrader_cars.get())
    cars.extend(collect_autowereld_cars.get())

    return cars


def get_cars(request):
    pool = Pool(processes=4)

    marktplaats_brands = pool.apply_async(
        get_marktplaats_brands_and_ids)
    speurders_brands = pool.apply_async(
        get_speurders_car_brands_and_ids)
    autotrader_brands = pool.apply_async(
        get_autotrader_car_brands_and_ids)
    autowereld_brands = pool.apply_async(
        get_autowereld_car_brands_and_ids)

    brand_name = request.POST['term']
    marktplaats_brand_id = ''
    speurders_brand_id = ''
    autotrader_brand_id = ''
    autowereld_brand_id = ''

    if brand_name in marktplaats_brands.get():
        marktplaats_brand_id = marktplaats_brands.get()[brand_name]
    if brand_name in speurders_brands.get():
        speurders_brand_id = speurders_brands.get()[brand_name]
    if brand_name in autotrader_brands.get():
        autotrader_brand_id = autotrader_brands.get()[brand_name]
    if brand_name in autowereld_brands.get():
        autowereld_brand_id = autowereld_brands.get()[brand_name]

    cars = get_cars_from_pages(autotrader_brand_id, autowereld_brand_id, brand_name, marktplaats_brand_id,
                               speurders_brand_id)

    return cars


def search(request):
    c = {}
    c.update(csrf(request))
    if request.POST:
        cars = get_cars(request)

        return render_to_response('search.html', context=c, context_instance=RequestContext(request),
                                  dictionary={'result': cars})
        # dictionary={'result': google(request.POST['term'], 10)})
    # return HttpResponseRedirect("/")
    else:
        return render_to_response('search.html', c, context_instance=RequestContext(request))





