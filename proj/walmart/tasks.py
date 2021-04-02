from proj.walmart.scripts.store import check_alerts
from celery import shared_task 
from walmart.scripts.store import store_product_info, check_alerts
from walmart.scripts.product_keys import product_keys


@shared_task(name='product_info') 
def save_product_info():
    store_product_info(product_keys)
    check_alerts()
