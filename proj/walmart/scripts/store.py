import os
import django

os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
django.setup()

from scraper_api import ScraperAPIClient
from walmart.models import Product
from walmart.scripts.product_keys import product_keys
from walmart.scripts.upload_constants import base_url, count, offset, page, store_id


def store_product_info(product_keys):
    for key in product_keys:
        url = gen_url(base_url, count, offset, page, store_id, key)
        try:
            client = ScraperAPIClient('2afffa25a502bf4f254f972578ad9550')
            result = client.get(url=url)
            if result.status_code == 200:
                res_json = result.json()
            elif result.status_code == 500:
                raise Exception("Request not successful, status: 500")
            elif result.status_code == 403:
                raise Exception("Plan max request exceeded, status: 403")
            elif result.status_code == 404:
                raise Exception("Request not found, status: 404")
            elif result.status_code == 410:
                raise Exception("Request gone or deleted, status: 410")
        except Exception as e:
            print("failed to fetch product info, error: " + str(e))

        try:
            store_to_db(res_json["products"])
        except Exception as e:
            print("failed to save product info, error: " + str(e))


def store_to_db(products):
    for product in products:
        product_obj = Product.objects.create(
            product_id=product["USItemId"],
            name=product["basic"]["name"],
            previous_price=product["store"]["price"]["previousPrice"],
            display_price=product["store"]["price"]["displayPrice"],
            is_out_of_stock=product["store"]["isOutOfStock"]
        )
        product_obj.save()


def gen_url(base_url, count, offset, page, store_id, query):
    url = f"{base_url}?count={count}&offset={offset}&page={page}&storeId={store_id}&query={query}"
    return url

if __name__ == "__main__":
    store_product_info(product_keys)