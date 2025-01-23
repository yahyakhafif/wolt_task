from flask import Flask, request
app = Flask(__name__)

@app.route("/api/v1/delivery-order-price", methods=["GET"])
def response():
    venue_slug = request.args.get("venue_slug", type=str)
    cart_value = request.args.get("cart_value", type=int)
    user_lat = request.args.get("user_lat", type=float)
    user_lon = request.args.get("user_lon", type=float)

    return {
             "total_price": total_price,
             "small_order_surcharge": small_order_surcharge,
             "cart_value": cart_value,
             "delivery": {
                "fee": delivery_fee,
                "distance": delivery_distance
               }
            }

def small_order_surcharge(cart_value, order_minimum_no_surcharge):
    if cart_value < order_minimum_no_surcharge:
        return "no surcharge"
    else:
        small_order_surcharge = order_minimum_no_surcharge - cart_value
        return  small_order_surcharge

def order_minimum_no_surcharge():
    pass

def hervesine_formula(user_lat, user_long, venue_lat, venue_long):
    pass

def delivery_distance(user_lat, user_long, venue_lat, venue_long):
    delivery_distance = hervesine_formula(user_lat, user_long, venue_lat, venue_long) 
    return delivery_distance

def delivery_fee(base_price, a, b, delivery_distance):
    delivery_fee = base_price + a + b * delivery_distance / 10
    return delivery_fee 

def total_price(cart_value, small_order_surcharge, delivery_fee):
    total_price = cart_value + small_order_surcharge + delivery_fee 
    return total_price


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
