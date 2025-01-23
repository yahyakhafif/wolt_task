from flask import Flask, request, jsonify
from functions import total_price, small_order_surcharge, delivery_fee, delivery_distance
import requests, traceback

app = Flask(__name__)

# error handling function
def detailed_error_response(exception):
    error_message = str(exception)
    error_traceback = traceback.format_exc()

    return {
        "error": {
            "message": error_message,
            "traceback": error_traceback.split('\n')
        }
    }, 400


@app.route("/api/v1/delivery-order-price", methods=["GET"])
def response():
    try:
        # extracting the values from the query
        venue_slug = request.args.get("venue_slug", type=str)
        cart_value = request.args.get("cart_value", type=int)
        user_lat = request.args.get("user_lat", type=float)
        user_lon = request.args.get("user_lon", type=float)

        # checking if all values are provided
        if not all([venue_slug, cart_value, user_lat, user_lon]):
            return jsonify({"error": "Missing required parameters"}), 400

        # fetching the home assignment api
        static_home_assignment_api = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/static"
        dynamic_home_assignment_api = f"https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/{venue_slug}/dynamic"
        
        # getting data from home assignment api 
        try:
            static_response = requests.get(static_home_assignment_api)
            dynamic_response = requests.get(dynamic_home_assignment_api)
            static_response.raise_for_status()
            dynamic_response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return jsonify({"error": f"Error fetching API data: {str(e)}"}), 400

        venue_static_data = static_response.json()
        venue_dynamic_data = dynamic_response.json()

        # extracting relevant data from the home assignment api response
        try:
            venue_lat = venue_static_data['venue_raw']['location']['coordinates'][1]
            venue_lon = venue_static_data['venue_raw']['location']['coordinates'][0]
            order_minimum_no_surcharge = venue_dynamic_data["venue_raw"]["delivery_specs"]["order_minimum_no_surcharge"]
            base_price = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["base_price"]
            distance_ranges = venue_dynamic_data["venue_raw"]["delivery_specs"]["delivery_pricing"]["distance_ranges"]
            
        except KeyError as e:
            return jsonify({"error": f"Missing key in API data: {str(e)}"}), 400

        # calculate the delivery distance
        delivery_distance_meters = delivery_distance(user_lat, user_lon, venue_lat, venue_lon)

        # calculate delivery fee
        delivery_fee_amount = delivery_fee(base_price, distance_ranges, delivery_distance_meters)

        # when the delivery distance is out of range
        if delivery_fee_amount is None:
            return jsonify({"error": "Delivery not available for this distance"}), 400

        # calculate small order surcharge
        small_order_surcharge_amount = small_order_surcharge(cart_value, order_minimum_no_surcharge)

        # calculate total price
        total_price_amount = total_price(cart_value, small_order_surcharge_amount, delivery_fee_amount)

        # the response
        return jsonify({
            "total_price": total_price_amount,
            "small_order_surcharge": small_order_surcharge_amount,
            "cart_value": cart_value,
            "delivery": {
                "fee": delivery_fee_amount,
                "distance": delivery_distance_meters
            }
        })

    except Exception as e:
        return detailed_error_response(e)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)