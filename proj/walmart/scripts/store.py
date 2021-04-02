import os
import django
import structlog
from django.core.mail import send_mail

os.environ["DJANGO_SETTINGS_MODULE"] = "proj.settings"
django.setup()

from scraper_api import ScraperAPIClient
from walmart.models import Product, UserProductAlert
from walmart.scripts.product_keys import product_keys
from walmart.scripts.upload_constants import base_url, count, offset, page, store_id
from django.conf import settings
from django.contrib.auth.models import User

structlog.dev.ConsoleRenderer(
    pad_event=30,
    colors=True,
    force_colors=True,
    repr_native_str=False,
    level_styles=None,
)
logger = structlog.get_logger(__name__)

def store_product_info(product_keys):
    for key in product_keys:
        url = gen_url(base_url, count, offset, page, store_id, key)
        try:
            client = ScraperAPIClient(settings.SCRAPER_API_KEY)
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
            logger.error("failed to fetch product info, error: " + str(e))

        try:
            store_to_db(res_json["products"])
        except Exception as e:
            logger.error("failed to save product info, error: " + str(e))


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


def check_alerts():
    alerts = UserProductAlert.objects.values()

    for alert in alerts:
        user = User.objects.get(id=alert["user_id"])
        product = Product.objects.filter(product_id=alert["product_id"]).order_by('-id').values()[0]
        if product["display_price"] <= alert["alert_price"]:
            sendmail(user.email, product["name"])
            print("sent successfully")


def sendmail(email, product_name):
    subject = 'Price Got Down'
    message = "Price got dropped for the product {}".format(product_name)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


if __name__ == "__main__":
    # store_product_info(product_keys)
    check_alerts()