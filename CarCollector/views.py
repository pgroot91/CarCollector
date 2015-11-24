# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from CarCollector import speurders_crawler
from CarCollector import marktplaats_crawler
from CarCollector import autotrader_crawler
from CarCollector import autowereld_crawler


def search(request):
    c = {}
    c.update(csrf(request))
    if request.POST:
        marktplaats_brands = marktplaats_crawler.get_car_brands_and_ids(marktplaats_crawler.crawl_car_brand_tags())
        speurders_brands = speurders_crawler.get_car_brands_and_ids(speurders_crawler.crawl_car_brand_tags())
        autotrader_brands = autotrader_crawler.get_car_brands_and_ids(autotrader_crawler.crawl_car_brand_tags())
        autowereld_brands = autowereld_crawler.get_car_brands_and_ids(autowereld_crawler.crawl_car_brand_tags())
        brand_name = request.POST['term']
        marktplaats_brand_id = marktplaats_brands[brand_name]
        speurders_brand_id = speurders_brands[brand_name]
        autotrader_brand_id = autotrader_brands[brand_name]
        autowereld_brand_id = autowereld_brands[brand_name]
        cars = []
        cars.extend(marktplaats_crawler.collect_cars(marktplaats_brand_id, brand_name))
        cars.extend(speurders_crawler.collect_cars(speurders_brand_id, brand_name))
        cars.extend(autotrader_crawler.collect_cars(autotrader_brand_id, brand_name))
        cars.extend(autowereld_crawler.collect_cars(autowereld_brand_id, brand_name))

        return render_to_response('search.html', context=c, context_instance=RequestContext(request),
                                  dictionary={'result': cars})
                                  # dictionary={'result': google(request.POST['term'], 10)})
    # return HttpResponseRedirect("/")
    else:
        return render_to_response('search.html', c, context_instance=RequestContext(request))





