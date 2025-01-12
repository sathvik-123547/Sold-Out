import requests

def get_restaurants_osm(lat, lng, radius=5000):
    """
    Fetch nearby restaurants using OpenStreetMap's Overpass API.
    Includes nodes, ways, and relations for better coverage.
    """
    overpass_url = "http://overpass-api.de/api/interpreter"
    query = f"""
    [out:json][maxsize:10485760];
    (
      node["amenity"="restaurant"](around:{radius},{lat},{lng});
      way["amenity"="restaurant"](around:{radius},{lat},{lng});
      relation["amenity"="restaurant"](around:{radius},{lat},{lng});
    );
    out body;
    """
    response = requests.get(overpass_url, params={'data': query})
    
    if response.status_code == 200:
        data = response.json()
        restaurants = []
        for element in data['elements']:
            restaurant = {
                "name": element.get("tags", {}).get("name", "Unnamed Restaurant"),
                "latitude": element.get("lat", None),
                "longitude": element.get("lon", None),
                "tags": element.get("tags", {})
            }
            restaurants.append(restaurant)
        return restaurants
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

# Example Usage
if __name__ == "__main__":
    lat, lng = 17.3948, 78.3672  # Kokapet, Hyderabad
    restaurants = get_restaurants_osm(lat, lng, radius=5000)
    if restaurants:
        for r in restaurants:
            print(f"Name: {r['name']}, Latitude: {r['latitude']}, Longitude: {r['longitude']}, Tags: {r['tags']}")
    else:
        print("No restaurants found.")
