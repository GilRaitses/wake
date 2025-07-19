#!/usr/bin/env python3
"""
Generate custom annotated walking maps with colored overlays
Uses matplotlib with Google Static Maps as background
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Rectangle
import requests
import numpy as np
import googlemaps
import time
import os
from PIL import Image
from io import BytesIO

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Google Maps API key
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
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

# Color mapping to match booking booklet
color_map = {
    'red': '#FF0000',
    'orange': '#FFA500', 
    'green': '#008000',
    'blue': '#0000FF',
    'purple': '#800080'
}

# Enhanced town data
towns_data = {
    "bozeman_mt": {
        "name": "Bozeman, Montana",
        "accommodation": {"name": "Kimpton Armory Hotel", "address": "24 W Mendenhall St, Bozeman, MT 59715"},
        "regions": [
            {"name": "Main Street Historic District", "center": "Main St & Mendenhall St, Bozeman, MT", "color": "red", "size": 0.008}
        ],
        "points_of_interest": [
            {"name": "Wild Crumb Bakery", "address": "1424 W Main St, Bozeman, MT", "color": "orange"},
            {"name": "Blackbird Kitchen", "address": "200 W Main St, Bozeman, MT", "color": "green"},
            {"name": "Montana Ale Works", "address": "611 E Main St, Bozeman, MT", "color": "blue"},
            {"name": "Bogert Park", "address": "325 S Church Ave, Bozeman, MT", "color": "purple"}
        ]
    },
    
    "missoula_mt": {
        "name": "Missoula, Montana",
        "accommodation": {"name": "AC Hotel Missoula Downtown", "address": "200 S Pattee St, Missoula, MT 59802"},
        "regions": [],
        "points_of_interest": [
            {"name": "Clark Fork Riverfront Trail", "address": "Caras Park, Missoula, MT", "color": "blue"},
            {"name": "Le Petit Outre", "address": "129 W Front St, Missoula, MT", "color": "orange"},
            {"name": "Plonk Wine Bar", "address": "322 N Higgins Ave, Missoula, MT", "color": "purple"},
            {"name": "University of Montana", "address": "32 Campus Dr, Missoula, MT", "color": "green"},
            {"name": "Missoula Art Museum", "address": "335 N Pattee St, Missoula, MT", "color": "red"}
        ]
    },
    
    "mccall_id": {
        "name": "McCall, Idaho",
        "accommodation": {"name": "LA CASA ITALIANA Condo", "address": "Downtown McCall, ID 83638"},
        "regions": [
            {"name": "Downtown McCall", "center": "3rd St & Lake St, McCall, ID", "color": "red", "size": 0.005}
        ],
        "points_of_interest": [
            {"name": "Payette Lake Beach", "address": "Payette Lake, McCall, ID", "color": "blue"},
            {"name": "Smoky Mountain Pizzeria", "address": "815 N 3rd St, McCall, ID", "color": "green"},
            {"name": "Legacy Park", "address": "Legacy Park, McCall, ID", "color": "purple"},
            {"name": "McCall Activity Barn", "address": "1300 E Lake St, McCall, ID", "color": "orange"}
        ]
    },
    
    "joseph_or": {
        "name": "Joseph, Oregon",
        "accommodation": {"name": "The Jennings Hotel", "address": "100 Main St, Joseph, OR 97846"},
        "regions": [
            {"name": "Main Street Historic District", "center": "Main St & Russell St, Joseph, OR", "color": "purple", "size": 0.003}
        ],
        "points_of_interest": [
            {"name": "Valley Bronze of Oregon", "address": "18 S Main St, Joseph, OR", "color": "red"},
            {"name": "Embers Brewhouse", "address": "204 N Main St, Joseph, OR", "color": "green"},
            {"name": "Lear's Main Street Grill", "address": "111 W Main St, Joseph, OR", "color": "orange"},
            {"name": "Town Park", "address": "Joseph, OR", "color": "blue"}
        ]
    },
    
    "lostine_oregon_town": {
        "name": "Lostine, Oregon",
        "accommodation": {"name": "Day Trip from Joseph", "address": "Main St, Lostine, OR 97857"},
        "regions": [],
        "points_of_interest": [
            {"name": "M. Crow & Co. General Store", "address": "Main St, Lostine, OR", "color": "red"},
            {"name": "Lostine Tavern", "address": "Main St, Lostine, OR", "color": "green"}
        ]
    },
    
    "walla_walla_wa": {
        "name": "Walla Walla, Washington",
        "accommodation": {"name": "Eritage Resort", "address": "1319 Bergevin Springs Road, Walla Walla, WA 99362"},
        "regions": [
            {"name": "Downtown Historic District", "center": "Main St & 2nd Ave, Walla Walla, WA", "color": "red", "size": 0.006}
        ],
        "points_of_interest": [
            {"name": "Farmers Market", "address": "4th Ave & Main St, Walla Walla, WA", "color": "green"},
            {"name": "Colville Street Patisserie", "address": "1425 Plaza Way, Walla Walla, WA", "color": "orange"},
            {"name": "Pioneer Park", "address": "730 Rose St, Walla Walla, WA", "color": "blue"},
            {"name": "Wine Tasting Rooms", "address": "Main St, Walla Walla, WA", "color": "purple"}
        ]
    },
    
    "cascade_locks_or": {
        "name": "Cascade Locks, Oregon",
        "accommodation": {"name": "Under Canvas Columbia River", "address": "1681 Little White Salmon Rd, Cook, WA 98605"},
        "regions": [],
        "points_of_interest": [
            {"name": "Bridge of the Gods", "address": "Cascade Locks, OR", "color": "red"},
            {"name": "Thunder Island Brewing", "address": "515 WaNaPa St, Cascade Locks, OR", "color": "green"},
            {"name": "Historic Locks and Dam", "address": "Cascade Locks, OR", "color": "purple"},
            {"name": "Marine Park", "address": "355 WaNaPa St, Cascade Locks, OR", "color": "blue"},
            {"name": "Columbia River Trail", "address": "Cascade Locks, OR", "color": "orange"}
        ]
    },
    
    "seattle_wa": {
        "name": "Seattle, Washington",
        "accommodation": {"name": "The Fairmont Olympic Seattle", "address": "411 University St, Seattle, WA 98101"},
        "regions": [
            {"name": "Pioneer Square", "center": "600 1st Ave, Seattle, WA", "color": "orange", "size": 0.004}
        ],
        "points_of_interest": [
            {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "color": "red"},
            {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "color": "purple"},
            {"name": "Waterfront Park", "address": "1401 Alaskan Way, Seattle, WA", "color": "blue"},
            {"name": "Grand Central Bakery", "address": "214 1st Ave S, Seattle, WA", "color": "green"}
        ]
    }
}

def create_custom_annotated_map(town_key, town_data):
    """Create a custom annotated map with colored overlays."""
    print(f"Creating custom annotated map for {town_data['name']}...")
    
    # Geocode the accommodation
    hotel_coords = geocode_with_retry(town_data['accommodation']['address'])
    if not hotel_coords:
        print(f"Could not geocode accommodation for {town_data['name']}")
        return None
    
    # Collect all coordinates to determine bounds
    all_coords = [hotel_coords]
    poi_data = []
    
    for poi in town_data['points_of_interest']:
        coords = geocode_with_retry(poi['address'])
        if coords:
            poi_data.append((coords, poi['color'], poi['name']))
            all_coords.append(coords)
        time.sleep(0.2)  # Rate limiting
    
    # Get region coordinates
    region_data = []
    for region in town_data['regions']:
        coords = geocode_with_retry(region['center'])
        if coords:
            region_data.append((coords, region['color'], region['name'], region['size']))
            all_coords.append(coords)
        time.sleep(0.2)
    
    if not all_coords:
        print(f"No coordinates found for {town_data['name']}")
        return None
    
    # Calculate bounds
    lats, lons = zip(*all_coords)
    center_lat, center_lon = np.mean(lats), np.mean(lons)
    lat_range = max(lats) - min(lats)
    lon_range = max(lons) - min(lons)
    
    # Add padding
    padding = max(lat_range, lon_range) * 0.3
    
    # Get Google Static Map as background
    zoom = 15
    size = "800x600"
    maptype = "roadmap"
    
    base_url = "https://maps.googleapis.com/maps/api/staticmap"
    params = {
        'center': f"{center_lat},{center_lon}",
        'zoom': zoom,
        'size': size,
        'maptype': maptype,
        'key': GOOGLE_MAPS_API_KEY,
        'style': 'feature:poi|visibility:simplified',  # Simplify POI markers
    }
    
    # Build URL
    url = base_url + "?" + "&".join([f"{k}={v}" for k, v in params.items()])
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Load the background map
            background_img = Image.open(BytesIO(response.content))
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(12, 9))
            
            # Display background map
            ax.imshow(background_img, extent=(
                center_lon - lon_range/2 - padding,
                center_lon + lon_range/2 + padding,
                center_lat - lat_range/2 - padding,
                center_lat + lat_range/2 + padding
            ))
            
            # Add custom overlays
            
            # 1. Add regions (shaded areas)
            for coords, color, name, size in region_data:
                lat, lon = coords
                rect = Rectangle(
                    (lon - size/2, lat - size/2), size, size,
                    facecolor=color_map[color], alpha=0.3, 
                    edgecolor='black', linewidth=2
                )
                ax.add_patch(rect)
            
            # 2. Add hotel (red square)
            hotel_lat, hotel_lon = hotel_coords
            hotel_square = Rectangle(
                (hotel_lon - 0.001, hotel_lat - 0.001), 0.002, 0.002,
                facecolor='darkred', edgecolor='black', linewidth=2
            )
            ax.add_patch(hotel_square)
            
            # 3. Add POIs (colored circles)
            for (lat, lon), color, name in poi_data:
                circle = Circle(
                    (lon, lat), 0.002,
                    facecolor=color_map[color], alpha=0.7,
                    edgecolor='black', linewidth=1.5
                )
                ax.add_patch(circle)
            
            # Set proper aspect ratio and limits
            ax.set_xlim(center_lon - lon_range/2 - padding, center_lon + lon_range/2 + padding)
            ax.set_ylim(center_lat - lat_range/2 - padding, center_lat + lat_range/2 + padding)
            ax.set_aspect('equal')
            
            # Remove axes
            ax.set_xticks([])
            ax.set_yticks([])
            
            # Add title
            ax.set_title(f'{town_data["name"]} Walking Area', 
                        fontsize=16, fontweight='bold', pad=20)
            
            # Save the map
            filename = f"images/{town_key}_walking_map.png"
            plt.tight_layout()
            plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
            plt.close()
            
            print(f"Saved custom annotated map: {filename}")
            return filename
            
    except Exception as e:
        print(f"Error creating map for {town_data['name']}: {e}")
        return None

def main():
    """Generate all custom annotated walking maps."""
    print("Generating custom annotated walking maps...")
    
    for town_key, town_data in towns_data.items():
        create_custom_annotated_map(town_key, town_data)
        time.sleep(1)  # Rate limiting between API calls
    
    print("All custom annotated walking maps generated!")

if __name__ == "__main__":
    main() 