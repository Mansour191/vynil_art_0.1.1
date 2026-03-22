import json
import os
from urllib import error, parse, request


class ERPNextClient:
    def __init__(self):
        self.base_url = os.getenv("ERPNEXT_BASE_URL", "").rstrip("/")
        self.api_key = os.getenv("ERPNEXT_API_KEY", "")
        self.api_secret = os.getenv("ERPNEXT_API_SECRET", "")
        self.timeout = int(os.getenv("ERPNEXT_TIMEOUT", "30"))

        if not self.base_url:
            raise ValueError("ERPNEXT_BASE_URL is not configured.")
        if not self.api_key or not self.api_secret:
            raise ValueError("ERPNEXT_API_KEY / ERPNEXT_API_SECRET are not configured.")

        self.auth_header = f"token {self.api_key}:{self.api_secret}"

    def _request(self, method, path, payload=None):
        data = None
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")

        req = request.Request(
            url=f"{self.base_url}{path}",
            method=method,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Authorization": self.auth_header,
            },
        )

        try:
            with request.urlopen(req, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
                parsed = json.loads(raw or "{}")
                return parsed.get("data", parsed)
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="ignore")
            raise RuntimeError(f"ERPNext HTTP {exc.code}: {body}") from exc
        except error.URLError as exc:
            raise RuntimeError(f"ERPNext connection error: {exc.reason}") from exc

    def get_item(self, item_code):
        safe_code = parse.quote(item_code)
        return self._request("GET", f"/api/resource/Item/{safe_code}")

    def upsert_item(self, item_payload):
        item_code = item_payload["item_code"]
        try:
            self.get_item(item_code)
            safe_code = parse.quote(item_code)
            return self._request("PUT", f"/api/resource/Item/{safe_code}", item_payload)
        except RuntimeError:
            return self._request("POST", "/api/resource/Item", item_payload)

    def get_customer(self, customer_name):
        safe_name = parse.quote(customer_name)
        return self._request("GET", f"/api/resource/Customer/{safe_name}")

    def upsert_customer(self, customer_payload):
        customer_name = customer_payload["customer_name"]
        try:
            self.get_customer(customer_name)
            safe_name = parse.quote(customer_name)
            return self._request("PUT", f"/api/resource/Customer/{safe_name}", customer_payload)
        except RuntimeError:
            return self._request("POST", "/api/resource/Customer", customer_payload)

    def create_sales_order(self, sales_order_payload):
        return self._request("POST", "/api/resource/Sales Order", sales_order_payload)
