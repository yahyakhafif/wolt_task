from flask import Flask, request
app = Flask(__name__)

@app.route("/api/v1/delivery-order-price", methods=["GET"])
def response():
    venue_slug = request.args.get("venue_slug", type=str)
    cart_value = request.args.get("cart_value", type=int)
    user_lat = request.args.get("user_lat", type=float)
    user_lon = request.args.get("user_lon", type=float)

    return {
             "total_price": 1190,
             "small_order_surcharge": 0,
             "cart_value": 1000,
             "delivery": {
                "fee": 190,
                "distance": 177
               }
            }


def small_order_surcharge():
    pass

def order_minimum_no_surcharge():
    pass

def delivery_distance():
    pass

def delivery_fee():
    pass

def total_price():
    pass

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
