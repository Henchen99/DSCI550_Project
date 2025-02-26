import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Define directories
raw_data_dir = os.path.join("..", "data", "raw")
os.makedirs(raw_data_dir, exist_ok=True)

# Define file path
sun_data_file = os.path.join(raw_data_dir, "sunrise_sunset_data.csv")

# List of cities to scrape from haunted_places_list.csv
city_list = os.path.join(raw_data_dir, "haunted_places_list.csv")
cities_df = pd.read_csv(city_list)
cities = cities_df['city'].unique()


# Base URL
base_url = "https://www.timeanddate.com/sun/usa/"

# Initialize list for storing results
data = []

# Loop through cities and scrape data
for city in cities:
    url = f"{base_url}{city}"
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract sunrise and sunset times
        try:
            sunrise = soup.find("td", class_="c sep-l").text.strip()
            sunset = soup.find("td", class_="c").find_next_sibling("td").text.strip()
            print(f"Scraped {city.capitalize()}: Sunrise {sunrise}, Sunset {sunset}")
            data.append([city.replace("-", " ").title(), sunrise, sunset])
        except AttributeError:
            print(f"Could not extract data for {city}")

    else:
        print(f"Failed to retrieve {city}, Status Code: {response.status_code}")

# Convert to DataFrame
sun_data_df = pd.DataFrame(data, columns=["City", "Sunrise", "Sunset"])

# Save to CSV
sun_data_df.to_csv(sun_data_file, index=False)
print(f"Sunrise and sunset data saved at: {sun_data_file}")
