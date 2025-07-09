#!/usr/bin/env python3
"""
Generate static PNG images for location recommendation maps using Google Maps Static API
"""

import requests
import os
import googlemaps
import time
from urllib.parse import quote

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyD0tZfpi0PQPBbYh6iwMrkQKda9n1XPQnI"

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def geocode_with_retry(location, max_retries=3):
    """Geocode a location with retries using Google Maps API."""
    for attempt in range(max_retries):
        try:
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                location_data = geocode_result[0]['geometry']['location']
                return (location_data['lat'], location_data['lng'])
            time.sleep(1)
        except Exception as e:
            print(f"Geocoding attempt {attempt + 1} failed for {location}: {e}")
            time.sleep(2)
    return None

# Location recommendation data
locations_data = {
    "bozeman_mt": {
        "name": "Bozeman, Montana Recommendations",
        "accommodation": "Kimpton Armory Hotel",
        "accommodation_address": "24 W Mendenhall St, Bozeman, MT 59715",
        "recommendations": [
            {"name": "Wild Crumb Bakery", "address": "1424 W Main St, Bozeman, MT", "type": "restaurant", "color": "orange"},
            {"name": "Blackbird Kitchen", "address": "200 W Main St, Bozeman, MT", "type": "restaurant", "color": "red"},
            {"name": "Montana Ale Works", "address": "611 E Main St, Bozeman, MT", "type": "restaurant", "color": "green"},
            {"name": "Museum of the Rockies", "address": "600 W Kagy Blvd, Bozeman, MT", "type": "attraction", "color": "purple"},
            {"name": "Hyalite Canyon", "address": "Hyalite Canyon Rd, Bozeman, MT", "type": "outdoor", "color": "blue"},
            {"name": "Main Street Historic District", "address": "Main St, Bozeman, MT", "type": "attraction", "color": "yellow"}
        ]
    },
    
    "missoula_mt": {
        "name": "Missoula, Montana Recommendations",
        "accommodation": "AC Hotel Missoula Downtown",
        "accommodation_address": "200 S Pattee St, Missoula, MT 59802",
        "recommendations": [
            {"name": "Le Petit Outre", "address": "129 W Front St, Missoula, MT", "type": "restaurant", "color": "orange"},
            {"name": "Plonk Wine Bar", "address": "322 N Higgins Ave, Missoula, MT", "type": "restaurant", "color": "red"},
            {"name": "Clark Fork Riverfront Trail", "address": "Caras Park, Missoula, MT", "type": "outdoor", "color": "blue"},
            {"name": "Missoula Art Museum", "address": "335 N Pattee St, Missoula, MT", "type": "attraction", "color": "purple"},
            {"name": "Caras Park", "address": "1120 W Front St, Missoula, MT", "type": "outdoor", "color": "green"},
            {"name": "University of Montana", "address": "32 Campus Dr, Missoula, MT", "type": "attraction", "color": "yellow"}
        ]
    },
    
    "mccall_id": {
        "name": "McCall, Idaho Recommendations",
        "accommodation": "Shore Lodge",
        "accommodation_address": "501 W Lake St, McCall, ID 83638",
        "recommendations": [
            {"name": "Smoky Mountain Pizzeria", "address": "815 N 3rd St, McCall, ID", "type": "restaurant", "color": "orange"},
            {"name": "Sushi Time", "address": "307 E Lake St, McCall, ID", "type": "restaurant", "color": "red"},
            {"name": "Payette Lake Activities", "address": "Payette Lake, McCall, ID", "type": "outdoor", "color": "blue"},
            {"name": "Central Idaho Historical Museum", "address": "1001 State St, McCall, ID", "type": "attraction", "color": "purple"},
            {"name": "Ponderosa State Park", "address": "1920 Davis Ave, McCall, ID", "type": "outdoor", "color": "green"},
            {"name": "Downtown Shopping", "address": "3rd St, McCall, ID", "type": "shopping", "color": "yellow"}
        ]
    },
    
    "joseph_or": {
        "name": "Joseph, Oregon Recommendations", 
        "accommodation": "The Jennings Hotel",
        "accommodation_address": "100 Main St, Joseph, OR 97846",
        "recommendations": [
            {"name": "Embers Brewhouse", "address": "204 N Main St, Joseph, OR", "type": "restaurant", "color": "orange"},
            {"name": "Lear's Main Street Grill", "address": "111 W Main St, Joseph, OR", "type": "restaurant", "color": "red"},
            {"name": "Valley Bronze of Oregon", "address": "18 S Main St, Joseph, OR", "type": "attraction", "color": "purple"},
            {"name": "Wallowa Lake Tramway", "address": "59919 Wallowa Lake Hwy, Joseph, OR", "type": "outdoor", "color": "blue"},
            {"name": "Chief Joseph Days Museum", "address": "610 N Main St, Joseph, OR", "type": "attraction", "color": "green"},
            {"name": "Main Street Art Galleries", "address": "Main St, Joseph, OR", "type": "shopping", "color": "yellow"}
        ]
    },
    
    "walla_walla_wa": {
        "name": "Walla Walla, Washington Recommendations",
        "accommodation": "Eritage Resort",
        "accommodation_address": "1000 N 2nd Ave, Walla Walla, WA 99362",
        "recommendations": [
            {"name": "Colville Street Patisserie", "address": "1425 Plaza Way, Walla Walla, WA", "type": "restaurant", "color": "orange"},
            {"name": "Brasserie Four", "address": "4 E Main St, Walla Walla, WA", "type": "restaurant", "color": "red"},
            {"name": "L'Ecole No 41 Winery", "address": "41 Lowden School Rd, Lowden, WA", "type": "winery", "color": "purple"},
            {"name": "Downtown Wine District", "address": "Main St, Walla Walla, WA", "type": "winery", "color": "blue"},
            {"name": "Pioneer Park", "address": "730 Rose St, Walla Walla, WA", "type": "outdoor", "color": "green"},
            {"name": "Historic Downtown", "address": "Main St, Walla Walla, WA", "type": "attraction", "color": "yellow"}
        ]
    },
    
    "cascade_locks_or": {
        "name": "Columbia River Gorge Recommendations",
        "accommodation": "Under Canvas Columbia River",
        "accommodation_address": "1681 Little White Salmon Rd, Cook, WA 98605",
        "recommendations": [
            {"name": "Thunder Island Brewing", "address": "515 WaNaPa St, Cascade Locks, OR", "type": "restaurant", "color": "orange"},
            {"name": "Bridge of the Gods", "address": "Cascade Locks, OR", "type": "attraction", "color": "red"},
            {"name": "Multnomah Falls", "address": "53000 E Historic Columbia River Hwy, Bridal Veil, OR", "type": "outdoor", "color": "blue"},
            {"name": "Cascade Locks Historic Museum", "address": "1 Portage Rd, Cascade Locks, OR", "type": "attraction", "color": "purple"},
            {"name": "Marine Park", "address": "355 WaNaPa St, Cascade Locks, OR", "type": "outdoor", "color": "green"},
            {"name": "Bonneville Dam", "address": "Cascade Locks, OR", "type": "attraction", "color": "yellow"}
        ]
    },
    
    "seattle_wa": {
        "name": "Seattle, Washington Recommendations",
        "accommodation": "The Fairmont Olympic Seattle",
        "accommodation_address": "411 University St, Seattle, WA 98101", 
        "recommendations": [
            {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "type": "attraction", "color": "red"},
            {"name": "Grand Central Bakery", "address": "214 1st Ave S, Seattle, WA", "type": "restaurant", "color": "orange"},
            {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "type": "attraction", "color": "purple"},
            {"name": "Pioneer Square", "address": "600 1st Ave, Seattle, WA", "type": "attraction", "color": "blue"},
            {"name": "Waterfront Park", "address": "1401 Alaskan Way, Seattle, WA", "type": "outdoor", "color": "green"},
            {"name": "Space Needle", "address": "400 Broad St, Seattle, WA", "type": "attraction", "color": "yellow"}
        ]
    }
}

def create_static_recommendation_map(location_key, location_data):
    """Create a static PNG recommendation map using Google Maps Static API."""
    print(f"Creating recommendation map for {location_data['name']}...")
    
    # Geocode the accommodation
    hotel_coords = geocode_with_retry(location_data['accommodation_address'])
    
    if not hotel_coords:
        print(f"Could not geocode accommodation for {location_data['name']}")
        return None
    
    # Start building the Static Maps API URL
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Map parameters
    params = {
        'center': f"{hotel_coords[0]},{hotel_coords[1]}",
        'zoom': '12',  # Wider view for recommendations
        'size': '800x600',
        'maptype': 'terrain',  # terrain mode for better topographical visibility
        'key': GOOGLE_MAPS_API_KEY,
        'format': 'png',
        'scale': '2'  # High resolution
    }
    
    # Add hotel marker (large red marker)
    markers = [f"color:red|size:large|label:H|{hotel_coords[0]},{hotel_coords[1]}"]
    
    # Add recommendation markers
    for i, rec in enumerate(location_data['recommendations']):
        rec_coords = geocode_with_retry(rec['address'])
        if rec_coords:
            # Use numbers 1-9 for first 9, then letters for rest
            if i < 9:
                label = str(i + 1)
            else:
                label = chr(65 + i - 9)  # A, B, C...
            color = rec.get('color', 'blue')
            markers.append(f"color:{color}|size:mid|label:{label}|{rec_coords[0]},{rec_coords[1]}")
            time.sleep(0.2)  # Rate limiting
    
    # Build URL
    url_params = []
    for key, value in params.items():
        url_params.append(f"{key}={quote(str(value))}")
    
    # Add markers
    for marker in markers:
        url_params.append(f"markers={quote(marker)}")
    
    url = base_url + "&".join(url_params)
    
    # Download the image
    try:
        response = requests.get(url)
        if response.status_code == 200:
            filename = f"images/{location_key}_recommendations_map.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Saved recommendation map: {filename}")
            
            # Also create a legend text file
            legend_filename = f"images/{location_key}_recommendations_map_legend.txt"
            with open(legend_filename, 'w') as f:
                f.write(f"{location_data['name']}\n")
                f.write(f"Hotel: {location_data['accommodation']} (Red H)\n\n")
                f.write("Recommendations:\n")
                for i, rec in enumerate(location_data['recommendations']):
                    if i < 9:
                        label = str(i + 1)
                    else:
                        label = chr(65 + i - 9)
                    f.write(f"{label} - {rec['name']} ({rec['type']})\n")
            
            return filename
        else:
            print(f"Error downloading map: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating recommendation map: {e}")
        return None

def main():
    """Generate all static location recommendation maps."""
    print("Generating static PNG recommendation maps for all locations...")
    
    for location_key, location_data in locations_data.items():
        create_static_recommendation_map(location_key, location_data)
        time.sleep(1)  # Rate limiting between API calls
    
    print("All static recommendation maps generated!")

if __name__ == "__main__":
    main() 