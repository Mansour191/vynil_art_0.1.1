import time

from django.utils import timezone

from api.models import ERPNextSyncLog, Order, Product
from api.services.erpnext_client import ERPNextClient
from api.services.erpnext_mappers import (
    map_order_to_customer,
    map_order_to_sales_order,
    map_product_to_item,
)


def _retry(operation, retries=3, base_delay=1):
    last_error = None
    for attempt in range(retries):
        try:
            return operation()
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt < retries - 1:
                time.sleep(base_delay * (2 ** attempt))
    raise last_error


def sync_product_to_erpnext(product_id):
    product = Product.objects.select_related("category").get(id=product_id)
    log = ERPNextSyncLog.objects.create(
        action="sync_product",
        status="in_progress",
        message=f"Syncing product {product.slug}",
    )
    product.sync_status = "in_progress"
    product.sync_error = ""
    product.save(update_fields=["sync_status", "sync_error"])

    try:
        client = ERPNextClient()
        payload = map_product_to_item(product)
        response = _retry(lambda: client.upsert_item(payload))

        product.erpnext_item_code = response.get("item_code", payload["item_code"])
        product.sync_status = "synced"
        product.sync_error = ""
        product.last_synced_at = timezone.now()
        product.save(update_fields=["erpnext_item_code", "sync_status", "sync_error", "last_synced_at"])

        log.status = "success"
        log.message = f"Product synced as {product.erpnext_item_code}"
        log.save(update_fields=["status", "message"])
        return product.erpnext_item_code
    except Exception as exc:  # noqa: BLE001
        product.sync_status = "failed"
        product.sync_error = str(exc)
        product.save(update_fields=["sync_status", "sync_error"])

        log.status = "failed"
        log.message = str(exc)
        log.save(update_fields=["status", "message"])
        raise


def sync_order_to_erpnext(order_id):
    order = Order.objects.prefetch_related("items__product").get(id=order_id)
    log = ERPNextSyncLog.objects.create(
        action="sync_order",
        status="in_progress",
        message=f"Syncing order {order.order_number}",
    )
    order.sync_status = "in_progress"
    order.sync_error = ""
    order.save(update_fields=["sync_status", "sync_error"])

    try:
        client = ERPNextClient()
        customer_payload = map_order_to_customer(order)
        customer_response = _retry(lambda: client.upsert_customer(customer_payload))
        customer_name = customer_response.get("name", customer_payload["customer_name"])

        sales_order_payload = map_order_to_sales_order(order, customer_name)
        sales_order_response = _retry(lambda: client.create_sales_order(sales_order_payload))

        order.erpnext_sales_order_id = sales_order_response.get("name", "")
        order.sync_status = "synced"
        order.sync_error = ""
        order.last_synced_at = timezone.now()
        order.save(
            update_fields=["erpnext_sales_order_id", "sync_status", "sync_error", "last_synced_at"]
        )

        log.status = "success"
        log.message = f"Order synced as {order.erpnext_sales_order_id}"
        log.save(update_fields=["status", "message"])
        return order.erpnext_sales_order_id
    except Exception as exc:  # noqa: BLE001
        order.sync_status = "failed"
        order.sync_error = str(exc)
        order.save(update_fields=["sync_status", "sync_error"])

        log.status = "failed"
        log.message = str(exc)
        log.save(update_fields=["status", "message"])
        raise
