import requests
from bs4 import BeautifulSoup
import json
from googlesearch import search
import random
import time

# List of user agents to avoid getting blocked
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"
]

def get_top_restaurants(city_name):
    # Perform a Google search to find top restaurants in the city
    query = f"top restaurants in {city_name}"
    search_results = list(search(query, num_results=10))  # Convert to a list
    
    restaurant_data = {}

    # Loop through the first 10 search results
    for result in search_results:
        try:
            headers = {'User-Agent': random.choice(user_agents)}
            response = requests.get(result, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Example: Extract restaurant names, ratings, and reviews
            restaurants_on_page = soup.find_all(['h2', 'h3'], string=True)  # Adjust according to actual tags
            
            for restaurant in restaurants_on_page:
                name = restaurant.get_text().strip()
                rating = "N/A"
                reviews = "N/A"
                
                # Look for rating in a specific span or class
                rating_tag = soup.find('span', {'class': 'rating-class'})  # Adjust according to actual class
                if rating_tag:
                    rating = rating_tag.get_text().strip()
                
                # Look for reviews in a specific div or span
                reviews_tag = soup.find('span', {'class': 'reviews-class'})  # Adjust according to actual class
                if reviews_tag:
                    reviews = reviews_tag.get_text().strip()
                
                # Store each restaurant's data under its name
                restaurant_data[name] = {
                    'Rating': rating,
                    'Reviews': reviews,
                    'URL': result
                }
            
            # Sleep for a short time to avoid being blocked
            time.sleep(random.randint(1, 3))
        
        except Exception as e:
            print(f"Error while scraping {result}: {e}")
            continue
    
    return restaurant_data

def save_to_json(data, filename='restaurants.json'):
    # Save the collected data to a JSON file
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def main():
    city_name = input("Enter the name of the city: ")
    restaurant_data = get_top_restaurants(city_name)
    save_to_json(restaurant_data)
    print(f"Top 10 restaurants data for {city_name} has been saved to 'restaurants.json'.")

if __name__ == '__main__':
    main()
