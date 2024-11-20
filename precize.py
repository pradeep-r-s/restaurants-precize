import requests
import json

def get_top_restaurants(city_name, api_key, cse_id):
    """
    Fetch the top 10 restaurants in the specified city using Google Custom Search API.
    """
    print(f"Fetching top restaurants for '{city_name}' based on ratings and reviews...")
    search_query = f"top 10 restaurants in {city_name} with ratings and reviews"
    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cse_id}&q={search_query}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP status codes 4xx/5xx
        data = response.json()

        restaurant_data = {}
        if 'items' in data:
            for item in data['items']:
                name = item.get('title', 'Unknown Restaurant')
                snippet = item.get('snippet', 'No details available.')
                link = item.get('link', 'No URL available.')

                rating = None
                reviews = None
                try:
                    # Assuming ratings are embedded in the snippet, you can adapt this logic
                    if "rating" in snippet.lower():
                        rating = snippet.split("rating:")[1].split(",")[0].strip()
                    if "reviews" in snippet.lower():
                        reviews = snippet.split("reviews:")[1].split(",")[0].strip()
                except IndexError:
                    pass

                # Fallback if rating or reviews are not found
                if not rating:
                    rating = "Rating not available"
                if not reviews:
                    reviews = "No reviews available."

                restaurant_data[name] = {
                    'First Rating': rating,
                    'review': reviews,
                    'Link': link
                }
            print(f"Fetched {len(restaurant_data)} restaurants.")
        else:
            print("No results found in the search query.")

        return restaurant_data

    except requests.exceptions.RequestException as e:
        print(f"Error while making API request: {e}")
        return {}

def save_to_json(data, filename='restaurants.json'):
    """
    Save restaurant data to a JSON file.
    """
    if data:
        with open(filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data saved to '{filename}'.")
    else:
        print("No data to save.")

def main():
    """
    Main function to get input from the user and execute the API call.
    """
    api_key = "abc"  # Your API Key
    cse_id = "efg"  # Your Search Engine ID

    if not api_key or not cse_id:
        print("Please ensure your API Key and CSE ID are set correctly.")
        return

    city_name = input("Enter the name of the city: ")
    restaurant_data = get_top_restaurants(city_name, api_key, cse_id)
    save_to_json(restaurant_data)

if __name__ == '__main__':
    main()
