#!/usr/bin/env python3
"""
Generate location-specific recommendation maps for each leg of the trip.
Each map will be centered on the accommodation and show nearby recommendations.
"""

import folium
import json
import os
import googlemaps
import time

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Google Maps API key (same as in generate_route_maps.py)
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

# Trip legs with accommodations and recommendations
trip_legs = {
    "bozeman_montana": {
        "name": "Bozeman, Montana",
        "dates": "August 3-4",
        "accommodation": {
            "name": "Kimpton Armory Hotel Bozeman",
            "address": "24 W Mendenhall St, Bozeman, MT 59715",
            "phone": "(406) 551-7700",
            "website": "kimptonarmoryhotel.com"
        },
        "recommendations": {
            "museums": [
                {"name": "Museum of the Rockies", "address": "600 W Kagy Blvd, Bozeman, MT", "type": "museum"},
                {"name": "Montana State University", "address": "MSU Campus, Bozeman, MT", "type": "campus"}
            ],
            "bakeries": [
                {"name": "Great Harvest Bread Co.", "address": "1716 W Babcock St, Bozeman, MT", "type": "bakery"},
                {"name": "Wild Crumb Bakery & Cafe", "address": "1424 W Main St, Bozeman, MT", "type": "bakery"}
            ],
            "bbq": [
                {"name": "Bar 3 BBQ & Brewing", "address": "124 Main St, Belgrade, MT", "type": "bbq"},
                {"name": "Blue Smoke Barbeque", "address": "Bozeman, MT", "type": "bbq"}
            ],
            "specialty": [
                {"name": "Blackbird Kitchen", "address": "Bozeman, MT", "type": "argentine"},
                {"name": "Montana Wagyu Ranch", "address": "Bozeman area, MT", "type": "ranch"}
            ]
        }
    },
    
    "missoula_montana": {
        "name": "Missoula, Montana", 
        "dates": "August 5",
        "accommodation": {
            "name": "AC Hotel Missoula Downtown",
            "address": "200 S Pattee St, Missoula, MT 59802",
            "phone": "(406) 541-8000",
            "website": "marriott.com"
        },
        "recommendations": {
            "cultural": [
                {"name": "University of Montana", "address": "32 Campus Dr, Missoula, MT", "type": "campus"},
                {"name": "Clark Fork Riverfront Trail", "address": "Missoula, MT", "type": "trail"}
            ],
            "bakeries": [
                {"name": "Le Petit Outre", "address": "129 W Front St, Missoula, MT", "type": "bakery"},
                {"name": "Bernice's Bakery", "address": "190 S 3rd St W, Missoula, MT", "type": "bakery"}
            ],
            "bbq": [
                {"name": "T-Rex BBQ", "address": "124 Main St, Three Forks, MT", "type": "bbq"},
                {"name": "Riverhouse BBQ", "address": "Big Sky, MT", "type": "bbq"}
            ],
            "specialty": [
                {"name": "Plonk Wine Bar", "address": "322 N Higgins Ave, Missoula, MT", "type": "wine_bar"}
            ]
        }
    },
    
    "mccall_idaho": {
        "name": "McCall, Idaho",
        "dates": "August 7-8", 
        "accommodation": {
            "name": "Shore Lodge",
            "address": "501 W Lake St, McCall, ID 83638",
            "phone": "(800) 657-6464",
            "website": "shorelodge.com"
        },
        "recommendations": {
            "hot_springs": [
                {"name": "Trail Creek Hot Springs", "address": "Trail Creek Road, McCall, ID", "type": "hot_springs"},
                {"name": "Burgdorf Hot Springs", "address": "Burgdorf Road, McCall, ID", "type": "hot_springs"},
                {"name": "Gold Fork Hot Springs", "address": "Gold Fork Road, McCall, ID", "type": "hot_springs"}
            ],
            "dining": [
                {"name": "Narrows Steakhouse", "address": "501 W Lake St, McCall, ID", "type": "steakhouse"},
                {"name": "Smoky Mountain Pizzeria", "address": "815 N 3rd St, McCall, ID", "type": "pizzeria"}
            ],
            "bakeries": [
                {"name": "Alpine Bagel Company", "address": "1101 N 3rd St, McCall, ID", "type": "bakery"},
                {"name": "Rupert's at Hotel McCall", "address": "1101 N 3rd St, McCall, ID", "type": "bakery"}
            ],
            "activities": [
                {"name": "Payette Lake", "address": "McCall, ID", "type": "lake"},
                {"name": "Brundage Mountain", "address": "McCall, ID", "type": "mountain"}
            ]
        }
    },
    
    "joseph_oregon": {
        "name": "Joseph, Oregon",
        "dates": "August 9",
        "accommodation": {
            "name": "The Jennings Hotel", 
            "address": "100 Main St, Joseph, OR 97846",
            "phone": "(541) 432-0230",
            "website": "jenningshotel.com"
        },
        "recommendations": {
            "cultural": [
                {"name": "Valley Bronze of Oregon", "address": "18 S Main St, Joseph, OR", "type": "art"},
                {"name": "Josephy Center for Arts & Culture", "address": "403 N Main St, Joseph, OR", "type": "arts_center"},
                {"name": "Wallowa Lake", "address": "Wallowa Lake, OR", "type": "lake"}
            ],
            "dining": [
                {"name": "Embers Brewhouse & Eatery", "address": "204 N Main St, Joseph, OR", "type": "brewery"},
                {"name": "Lear's Main Street Grill", "address": "111 W Main St, Joseph, OR", "type": "grill"},
                {"name": "Wallowa Lake Lodge", "address": "60060 Wallowa Lake Hwy, Joseph, OR", "type": "lodge"}
            ],
            "shopping": [
                {"name": "M. Crow Store", "address": "Lostine, OR", "type": "store"}
            ]
        }
    },
    
    "walla_walla_washington": {
        "name": "Walla Walla, Washington",
        "dates": "August 10",
        "accommodation": {
            "name": "Eritage Resort",
            "address": "1000 N 2nd Ave, Walla Walla, WA 99362", 
            "phone": "(509) 394-4700",
            "website": "eritage.com"
        },
        "recommendations": {
            "wineries": [
                {"name": "Leonetti Cellar", "address": "1321 School Ave, Walla Walla, WA", "type": "winery"},
                {"name": "Woodward Canyon Winery", "address": "11920 W Highway 12, Walla Walla, WA", "type": "winery"},
                {"name": "L'Ecole No 41", "address": "41 Lowden School Rd, Lowden, WA", "type": "winery"}
            ],
            "cultural": [
                {"name": "Whitman Mission National Historic Site", "address": "328 Whitman Mission Rd, Walla Walla, WA", "type": "historic"},
                {"name": "Fort Walla Walla Museum", "address": "755 Myra Rd, Walla Walla, WA", "type": "museum"}
            ],
            "dining": [
                {"name": "Brasserie Four", "address": "4 E Main St, Walla Walla, WA", "type": "french"},
                {"name": "Saffron Mediterranean Kitchen", "address": "125 W Alder St, Walla Walla, WA", "type": "mediterranean"}
            ]
        }
    },
    
    "columbia_river_gorge": {
        "name": "Columbia River Gorge",
        "dates": "August 11", 
        "accommodation": {
            "name": "Under Canvas Columbia River",
            "address": "1681 Little White Salmon Rd, Cook, WA 98605",
            "phone": "Contact needed",
            "website": "undercanvas.com"
        },
        "recommendations": {
            "dining": [
                {"name": "Thunder Island Brewing", "address": "515 WaNaPa St, Cascade Locks, OR", "type": "brewery"},
                {"name": "Bonneville Hot Springs Resort", "address": "1252 E Cascade Dr, North Bonneville, WA", "type": "resort"},
                {"name": "Skamania Lodge", "address": "1131 SW Skamania Lodge Way, Stevenson, WA", "type": "lodge"}
            ],
            "attractions": [
                {"name": "Multnomah Falls", "address": "Bridal Veil, OR", "type": "waterfall"},
                {"name": "Bonneville Lock and Dam", "address": "Cascade Locks, OR", "type": "dam"},
                {"name": "Bridge of the Gods", "address": "Cascade Locks, OR", "type": "bridge"}
            ],
            "towns": [
                {"name": "Stevenson, WA", "address": "Stevenson, WA", "type": "town"},
                {"name": "Hood River, OR", "address": "Hood River, OR", "type": "town"}
            ]
        }
    },
    
    "seattle_washington": {
        "name": "Seattle, Washington",
        "dates": "August 12-14",
        "accommodation": {
            "name": "The Fairmont Olympic Seattle",
            "address": "411 University St, Seattle, WA 98101",
            "phone": "(206) 621-1700", 
            "website": "fairmont.com/seattle"
        },
        "recommendations": {
            "attractions": [
                {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "type": "market"},
                {"name": "Space Needle", "address": "400 Broad St, Seattle, WA", "type": "landmark"},
                {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "type": "museum"},
                {"name": "Burke Museum", "address": "4300 15th Ave NE, Seattle, WA", "type": "museum"}
            ],
            "neighborhoods": [
                {"name": "Capitol Hill", "address": "Capitol Hill, Seattle, WA", "type": "neighborhood"},
                {"name": "Fremont", "address": "Fremont, Seattle, WA", "type": "neighborhood"},
                {"name": "Ballard", "address": "Ballard, Seattle, WA", "type": "neighborhood"}
            ],
            "dining": [
                {"name": "Asado", "address": "2810 NW Market St, Seattle, WA", "type": "argentine"},
                {"name": "Matt's in the Market", "address": "94 Pike St, Seattle, WA", "type": "seafood"}
            ],
            "day_trips": [
                {"name": "North Bend (Twin Peaks)", "address": "North Bend, WA", "type": "town"},
                {"name": "Snoqualmie Falls", "address": "Snoqualmie, WA", "type": "waterfall"}
            ]
        }
    }
}

def create_location_map(leg_name, leg_data):
    """Create a map for a specific location with accommodation and recommendations."""
    print(f"Creating map for {leg_data['name']}...")
    
    # Geocode the accommodation
    accommodation = leg_data['accommodation']
    hotel_coords = geocode_with_retry(f"{accommodation['address']}")
    
    if not hotel_coords:
        print(f"Could not geocode hotel for {leg_data['name']}")
        return None
    
    # Create map centered on the accommodation
    m = folium.Map(
        location=hotel_coords,
        zoom_start=12,
        tiles='OpenStreetMap'
    )
    
    # Add accommodation marker (larger, distinctive)
    folium.Marker(
        hotel_coords,
        popup=f"<b>{accommodation['name']}</b><br>{accommodation['address']}<br>Phone: {accommodation['phone']}",
        tooltip=f"🏨 {accommodation['name']}",
        icon=folium.Icon(color='red', icon='home', prefix='fa')
    ).add_to(m)
    
    # Color coding for different types of recommendations
    type_colors = {
        'museum': 'blue',
        'bakery': 'orange', 
        'bbq': 'darkred',
        'hot_springs': 'lightblue',
        'winery': 'purple',
        'brewery': 'green',
        'restaurant': 'darkgreen',
        'attraction': 'cadetblue',
        'default': 'gray'
    }
    
    # Add recommendation markers
    for category, places in leg_data['recommendations'].items():
        for place in places:
            place_coords = geocode_with_retry(f"{place['address']}")
            if place_coords:
                place_type = place.get('type', 'default')
                color = type_colors.get(place_type, type_colors['default'])
                
                # Create icon based on type
                if place_type == 'bakery':
                    icon_name = 'cutlery'
                elif place_type == 'bbq':
                    icon_name = 'fire'
                elif place_type == 'hot_springs':
                    icon_name = 'tint'
                elif place_type == 'winery':
                    icon_name = 'glass'
                elif place_type == 'museum':
                    icon_name = 'university'
                elif place_type == 'brewery':
                    icon_name = 'beer'
                else:
                    icon_name = 'info-sign'
                
                folium.Marker(
                    place_coords,
                    popup=f"<b>{place['name']}</b><br>{place['address']}<br>Type: {place_type.title()}",
                    tooltip=f"{place['name']} ({place_type})",
                    icon=folium.Icon(color=color, icon=icon_name, prefix='fa')
                ).add_to(m)
                
                time.sleep(0.5)  # Rate limiting
    
    # Add a legend
    legend_html = f'''
    <div style="position: fixed; 
                 bottom: 50px; left: 50px; width: 200px; height: auto; 
                 background-color: white; border:2px solid grey; z-index:9999; 
                 font-size:14px; padding: 10px">
    <h4>{leg_data['name']}</h4>
    <p><b>{leg_data['dates']}</b></p>
    <p><i class="fa fa-home" style="color:red"></i> Accommodation</p>
    <p><i class="fa fa-cutlery" style="color:orange"></i> Bakeries</p>
    <p><i class="fa fa-fire" style="color:darkred"></i> BBQ/Smokehouse</p>
    <p><i class="fa fa-tint" style="color:lightblue"></i> Hot Springs</p>
    <p><i class="fa fa-glass" style="color:purple"></i> Wineries</p>
    <p><i class="fa fa-beer" style="color:green"></i> Breweries</p>
    <p><i class="fa fa-university" style="color:blue"></i> Museums/Culture</p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))
    
    # Save the map
    map_filename = f"images/{leg_name}_recommendations_map.html"
    m.save(map_filename)
    print(f"Saved map: {map_filename}")
    
    return m

def main():
    """Generate all location recommendation maps."""
    print("Generating location-specific recommendation maps...")
    
    for leg_name, leg_data in trip_legs.items():
        create_location_map(leg_name, leg_data)
        time.sleep(2)  # Rate limiting between API calls
    
    print("All location recommendation maps generated!")
    
    # Create an index of all maps
    index_content = """
# Location Recommendation Maps

The following interactive maps show recommendations centered around your accommodation for each leg of the trip:

"""
    
    for leg_name, leg_data in trip_legs.items():
        index_content += f"- **{leg_data['name']}** ({leg_data['dates']}): [View Map](images/{leg_name}_recommendations_map.html)\n"
    
    with open('location_maps_index.md', 'w') as f:
        f.write(index_content)

if __name__ == "__main__":
    main() 