from django.contrib import admin

from .models import Site
from .models import Brand
from .models import SiteBrand
from .models import Model
from .models import SiteModel

from multiprocessing import Pool

from CarCollector import speurders_crawler
from CarCollector import marktplaats_crawler
from CarCollector import autotrader_crawler
from CarCollector import autowereld_crawler

def get_marktplaats_brands_and_ids(site):
    return marktplaats_crawler.get_car_brands_and_ids(marktplaats_crawler.crawl_car_brand_tags(), site)

def get_speurders_car_brands_and_ids(site):
    return speurders_crawler.get_car_brands_and_ids(speurders_crawler.crawl_car_brand_tags(), site)


def get_autotrader_car_brands_and_ids(site):
    return autotrader_crawler.get_car_brands_and_ids(autotrader_crawler.crawl_car_brand_tags(), site)

def get_autowereld_car_brands_and_ids(site):
    return autowereld_crawler.get_car_brands_and_ids(autowereld_crawler.crawl_car_brand_tags(), site)


def get_marktplaats_models_and_ids(site):
    return marktplaats_crawler.crawl_car_model_tags(site)

def get_speurders_car_models_and_ids(site):
    return speurders_crawler.crawl_car_model_tags(site)

def get_autotrader_car_models_and_ids(site):
    return autotrader_crawler.crawl_car_model_tags(site)


def get_autowereld_car_models_and_ids(site):
    return autowereld_crawler.crawl_car_model_tags(site)

def collect_brands(modeladmin, request, queryset):

    marktplaats_site = Site.objects.get(pk='e5927dda-3289-446d-8102-668ce8c67664')
    speurders_site = Site.objects.get(pk='9d8bd147-563c-487c-a56d-ad0488b840cc')
    autotrader_site = Site.objects.get(pk='f5c551c4-6871-45fa-b4e6-f8634c82c559')
    autowereld_site = Site.objects.get(pk='ac32187e-62c9-4349-8b65-6cc8e7ff1bdf')

    get_marktplaats_brands_and_ids(marktplaats_site)
    get_speurders_car_brands_and_ids(speurders_site)
    get_autotrader_car_brands_and_ids(autotrader_site)
    get_autowereld_car_brands_and_ids(autowereld_site)

def collect_models(modeladmin, request, queryset):

    marktplaats_site = Site.objects.get(pk='e5927dda-3289-446d-8102-668ce8c67664')
    speurders_site = Site.objects.get(pk='9d8bd147-563c-487c-a56d-ad0488b840cc')
    autotrader_site = Site.objects.get(pk='f5c551c4-6871-45fa-b4e6-f8634c82c559')
    autowereld_site = Site.objects.get(pk='ac32187e-62c9-4349-8b65-6cc8e7ff1bdf')

    get_marktplaats_models_and_ids(marktplaats_site)
    get_speurders_car_models_and_ids(speurders_site)
    get_autotrader_car_models_and_ids(autotrader_site)
    get_autowereld_car_models_and_ids(autowereld_site)

collect_brands.short_description = "Collect brands"
collect_models.short_description = "Collect models"

class BrandAdmin(admin.ModelAdmin):
    list_display = ['name']
    ordering = ['name']
    actions = [collect_brands]

class ModelAdmin(admin.ModelAdmin):
    list_display = ['brand', 'name']
    ordering = ['brand', 'name']
    actions = [collect_models]

class SiteAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url']
    ordering = ['name']

class SiteBrandAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'brand', 'site']
    ordering = ['identifier']

class SiteModelAdmin(admin.ModelAdmin):
    list_display = ['identifier', 'model', 'site']
    ordering = ['identifier']

admin.site.register(Site, SiteAdmin)
admin.site.register(Brand, BrandAdmin)
admin.site.register(SiteBrand, SiteBrandAdmin)
admin.site.register(Model, ModelAdmin)
admin.site.register(SiteModel, SiteModelAdmin)

