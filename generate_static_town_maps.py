#!/usr/bin/env python3
"""
Generate static PNG images for walking vicinity maps using Google Maps Static API
"""

import requests
import os
import googlemaps
import time
from urllib.parse import quote

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

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

# Town data for static maps
towns_data = {
    "bozeman_mt": {
        "name": "Downtown Bozeman, Montana",
        "accommodation": "Kimpton Armory Hotel",
        "accommodation_address": "24 W Mendenhall St, Bozeman, MT 59715",
        "points_of_interest": [
            {"name": "Main Street Historic District", "address": "Main St, Bozeman, MT", "color": "red"},
            {"name": "Wild Crumb Bakery", "address": "1424 W Main St, Bozeman, MT", "color": "orange"},
            {"name": "Blackbird Kitchen", "address": "200 W Main St, Bozeman, MT", "color": "green"},
            {"name": "Montana Ale Works", "address": "611 E Main St, Bozeman, MT", "color": "blue"},
            {"name": "Bogert Park", "address": "325 S Church Ave, Bozeman, MT", "color": "purple"}
        ]
    },
    
    "missoula_mt": {
        "name": "Downtown Missoula, Montana", 
        "accommodation": "AC Hotel Missoula Downtown",
        "accommodation_address": "200 S Pattee St, Missoula, MT 59802",
        "points_of_interest": [
            {"name": "Clark Fork Riverfront Trail", "address": "Caras Park, Missoula, MT", "color": "blue"},
            {"name": "Le Petit Outre", "address": "129 W Front St, Missoula, MT", "color": "orange"},
            {"name": "Plonk Wine Bar", "address": "322 N Higgins Ave, Missoula, MT", "color": "purple"},
            {"name": "University of Montana", "address": "32 Campus Dr, Missoula, MT", "color": "green"},
            {"name": "Missoula Art Museum", "address": "335 N Pattee St, Missoula, MT", "color": "red"}
        ]
    },
    
    "lucile_id": {
        "name": "Lucile, Idaho - Steelhead Lodge Area",
        "accommodation": "Steelhead Lodge",
        "accommodation_address": "Lucile, ID 83542",
        "points_of_interest": [
            {"name": "Salmon River Access", "address": "Salmon River, Lucile, ID", "color": "blue"},
            {"name": "Steelhead Lodge Marina", "address": "Lucile, ID", "color": "red"},
            {"name": "River Canyon Overlook", "address": "Salmon River Canyon, Lucile, ID", "color": "green"},
            {"name": "Fishing Guide Services", "address": "Lucile, ID", "color": "purple"},
            {"name": "Historic Mining Sites", "address": "Salmon River Canyon, ID", "color": "orange"}
        ]
    },
    
    "orcas_island_wa": {
        "name": "Orcas Island - Eastsound Area",
        "accommodation": "Round House Suite, Rosario Village",
        "accommodation_address": "1400 Rosario Rd, Eastsound, WA 98245",
        "points_of_interest": [
            {"name": "Rosario Village Marina", "address": "Rosario Village, Eastsound, WA", "color": "blue"},
            {"name": "Eastsound Village Center", "address": "Eastsound, WA", "color": "red"},
            {"name": "Kayak Launch Point", "address": "Rosario Village, WA", "color": "green"},
            {"name": "Orcas Island Winery", "address": "Eastsound, WA", "color": "purple"},
            {"name": "Olga Orca Viewing", "address": "Olga, Orcas Island, WA", "color": "orange"}
        ]
    },
    
    "san_juan_island_wa": {
        "name": "San Juan Island - Friday Harbor",
        "accommodation": "Friday Harbor area",
        "accommodation_address": "Friday Harbor, WA 98250",
        "points_of_interest": [
            {"name": "Friday Harbor Downtown", "address": "Friday Harbor, WA", "color": "red"},
            {"name": "The Whale Museum", "address": "62 1st St N, Friday Harbor, WA", "color": "purple"},
            {"name": "Ferry Terminal", "address": "Friday Harbor, WA", "color": "blue"},
            {"name": "Roche Harbor", "address": "Roche Harbor, WA", "color": "green"},
            {"name": "Lime Kiln Point Park", "address": "Westside Rd, Friday Harbor, WA", "color": "orange"}
        ]
    },
    
    "lopez_island_wa": {
        "name": "Lopez Island Village",
        "accommodation": "Lopez Village area",
        "accommodation_address": "Lopez Village, WA 98261",
        "points_of_interest": [
            {"name": "Chimera Gallery", "address": "Lopez Village, WA", "color": "purple"},
            {"name": "Lopez Island Pottery", "address": "Lopez Village, WA", "color": "red"},
            {"name": "Islands' Sounder Building", "address": "Lopez Village, WA", "color": "orange"},
            {"name": "Textile Arts Studios", "address": "Lopez Village, WA", "color": "green"},
            {"name": "Ferry Terminal", "address": "Lopez Island, WA", "color": "blue"}
        ]
    },
    
    "joseph_or": {
        "name": "Joseph, Oregon Town Center",
        "accommodation": "The Jennings Hotel",
        "accommodation_address": "100 Main St, Joseph, OR 97846", 
        "points_of_interest": [
            {"name": "Valley Bronze of Oregon", "address": "18 S Main St, Joseph, OR", "color": "red"},
            {"name": "Embers Brewhouse", "address": "204 N Main St, Joseph, OR", "color": "green"},
            {"name": "Main Street Historic District", "address": "Main St, Joseph, OR", "color": "purple"},
            {"name": "Lear's Main Street Grill", "address": "111 W Main St, Joseph, OR", "color": "orange"},
            {"name": "Town Park", "address": "Joseph, OR", "color": "blue"}
        ]
    },
    
    "lostine_oregon_town": {
        "name": "Lostine, Oregon Historic Town",
        "accommodation": "M. Crow & Co. General Store",
        "accommodation_address": "Main St, Lostine, OR 97857",
        "points_of_interest": [
            {"name": "M. Crow & Co. General Store", "address": "Main St, Lostine, OR", "color": "red"},
            {"name": "Lostine Tavern", "address": "Main St, Lostine, OR", "color": "green"},
            {"name": "Historic Methodist Church", "address": "Main St, Lostine, OR", "color": "purple"},
            {"name": "Lostine River Access", "address": "Lostine River, Lostine, OR", "color": "blue"},
            {"name": "Historic Main Street Buildings", "address": "Main St, Lostine, OR", "color": "orange"},
            {"name": "Eagle Cap Wilderness Access", "address": "Lostine Canyon Rd, Lostine, OR", "color": "yellow"},
            {"name": "Working Cattle Ranches", "address": "Lostine Valley, OR", "color": "brown"},
            {"name": "Wallowa National Forest Access", "address": "Lostine, OR", "color": "darkgreen"}
        ]
    },
    
    "walla_walla_wa": {
        "name": "Downtown Walla Walla, Washington",
        "accommodation": "Eritage Resort",
        "accommodation_address": "1000 N 2nd Ave, Walla Walla, WA 99362",
        "points_of_interest": [
            {"name": "Downtown Historic District", "address": "Main St, Walla Walla, WA", "color": "red"},
            {"name": "Farmers Market", "address": "4th Ave & Main St, Walla Walla, WA", "color": "green"},
            {"name": "Colville Street Patisserie", "address": "1425 Plaza Way, Walla Walla, WA", "color": "orange"},
            {"name": "Pioneer Park", "address": "730 Rose St, Walla Walla, WA", "color": "blue"},
            {"name": "Wine Tasting Rooms", "address": "Main St, Walla Walla, WA", "color": "purple"}
        ]
    },
    
    "cascade_locks_or": {
        "name": "Cascade Locks, Oregon",
        "accommodation": "Under Canvas Columbia River",
        "accommodation_address": "1681 Little White Salmon Rd, Cook, WA 98605",
        "points_of_interest": [
            {"name": "Bridge of the Gods", "address": "Cascade Locks, OR", "color": "red"},
            {"name": "Thunder Island Brewing", "address": "515 WaNaPa St, Cascade Locks, OR", "color": "green"},
            {"name": "Historic Locks", "address": "Cascade Locks, OR", "color": "purple"},
            {"name": "Marine Park", "address": "355 WaNaPa St, Cascade Locks, OR", "color": "blue"},
            {"name": "Columbia River Trail", "address": "Cascade Locks, OR", "color": "orange"}
        ]
    },
    
    "seattle_wa": {
        "name": "Downtown Seattle, Washington",
        "accommodation": "The Fairmont Olympic Seattle", 
        "accommodation_address": "411 University St, Seattle, WA 98101",
        "points_of_interest": [
            {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "color": "red"},
            {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "color": "purple"},
            {"name": "Pioneer Square", "address": "600 1st Ave, Seattle, WA", "color": "orange"},
            {"name": "Waterfront Park", "address": "1401 Alaskan Way, Seattle, WA", "color": "blue"},
            {"name": "Grand Central Bakery", "address": "214 1st Ave S, Seattle, WA", "color": "green"}
        ]
    }
}

def create_static_map(town_key, town_data):
    """Create a static PNG map using Google Maps Static API."""
    print(f"Creating static map for {town_data['name']}...")
    
    # Geocode the accommodation
    hotel_coords = geocode_with_retry(town_data['accommodation_address'])
    
    if not hotel_coords:
        print(f"Could not geocode accommodation for {town_data['name']}")
        return None
    
    # Start building the Static Maps API URL
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Map parameters
    params = {
        'center': f"{hotel_coords[0]},{hotel_coords[1]}",
        'zoom': '15',
        'size': '800x600',
        'maptype': 'terrain',  # terrain mode for better topographical visibility
        'key': GOOGLE_MAPS_API_KEY,
        'format': 'png',
        'scale': '2'  # High resolution
    }
    
    # Add hotel marker (large red marker with H)
    markers = [f"color:red|size:large|label:H|{hotel_coords[0]},{hotel_coords[1]}"]
    
    # Add points of interest markers with proper colors
    for i, poi in enumerate(town_data['points_of_interest']):
        poi_coords = geocode_with_retry(poi['address'])
        if poi_coords:
            # Use letters A-Z for POI markers
            label = chr(65 + i) if i < 26 else str(i-25)
            color = poi.get('color', 'blue')
            markers.append(f"color:{color}|size:mid|label:{label}|{poi_coords[0]},{poi_coords[1]}")
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
            filename = f"images/{town_key}_walking_map.png"
            with open(filename, 'wb') as f:
                f.write(response.content)
            print(f"Saved static map: {filename}")
            
            # Also create a legend text file
            legend_filename = f"images/{town_key}_walking_map_legend.txt"
            with open(legend_filename, 'w') as f:
                f.write(f"{town_data['name']}\n")
                f.write(f"Hotel: {town_data['accommodation']} (Red H)\n\n")
                f.write("Points of Interest:\n")
                for i, poi in enumerate(town_data['points_of_interest']):
                    label = chr(65 + i) if i < 26 else str(i-25)
                    f.write(f"{label} - {poi['name']}\n")
            
            return filename
        else:
            print(f"Error downloading map: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error creating static map: {e}")
        return None

def main():
    """Generate all static town walking maps."""
    print("Generating static PNG walking maps for all towns...")
    
    for town_key, town_data in towns_data.items():
        create_static_map(town_key, town_data)
        time.sleep(1)  # Rate limiting between API calls
    
    print("All static walking maps generated!")

if __name__ == "__main__":
    main() 