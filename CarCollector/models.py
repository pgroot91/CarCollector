import uuid
from django.db import models


# Create your models here.
class Site(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __unicode__(self):
        return self.name

class Brand(models.Model):
    name = models.CharField(unique=True, max_length=200)
    url = models.URLField()
    site_brands = models.ManyToManyField(Site, through='SiteBrand')

    def __unicode__(self):
        return self.name

class SiteBrand(models.Model):
    site = models.ForeignKey(Site)
    brand = models.ForeignKey(Brand)
    identifier = models.CharField(max_length=200)
    url = models.URLField()
    
    def __unicode__(self):
        return self.identifier

class Model(models.Model):
    name = models.CharField(max_length=200)
    brand = models.ForeignKey(Brand)
    url = models.URLField()
    site_models = models.ManyToManyField(Site, through='SiteModel')

    def __unicode__(self):
        return self.name

class SiteModel(models.Model):
    site = models.ForeignKey(Site)
    model = models.ForeignKey(Model)
    identifier = models.CharField(max_length=200)
    url = models.URLField()
    
    def __unicode__(self):
        return self.identifier

class Car(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    brand = models.ForeignKey(Brand)
    model = models.ForeignKey(Model)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    license = models.CharField(max_length=20)
    title = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200)
    url = models.URLField(default=None)
    image_url = models.URLField(default=None)

    def brand_name(self):
        return self.brand.name

    def model_name(self):
        return self.model.name

    def __unicode__(self):
        return self.brand + ' ' + self.model + ' ' + str(self.price) + ' ' + self.license + '\n' + self.description.decode('utf-8') + '\n' \
               + '<a href="' + self.url + '">' + self.url + '</a>'
