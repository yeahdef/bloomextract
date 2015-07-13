from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.models import RequestSite
from django.db import IntegrityError
from extract.models import Product, Category, Feature
import requests
from bs4 import BeautifulSoup


def get_price(html):
    '''Grabs the price from the product page'''
    price = html.find("span", {"id": "priceblock_ourprice"})
    if not price:
        price = html.find("span", {"id": "priceblock_saleprice"})
    if price:
        return price.text
    else:
        return False


def test_product_page(html, url):
    p = None
    if 'add to cart' in html.text.lower() and 'amazon' in url:
        bread = html.find('div', {"id": "nav-subnav"})
        cat = bread.find_all("a", href=True)[0]
        c, created = Category.objects.get_or_create(description=cat.text, url='http://amazon.com{0}'.format(cat['href']))
        p, created = Product.objects.get_or_create(url=url, description=html.title.text, category=c, price=get_price(html))

        fb = html.find("div", {"id": "feature-bullets"})
        db = html.find("div", {"id": "detail-bullets"})
        if fb:
            for f in fb.find_all('span', {"class": 'a-list-item'}):
                feature, created = Feature.objects.get_or_create(description=f.text, product=p)
        if db:
            for f in db.find_all('li'):
                try:
                    feature, created = Feature.objects.get_or_create(description=f.text, product=p)
                except UnicodeEncodeError, e:
                    pass
    return p


def test_category_page(html, url):
    c = None
    if 'add to cart' not in html.text.lower() and 'amazon' in url:
        c, created = Category.objects.get_or_create(url=url, description=html.title.text)
        for a in html.find_all('a', href=True, title=True):
            Product.objects.get_or_create(url='http://amazon.com{0}'.format(a['href']), category=c, description=a['title'])
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
        category = test_category_page(html, url)
        product = test_product_page(html, url)

        return render_to_response(
            'index.html',
            RequestContext(request, {
                'product': product,
                'category': category,
                'related_products': Product.objects.filter(category=category),
                'related_features': Feature.objects.filter(product=product),
            })
        )
