#!/usr/bin/env python3
"""
Generate a detailed town map for Lostine, Oregon
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

# Lostine town data
lostine_data = {
    "name": "Lostine, Oregon",
    "description": "Historic ranching town and gateway to Wallowa Mountains",
    "center": "Lostine, OR 97857",
    "points_of_interest": [
        {
            "name": "M. Crow & Co. General Store",
            "address": "46923 Main St, Lostine, OR 97857",
            "type": "store",
            "description": "Famous design store by Tyler Hays, featuring handcrafted furniture and home goods",
            "hours": "Daily 10 AM - 6 PM",
            "phone": "(541) 569-2394"
        },
        {
            "name": "Lostine Tavern",
            "address": "46959 Main St, Lostine, OR 97857", 
            "type": "restaurant",
            "description": "Historic local tavern and restaurant serving hearty mountain fare",
            "hours": "Daily 11 AM - 10 PM"
        },
        {
            "name": "Lostine River",
            "address": "Lostine River, Lostine, OR",
            "type": "nature",
            "description": "Beautiful river running through town, popular for fishing and relaxing"
        },
        {
            "name": "Wallowa-Whitman National Forest Access",
            "address": "Lostine Canyon Rd, Lostine, OR",
            "type": "nature",
            "description": "Trailhead access to Eagle Cap Wilderness and alpine lakes"
        },
        {
            "name": "Historic Lostine Methodist Church",
            "address": "Main St, Lostine, OR",
            "type": "historic",
            "description": "Beautiful 1920s wooden church, architectural landmark"
        },
        {
            "name": "Lostine Post Office",
            "address": "46949 Main St, Lostine, OR 97857",
            "type": "service",
            "description": "Historic small-town post office"
        },
        {
            "name": "Lostine Community Center",
            "address": "Main St, Lostine, OR",
            "type": "community",
            "description": "Local community gathering place and events venue"
        },
        {
            "name": "Historic Ranches",
            "address": "Lostine Valley, OR",
            "type": "historic",
            "description": "Working cattle ranches that define the valley's character"
        }
    ]
}

def create_lostine_map():
    """Create a detailed map of Lostine, Oregon."""
    print("Creating detailed map of Lostine, Oregon...")
    
    # Geocode the town center
    center_coords = geocode_with_retry(lostine_data["center"])
    
    if not center_coords:
        print("Could not geocode Lostine center")
        return None
    
    # Create map centered on Lostine
    m = folium.Map(
        location=center_coords,
        zoom_start=15,
        tiles='OpenStreetMap'
    )
    
    # Color coding for different types of points
    type_colors = {
        'store': 'red',
        'restaurant': 'green', 
        'nature': 'blue',
        'historic': 'purple',
        'service': 'orange',
        'community': 'darkgreen'
    }
    
    # Add points of interest
    for poi in lostine_data['points_of_interest']:
        poi_coords = geocode_with_retry(poi['address'])
        if poi_coords:
            poi_type = poi.get('type', 'default')
            color = type_colors.get(poi_type, 'gray')
            
            # Create icon based on type
            if poi_type == 'store':
                icon_name = 'shopping-cart'
            elif poi_type == 'restaurant':
                icon_name = 'cutlery'
            elif poi_type == 'nature':
                icon_name = 'tree'
            elif poi_type == 'historic':
                icon_name = 'university'
            elif poi_type == 'service':
                icon_name = 'envelope'
            elif poi_type == 'community':
                icon_name = 'users'
            else:
                icon_name = 'info-sign'
            
            # Create popup content
            popup_content = f"""
            <b>{poi['name']}</b><br>
            {poi['description']}<br>
            """
            if 'hours' in poi:
                popup_content += f"<br><b>Hours:</b> {poi['hours']}"
            if 'phone' in poi:
                popup_content += f"<br><b>Phone:</b> {poi['phone']}"
            
            folium.Marker(
                poi_coords,
                popup=popup_content,
                tooltip=f"{poi['name']} ({poi_type})",
                icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
            ).add_to(m)
            
            time.sleep(0.5)  # Rate limiting
    
    # Add a legend
    legend_html = f'''
    <div style="position: fixed; 
                 top: 50px; left: 50px; width: 280px; height: auto; 
                 background-color: white; border:2px solid grey; z-index:9999; 
                 font-size:14px; padding: 15px">
    <h3 style="margin-top: 0;">Lostine, Oregon</h3>
    <p><b>Historic ranching town & mountain gateway</b></p>
    <p><i class="fa fa-shopping-cart" style="color:red"></i> M. Crow & Co. Store</p>
    <p><i class="fa fa-cutlery" style="color:green"></i> Restaurants & Dining</p>
    <p><i class="fa fa-tree" style="color:blue"></i> Nature & Outdoor Access</p>
    <p><i class="fa fa-university" style="color:purple"></i> Historic Sites</p>
    <p><i class="fa fa-envelope" style="color:orange"></i> Services</p>
    <p><i class="fa fa-users" style="color:darkgreen"></i> Community Spaces</p>
    <hr>
    <p><small><b>Distance from Joseph:</b> 8 miles north<br>
    <b>Drive time:</b> 12 minutes<br>
    <b>Elevation:</b> 3,640 ft</small></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    map_filename = "images/lostine_oregon_town_map.html"
    m.save(map_filename)
    print(f"Saved map: {map_filename}")
    
    return m

def main():
    """Generate the Lostine town map."""
    print("Generating detailed Lostine, Oregon town map...")
    create_lostine_map()
    print("Lostine town map generated!")

if __name__ == "__main__":
    main() 