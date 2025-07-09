#!/usr/bin/env python3
"""
Generate detailed walking vicinity maps for every town/city on the trip
Shows points of interest within 30 minutes walking distance of each accommodation
"""

import folium
import json
import os
import googlemaps
import time

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

# All town data for walking vicinity maps
towns_data = {
    "bozeman_mt": {
        "name": "Downtown Bozeman, Montana",
        "accommodation": "Kimpton Armory Hotel",
        "accommodation_address": "24 W Mendenhall St, Bozeman, MT 59715",
        "walking_radius": "30 minutes walking from hotel",
        "points_of_interest": [
            {"name": "Main Street Historic District", "address": "Main St, Bozeman, MT", "type": "historic", "description": "Historic downtown area with shops and restaurants"},
            {"name": "Bozeman Public Library", "address": "626 E Main St, Bozeman, MT", "type": "culture", "description": "Beautiful Carnegie library building"},
            {"name": "Gallatin History Museum", "address": "317 W Main St, Bozeman, MT", "type": "museum", "description": "Local history and culture exhibits"},
            {"name": "Downtown Bozeman Farmers Market", "address": "27 E Main St, Bozeman, MT", "type": "market", "description": "Saturday farmers market (seasonal)"},
            {"name": "Wild Crumb Bakery & Cafe", "address": "1424 W Main St, Bozeman, MT", "type": "bakery", "description": "European-style artisan breads"},
            {"name": "Blackbird Kitchen", "address": "200 W Main St, Bozeman, MT", "type": "restaurant", "description": "Wood-fired Argentine-style asado"},
            {"name": "Montana Ale Works", "address": "611 E Main St, Bozeman, MT", "type": "brewery", "description": "Local brewery in historic railroad building"},
            {"name": "Bogert Park", "address": "325 S Church Ave, Bozeman, MT", "type": "park", "description": "Riverside park with walking trails"},
            {"name": "Peets Hill/Burke Park", "address": "Burke Park, Bozeman, MT", "type": "nature", "description": "Hill with city views and walking trails"}
        ]
    },
    
    "missoula_mt": {
        "name": "Downtown Missoula, Montana", 
        "accommodation": "AC Hotel Missoula Downtown",
        "accommodation_address": "200 S Pattee St, Missoula, MT 59802",
        "walking_radius": "30 minutes walking from hotel",
        "points_of_interest": [
            {"name": "Clark Fork Riverfront Trail", "address": "Caras Park, Missoula, MT", "type": "nature", "description": "Scenic walking/biking trail along river"},
            {"name": "Caras Park", "address": "123 N Orange St, Missoula, MT", "type": "park", "description": "Riverfront park with carousel and events"},
            {"name": "Higgins Avenue Bridge", "address": "Higgins Ave, Missoula, MT", "type": "landmark", "description": "Historic bridge with river views"},
            {"name": "University of Montana Campus", "address": "32 Campus Dr, Missoula, MT", "type": "campus", "description": "Beautiful tree-lined campus"},
            {"name": "Le Petit Outre", "address": "129 W Front St, Missoula, MT", "type": "bakery", "description": "French-style pastries and breads"},
            {"name": "Bernice's Bakery", "address": "190 S 3rd St W, Missoula, MT", "type": "bakery", "description": "Traditional American bakery"},
            {"name": "Plonk Wine Bar", "address": "322 N Higgins Ave, Missoula, MT", "type": "wine_bar", "description": "Argentine-inspired wine bar"},
            {"name": "Missoula Art Museum", "address": "335 N Pattee St, Missoula, MT", "type": "museum", "description": "Contemporary art exhibitions"},
            {"name": "Downtown Historic District", "address": "Higgins Ave, Missoula, MT", "type": "historic", "description": "Historic buildings and shops"}
        ]
    },
    
    "mccall_id": {
        "name": "McCall, Idaho Town Center",
        "accommodation": "Shore Lodge", 
        "accommodation_address": "501 W Lake St, McCall, ID 83638",
        "walking_radius": "30 minutes walking from Shore Lodge",
        "points_of_interest": [
            {"name": "Payette Lake Beach", "address": "Payette Lake, McCall, ID", "type": "nature", "description": "Beautiful mountain lake with beach access"},
            {"name": "McCall City Beach", "address": "1300 E Lake St, McCall, ID", "type": "beach", "description": "Public beach with swimming and activities"},
            {"name": "Legacy Park", "address": "Legacy Park, McCall, ID", "type": "park", "description": "Lakefront park with walking paths"},
            {"name": "Downtown McCall", "address": "3rd St, McCall, ID", "type": "shopping", "description": "Mountain town shops and restaurants"},
            {"name": "Smoky Mountain Pizzeria", "address": "815 N 3rd St, McCall, ID", "type": "restaurant", "description": "Wood-fired pizza and smoked meats"},
            {"name": "Alpine Bagel Company", "address": "1101 N 3rd St, McCall, ID", "type": "bakery", "description": "Fresh bagels and mountain bakery goods"},
            {"name": "McCall Fish Hatchery", "address": "204 Mather Rd, McCall, ID", "type": "attraction", "description": "Educational fish hatchery tours"},
            {"name": "Ponderosa State Park", "address": "1920 Davis Ave, McCall, ID", "type": "park", "description": "State park with hiking trails (nearby)"},
            {"name": "McCall Activity Barn", "address": "1300 E Lake St, McCall, ID", "type": "activity", "description": "Seasonal activities and equipment rental"}
        ]
    },
    
    "joseph_or": {
        "name": "Joseph, Oregon Town Center",
        "accommodation": "The Jennings Hotel",
        "accommodation_address": "100 Main St, Joseph, OR 97846", 
        "walking_radius": "30 minutes walking from Jennings Hotel",
        "points_of_interest": [
            {"name": "Valley Bronze of Oregon", "address": "18 S Main St, Joseph, OR", "type": "art", "description": "Working bronze foundry with tours"},
            {"name": "Josephy Center for Arts & Culture", "address": "403 N Main St, Joseph, OR", "type": "culture", "description": "Local arts center and pottery classes"},
            {"name": "Main Street Historic District", "address": "Main St, Joseph, OR", "type": "historic", "description": "Historic western town atmosphere"},
            {"name": "Embers Brewhouse & Eatery", "address": "204 N Main St, Joseph, OR", "type": "restaurant", "description": "Local brewery with wood-fired pizza"},
            {"name": "Lear's Main Street Grill", "address": "111 W Main St, Joseph, OR", "type": "restaurant", "description": "Mountain BBQ and smoked meats"},
            {"name": "Joseph Branch Railhead", "address": "Joseph, OR", "type": "historic", "description": "Historic railroad remnants"},
            {"name": "Chief Joseph Monument", "address": "Joseph, OR", "type": "monument", "description": "Monument to Nez Perce leader"},
            {"name": "Town Park", "address": "Joseph, OR", "type": "park", "description": "Small town park for relaxation"},
            {"name": "Local Art Galleries", "address": "Main St, Joseph, OR", "type": "art", "description": "Various art galleries throughout downtown"}
        ]
    },
    
    "walla_walla_wa": {
        "name": "Downtown Walla Walla, Washington",
        "accommodation": "Eritage Resort",
        "accommodation_address": "1000 N 2nd Ave, Walla Walla, WA 99362",
        "walking_radius": "30 minutes walking from Eritage Resort", 
        "points_of_interest": [
            {"name": "Downtown Historic District", "address": "Main St, Walla Walla, WA", "type": "historic", "description": "Historic downtown with shops and restaurants"},
            {"name": "Walla Walla Farmers Market", "address": "4th Ave & Main St, Walla Walla, WA", "type": "market", "description": "Saturday farmers market"},
            {"name": "Colville Street Patisserie", "address": "1425 Plaza Way, Walla Walla, WA", "type": "bakery", "description": "French pastries and artisan breads"},
            {"name": "Bright's Candies & Bakery", "address": "226 E Main St, Walla Walla, WA", "type": "bakery", "description": "Traditional breads and candies"},
            {"name": "Saffron Mediterranean Kitchen", "address": "125 W Alder St, Walla Walla, WA", "type": "restaurant", "description": "Mediterranean cuisine with lamb specialties"},
            {"name": "Pioneer Park", "address": "730 Rose St, Walla Walla, WA", "type": "park", "description": "Large park with walking paths and aviary"},
            {"name": "Whitman College Campus", "address": "345 Boyer Ave, Walla Walla, WA", "type": "campus", "description": "Beautiful liberal arts college campus"},
            {"name": "Walla Walla Wine Tasting Rooms", "address": "Main St, Walla Walla, WA", "type": "winery", "description": "Multiple downtown tasting rooms"},
            {"name": "Carnegie Art Center", "address": "109 S 4th Ave, Walla Walla, WA", "type": "art", "description": "Community art center in historic building"}
        ]
    },
    
    "cascade_locks_or": {
        "name": "Cascade Locks, Oregon",
        "accommodation": "Under Canvas Columbia River",
        "accommodation_address": "1681 Little White Salmon Rd, Cook, WA 98605",
        "walking_radius": "Walking distance in Cascade Locks town",
        "points_of_interest": [
            {"name": "Bridge of the Gods", "address": "Cascade Locks, OR", "type": "landmark", "description": "Iconic steel bridge spanning Columbia River"},
            {"name": "Cascade Locks Marine Park", "address": "355 WaNaPa St, Cascade Locks, OR", "type": "park", "description": "Waterfront park with historic locks"},
            {"name": "Thunder Island Brewing", "address": "515 WaNaPa St, Cascade Locks, OR", "type": "brewery", "description": "Craft brewery with smoked meats"},
            {"name": "Historic Locks and Dam", "address": "Cascade Locks, OR", "type": "historic", "description": "Historic 1896 navigation locks"},
            {"name": "Cascade Locks Visitor Center", "address": "Cascade Locks, OR", "type": "info", "description": "Local information and exhibits"},
            {"name": "Port of Cascade Locks", "address": "355 WaNaPa St, Cascade Locks, OR", "type": "historic", "description": "Historic river port facilities"},
            {"name": "Bonneville Lock and Dam", "address": "70543 NE Herman Loop, Cascade Locks, OR", "type": "attraction", "description": "Modern dam with fish viewing (nearby)"},
            {"name": "Columbia River Walking Trail", "address": "Cascade Locks, OR", "type": "nature", "description": "Riverside walking paths"},
            {"name": "Cascade Locks Museum", "address": "Cascade Locks, OR", "type": "museum", "description": "Local history and river culture"}
        ]
    },
    
    "seattle_wa": {
        "name": "Downtown Seattle, Washington",
        "accommodation": "The Fairmont Olympic Seattle", 
        "accommodation_address": "411 University St, Seattle, WA 98101",
        "walking_radius": "30 minutes walking from Fairmont Olympic",
        "points_of_interest": [
            {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "type": "market", "description": "Iconic public market with vendors and food"},
            {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "type": "museum", "description": "Premier art museum downtown"},
            {"name": "Westlake Center", "address": "400 Pine St, Seattle, WA", "type": "shopping", "description": "Shopping center and transit hub"},
            {"name": "Seattle Central Library", "address": "1000 4th Ave, Seattle, WA", "type": "culture", "description": "Stunning modern architecture"},
            {"name": "Pioneer Square", "address": "600 1st Ave, Seattle, WA", "type": "historic", "description": "Historic district with underground tours"},
            {"name": "Waterfront Park", "address": "1401 Alaskan Way, Seattle, WA", "type": "park", "description": "Waterfront with pier and Puget Sound views"},
            {"name": "Grand Central Bakery", "address": "214 1st Ave S, Seattle, WA", "type": "bakery", "description": "Artisan sourdough and breads"},
            {"name": "Matt's in the Market", "address": "94 Pike St, Seattle, WA", "type": "restaurant", "description": "Seafood restaurant overlooking market"},
            {"name": "Elliott Bay Waterfront", "address": "Alaskan Way, Seattle, WA", "type": "nature", "description": "Scenic waterfront walking area"},
            {"name": "Benaroya Hall", "address": "200 University St, Seattle, WA", "type": "culture", "description": "Seattle Symphony concert hall"},
            {"name": "Olympic Sculpture Park", "address": "2901 Western Ave, Seattle, WA", "type": "art", "description": "Outdoor sculpture park by water"}
        ]
    }
}

def create_town_map(town_key, town_data):
    """Create a walking vicinity map for a specific town."""
    print(f"Creating walking map for {town_data['name']}...")
    
    # Geocode the accommodation
    hotel_coords = geocode_with_retry(town_data['accommodation_address'])
    
    if not hotel_coords:
        print(f"Could not geocode accommodation for {town_data['name']}")
        return None
    
    # Create map centered on the accommodation with Google Maps satellite imagery
    m = folium.Map(
        location=hotel_coords,
        zoom_start=16,  # Higher zoom for walking vicinity
        tiles=None  # No default tiles, we'll add custom ones
    )
    
    # Add Google satellite layer as base
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add Google hybrid (satellite + roads) overlay
    folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Hybrid',
        overlay=False,
        control=True
    ).add_to(m)
    
    # Add accommodation marker (distinctive red house)
    folium.Marker(
        hotel_coords,
        popup=f"<b>{town_data['accommodation']}</b><br>{town_data['accommodation_address']}<br><b>Your Hotel</b>",
        tooltip=f"🏨 {town_data['accommodation']}",
        icon=folium.Icon(color='red', icon='home', prefix='fa', icon_size=(20, 20))
    ).add_to(m)
    
    # Color coding for different types of points
    type_colors = {
        'restaurant': 'green',
        'bakery': 'orange', 
        'brewery': 'darkgreen',
        'wine_bar': 'purple',
        'winery': 'purple',
        'market': 'blue',
        'museum': 'darkblue',
        'art': 'cadetblue',
        'culture': 'darkblue',
        'historic': 'darkred',
        'park': 'lightgreen',
        'nature': 'lightgreen',
        'beach': 'lightblue',
        'shopping': 'pink',
        'campus': 'gray',
        'landmark': 'black',
        'monument': 'darkred',
        'attraction': 'blue',
        'activity': 'green',
        'info': 'gray',
        'default': 'gray'
    }
    
    # Add points of interest
    for poi in town_data['points_of_interest']:
        poi_coords = geocode_with_retry(poi['address'])
        if poi_coords:
            poi_type = poi.get('type', 'default')
            color = type_colors.get(poi_type, type_colors['default'])
            
            # Create icon based on type
            icon_mapping = {
                'restaurant': 'cutlery',
                'bakery': 'cutlery', 
                'brewery': 'beer',
                'wine_bar': 'glass',
                'winery': 'glass',
                'market': 'shopping-cart',
                'museum': 'university',
                'art': 'paint-brush',
                'culture': 'university',
                'historic': 'university',
                'park': 'tree',
                'nature': 'tree',
                'beach': 'sun-o',
                'shopping': 'shopping-bag',
                'campus': 'graduation-cap',
                'landmark': 'star',
                'monument': 'monument',
                'attraction': 'eye',
                'activity': 'bicycle',
                'info': 'info',
                'default': 'info-circle'
            }
            
            icon_name = icon_mapping.get(poi_type, 'info-circle')
            
            folium.Marker(
                poi_coords,
                popup=f"<b>{poi['name']}</b><br>{poi['description']}<br><i>{poi['address']}</i>",
                tooltip=f"{poi['name']} ({poi_type})",
                icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
            ).add_to(m)
            
            time.sleep(0.3)  # Rate limiting
    
    # Add a comprehensive legend
    legend_html = f'''
    <div style="position: fixed; 
                 top: 50px; left: 50px; width: 280px; height: auto; 
                 background-color: white; border:2px solid grey; z-index:9999; 
                 font-size:12px; padding: 15px; max-height: 80vh; overflow-y: auto;">
    <h3 style="margin-top: 0; font-size: 16px;">{town_data['name']}</h3>
    <p><b>🏨 {town_data['accommodation']}</b></p>
    <p><i>{town_data['walking_radius']}</i></p>
    <hr style="margin: 10px 0;">
    <p><i class="fa fa-home" style="color:red"></i> Your Accommodation</p>
    <p><i class="fa fa-cutlery" style="color:green"></i> Dining & Food</p>
    <p><i class="fa fa-cutlery" style="color:orange"></i> Bakeries</p>
    <p><i class="fa fa-beer" style="color:darkgreen"></i> Breweries</p>
    <p><i class="fa fa-glass" style="color:purple"></i> Wine & Cocktails</p>
    <p><i class="fa fa-shopping-cart" style="color:blue"></i> Markets</p>
    <p><i class="fa fa-university" style="color:darkblue"></i> Museums & Culture</p>
    <p><i class="fa fa-paint-brush" style="color:cadetblue"></i> Art Galleries</p>
    <p><i class="fa fa-university" style="color:darkred"></i> Historic Sites</p>
    <p><i class="fa fa-tree" style="color:lightgreen"></i> Parks & Nature</p>
    <p><i class="fa fa-shopping-bag" style="color:pink"></i> Shopping</p>
    <p><i class="fa fa-star" style="color:black"></i> Landmarks</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    map_filename = f"images/{town_key}_walking_map.html"
    m.save(map_filename)
    print(f"Saved walking map: {map_filename}")
    
    return m

def main():
    """Generate all town walking vicinity maps."""
    print("Generating walking vicinity maps for all towns...")
    
    for town_key, town_data in towns_data.items():
        create_town_map(town_key, town_data)
        time.sleep(2)  # Rate limiting between API calls
    
    print("All town walking maps generated!")
    
    # Create an index of all maps
    index_content = """
# Walking Vicinity Maps for All Towns

Interactive maps showing everything within 30 minutes walking distance of your accommodation:

"""
    
    for town_key, town_data in towns_data.items():
        index_content += f"- **{town_data['name']}** ({town_data['accommodation']}): [View Walking Map](images/{town_key}_walking_map.html)\n"
    
    with open('town_walking_maps_index.md', 'w') as f:
        f.write(index_content)

if __name__ == "__main__":
    main() 