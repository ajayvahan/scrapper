import mechanicalsoup
import os
import urllib
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen
from apps import constants as con
from apps.home.models import Product

class Scrap(object):
    """Scrap the web site

    Scrapping flipnart and amazon based on the search argument """

    def __init__(self, *args, **kwargs):
        self.flipkart_URL = con.FLIPKART_URL
        self.amazon_URL = con.AMAZON_URL

    def flipkart(self, search=None):
        browser = mechanicalsoup.Browser()
        home = browser.get(self.flipkart_URL)
        form = home.soup.find("form", {"id": "fk-header-search-form"})

        form.find("input", {"id": "fk-top-search-box"})["value"] = search
        response = browser.submit(form, home.url)

        div_tag = response.soup.find('div', {'class': 'product-unit'})
        div_tags = response.soup.find_all('div', {'class': 'product-unit'})

        product_list = []

        for div_tag in div_tags:
            price = div_tag.find('div', {'class': 'pu-final'}).span.get_text()
            price = price.replace('Rs.','').strip(' ').replace(',','')
            name = div_tag.find('div', {'class': 'pu-details lastUnit'}).a.get_text().strip()
            href = self.flipkart_URL + div_tag.a.attrs['href']
            img_src = div_tag.img.attrs['data-src']
            description = div_tag.find('ul', {'class': 'pu-usp'})
            try:
                product_type = div_tag.find('div', {'class': 'pu-category'}).span.get_text()
            except:
                product_type = search

            data = {
                'name': name, 'product_type': product_type, 'price': price,
                'description': str(description), 'landing_url': href, 'image': img_src,
                'site_reference': 'flipkart'
            }
            # print(data)
            try:
                product = Product.objects.filter(
                    site_reference='flipkart', name=name, product_type=product_type)
                print(product)
                # print(product[0].pk)
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                else:
                    p = Product.objects.create(**data)
            except Exception as e:
                print(e)
                p = None
            print(p)

            if p:
                product_list.append(p)
        # product_list is return to the view to display it in front end
        return product_list



    def amazon(self, search, *args, **kwargs):
        browser = mechanicalsoup.Browser()
        home = browser.get(self.amazon_URL)
        form = home.soup.find("form", {"name": "site-search"})

        form.find("input", {"id": "twotabsearchtextbox"})["value"] = search
        response = browser.submit(form, home.url)

        div_tag = response.soup.find('div', {'class': 'a-fixed-left-grid-inner'})
        div_tags = response.soup.find_all('div', {'class': 'a-fixed-left-grid-inner'})

        product_list = []
        for div_tag in div_tags:
            name = div_tag.find('div', {'class': 'a-row a-spacing-small'}).h2.get_text()
            price = div_tag.find('span', {'class': 'currencyINR'}).next_sibling
            price = float(price.strip(' ').replace(',','').replace('-', '').replace('/',''))
            href = div_tag.find('div', {'class': 'a-row a-spacing-small'}).a.attrs['href']
            img_src = div_tag.img.attrs['src']
            product_type = div_tag.find('div', {'class':'a-column a-span5 a-span-last'}).find('span',{'class':'a-text-bold'}).get_text().strip(':')

            data = {
                'name': name, 'product_type': product_type, 'price': price,
                'landing_url': href, 'image': img_src,
                'site_reference': 'amazon'
            }
            # print(data)
            try:
                product = Product.objects.filter(
                    site_reference='flipkart', name=name, product_type=product_type)
                print(product)
                # print(product[0].pk)
                if product:
                    Product.objects.filter(pk=product[0].pk).update(**data)
                    product[0].save()
                    p = product[0]
                else:
                    p = Product.objects.create(**data)
            except Exception as e:
                print(e)
                p = None
            print(p)

            if p:
                product_list.append(p)
        # product_list is return to the view to display it in front end
        return product_list
