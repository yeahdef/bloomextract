from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.db import IntegrityError
from extract.models import Product, Category, Feature
import requests
from bs4 import BeautifulSoup
import re


def get_price(html):
    '''Grabs the price from the product page'''
    price = html.find_all("span", {"class": "moula"})
    prices = []
    if price:
        for p in price:
            parsed_price = ''.join(n for n in p.text if n.isdigit() or n == '.')
            prices.append(float(parsed_price))
        return max(prices)
    else:
        return False


def test_product_page(html, url):
    p = None
    cat = html.find('a', {"itemprop": "brand"})
    c, created = Category.objects.get_or_create(description=cat.text, url='http://turntablelab.com{0}'.format(cat['href']))
    p, created = Product.objects.get_or_create(url=url, description=html.title.text, category=c, price=get_price(html))
    for f in html.find_all('li'):
        if f.find_all('a'):
            pass
        else:
            # probably a feature
            if len(f.text.strip()) > 0:
                feature, created = Feature.objects.get_or_create(description=f.text.strip(), product=p)
    return p


def test_category_page(html, url):
    c = None
    c, created = Category.objects.get_or_create(url=url, description=html.title.text)
    for f in html.find_all('li', {'class': 'titles'}):
        for a in f.find_all('a'):
            p, created = Product.objects.get_or_create(url='http://turntablelab.com{0}'.format(a['href']), category=c, description=a.text.strip())
    return c


def home(request):
    """Handles get requests."""
    if request.method == "GET":
        return render_to_response(
            'index.html',
            RequestContext(request, {})
        )
    if request.method == "POST":
        url = request.POST['url']
        # should probably use a better regex parsing here
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        r = requests.get(url)
        # get soupy
        html = BeautifulSoup(r.text, "html.parser")
        if (html.find('span', {'class': 'big_prodtitle'}) \
        or html.find('span', {'class': 'prodtitle'})) \
        and not html.find('div', {'id': 'bigbread'}) \
        and html.find('div', {'class': 'user-column'}) \
        and html.find('div', {'class': 'freeshipping'}):
            # confirmed product, parse details
            product = test_product_page(html, url)
            category = None
            related_products = None,
            related_features = Feature.objects.filter(product=product)
        else:
            # not a product, look for product links - probably a category
            category = test_category_page(html, url)
            product = None
            related_products = Product.objects.filter(category=category)
            related_features = None,

        return render_to_response(
            'index.html',
            RequestContext(request, {
                'product': product,
                'category': category,
                'related_products': related_products,
                'related_features': related_features,
            })
        )
