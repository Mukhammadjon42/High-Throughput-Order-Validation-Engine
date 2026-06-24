import os
import time
import logging
from flask import Flask, request, jsonify
from redis import Redis

app = Flask(__name__)

# Configure structured logging to output to a file inside the container
log_file = os.environ.get("LOG_FILE", "/var/log/app/engine.log")
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] - %(message)s'
)

# Connect to Redis using Docker's internal DNS name
db = Redis(host='order-cache', port=6379, decode_responses=True)

@app.route('/v1/order/validate', methods=['POST'])
def validate_order():
    data = request.get_json() or {}
    order_id = data.get("order_id")
    symbol = data.get("symbol")
    quantity = data.get("quantity")

    if not order_id or not symbol or not quantity:
        logging.warning("Rejected invalid payload structure.")
        return jsonify({"status": "REJECTED", "reason": "Missing required order parameters"}), 400

    # Production Check: Look for duplicate orders inside Redis memory cache
    if db.exists(order_id):
        logging.error(f"DUPLICATE ORDER ALERT: Order ID {order_id} attempted a double execution.")
        return jsonify({"status": "REJECTED", "reason": "Duplicate Order ID detected (Idempotency Violation)"}), 409

    # Cache the order ID for 60 seconds to prevent rapid double-clicks
    db.setex(order_id, 60, "PROCESSED")
    
    logging.info(f"SUCCESS: Order {order_id} validated for {quantity} shares of {symbol}.")
    return jsonify({
        "status": "VALIDATED",
        "order_id": order_id,
        "engine_timestamp": time.time()
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)