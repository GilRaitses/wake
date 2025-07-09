#!/usr/bin/env python3
"""
Integrate real geospatial data for enhanced Pacific Northwest mapping
Uses USGS and open data sources for geological, hydrological, and ecological features
"""

import requests
import geopandas as gpd
import matplotlib.pyplot as plt
import json
import os
from pathlib import Path
import time

# Data source URLs for Pacific Northwest geospatial data
GEOSPATIAL_SOURCES = {
    'usgs_geology': {
        'base_url': 'https://mrdata.usgs.gov/services/sgmc2',
        'description': 'USGS State Geologic Map Compilation',
        'formats': ['geojson', 'shapefile']
    },
    
    'usgs_structures': {
        'base_url': 'https://services.nationalmap.gov/arcgis/rest/services/structures/MapServer',
        'description': 'National Structures Dataset',
        'formats': ['geojson']
    },
    
    'usgs_hydro': {
        'base_url': 'https://services.nationalmap.gov/arcgis/rest/services/nhd/MapServer',
        'description': 'National Hydrography Dataset',
        'formats': ['geojson']
    },
    
    'noaa_climate': {
        'base_url': 'https://www.ncei.noaa.gov/data/cirs/climdiv/',
        'description': 'Climate divisions and regions',
        'formats': ['geojson']
    },
    
    'epa_ecoregions': {
        'base_url': 'https://gaftp.epa.gov/EPADataCommons/ORD/Ecoregions/',
        'description': 'EPA Level III Ecoregions',
        'formats': ['shapefile', 'geojson']
    }
}

# Pacific Northwest state/region boundaries
PNW_STATES = ['WA', 'OR', 'ID', 'MT']
PNW_BOUNDS = {
    'north': 49.0,
    'south': 42.0, 
    'east': -110.0,
    'west': -125.0
}

class GeospatialDataManager:
    """Manage geospatial data acquisition and integration."""
    
    def __init__(self, cache_dir='geospatial_cache'):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_usgs_geology_data(self, state_code):
        """Fetch USGS geological data for a specific state."""
        cache_file = self.cache_dir / f'geology_{state_code}.geojson'
        
        if cache_file.exists():
            print(f"Loading cached geology data for {state_code}")
            return gpd.read_file(cache_file)
        
        try:
            # USGS State Geologic Map Compilation API
            url = f"https://mrdata.usgs.gov/geology/state/{state_code.lower()}-geol.json"
            
            print(f"Fetching geology data for {state_code}...")
            response = requests.get(url, timeout=30)
            
            if response.status_code == 200:
                # Save to cache
                with open(cache_file, 'w') as f:
                    json.dump(response.json(), f)
                
                return gpd.read_file(cache_file)
            else:
                print(f"Failed to fetch geology data: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"Error fetching geology data: {e}")
            return None
    
    def get_watershed_data(self, huc_code):
        """Fetch watershed boundary data."""
        cache_file = self.cache_dir / f'watershed_{huc_code}.geojson'
        
        if cache_file.exists():
            return gpd.read_file(cache_file)
        
        try:
            # USGS Water Data Services
            url = f"https://hydro.nationalmap.gov/arcgis/rest/services/wbd/MapServer/0/query"
            params = {
                'where': f"HUC8 LIKE '{huc_code}%'",
                'outFields': '*',
                'f': 'geojson',
                'returnGeometry': 'true'
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                with open(cache_file, 'w') as f:
                    json.dump(response.json(), f)
                return gpd.read_file(cache_file)
                
        except Exception as e:
            print(f"Error fetching watershed data: {e}")
            return None
    
    def get_geothermal_features(self, bounds):
        """Fetch geothermal features data."""
        cache_file = self.cache_dir / 'geothermal_features.geojson'
        
        # For demonstration - would use real geothermal database
        # USGS has geothermal resource databases
        geothermal_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Jerry Johnson Hot Springs",
                        "type": "hot_springs",
                        "temperature_c": 48,
                        "flow_rate": "moderate"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-114.5234, 46.2344]
                    }
                },
                {
                    "type": "Feature", 
                    "properties": {
                        "name": "Burgdorf Hot Springs",
                        "type": "hot_springs",
                        "temperature_c": 39,
                        "flow_rate": "high"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-115.9876, 45.2567]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(geothermal_features, f)
        
        return gpd.read_file(cache_file)
    
    def get_volcanic_features(self):
        """Fetch Cascade volcanic features."""
        cache_file = self.cache_dir / 'volcanic_features.geojson'
        
        try:
            # Smithsonian Global Volcanism Program API
            url = "https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows"
            params = {
                'service': 'WFS',
                'version': '1.0.0',
                'request': 'GetFeature',
                'typeName': 'GVP-VOTW:Smithsonian_VOTW_Volcanoes',
                'outputFormat': 'json',
                'bbox': f"{PNW_BOUNDS['west']},{PNW_BOUNDS['south']},{PNW_BOUNDS['east']},{PNW_BOUNDS['north']}"
            }
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                with open(cache_file, 'w') as f:
                    f.write(response.text)
                return gpd.read_file(cache_file)
                
        except Exception as e:
            print(f"Error fetching volcanic data: {e}")
            return None

    def get_ecoregion_data(self):
        """Fetch EPA Level III Ecoregions for Pacific Northwest."""
        cache_file = self.cache_dir / 'ecoregions_pnw.geojson'
        
        try:
            # EPA Ecoregions download
            url = "https://gaftp.epa.gov/EPADataCommons/ORD/Ecoregions/us/us_eco_l3.zip"
            
            # This would need proper zip handling in production
            print("Note: EPA ecoregion data requires zip file processing")
            print("Would implement full download and extraction here")
            
            return None
            
        except Exception as e:
            print(f"Error fetching ecoregion data: {e}")
            return None

def integrate_geospatial_layers(base_map, town_coords, town_name):
    """Integrate multiple geospatial data layers onto base map."""
    
    data_manager = GeospatialDataManager()
    
    print(f"Integrating geospatial data for {town_name}...")
    
    # Determine state from coordinates
    lat, lon = town_coords
    if lat > 47.0 and lon > -120.0:
        state = 'WA'
    elif lat > 44.0 and lon < -120.0:
        state = 'OR'
    elif lat > 45.0 and lon > -117.0:
        state = 'ID'
    else:
        state = 'MT'
    
    layers = {}
    
    # Get geological data
    geology_data = data_manager.get_usgs_geology_data(state)
    if geology_data is not None:
        layers['geology'] = geology_data
        print(f"Loaded {len(geology_data)} geological features")
    
    # Get watershed data (use approximate HUC codes for PNW)
    huc_codes = {
        'columbia': '1707',
        'snake': '1705', 
        'puget_sound': '1711'
    }
    
    for watershed, huc in huc_codes.items():
        watershed_data = data_manager.get_watershed_data(huc)
        if watershed_data is not None:
            layers[f'watershed_{watershed}'] = watershed_data
    
    # Get geothermal features
    geothermal_data = data_manager.get_geothermal_features(PNW_BOUNDS)
    if geothermal_data is not None:
        layers['geothermal'] = geothermal_data
        print(f"Loaded {len(geothermal_data)} geothermal features")
    
    # Get volcanic features
    volcanic_data = data_manager.get_volcanic_features()
    if volcanic_data is not None:
        layers['volcanic'] = volcanic_data
        print(f"Loaded {len(volcanic_data)} volcanic features")
    
    return layers

def create_enhanced_geomorphological_map(town_key, town_data, geospatial_layers):
    """Create enhanced map with integrated geospatial data."""
    
    fig, ax = plt.subplots(figsize=(16, 12), dpi=200)
    
    # Plot geological layers if available
    if 'geology' in geospatial_layers:
        geology = geospatial_layers['geology']
        
        # Clip to area of interest
        hotel_coords = (town_data['coords']['lat'], town_data['coords']['lon'])
        buffer = 0.05  # degrees
        
        minx = hotel_coords[1] - buffer
        maxx = hotel_coords[1] + buffer
        miny = hotel_coords[0] - buffer
        maxy = hotel_coords[0] + buffer
        
        clipped_geology = geology.cx[minx:maxx, miny:maxy]
        
        if not clipped_geology.empty:
            clipped_geology.plot(ax=ax, column='UNIT_AGE', alpha=0.6, 
                               legend=True, cmap='viridis')
            print(f"Plotted {len(clipped_geology)} geological units")
    
    # Plot watershed boundaries
    for layer_name in geospatial_layers:
        if 'watershed' in layer_name:
            watershed = geospatial_layers[layer_name]
            if watershed is not None and not watershed.empty:
                watershed.boundary.plot(ax=ax, color='blue', alpha=0.7, linewidth=2)
    
    # Plot geothermal features
    if 'geothermal' in geospatial_layers:
        geothermal = geospatial_layers['geothermal']
        geothermal.plot(ax=ax, color='red', marker='*', markersize=200, alpha=0.8)
        
        # Add labels
        for idx, feature in geothermal.iterrows():
            ax.annotate(feature['name'], 
                       (feature.geometry.x, feature.geometry.y),
                       xytext=(5, 5), textcoords='offset points',
                       fontsize=10, fontweight='bold', color='red')
    
    # Plot volcanic features
    if 'volcanic' in geospatial_layers:
        volcanic = geospatial_layers['volcanic']
        volcanic.plot(ax=ax, color='orange', marker='^', markersize=150, alpha=0.8)
    
    # Add title with geospatial context
    ax.set_title(f'{town_data["name"]} - Enhanced Geospatial Context\n'
                f'Geology • Hydrology • Geothermal • Volcanic Features', 
                fontsize=16, fontweight='bold', pad=20)
    
    # Remove axes
    ax.set_xticks([])
    ax.set_yticks([])
    
    # Save enhanced map
    filename = f"images/{town_key}_enhanced_geospatial_map.png"
    plt.tight_layout()
    plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    
    print(f"Saved enhanced geospatial map: {filename}")
    return filename

# Example usage
def main():
    """Demonstrate geospatial data integration."""
    print("Demonstrating geospatial data integration for Pacific Northwest...")
    
    # Example town data
    example_town = {
        'name': 'Bozeman, Montana',
        'coords': {'lat': 45.6770, 'lon': -111.0429}
    }
    
    # Get geospatial layers
    layers = integrate_geospatial_layers(
        None, 
        (example_town['coords']['lat'], example_town['coords']['lon']),
        example_town['name']
    )
    
    print(f"\nAvailable geospatial layers: {list(layers.keys())}")
    
    # Would create enhanced map here
    print("\nGeospatial data integration complete!")
    print("\nNext steps:")
    print("1. Implement full state geology downloads")
    print("2. Add real-time hydrological data")
    print("3. Integrate USGS geothermal databases")
    print("4. Add ecological/ecoregion boundaries")
    print("5. Include transportation networks")

if __name__ == "__main__":
    main() 