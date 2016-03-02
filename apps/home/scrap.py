"""Scrapping amazon and flipkart."""


import mechanicalsoup
from apps import constants as con
from apps.home.models import Product
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(settings.LOGGER)


class Scrap(object):
    """Scrap the web site.

    Scrapping flipkart and amazon based on the search argument.
    """

    def __init__(self, *args, **kwargs):
        """Storing constants in class variable."""
        self.flipkart_URL = con.FLIPKART_URL
        self.amazon_URL = con.AMAZON_URL

    def flipkart(self, search=None):
        """Scraping flipkart.

        Parse html document using mechanicalsoup, find searchform input tag
        and pass search argument in it and submit.Get response and search for
        specific tags in it to find name, price, href, img src, description
        and store it in a dictionary. Iterate through all the tags and store
        all dictionaries in a list and return it.
        """
        try:
            # Creating brower object.
            browser = mechanicalsoup.Browser()

            # Select the form
            home = browser.get(self.flipkart_URL)
            form = home.soup.find("form", {"id": "fk-header-search-form"})

            # Pass search argument in form input.
            form.find("input", {"id": "fk-top-search-box"})["value"] = search

            # Get response.
            response = browser.submit(form, home.url)

            # Finding first div element with specific class in page.
            div_tag = response.soup.find('div', {'class': 'product-unit'})

            # Finding all div elements with specific class in page.
            div_tags = response.soup.find_all('div', {'class': 'product-unit'})

            # Defining empty list.
            product_list = []

            for div_tag in div_tags:
                if search in ['book', 'books']:
                    data = Scrap.flipkart_books(self, div_tag, search)
                else:
                    data = Scrap.flipkart_general(self, div_tag, search)
                try:
                    # Filtering product table with specific parameters
                    # If exist store in product variable.
                    product = Product.objects.filter(
                        site_reference='flipkart', name=data['name'],
                        product_type=data['product_type']
                    )

                    # If product exist.
                    if product:
                        # Update product table with data.
                        Product.objects.filter(pk=product[0].pk).update(**data)

                        # Save the changes
                        product[0].save()

                        # Assigning product[0] to variable product_obj.
                        product_obj = product[0]

                    # If product does not exist.
                    else:
                        # Create new product row.
                        product_obj = Product.objects.create(**data)
                except Exception as e:
                    logger.exception("EXCEPTION :" + str(e))
                    product_obj = None

                if product_obj:
                    # Appending p to product_list
                    product_list.append(product_obj)

            # product_list is return to the view to display it in front end
            return product_list

        except Exception as e:
            logger.exception("EXCEPTION :" + str(e))
            feedback = None
            return feedback

    def flipkart_general(self, div_tag, search):
        """Flipkart function for general search."""
        # Finding price in div.
        price = div_tag.find('div', {'class': 'pu-final'}).span.get_text()

        # Extracting only numbers from price.
        price = price.replace('Rs.', '').strip(' ').replace(',', '')

        # Finding product name in div
        name = div_tag.find(
            'div', {'class': 'pu-details lastUnit'}).a.get_text().strip()

        # Finding landing href of the product.
        href = self.flipkart_URL + div_tag.a.attrs['href']

        # Finding image src from img tag in div.
        img_src = div_tag.img.attrs['data-src']

        # Finding description of product in div.
        description = div_tag.find('ul', {'class': 'pu-usp'})

        # Handling if product_type doesnt exist.
        try:
            # if present assign to product_type.
            product_type = div_tag.find(
                'div', {'class': 'pu-category'}).span.get_text()

        except:
            # if not present then product_type is search argument.
            product_type = search

        # Storing all values in data dict.
        data = {
            'name': name, 'product_type': product_type, 'price': price,
            'description': str(description), 'landing_url': href,
            'image': img_src, 'site_reference': 'flipkart'
        }

        return data

    def flipkart_books(self, div_tag, search):
        """Function to search specifically books"""
        # Finding price in div.
        price = div_tag.find('div', {'class': 'pu-final'}).get_text()

        # Extracting only numbers from price.
        price = price.replace('Rs.', '').strip(' ').replace(',', '')

        # Finding product name in div
        name = div_tag.find('div', {'class': 'lu-title-wrapper'}).a.get_text()

        # Finding landing href of the product.
        href = self.flipkart_URL + div_tag.a.attrs['href']

        # Finding image src from img tag in div.
        img_src = div_tag.img.attrs['data-src']

        # Finding description of product in div.
        description = div_tag.find('ul', {'class': 'pu-usp'})

        # Handling if product_type doesnt exist.
        try:
            # if present assign to product_type.
            product_type = div_tag.find(
                'div', {'class': 'pu-category'}).span.get_text()

        except:
            # if not present then product_type is search argument.
            product_type = search

        # Storing all values in data dict.
        data = {
            'name': name, 'product_type': product_type, 'price': price,
            'description': str(description), 'landing_url': href,
            'image': img_src, 'site_reference': 'flipkart'
        }

        return data

    def amazon(self, search=None):
        """Scrapping amazon.

        Parse html document using mechanicalsoup, find searchform input tag
        and pass search argument in it and submit.Get response and search for
        specific tags in it to find name, price, href, img src, description
        and store it in a dictionary. Iterate through all the tags and store
        all dictionaries in a list and return it.
        """
        try:
            # Creating brower object.
            browser = mechanicalsoup.Browser()

            # Select the form
            home = browser.get(self.amazon_URL)
            form = home.soup.find("form", {"name": "site-search"})

            # Pass search argument in form input.
            form.find("input", {"id": "twotabsearchtextbox"})["value"] = search
            response = browser.submit(form, home.url)

            # Finding first div element with specific class in page.
            div_tag = response.soup.find(
                'div', {'class': 'a-fixed-left-grid-inner'}
            )

            # Finding all div elements with specific class in page.
            div_tags = response.soup.find_all(
                'div', {'class': 'a-fixed-left-grid-inner'}
            )

            # Defining empty list.
            product_list = []

            for div_tag in div_tags:
                # Finding product name in div
                name = div_tag.find(
                    'div', {'class': 'a-row a-spacing-small'}).h2.get_text()

                # Finding price in div.
                price = div_tag.find('span', {'class': 'currencyINR'}).next_sibling

                # Extracting only numbers from price and typecast to float
                price = float(
                    price.strip(' ').replace(',', '').replace('-', '').replace('/', ''))

                # Finding landing href of the product.
                href = div_tag.find(
                    'div', {'class': 'a-row a-spacing-small'}).a.attrs['href']

                # Finding image src from img tag in div.
                img_src = div_tag.img.attrs['src']

                # Finding product_type of product in div.
                product_type = div_tag.find(
                    'div', {'class': 'a-column a-span5 a-span-last'}).find(
                    'span', {'class': 'a-text-bold'}).get_text().strip(':')

                # Storing all values in data dict.
                data = {
                    'name': name, 'product_type': product_type, 'price': price,
                    'landing_url': href, 'image': img_src,
                    'site_reference': 'amazon'
                }

                try:
                    # Filtering product table with specific parameters
                    # If exist store in product variable.
                    product = Product.objects.filter(
                        site_reference='flipkart', name=name,
                        product_type=product_type)

                    # If product exist.
                    if product:
                        # Update product table with data.
                        Product.objects.filter(pk=product[0].pk).update(**data)

                        # Save the changes
                        product[0].save()

                        # Assigning product[0] to variable product_obj.
                        product_obj = product[0]

                    # If product does not exist.
                    else:
                        # Create new product row.
                        product_obj = Product.objects.create(**data)
                except Exception as e:
                    logger.exception("EXCEPTION :" + str(e))
                    product_obj = None

                if product_obj:
                    # Appending p to product_list
                    product_list.append(product_obj)

            # product_list is return to the view to display it in front end
            return product_list

        except Exception as e:
            logger.exception("EXCEPTION :" + str(e))
            return None
