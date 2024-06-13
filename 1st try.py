import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape Home Depot for a product's price
def scrape_home_depot(product_reference):
    url = f"https://www.homedepot.com/p/Frigidaire-30-in-18-3-cu-ft-Top-Freezer-Refrigerator-{product_reference}/311743494"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_container = soup.find('div', class_='price')
        if price_container:
            price = price_container.find('span').text.strip()
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Home Depot.")
            return None
    except Exception as e:
        print(f"Error fetching data from Home Depot: {e}")
        return None

# Function to scrape Lowe's for a product's price
def scrape_lowes(product_reference):
    url = f"https://www.lowes.com/pd/Frigidaire-18-3-cu-ft-Top-Freezer-Refrigerator-{product_reference}/1000407073"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_container = soup.find('span', class_='price')
        if price_container:
            price = price_container.text.strip()
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Lowe's.")
            return None
    except Exception as e:
        print(f"Error fetching data from Lowe's: {e}")
        return None

# Function to scrape Best Buy for a product's price
def scrape_best_buy(product_reference):
    url = f"https://www.bestbuy.com/site/frigidaire-18-cu-ft-top-freezer-refrigerator-{product_reference}/6429517.p"
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        price_container = soup.find('div', class_='priceView-hero-price priceView-customer-price')
        if price_container:
            price = price_container.find('span').text.strip()
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Best Buy.")
            return None
    except Exception as e:
        print(f"Error fetching data from Best Buy: {e}")
        return None

# Product reference number to search for
product_reference = "FFTR1835VW"

# Scrape each website for the product's prices
home_depot_price = scrape_home_depot(product_reference)
lowes_price = scrape_lowes(product_reference)
best_buy_price = scrape_best_buy(product_reference)

# Collect all prices
all_prices = [price for price in [home_depot_price, lowes_price, best_buy_price] if price is not None]

# Find the best price
if all_prices:
    best_price = min(all_prices)
    print(f"The best price for product reference {product_reference} is ${best_price:.2f}")
else:
    print(f"No prices found for product reference {product_reference}")

# Optionally, save the results to a CSV file
df = pd.DataFrame(all_prices, columns=['Price'])
df.to_csv('prices.csv', index=False)
