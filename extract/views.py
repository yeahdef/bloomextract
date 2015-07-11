from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib.sites.models import RequestSite
from extract.models import Product, Category, Feature
import requests
from bs4 import BeautifulSoup


KNOWN_CATEGORY = 'http://smile.amazon.com/music-rock-classical-pop-jazz/b/ref=nav_shopall_cd_vinyl?ie=UTF8&node=5174'
KNOWN_PRODUCT = 'http://smile.amazon.com/gp/product/B00VF7OZTY/ref=s9_newr_bw_d74_g15_i2?pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-4&pf_rd_r=02GDHN4GWVE3E7KHHBJD&pf_rd_t=101&pf_rd_p=1979743882&pf_rd_i=5174'


def test_product_page(html, url):
    p = None
    if 'add to cart' in html.text.lower():
        prime = False
        bread = html.find('div', {"id": "nav-subnav"})
        priceblock = html.find('tr', {"id": "priceblock_ourprice_row"})
        cat = bread.find_all("a", href=True)[0]
        c, created = Category.objects.get_or_create(description=cat.text, url='http://amazon.com{0}'.format(cat['href']))
        if len(priceblock.find_all("i", {"class": "a-icon a-icon-prime"})) > 0:
            prime = True        
        price = html.find("span", {"id": "priceblock_ourprice"}).text
        p, created = Product.objects.get_or_create(url=url, description=html.title.text, category=c, price=price, prime=prime)
        fb = html.find("div", {"id": "feature-bullets"})
        for f in fb.find_all('span', {"class": 'a-list-item'}):
            feature, created = Feature.objects.get_or_create(description=f.text, product=p)
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
        if not url.startswith('http://'):
            url = 'http://{0}'.format(url)
        r = requests.get(url)
        html = BeautifulSoup(r.text, "html.parser")
        # get soupy
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