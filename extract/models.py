from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
  url = models.CharField(max_length=255)
  price = models.CharField(max_length=255)
  prime = models.BooleanField(default=False)
  catagory = models.ForeignKey('Catagory')
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '%s' % (self.description)


class Catagory(models.Model):
  url = models.CharField(max_length=255)
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '%s' % (self.description)


class Feature(models.Model):
  product = models.ForeignKey(Product)
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '%s' % (self.description)