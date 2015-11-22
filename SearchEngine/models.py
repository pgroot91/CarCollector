from django.db import models


# Create your models here.
class Brand(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()

    def __unicode__(self):
        return self.name


class Car(models.Model):
    brand = models.CharField(max_length=200)
    model = models.CharField(max_length=200)
    price = models.DecimalField(decimal_places=2, max_digits=9, default=0)
    license = models.CharField(max_length=20)
    title = models.CharField(max_length=200, default=None)
    description = models.CharField(max_length=200)
    url = models.URLField(default=None)
    image_url = models.URLField(default=None)

    def brand_name(self):
        return self.brand.name

    def __unicode__(self):
        return self.brand + ' ' + self.model + ' ' + str(self.price) + ' ' + self.license + '\n' + self.description.decode('utf-8') + '\n' \
               + '<a href="' + self.url + '">' + self.url + '</a>'