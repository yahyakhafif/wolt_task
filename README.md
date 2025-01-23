# Prerequisites

Before getting started, ensure you have the following installed:

1- Python 3.x (with pip installed)     
2- Virtual Environment (optional)

# Steps to Setup the Project

**1. Download the Project ZIP File**

Download the zip file and extract the contents to a directory of your choice.

  

**2. Set Up a Virtual Environment**

Open a terminal in the extracted project directory and run the following commands:

    python3 -m venv venv
    
    source venv/bin/activate

  

**3. Install Dependencies**

install the required dependencies using the requirements.txt file provided in the project folder:

    pip install -r requirements.txt

  

**4. Running the App Locally**

you can start the app with the following command:

    python3 app.py

This will start the Flask development server, and you can access server at http://localhost:8000 and to test the api endpoint you can use the following [query](http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087)
