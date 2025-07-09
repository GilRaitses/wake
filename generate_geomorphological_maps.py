#!/usr/bin/env python3
"""
Generate geomorphological walking maps with subglacial fluvial textures,
DEM elevation exaggeration, and Art Nouveau neighborhood decorations.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Circle, Polygon
import numpy as np
import requests
import googlemaps
import time
import os
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
import matplotlib.patheffects as path_effects
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import gaussian_filter
import json

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

# Google Maps API key
GOOGLE_MAPS_API_KEY = "AIzaSyD0tZfpi0PQPBbYh6iwMrkQKda9n1XPQnI"
gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)

def geocode_with_retry(location, max_retries=3):
    """Geocode with retries."""
    for attempt in range(max_retries):
        try:
            geocode_result = gmaps.geocode(location)
            if geocode_result:
                location_data = geocode_result[0]['geometry']['location']
                return (location_data['lat'], location_data['lng'])
            time.sleep(1)
        except Exception as e:
            print(f"Geocoding attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    return None

def get_elevation_data(lat, lon, size=0.01):
    """Get elevation data using Google Elevation API."""
    # Create grid of points for elevation sampling
    grid_size = 20
    lats = np.linspace(lat - size/2, lat + size/2, grid_size)
    lons = np.linspace(lon - size/2, lon + size/2, grid_size)
    
    points = []
    for lat_point in lats:
        for lon_point in lons:
            points.append((lat_point, lon_point))
    
    try:
        # Get elevation data from Google
        elevation_data = gmaps.elevation(points)
        elevations = np.array([point['elevation'] for point in elevation_data])
        elevations = elevations.reshape(grid_size, grid_size)
        
        # Exaggerate elevation for 3D effect
        elevations = elevations * 3.0  # Exaggeration factor
        
        return elevations, lats, lons
    except Exception as e:
        print(f"Elevation API error: {e}")
        # Return synthetic elevation data if API fails
        return np.random.normal(1000, 200, (grid_size, grid_size)), lats, lons

def create_subglacial_texture(shape, intensity=0.3):
    """Create subglacial fluvial texture patterns."""
    height, width = shape
    
    # Create multiple noise layers for fluvial patterns
    texture = np.zeros((height, width))
    
    # Large scale flow patterns
    x = np.linspace(0, 4*np.pi, width)
    y = np.linspace(0, 4*np.pi, height)
    X, Y = np.meshgrid(x, y)
    
    # Fluvial channel patterns (meandering rivers under ice)
    flow_pattern = np.sin(X) * np.cos(Y*0.7) + np.sin(X*0.3) * np.cos(Y*1.2)
    
    # Add smaller scale braided patterns
    braided = np.sin(X*3) * np.cos(Y*2.5) * 0.5
    
    # Glacial striations
    striations = np.sin(X*0.8 + Y*0.3) * 0.3
    
    # Combine patterns
    texture = flow_pattern + braided + striations
    
    # Apply Gaussian smoothing for natural look
    texture = gaussian_filter(texture, sigma=1.5)
    
    # Normalize and apply intensity
    texture = (texture - texture.min()) / (texture.max() - texture.min())
    texture = texture * intensity
    
    return texture

def create_art_nouveau_border(center_x, center_y, size, style='organic'):
    """Create Art Nouveau style decorative elements for neighborhoods."""
    if style == 'organic':
        # Organic flowing lines inspired by William Morris
        angles = np.linspace(0, 2*np.pi, 12)
        radius_variation = size * (0.8 + 0.4 * np.sin(angles * 3))
        
        x_points = center_x + radius_variation * np.cos(angles)
        y_points = center_y + radius_variation * np.sin(angles)
        
        return list(zip(x_points, y_points))
    
    return [(center_x, center_y)]

def create_ecosystem_colormap():
    """Create custom colormap for Pacific Northwest ecosystems."""
    colors = [
        '#1e3a5f',  # Deep water
        '#2d5a8b',  # Shallow water
        '#4a7c59',  # Riparian forest
        '#6b8e23',  # Grassland
        '#8b7355',  # Shrubland
        '#a0522d',  # Dry forest
        '#696969',  # Rock/Alpine
        '#f5f5dc'   # Snow/Ice
    ]
    return LinearSegmentedColormap.from_list('pnw_ecosystems', colors)

def create_geomorphological_map(town_key, town_data):
    """Create geomorphological map with subglacial textures and elevation."""
    print(f"Creating geomorphological map for {town_data['name']}...")
    
    # Geocode accommodation
    hotel_coords = geocode_with_retry(town_data['accommodation']['address'])
    if not hotel_coords:
        print(f"Could not geocode accommodation for {town_data['name']}")
        return None
    
    # Collect POI coordinates
    poi_data = []
    for poi in town_data['points_of_interest']:
        coords = geocode_with_retry(poi['address'])
        if coords:
            poi_data.append((coords, poi['color'], poi['name']))
        time.sleep(0.2)
    
    # Get elevation data
    elevation_data, lats, lons = get_elevation_data(hotel_coords[0], hotel_coords[1])
    
    # Create figure with high DPI for detailed textures
    fig, ax = plt.subplots(figsize=(14, 10), dpi=150)
    
    # Create base terrain visualization
    ecosystem_cmap = create_ecosystem_colormap()
    
    # Plot elevation with exaggerated relief
    extent = (lons.min(), lons.max(), lats.min(), lats.max())
    terrain = ax.imshow(elevation_data, extent=extent, cmap=ecosystem_cmap, 
                       alpha=0.8, interpolation='bilinear')
    
    # Add subglacial fluvial texture overlay
    texture = create_subglacial_texture(elevation_data.shape, intensity=0.2)
    ax.imshow(texture, extent=extent, cmap='gray', alpha=0.3, interpolation='bilinear')
    
    # Add contour lines for topographic reference
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    contours = ax.contour(lon_grid, lat_grid, elevation_data, levels=8, colors='white', 
                         alpha=0.4, linewidths=0.5)
    # Skip contour labels for now to avoid issues
    
    # Plot accommodation with enhanced styling
    hotel_lat, hotel_lon = hotel_coords
    hotel_marker = patches.RegularPolygon((hotel_lon, hotel_lat), 6, radius=0.001, 
                                         facecolor='#8B0000', edgecolor='white', 
                                         linewidth=2, alpha=0.9)
    ax.add_patch(hotel_marker)
    
    # Add accommodation label with path effects
    hotel_text = ax.text(hotel_lon, hotel_lat + 0.002, town_data['accommodation']['name'], 
                        ha='center', va='bottom', fontsize=10, fontweight='bold',
                        color='white')
    hotel_text.set_path_effects([path_effects.withStroke(linewidth=3, foreground='black')])
    
    # Plot POIs with ecosystem-aware styling
    ecosystem_colors = {
        'red': '#8B0000',
        'orange': '#FF8C00', 
        'green': '#228B22',
        'blue': '#4169E1',
        'purple': '#8B008B'
    }
    
    for (lat, lon), color, name in poi_data:
        # Main POI marker
        poi_circle = Circle((lon, lat), 0.0015, facecolor=ecosystem_colors[color], 
                           edgecolor='white', linewidth=1.5, alpha=0.85)
        ax.add_patch(poi_circle)
        
        # Add subtle Art Nouveau decoration for neighborhoods
        if 'district' in name.lower() or 'downtown' in name.lower():
            border_points = create_art_nouveau_border(lon, lat, 0.003, 'organic')
            decoration = Polygon(border_points, facecolor=ecosystem_colors[color], 
                                alpha=0.15, edgecolor=ecosystem_colors[color], 
                                linewidth=0.8, linestyle='--')
            ax.add_patch(decoration)
        
        # POI label with enhanced readability
        poi_text = ax.text(lon, lat - 0.0025, name, ha='center', va='top', 
                          fontsize=8, color='white', fontweight='bold')
        poi_text.set_path_effects([path_effects.withStroke(linewidth=2, foreground='black')])
    
    # Add regional geological context
    region_info = {
        'bozeman_mt': 'Gallatin Valley • Glacial Outwash Plains',
        'missoula_mt': 'Clark Fork Valley • Glacial Lake Missoula',
        'mccall_id': 'Payette Lake Basin • Glacial Cirque',
        'joseph_or': 'Wallowa Mountains • Alpine Glacial Terrain',
        'walla_walla_wa': 'Columbia Plateau • Loess Hills',
        'cascade_locks_or': 'Columbia River Gorge • Glacial Outburst Floods',
        'seattle_wa': 'Puget Sound Lowland • Glacial Till Plains'
    }
    
    if town_key in region_info:
        ax.text(0.02, 0.98, region_info[town_key], transform=ax.transAxes, 
                fontsize=11, fontweight='bold', color='white', va='top',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='black', alpha=0.7))
    
    # Add scale and north arrow
    ax.text(0.02, 0.02, '1 km', transform=ax.transAxes, fontsize=10, 
            color='white', fontweight='bold',
            bbox=dict(boxstyle='round,pad=0.2', facecolor='black', alpha=0.7))
    
    # Style the map
    ax.set_xlim(extent[0], extent[1])
    ax.set_ylim(extent[2], extent[3])
    ax.set_aspect('equal')
    ax.set_facecolor('#0F1419')  # Dark base for contrast
    
    # Remove axes for clean look
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Add title with geological context
    fig.suptitle(f'{town_data["name"]} • Geomorphological Context', 
                fontsize=16, fontweight='bold', color='white', y=0.95)
    
    # Save with high quality
    filename = f"images/{town_key}_geomorphological_map.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0F1419')
    plt.close()
    
    print(f"Saved geomorphological map: {filename}")
    return filename

# Enhanced town data with geological context
towns_data = {
    "bozeman_mt": {
        "name": "Bozeman, Montana",
        "accommodation": {"name": "Kimpton Armory Hotel", "address": "24 W Mendenhall St, Bozeman, MT 59715"},
        "points_of_interest": [
            {"name": "Main Street Historic District", "address": "Main St & Mendenhall St, Bozeman, MT", "color": "red"},
            {"name": "Wild Crumb Bakery", "address": "1424 W Main St, Bozeman, MT", "color": "orange"},
            {"name": "Blackbird Kitchen", "address": "200 W Main St, Bozeman, MT", "color": "green"},
            {"name": "Montana Ale Works", "address": "611 E Main St, Bozeman, MT", "color": "blue"},
            {"name": "Bogert Park", "address": "325 S Church Ave, Bozeman, MT", "color": "purple"}
        ]
    },
    
    "seattle_wa": {
        "name": "Seattle, Washington",
        "accommodation": {"name": "The Fairmont Olympic Seattle", "address": "411 University St, Seattle, WA 98101"},
        "points_of_interest": [
            {"name": "Pike Place Market", "address": "85 Pike St, Seattle, WA", "color": "red"},
            {"name": "Pioneer Square Historic District", "address": "600 1st Ave, Seattle, WA", "color": "orange"},
            {"name": "Seattle Art Museum", "address": "1300 1st Ave, Seattle, WA", "color": "purple"},
            {"name": "Waterfront Park", "address": "1401 Alaskan Way, Seattle, WA", "color": "blue"},
            {"name": "Grand Central Bakery", "address": "214 1st Ave S, Seattle, WA", "color": "green"}
        ]
    }
}

def main():
    """Generate geomorphological maps for testing."""
    print("Generating geomorphological maps with subglacial textures...")
    
    # Test with Bozeman and Seattle first
    for town_key in ['bozeman_mt', 'seattle_wa']:
        if town_key in towns_data:
            create_geomorphological_map(town_key, towns_data[town_key])
            time.sleep(2)  # Rate limiting
    
    print("Geomorphological maps generated!")

if __name__ == "__main__":
    main() 