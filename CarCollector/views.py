# -*- coding: utf-8 -*-
from multiprocessing import Pool

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.context_processors import csrf

from CarCollector import speurders_crawler
from CarCollector import marktplaats_crawler
from CarCollector import autotrader_crawler
from CarCollector import autowereld_crawler

from CarCollector.models import Brand
from CarCollector.models import SiteBrand

from datetime import date


def get_cars_from_pages(autotrader_brand_id, autowereld_brand_id, marktplaats_brand_id,
                        speurders_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):
    cars = []

    pool = Pool(processes=4)
    collect_marktplaats_cars = pool.apply_async(marktplaats_crawler.collect_cars, (marktplaats_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage))
    collect_speurders_cars = pool.apply_async(speurders_crawler.collect_cars, (speurders_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage))
    collect_autotrader_cars = pool.apply_async(autotrader_crawler.collect_cars, (autotrader_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage))
    collect_autowereld_cars = pool.apply_async(autowereld_crawler.collect_cars, (autowereld_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage))

    cars.extend(collect_marktplaats_cars.get())
    print(len(cars))
    cars.extend(collect_speurders_cars.get())
    print(len(cars))
    cars.extend(collect_autotrader_cars.get())
    print(len(cars))
    cars.extend(collect_autowereld_cars.get())
    print(len(cars))

    pool.close()
    pool.join()

    return cars


def get_cars(brand_name, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage):

    brand = Brand.objects.filter(name=brand_name)[0]

    marktplaats_brand_id = SiteBrand.objects.filter(brand__name=brand_name).filter(site__pk='e5927dda-3289-446d-8102-668ce8c67664')[0].identifier
    speurders_brand_id = SiteBrand.objects.filter(brand__name=brand_name).filter(site__pk='9d8bd147-563c-487c-a56d-ad0488b840cc')[0].identifier
    autotrader_brand_id = SiteBrand.objects.filter(brand__name=brand_name).filter(site__pk='f5c551c4-6871-45fa-b4e6-f8634c82c559')[0].identifier
    autowereld_brand_id = SiteBrand.objects.filter(brand__name=brand_name).filter(site__pk='ac32187e-62c9-4349-8b65-6cc8e7ff1bdf')[0].identifier

    cars = get_cars_from_pages(autotrader_brand_id, autowereld_brand_id, marktplaats_brand_id,
                               speurders_brand_id, brand, model_name, min_price, max_price, min_year, max_year, min_milage, max_milage)

    return cars


def search(request, brand, model=None):
    print(request.GET)
    c = {}
    c.update(csrf(request))
    if request.POST:
	brand_name = request.POST['term']
	min_price = request.POST.get('min-price', '0')
	max_price = request.POST.get('max-price', '1000000')
	min_year = request.POST.get('min-year', '0')
	max_year = request.POST.get('max-year', str(date.today().year))
	min_milage = request.POST.get('min-milage', '0')
	max_milage = request.POST.get('max-milage', '1000000')
        cars = get_cars(brand_name, None, min_price, max_price, min_year, max_year, min_milage, max_milage)

        return render_to_response('search.html', context=c, context_instance=RequestContext(request),
                                  dictionary={'result': sorted(cars, key=lambda car: car.price ), 'brand_name': brand_name, 'min_price': min_price, 'max_price': max_price, 'min_year': min_year, 'max_year': max_year, 'min_milage': min_milage, 'max_milage': max_milage})
    else:
	print(brand)
	print(model)
	min_price = request.GET.get('min-price', '0')
	max_price = request.GET.get('max-price', '1000000')
	min_year = request.GET.get('min-year', '0')
	max_year = request.GET.get('max-year', str(date.today().year))
	min_milage = request.GET.get('min-milage', '0')
	max_milage = request.GET.get('max-milage', '1000000')
        cars = get_cars(brand, model, min_price, max_price, min_year, max_year, min_milage, max_milage)
        return render_to_response('search.html', context=c, context_instance=RequestContext(request),
                                  dictionary={'result': sorted(cars, key=lambda car: car.price ), 'brand_name': brand, 'model_name' : model, 'min_price': min_price, 'max_price': max_price, 'min_year': min_year, 'max_year': max_year, 'min_milage': min_milage, 'max_milage': max_milage})
        # dictionary={'result': google(request.POST['term'], 10)})
    # return HttpResponseRedirect("/")
    #else:
        #return render_to_response('search.html', c, context_instance=RequestContext(request))





