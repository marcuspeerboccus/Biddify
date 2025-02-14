import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import time

@dataclass
class CarData:
    mileage: str
    sale_date: str
    primary_damage: str
    engine: str
    images: List[str]

def extract_car_data(cookie: str, start_page: int = 1, end_page: int = 10) -> List[CarData]:
    """
    Extract car data from autohelperbot.com/sales for specific car model with pagination
    Args:
        cookie: Authentication cookie
        start_page: Starting page number
        end_page: Ending page number
    """
    base_url = "https://autohelperbot.com/sales?vehicle=AUTOMOBILE&year_from=2020&year_to=2024&make_id=8773&model_id=52810&_=1739238328991&page={}"
    headers = {
        "Cookie": cookie,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    all_car_listings = []

    for page in range(start_page, end_page + 1):
        try:
            url = base_url.format(page)
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Check if we've reached the end of available listings
            if "No items found" in response.text:
                print(f"No more listings found after page {page-1}")
                break
            
            for car_div in soup.find_all('div', class_='row py-2'):
                # Extract images (up to 6)
                image_box = car_div.find('div', class_='image_box')
                images = []
                if image_box:
                    main_image = image_box.find('img')
                    if main_image and main_image.get('src'):
                        images.append(main_image['src'])

                # Extract car details
                params_div = car_div.find_all('div', class_='params')
                if not params_div:
                    continue

                mileage = ""
                sale_date = ""
                primary_damage = ""
                engine = ""

                for param in params_div:
                    for div in param.find_all('div', class_='mt-1'):
                        label = div.find('b')
                        if not label:
                            continue
                        
                        label_text = label.text.strip().lower()
                        value_div = div.find('div', class_='values')
                        if not value_div:
                            continue
                        
                        value = value_div.text.strip()
                        
                        if 'mileage' in label_text:
                            mileage = value
                        elif 'date of sale' in label_text:
                            sale_date = value
                        elif 'main damage' in label_text:
                            primary_damage = value
                        elif 'engine' in label_text:
                            engine = value

                if any([mileage, sale_date, primary_damage, engine]):
                    car_data = CarData(
                        mileage=mileage,
                        sale_date=sale_date,
                        primary_damage=primary_damage,
                        engine=engine,
                        images=images[:6]
                    )
                    all_car_listings.append(car_data)
            
            # Add a small delay between requests to be respectful to the server
            time.sleep(1)
            print(f"Processed page {page}, found {len(all_car_listings)} cars so far")

        except requests.RequestException as e:
            print(f"Error fetching data from page {page}: {e}")
            continue

    return all_car_listings

# Example usage:
if __name__ == "__main__":
    # Replace with your actual cookie value
    cookie = "YOUR_COOKIE_HERE"
    # Extract data from first 5 pages
    cars = extract_car_data(cookie, start_page=1, end_page=5)
    
    print(f"\nTotal cars found: {len(cars)}")
    for idx, car in enumerate(cars, 1):
        print(f"\nCar #{idx}:")
        print(f"Mileage: {car.mileage}")
        print(f"Sale Date: {car.sale_date}")
        print(f"Primary Damage: {car.primary_damage}")
        print(f"Engine: {car.engine}")
        print(f"Images: {car.images}")