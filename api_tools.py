# api_tools.py
# This file simulates our company's backend systems and available APIs.

import datetime

# Mock database of customer orders
mock_orders_db = {
    "ORD12345": {
        "status": "Shipped",
        "placedDate": datetime.datetime.now() - datetime.timedelta(days=5),
        "trackingNumber": "1Z999AA10123456789",
        "estimatedDelivery": "3 days",
    },
    "ORD67890": {
        "status": "Delivered",
        "placedDate": datetime.datetime.now() - datetime.timedelta(days=15),
        "trackingNumber": "1Z999AA10198765432",
        "estimatedDelivery": "Delivered 5 days ago",
    },
    "ORDABCDE": {
        "status": "Processing",
        "placedDate": datetime.datetime.now() - datetime.timedelta(days=1),
        "trackingNumber": "N/A",
        "estimatedDelivery": "5-7 business days",
    }
}

# --- Tool 1: Order Tracking API ---
def OrderTracking(orderId: str) -> dict:
    """
    Simulates the OrderTracking API.
    Fetches order status and tracking information.
    """
    print(f"--- TOOL CALLED: OrderTracking(orderId='{orderId}') ---")
    order_info = mock_orders_db.get(orderId.upper())
    
    if order_info:
        return {
            "success": True,
            "orderId": orderId.upper(),
            "status": order_info["status"],
            "trackingNumber": order_info["trackingNumber"],
            "estimatedDelivery": order_info["estimatedDelivery"],
        }
    else:
        return {
            "success": False,
            "error": "Order not found.",
        }

# --- Tool 2: Order Cancellation API ---
def OrderCancellation(orderId: str) -> dict:
    """
    Simulates the OrderCancellation API.
    Processes an order cancellation request, enforcing company policy.
    """
    print(f"--- TOOL CALLED: OrderCancellation(orderId='{orderId}') ---")
    order_info = mock_orders_db.get(orderId.upper())

    if not order_info:
        return {
            "success": False,
            "error": "Order not found.",
        }

    # --- Policy Enforcement ---
    cancellation_window_days = 10
    order_date = order_info["placedDate"]
    days_since_order = (datetime.datetime.now() - order_date).days

    if days_since_order <= cancellation_window_days:
        return {
            "success": True,
            "message": f"Order {orderId.upper()} has been successfully cancelled.",
        }
    else:
        return {
            "success": False,
            "error": "Order is not eligible for cancellation.",
            "reason": f"The order was placed {days_since_order} days ago, which is outside the {cancellation_window_days}-day cancellation window.",
        }
