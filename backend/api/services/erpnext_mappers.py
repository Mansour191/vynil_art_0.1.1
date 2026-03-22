def map_product_to_item(product):
    return {
        "item_code": (product.erpnext_item_code or product.slug).upper(),
        "item_name": product.name_en,
        "description": product.description_en or product.description_ar or "",
        "item_group": product.category.name_en,
        "stock_uom": "Unit",
        "standard_rate": float(product.base_price),
        "disabled": 0,
    }


def map_order_to_customer(order):
    return {
        "customer_name": order.customer_name,
        "customer_group": "Individual",
        "territory": "All Territories",
        "mobile_no": order.phone,
        "email_id": order.email,
    }


def map_order_to_sales_order(order, erp_customer_name):
    items = []
    for item in order.items.select_related("product").all():
        area_m2 = (float(item.width) * float(item.height)) / 10000
        item_payload = {
            "item_code": (item.product.erpnext_item_code or item.product.slug).upper(),
            "qty": float(item.quantity),
            "uom": "Unit",
            "rate": float(item.price),
            "description": item.product.name_en,
            "custom_width_cm": float(item.width),
            "custom_height_cm": float(item.height),
            "custom_area_m2": round(area_m2, 4),
            "custom_dimension_unit": item.dimension_unit,
            "custom_marble_texture": item.marble_texture,
            "custom_design": item.custom_design,
        }
        items.append(item_payload)

    date_str = order.created_at.date().isoformat()
    return {
        "customer": erp_customer_name,
        "transaction_date": date_str,
        "delivery_date": date_str,
        "custom_order_number": order.order_number,
        "items": items,
    }
