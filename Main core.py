from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup

def scrape_home_depot_selenium(product_reference):
    url = f"https://www.homedepot.com/p/Frigidaire-30-in-18-3-cu-ft-Top-Freezer-Refrigerator-{product_reference}/311743494"
    try:
        # Set the path to chromedriver if it's not in your PATH
        chromedriver_path = 'C:/Users/jaret/Downloads/chromedriver-win64/chromedriver.exe'
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)
        
        driver.get(url)
        
        # Wait for the price container to be present
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'price-format__large price-format__main-price')))
        
        # Print the page source for debugging
        page_source = driver.page_source
        print(page_source)
        
        soup = BeautifulSoup(page_source, 'html.parser')
        driver.quit()
        
        # Locate the price container based on the provided HTML structure
        price_container = soup.find('div', class_='price-format__large price-format__main-price')
        
        if price_container:
            # Extract the price parts
            price_dollars = price_container.find_all('span')[1].text.strip()
            price_cents = price_container.find_all('span')[3].text.strip()
            
            # Combine the price parts into a single float value
            price = f"{price_dollars}.{price_cents}"
            return float(price.replace('$', '').replace(',', ''))
        else:
            print("Price container not found on Home Depot.")
            return None
    except Exception as e:
        print(f"Error fetching data from Home Depot: {e}")
        return None

# Product reference number to search for
product_reference = "FFTR1835VW"

# Scrape Home Depot for the product's price
home_depot_price = scrape_home_depot_selenium(product_reference)

# Check and print the price
if home_depot_price is not None:
    print(f"The price for product reference {product_reference} on Home Depot is ${home_depot_price:.2f}")
else:
    print(f"No price found for product reference {product_reference} on Home Depot")
