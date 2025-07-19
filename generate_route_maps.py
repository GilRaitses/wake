#!/usr/bin/env python3
"""
Generate route maps with driving times for the Pacific Northwest trip itinerary.
Uses Google Maps API for accurate route information and map generation.
"""

import googlemaps
import json
import time
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import requests
from urllib.parse import urlencode
import base64

# Google Maps API key - load from environment variable for security
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY')

if not GOOGLE_MAPS_API_KEY:
    print("Error: GOOGLE_MAPS_API_KEY environment variable not set")
    print("Please set your API key: export GOOGLE_MAPS_API_KEY='your_api_key_here'")
    exit(1)

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Initialize Google Maps client
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

# Trip waypoints with dates
waypoints = [
    {"name": "Bozeman, MT", "date": "Aug 3-4", "coords": None},
    {"name": "Missoula, MT", "date": "Aug 5", "coords": None},
    {"name": "Jerry Johnson Hot Springs, ID", "date": "Aug 6", "coords": None},
    {"name": "Lucile, ID", "date": "Aug 7-8", "coords": None},
    {"name": "Joseph, OR", "date": "Aug 9", "coords": None},
    {"name": "Walla Walla, WA", "date": "Aug 10", "coords": None},
    {"name": "Columbia River Gorge, WA", "date": "Aug 11", "coords": None},
    {"name": "Mount Rainier National Park, WA", "date": "Aug 12", "coords": None},
    {"name": "North Bend, WA", "date": "Aug 12", "coords": None},
    {"name": "San Juan Islands, WA", "date": "Aug 12-14", "coords": None}
]

# Special route segments
special_routes = [
    {
        "name": "Mount Rainier Scenic Route",
        "origin": "Under Canvas White Salmon, WA",
        "destination": "North Bend, WA",
        "waypoints": ["Mount Rainier National Park, WA"],
        "description": "Scenic mountain route via Mount Rainier National Park"
    },
    {
        "name": "Hells Canyon Scenic Route", 
        "origin": "Lucile, ID",
        "destination": "Joseph, OR",
        "waypoints": ["Hells Canyon National Recreation Area, ID"],
        "description": "Scenic canyon route via Hells Canyon overlooks"
    }
]

def get_coordinates_google(location):
    """Get coordinates for a location using Google Maps Geocoding API."""
    try:
        geocode_result = gmaps.geocode(location)
        if geocode_result:
            location_data = geocode_result[0]['geometry']['location']
            return (location_data['lat'], location_data['lng'])
        return None
    except Exception as e:
        print(f"Error geocoding {location}: {e}")
        return None

def get_driving_directions(origin, destination):
    """Get driving directions between two points using Google Maps Directions API."""
    try:
        directions_result = gmaps.directions(
            origin,
            destination,
            mode="driving",
            departure_time=datetime.now(),
            traffic_model="best_guess"
        )
        
        if directions_result:
            route = directions_result[0]['legs'][0]
            distance = route['distance']['value'] / 1000  # Convert to km
            duration = route['duration']['value'] / 3600  # Convert to hours
            duration_text = route['duration']['text']
            distance_text = route['distance']['text']
            
            # Get the encoded polyline for the route
            polyline = directions_result[0]['overview_polyline']['points']
            
            return {
                'distance_km': distance,
                'distance_miles': distance * 0.621371,
                'duration_hours': duration,
                'duration_text': duration_text,
                'distance_text': distance_text,
                'polyline': polyline
            }
        return None
    except Exception as e:
        print(f"Error getting directions from {origin} to {destination}: {e}")
        return None

def generate_static_map_with_route(origin, destination, filename="route_map.png"):
    """Generate a static map with actual road route between two points."""
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Get directions to get the route polyline
    directions = get_driving_directions(origin['name'], destination['name'])
    
    if not directions:
        print(f"Could not get directions from {origin['name']} to {destination['name']}")
        return False
    
    # Map parameters
    params = {
        'size': '800x600',
        'maptype': 'roadmap',
        'key': GOOGLE_MAPS_API_KEY,
        'format': 'png',
        'scale': 2
    }
    
    # Add markers for origin and destination
    markers = []
    if origin['coords']:
        lat, lng = origin['coords']
        markers.append(f"color:green|label:A|{lat},{lng}")
    
    if destination['coords']:
        lat, lng = destination['coords']
        markers.append(f"color:red|label:B|{lat},{lng}")
    
    if markers:
        params['markers'] = markers
    
    # Add the actual road route using the encoded polyline
    if directions['polyline']:
        params['path'] = f"enc:{directions['polyline']}"
    
    # Build URL
    url = base_url + urlencode(params, doseq=True)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'images/{filename}', 'wb') as f:
                f.write(response.content)
            print(f"Route map saved as images/{filename}")
            return True
        else:
            print(f"Error generating route map: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error generating route map: {e}")
        return False

def generate_static_map(waypoints_with_coords, filename="route_map.png"):
    """Generate a static map image using Google Maps Static API with actual routes."""
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Map parameters
    params = {
        'size': '800x600',
        'maptype': 'roadmap',
        'key': GOOGLE_MAPS_API_KEY,
        'format': 'png',
        'scale': 2
    }
    
    # Add markers for each waypoint
    markers = []
    for i, waypoint in enumerate(waypoints_with_coords):
        if waypoint['coords']:
            lat, lng = waypoint['coords']
            # Use different colored markers for each location
            colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'darkred', 'darkblue']
            color = colors[i % len(colors)]
            markers.append(f"color:{color}|label:{i+1}|{lat},{lng}")
    
    if markers:
        params['markers'] = markers
    
    # Get route polylines for the entire journey
    all_polylines = []
    for i in range(len(waypoints_with_coords) - 1):
        origin = waypoints_with_coords[i]
        destination = waypoints_with_coords[i+1]
        
        if origin['coords'] and destination['coords']:
            directions = get_driving_directions(origin['name'], destination['name'])
            if directions and directions['polyline']:
                all_polylines.append(directions['polyline'])
    
    # Add all route segments as paths
    if all_polylines:
        for polyline in all_polylines:
            params['path'] = f"color:0x0000ff|weight:3|enc:{polyline}"
    
    # Build URL
    url = base_url + urlencode(params, doseq=True)
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'images/{filename}', 'wb') as f:
                f.write(response.content)
            print(f"Static map saved as images/{filename}")
            return True
        else:
            print(f"Error generating static map: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error generating static map: {e}")
        return False

def generate_route_overview_map():
    """Generate an overview map showing the entire route."""
    # Get coordinates for all waypoints
    for waypoint in waypoints:
        coords = get_coordinates_google(waypoint["name"])
        waypoint["coords"] = coords
        if coords:
            print(f"✓ {waypoint['name']}: {coords}")
        else:
            print(f"✗ Failed to geocode: {waypoint['name']}")
        time.sleep(0.1)  # Be respectful to the API
    
    # Generate static map with actual routes
    generate_static_map(waypoints, "route_overview_map.png")
    
    return waypoints

def generate_driving_times_table():
    """Generate a table with driving times and distances using Google Maps."""
    print("\n" + "="*80)
    print("PACIFIC NORTHWEST TRIP - DRIVING TIMES & DISTANCES (Google Maps)")
    print("="*80)
    
    route_info = []
    
    for i in range(len(waypoints) - 1):
        origin = waypoints[i]["name"]
        destination = waypoints[i+1]["name"]
        
        print(f"Getting directions: {origin} → {destination}")
        
        directions = get_driving_directions(origin, destination)
        
        if directions:
            route_info.append({
                "from": origin,
                "to": destination,
                "distance_km": directions['distance_km'],
                "distance_miles": directions['distance_miles'],
                "distance_text": directions['distance_text'],
                "driving_time_hours": directions['duration_hours'],
                "driving_time_text": directions['duration_text']
            })
            
            print(f"  ✓ {directions['distance_text']} - {directions['duration_text']}")
        else:
            print(f"  ✗ Failed to get directions")
        
        time.sleep(0.1)  # Be respectful to the API
    
    # Print formatted table
    print(f"\n{'From':<30} {'To':<30} {'Distance':<12} {'Time':<12}")
    print("-" * 84)
    
    for route in route_info:
        print(f"{route['from']:<30} {route['to']:<30} {route['distance_text']:<12} {route['driving_time_text']:<12}")
    
    # Save route info to file for embedding in document
    with open('images/route_info.json', 'w') as f:
        json.dump(route_info, f, indent=2)
    
    return route_info

def generate_individual_leg_maps():
    """Generate individual static maps for each leg of the journey with actual routes."""
    print("\nGenerating individual leg maps with actual road routes...")
    
    for i in range(len(waypoints) - 1):
        origin = waypoints[i]
        destination = waypoints[i+1]
        
        if origin['coords'] and destination['coords']:
            filename = f"leg_{i+1}_{origin['name'].replace(' ', '_').replace(',', '')}_to_{destination['name'].replace(' ', '_').replace(',', '')}.png"
            
            # Generate static map for this leg with actual route
            generate_static_map_with_route(origin, destination, filename)
            print(f"  ✓ Generated: {filename}")

def create_elevation_profile():
    """Create elevation profile using more accurate data."""
    # More precise elevations for key points
    elevations = {
        "Bozeman, MT": 4820,
        "Missoula, MT": 3209,
        "Jerry Johnson Hot Springs, ID": 3200,
        "Lucile, ID": 5021,
        "Joseph, OR": 4372,
        "Walla Walla, WA": 1200,
        "Columbia River Gorge, WA": 200,
        "Mount Rainier National Park, WA": 175,
        "North Bend, WA": 175,
        "San Juan Islands, WA": 175
    }
    
    locations = list(elevations.keys())
    heights = list(elevations.values())
    
    plt.figure(figsize=(14, 8))
    plt.plot(range(len(locations)), heights, marker='o', linewidth=3, markersize=10, 
             color='#2E86AB', markerfacecolor='#A23B72', markeredgecolor='#F18F01')
    plt.title('Elevation Profile - Pacific Northwest Adventure Route', fontsize=18, fontweight='bold')
    plt.xlabel('Route Stops', fontsize=14)
    plt.ylabel('Elevation (feet)', fontsize=14)
    plt.xticks(range(len(locations)), [loc.split(',')[0] for loc in locations], rotation=45)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    
    # Add elevation annotations
    for i, (location, height) in enumerate(zip(locations, heights)):
        plt.annotate(f'{height:,} ft', (i, height), textcoords="offset points", 
                    xytext=(0,10), ha='center', fontsize=10)
    
    plt.savefig('images/elevation_profile.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Enhanced elevation profile saved as images/elevation_profile.png")

def main():
    """Main function to generate all route maps and data using Google Maps."""
    print("🗺️  Generating route maps using Google Maps API...")
    print(f"API Key: {GOOGLE_MAPS_API_KEY[:10]}...")
    
    # Generate route overview map with coordinates
    waypoints_with_coords = generate_route_overview_map()
    
    # Generate driving times table using Google Maps
    route_info = generate_driving_times_table()
    
    # Generate individual leg maps with actual routes
    generate_individual_leg_maps()
    
    # Create elevation profile
    create_elevation_profile()
    
    print(f"\n🎉 Files generated:")
    print(f"📍 Route overview map: images/route_overview_map.png")
    print(f"📊 Route data: images/route_info.json")
    print(f"📈 Elevation profile: images/elevation_profile.png")
    print(f"🛣️  Individual leg maps: images/leg_*.png")
    
    if route_info:
        total_distance = sum(r['distance_miles'] for r in route_info)
        total_time = sum(r['driving_time_hours'] for r in route_info)
        print(f"\n📏 Total trip distance: {total_distance:.0f} miles")
        print(f"⏱️  Total driving time: {total_time:.1f} hours")
        print(f"🚗 Average daily driving: {total_time/len(route_info):.1f} hours")

if __name__ == "__main__":
    main() 