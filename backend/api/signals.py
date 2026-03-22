from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import Order, Product
from api.services.sync import sync_order_to_erpnext, sync_product_to_erpnext


@receiver(post_save, sender=Product)
def queue_product_sync(sender, instance, created, **kwargs):
    if not created and instance.sync_status == "in_progress":
        return
    transaction.on_commit(lambda: sync_product_to_erpnext(instance.id))


@receiver(post_save, sender=Order)
def queue_order_sync(sender, instance, created, **kwargs):
    if not created:
        return
    transaction.on_commit(lambda: sync_order_to_erpnext(instance.id))
