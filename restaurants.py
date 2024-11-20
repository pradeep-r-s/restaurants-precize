import json
import re
from googleapiclient.discovery import build


def get_top_restaurants(city, food_type, api_key, cse_id):
    
    search_service = build("customsearch", "v1", developerKey=api_key)

    query = f"top 10 {food_type} restaurants in {city} with ratings"
    search_results = search_service.cse().list(q=query, cx=cse_id).execute()

    restaurant_data = {}

    for result in search_results.get('items', []):
        restaurant_name = result['title'].split('-')[0].strip()

        rating = None
        review = result.get('snippet', '')
        match = re.search(r'(\d+(?:\.\d+)?\/\d+)', review)
        if match:
            rating = match.group(0)

        restaurant_data[restaurant_name] = {
            'Link': result['link'],
            'Review': review,
            'Rating': rating
        }

    return restaurant_data


def main():
    city = input("Enter the name of the city: ")
    food_type = input("Enter the type of food: ")

    api_key = "AIzaSyDLG62DwvEJoZStXUkUHmQeGKHqFKVLvjQ"
    cse_id = "a217bb43341ad4b78"

    restaurant_data = get_top_restaurants(city, food_type, api_key, cse_id)

    with open('restaurant_data.json', 'w') as file:
        json.dump(restaurant_data, file, indent=4)

    print("Restaurant data saved to restaurant_data.json")


if __name__ == "__main__":
    main()
