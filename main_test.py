from functions import small_order_surcharge, delivery_distance, delivery_fee, total_price
from main import app

base_url = "/api/v1/delivery-order-price"

# testing the functions are returning right values 
def test_delivery_fee_calculation():
    user_lat = 60.17010
    user_lon = 24.93895
    venue_lat = 60.17012143
    venue_lon = 24.92813512
    cart_value = 800
    order_minimum_no_surcharge = 1000
    base_price = 199
    distance_ranges = [
        {"min": 0, "max": 500, "a": 0, "b": 0.0},
        {"min": 500, "max": 1000, "a": 100, "b": 1},
        {"min": 1000, "max": 0, "a": 0, "b": 0.0},
    ]

    distance = delivery_distance(user_lat, user_lon, venue_lat, venue_lon)
    assert distance == 600

    surcharge = small_order_surcharge(cart_value, order_minimum_no_surcharge)
    assert surcharge == 200

    fee = delivery_fee(base_price, distance_ranges, distance)
    assert fee == 359

    total = total_price(cart_value, surcharge, fee)
    assert total == 1359

# testing surhcarge for minimum cart value
def test_cart_value_at_minimum_no_surcharge():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.16615&user_lon=24.93452"
        )
        assert response.status_code == 200
        data = response.get_json()
        assert data["delivery"]["fee"] == 290  
        assert data["total_price"] == 1290


# testing query with invalid cart value
def test_invalid_cart_value():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=-1&user_lat=60.16615&user_lon=24.93452"
        )
        assert response.status_code == 400 
        data = response.get_json()
        assert data["error"] == "missing required parameters or invalid parameter"

# testing query with missing cart value parameter
def test_missing_cart_value():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?venue_slug=home-assignment-venue-helsinki&user_lat=60.16615&user_lon=24.93452"
        )
        assert response.status_code == 400  
        data = response.get_json()
        assert data["error"] == "missing required parameters or invalid parameter"

# testing query with missing venue parameter
def test_missing_venue_slug():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?cart_value=10&user_lat=60.16615&user_lon=24.93452"
        )
        assert response.status_code == 400  
        data = response.get_json()
        assert data["error"] == "missing required parameters or invalid parameter"

# testing query with invalid location parameter
def test_invalid_user_coordinates():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=10&user_lat=abc&user_lon=24.93452"
        )
        assert response.status_code == 400 
        data = response.get_json()
        assert data["error"] == "missing required parameters or invalid parameter"

# testing query with float cart value instead of integer
def test_cart_value_with_float_value():
    with app.test_client() as client:
        response = client.get(
            f"{base_url}?venue_slug=home-assignment-venue-helsinki&cart_value=99.99&user_lat=60.16615&user_lon=24.93452"
        )
        assert response.status_code == 400
        data = response.get_json()
        assert data["error"] == "missing required parameters or invalid parameter"
