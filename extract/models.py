from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
  url = models.CharField(max_length=255)
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '{0}: {1}' % (self.pk, self.description)


class Product(models.Model):
  url = models.CharField(max_length=255)
  price = models.CharField(max_length=255)
  category = models.ForeignKey(Category)
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '{0}: {1}' % (self.pk, self.description)


class Feature(models.Model):
  product = models.ForeignKey(Product)
  description = models.CharField(max_length=255, )

  def __unicode__(self):
    return '{0}: {1}' % (self.pk, self.description)