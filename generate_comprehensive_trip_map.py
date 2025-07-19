#!/usr/bin/env python3
"""
Generate a comprehensive trip map showing the entire Pacific Northwest route
with detailed annotations and route information formatted as a PDF.
"""

import googlemaps
import json
import time
import os
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_pdf import PdfPages
import requests
from urllib.parse import urlencode
import numpy as np
from PIL import Image
import io

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

# Updated trip waypoints with dates and descriptions
waypoints = [
    {"name": "Bozeman, MT", "date": "Aug 3-4", "description": "Kimpton Armory Hotel - Luxury mountain town stay", "coords": None},
    {"name": "Missoula, MT", "date": "Aug 5", "description": "AC Hotel Downtown - Modern university town luxury", "coords": None},
    {"name": "Jerry Johnson Hot Springs, ID", "date": "Aug 6", "description": "Natural hot springs in pristine wilderness", "coords": None},
    {"name": "Lucile, ID", "date": "Aug 7-8", "description": "Steelhead Lodge - Upscale river lodge with salmon fishing & gaucho BBQ", "coords": None},
    {"name": "Joseph, OR", "date": "Aug 9", "description": "Jennings Hotel - Historic luxury in Wallowa Mountains", "coords": None},
    {"name": "Walla Walla, WA", "date": "Aug 10", "description": "Eritage Resort - Premium wine country resort", "coords": None},
    {"name": "White Salmon, WA", "date": "Aug 11", "description": "Under Canvas Columbia River Gorge - Luxury glamping with waterfalls", "coords": None},
    {"name": "Mount Rainier National Park, WA", "date": "Aug 12", "description": "Scenic mountain drive to Twin Peaks country", "coords": None},
    {"name": "North Bend, WA", "date": "Aug 12", "description": "Twin Peaks filming locations tour", "coords": None},
    {"name": "San Juan Islands, WA", "date": "Aug 12-14", "description": "Luxury island honeymoon - Orca watching & romance", "coords": None}
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

def generate_comprehensive_route_map():
    """Generate a large comprehensive map showing the entire route."""
    print("Generating comprehensive route map...")
    
    # Get coordinates for all waypoints
    for waypoint in waypoints:
        coords = get_coordinates_google(waypoint["name"])
        waypoint["coords"] = coords
        if coords:
            print(f"✓ {waypoint['name']}: {coords}")
        else:
            print(f"✗ Failed to geocode: {waypoint['name']}")
        time.sleep(0.1)  # Be respectful to the API
    
    base_url = "https://maps.googleapis.com/maps/api/staticmap?"
    
    # Map parameters - large size for high quality
    params = {
        'size': '1600x1200',  # Large size for detail
        'maptype': 'terrain',  # Terrain to show geographical features
        'key': GOOGLE_MAPS_API_KEY,
        'format': 'png',
        'scale': 2  # High resolution
    }
    
    # Add numbered markers for each waypoint
    markers = []
    for i, waypoint in enumerate(waypoints):
        if waypoint['coords']:
            lat, lng = waypoint['coords']
            # Use custom markers with numbers
            markers.append(f"color:red|label:{i+1}|size:mid|{lat},{lng}")
    
    if markers:
        params['markers'] = markers
    
    # Get route segments data for later use, but don't add paths to the map request
    # to avoid URL length limits
    route_segments = []
    
    for i in range(len(waypoints) - 1):
        origin = waypoints[i]
        destination = waypoints[i+1]
        
        if origin['coords'] and destination['coords']:
            directions = get_driving_directions(origin['name'], destination['name'])
            if directions:
                route_segments.append({
                    'from': origin,
                    'to': destination,
                    'directions': directions
                })
                print(f"✓ Route {i+1}: {origin['name'].split(',')[0]} → {destination['name'].split(',')[0]} ({directions['distance_text']}, {directions['duration_text']})")
    
    # Build URL without paths to avoid 400 error
    url = base_url + urlencode(params, doseq=True)
    
    print(f"Map URL length: {len(url)} characters")
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open('images/comprehensive_trip_map.png', 'wb') as f:
                f.write(response.content)
            print("✓ Comprehensive route map saved as images/comprehensive_trip_map.png")
            return route_segments
        else:
            print(f"Error generating comprehensive map: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error generating comprehensive map: {e}")
        return None

def create_annotated_trip_pdf(route_segments):
    """Create a comprehensive PDF with the map and detailed route information."""
    print("Creating annotated trip PDF...")
    
    # Create figure with specific layout
    fig = plt.figure(figsize=(16, 20))  # Portrait orientation, large size
    
    # Load the comprehensive map image
    try:
        map_img = Image.open('images/comprehensive_trip_map.png')
        
        # Create subplot for map (top 60% of the page)
        ax_map = plt.subplot2grid((10, 1), (0, 0), rowspan=6)
        ax_map.imshow(map_img)
        ax_map.set_title('PACIFIC NORTHWEST SUMMER ADVENTURE 2025\nComplete Route Overview', 
                        fontsize=24, fontweight='bold', pad=20)
        ax_map.axis('off')
        
        # Add elegant border around map
        rect = patches.Rectangle((0, 0), map_img.width, map_img.height, 
                               linewidth=3, edgecolor='darkblue', facecolor='none')
        ax_map.add_patch(rect)
        
    except Exception as e:
        print(f"Error loading map image: {e}")
        return
    
    # Create subplot for route details (bottom 40% of the page)
    ax_details = plt.subplot2grid((10, 1), (6, 0), rowspan=4)
    ax_details.axis('off')
    
    # Prepare route information
    route_info_text = []
    total_distance = 0
    total_time = 0
    
    # Header for route details
    route_info_text.append("DETAILED ROUTE SEGMENTS")
    route_info_text.append("=" * 80)
    route_info_text.append("")
    
    # Add each route segment
    for i, segment in enumerate(route_segments):
        leg_num = i + 1
        from_location = segment['from']['name'].split(',')[0]
        to_location = segment['to']['name'].split(',')[0]
        from_date = segment['from']['date']
        to_date = segment['to']['date']
        from_desc = segment['from']['description']
        to_desc = segment['to']['description']
        
        directions = segment['directions']
        distance_text = directions['distance_text']
        duration_text = directions['duration_text']
        
        total_distance += directions['distance_miles']
        total_time += directions['duration_hours']
        
        # Format route segment information
        route_info_text.append(f"LEG {leg_num}: {from_location} → {to_location}")
        route_info_text.append(f"   Distance: {distance_text} | Driving Time: {duration_text}")
        route_info_text.append(f"   Depart: {from_date} - {from_desc}")
        route_info_text.append(f"   Arrive: {to_date} - {to_desc}")
        route_info_text.append("")
    
    # Add summary statistics
    route_info_text.append("TRIP SUMMARY")
    route_info_text.append("-" * 40)
    route_info_text.append(f"Total Distance: {total_distance:.0f} miles")
    route_info_text.append(f"Total Driving Time: {total_time:.1f} hours")
    route_info_text.append(f"Average Daily Driving: {total_time/len(route_segments):.1f} hours")
    route_info_text.append(f"Trip Duration: August 3-14, 2025 (11 days)")
    route_info_text.append("")
    
    # Add special highlights
    route_info_text.append("TRIP HIGHLIGHTS")
    route_info_text.append("-" * 40)
    highlights = [
        "Luxury hotels and boutique lodges throughout",
        "Natural hot springs in pristine wilderness",
        "Salmon fishing on the Snake River at Steelhead Lodge",
        "Wine country exploration in Walla Walla",
        "Columbia River Gorge waterfalls and luxury glamping",
        "Mount Rainier scenic drive",
        "Twin Peaks filming locations tour",
        "Orca watching in San Juan Islands",
        "Romantic island honeymoon finale"
    ]
    
    for highlight in highlights:
        route_info_text.append(f"   {highlight}")
    
    # Display route information as text
    full_text = '\n'.join(route_info_text)
    ax_details.text(0.05, 0.95, full_text, transform=ax_details.transAxes, 
                   fontsize=11, fontfamily='monospace', verticalalignment='top',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    # Add footer with generation info
    footer_text = f"Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}"
    plt.figtext(0.5, 0.02, footer_text, ha='center', fontsize=10, style='italic')
    
    # Save as PDF
    plt.tight_layout()
    pdf_filename = 'images/Pacific_Northwest_Trip_2025_Complete_Map.pdf'
    plt.savefig(pdf_filename, format='pdf', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Comprehensive trip PDF saved as {pdf_filename}")
    
    # Also save as high-resolution PNG
    fig = plt.figure(figsize=(16, 20))
    ax_map = plt.subplot2grid((10, 1), (0, 0), rowspan=6)
    ax_map.imshow(map_img)
    ax_map.set_title('PACIFIC NORTHWEST SUMMER ADVENTURE 2025\nComplete Route Overview', 
                    fontsize=24, fontweight='bold', pad=20)
    ax_map.axis('off')
    
    rect = patches.Rectangle((0, 0), map_img.width, map_img.height, 
                           linewidth=3, edgecolor='darkblue', facecolor='none')
    ax_map.add_patch(rect)
    
    ax_details = plt.subplot2grid((10, 1), (6, 0), rowspan=4)
    ax_details.axis('off')
    ax_details.text(0.05, 0.95, full_text, transform=ax_details.transAxes, 
                   fontsize=11, fontfamily='monospace', verticalalignment='top',
                   bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
    
    plt.figtext(0.5, 0.02, footer_text, ha='center', fontsize=10, style='italic')
    plt.tight_layout()
    
    png_filename = 'images/Pacific_Northwest_Trip_2025_Complete_Map.png'
    plt.savefig(png_filename, format='png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"✓ Comprehensive trip PNG saved as {png_filename}")

def main():
    """Main function to generate the comprehensive trip map and PDF."""
    print("🗺️  Generating comprehensive Pacific Northwest trip map...")
    print(f"API Key: {GOOGLE_MAPS_API_KEY[:10]}...")
    
    # Generate the comprehensive route map
    route_segments = generate_comprehensive_route_map()
    
    if route_segments:
        # Create the annotated PDF with route details
        create_annotated_trip_pdf(route_segments)
        
        print(f"\n🎉 Comprehensive trip map generated!")
        print(f"📍 Large route map: images/comprehensive_trip_map.png")
        print(f"📄 Annotated PDF: images/Pacific_Northwest_Trip_2025_Complete_Map.pdf")
        print(f"🖼️  High-res PNG: images/Pacific_Northwest_Trip_2025_Complete_Map.png")
        
        # Calculate and display summary
        if route_segments:
            total_distance = sum(seg['directions']['distance_miles'] for seg in route_segments)
            total_time = sum(seg['directions']['duration_hours'] for seg in route_segments)
            print(f"\n📏 Total trip distance: {total_distance:.0f} miles")
            print(f"⏱️  Total driving time: {total_time:.1f} hours")
            print(f"🚗 Daily average: {total_time/len(route_segments):.1f} hours driving")
    else:
        print("❌ Failed to generate route segments")

if __name__ == "__main__":
    main() 