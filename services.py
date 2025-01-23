import geopy.distance

# function to calculate the surcharge
def small_order_surcharge(cart_value, order_minimum_no_surcharge):
    if cart_value < order_minimum_no_surcharge:
        return order_minimum_no_surcharge - cart_value
    return 0

# function to calculate the delivery distance using geopy library
def delivery_distance(user_lat, user_lon, venue_lat, venue_lon):
    user_coordinates = (user_lat, user_lon)
    venue_coordinates = (venue_lat, venue_lon)
    return round(geopy.distance.geodesic(user_coordinates, venue_coordinates).meters)

# function to calculate the delivery fee depending on distance range
def delivery_fee(base_price, distance_ranges, delivery_distance):
    for distance_range in distance_ranges:
        if delivery_distance >= distance_range["min"] and delivery_distance < distance_range["max"]:
            if distance_range["max"] == 0:
                return None
            return base_price + distance_range["a"] + round(distance_range["b"] * delivery_distance / 10)
    return None

# function to calculate the total price 
def total_price(cart_value, small_order_surcharge, delivery_fee):
    return cart_value + small_order_surcharge + delivery_fee