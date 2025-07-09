#!/usr/bin/env python3
"""
Walla Walla Enhanced Geospatial Mapping
Columbia Plateau loess hills & wine country terroir geology
"""

import matplotlib.pyplot as plt
import numpy as np
import json
import time
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Polygon
import matplotlib.patheffects as path_effects
from scipy.ndimage import gaussian_filter

# Create cache directory
CACHE_DIR = Path('geospatial_cache')
CACHE_DIR.mkdir(exist_ok=True)

# Walla Walla study area bounds
WALLA_WALLA_BOUNDS = {
    'north': 46.15,
    'south': 46.0,
    'east': -118.2,
    'west': -118.6
}

# Key locations in Walla Walla
WALLA_WALLA_LOCATIONS = {
    'eritage_resort': {'lat': 46.0647, 'lon': -118.3430, 'name': 'Eritage Resort'},
    'downtown': {'lat': 46.0646, 'lon': -118.3430, 'name': 'Historic Downtown'},
    'whitman_college': {'lat': 46.0691, 'lon': -118.3267, 'name': 'Whitman College'},
    'fort_walla_walla': {'lat': 46.0454, 'lon': -118.3267, 'name': 'Fort Walla Walla'},
    'wine_district': {'lat': 46.0500, 'lon': -118.3600, 'name': 'Wine District'}
}

class WallaWallaGeoMapper:
    """Enhanced mapping for Walla Walla wine country with Columbia Plateau geology."""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        
    def get_elevation_data(self):
        """Generate realistic elevation data for Walla Walla Valley."""
        cache_file = self.cache_dir / 'walla_walla_elevation.json'
        
        if cache_file.exists():
            print("Loading cached elevation data...")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        print("Generating elevation data for Walla Walla...")
        
        # Create elevation grid
        lats = np.linspace(WALLA_WALLA_BOUNDS['south'], WALLA_WALLA_BOUNDS['north'], 40)
        lons = np.linspace(WALLA_WALLA_BOUNDS['west'], WALLA_WALLA_BOUNDS['east'], 50)
        
        elevations = np.zeros((40, 50))
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                # Valley floor base elevation (~350m/1150ft)
                base_elevation = 350
                
                # Walla Walla River runs northwest-southeast
                river_lat = 46.045 + (lon + 118.4) * 0.3  # River gradient
                dist_from_river = abs(lat - river_lat)
                
                # Gentle valley sides rising to rolling hills
                elevation = base_elevation + (dist_from_river * 800)  # Up to 280m rise
                
                # Blue Mountains influence from northeast
                if lat > 46.1 and lon > -118.3:
                    elevation += 200  # Blue Mountains foothills
                
                # Wine country rolling hills (loess deposits)
                hill_pattern = np.sin((lat - 46.05) * 20) * np.cos((lon + 118.4) * 15)
                elevation += hill_pattern * 50  # Rolling loess hills
                
                # Add realistic terrain variation
                elevation += np.random.normal(0, 15)
                
                # Keep river valley low
                if abs(lat - river_lat) < 0.005:
                    elevation = base_elevation + np.random.normal(0, 5)
                
                elevations[i, j] = max(elevation, base_elevation)
        
        # Moderate exaggeration for wine country topography
        elevations = elevations * 1.2
        
        elevation_data = {
            'elevations': elevations.tolist(),
            'lats': lats.tolist(),
            'lons': lons.tolist(),
            'bounds': WALLA_WALLA_BOUNDS
        }
        
        # Cache the data
        with open(cache_file, 'w') as f:
            json.dump(elevation_data, f)
        
        return elevation_data
    
    def get_geological_features(self):
        """Get geological features specific to Walla Walla Columbia Plateau."""
        cache_file = self.cache_dir / 'walla_walla_geology.json'
        
        geological_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Columbia River Basalt Group",
                        "age": "15.6-6.0 Ma",
                        "type": "flood_basalt",
                        "description": "Grande Ronde & Wanapum Basalt formations"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-118.6, 46.0], [-118.2, 46.0], 
                            [-118.2, 46.15], [-118.6, 46.15], 
                            [-118.6, 46.0]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Palouse Formation (Loess)",
                        "age": "2.6 Ma - Present",
                        "type": "wind_blown_sediment",
                        "description": "Glacial flour from Missoula Floods"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-118.5, 46.02], [-118.25, 46.02],
                            [-118.25, 46.12], [-118.5, 46.12],
                            [-118.5, 46.02]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Walla Walla River Alluvium",
                        "age": "Holocene",
                        "type": "fluvial_deposit",
                        "description": "Modern river terraces and floodplain"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-118.55, 46.04], [-118.3, 46.04],
                            [-118.3, 46.06], [-118.55, 46.06],
                            [-118.55, 46.04]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wine Terroir Zones",
                        "age": "Anthropocene",
                        "type": "agricultural_geology",
                        "description": "Basalt bedrock with loess soil perfect for viticulture"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-118.45, 46.03], [-118.32, 46.03],
                            [-118.32, 46.08], [-118.45, 46.08],
                            [-118.45, 46.03]
                        ]]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(geological_features, f)
        
        return geological_features
    
    def get_hydrological_features(self):
        """Get hydrological features of Walla Walla."""
        cache_file = self.cache_dir / 'walla_walla_hydrology.json'
        
        hydro_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Walla Walla River",
                        "type": "major_river",
                        "flow_direction": "northwest",
                        "importance": "Primary drainage for wine country"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-118.2, 46.02], [-118.35, 46.045],
                            [-118.5, 46.07], [-118.6, 46.10]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Mill Creek",
                        "type": "creek",
                        "flow_direction": "northwest",
                        "importance": "Historic water source"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-118.25, 46.03], [-118.32, 46.065],
                            [-118.38, 46.08]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Irrigation Channels",
                        "type": "agricultural_water",
                        "importance": "Wine country water management"
                    },
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [
                            [[-118.4, 46.035], [-118.35, 46.05]],
                            [[-118.42, 46.06], [-118.33, 46.07]]
                        ]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(hydro_features, f)
        
        return hydro_features
    
    def create_subglacial_texture(self, shape, intensity=0.25):
        """Create wind-blown loess and agricultural terrace texture."""
        height, width = shape
        
        # Create texture layers
        texture = np.zeros((height, width))
        
        # Large scale features - loess hills (gentle rolling)
        x = np.linspace(0, 4*np.pi, width)
        y = np.linspace(0, 4*np.pi, height)
        X, Y = np.meshgrid(x, y)
        
        # Loess hill patterns (gentle undulations)
        loess_hills = np.sin(X*1.5) * np.cos(Y*1.2) * 0.6
        
        # Agricultural terraces (human modification)
        terraces = np.sin(Y*8) * 0.2
        
        # Wind patterns (prevalent westerlies)
        wind_texture = np.sin((X - Y)*2) * 0.3
        
        # Combine patterns
        texture = loess_hills + terraces + wind_texture
        
        # Apply smoothing for gentle wine country topography
        texture = gaussian_filter(texture, sigma=1.5)
        
        # Normalize and apply intensity
        texture = (texture - texture.min()) / (texture.max() - texture.min())
        texture = texture * intensity
        
        return texture
    
    def create_wine_country_colormap(self):
        """Create custom colormap for Walla Walla wine country."""
        colors = [
            '#8B4513',  # Walla Walla River (brown)
            '#CD853F',  # Alluvial soils (sandy brown)
            '#DAA520',  # Loess hills (golden)
            '#9ACD32',  # Vineyard green (yellow-green)
            '#6B8E23',  # Wheat fields (olive)
            '#8FBC8F',  # Grassland (dark sea green)
            '#A0522D',  # Basalt bedrock (sienna)
            '#D2B48C'   # Dry hills (tan)
        ]
        return LinearSegmentedColormap.from_list('walla_walla', colors)
    
    def create_enhanced_map(self):
        """Create the complete enhanced Walla Walla wine country map."""
        print("Creating enhanced Walla Walla wine country map...")
        
        # Get all data layers
        elevation_data = self.get_elevation_data()
        geological_features = self.get_geological_features()
        hydro_features = self.get_hydrological_features()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(18, 12), dpi=200)
        
        # Get data arrays
        elevations = np.array(elevation_data['elevations'])
        lats = np.array(elevation_data['lats'])
        lons = np.array(elevation_data['lons'])
        
        # Create extent
        extent = (WALLA_WALLA_BOUNDS['west'], WALLA_WALLA_BOUNDS['east'], 
                 WALLA_WALLA_BOUNDS['south'], WALLA_WALLA_BOUNDS['north'])
        
        # Create custom colormap
        wine_cmap = self.create_wine_country_colormap()
        
        # Plot elevation with wine country colors
        terrain = ax.imshow(elevations, extent=extent, cmap=wine_cmap, 
                           alpha=0.9, interpolation='bilinear', aspect='auto')
        
        # Add loess texture overlay
        texture = self.create_subglacial_texture(elevations.shape, intensity=0.15)
        ax.imshow(texture, extent=extent, cmap='copper', alpha=0.3, 
                 interpolation='bilinear', aspect='auto')
        
        # Add gentle contour lines
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        contours = ax.contour(lon_grid, lat_grid, elevations, levels=8, 
                             colors='white', alpha=0.4, linewidths=0.6)
        
        # Plot geological features
        for feature in geological_features['features']:
            geom = feature['geometry']
            props = feature['properties']
            
            if geom['type'] == 'Polygon':
                coords = geom['coordinates'][0]
                polygon = Polygon(coords, alpha=0.25, 
                                facecolor=self._get_geology_color(props['type']),
                                edgecolor='black', linewidth=1)
                ax.add_patch(polygon)
                
                # Add label
                center_lon = np.mean([c[0] for c in coords])
                center_lat = np.mean([c[1] for c in coords])
                ax.text(center_lon, center_lat, props['name'], 
                       ha='center', va='center', fontsize=8, fontweight='bold',
                       color='white', 
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])
        
        # Plot hydrological features
        for feature in hydro_features['features']:
            geom = feature['geometry']
            props = feature['properties']
            
            if geom['type'] == 'LineString':
                coords = geom['coordinates']
                lons_river = [c[0] for c in coords]
                lats_river = [c[1] for c in coords]
                
                width = 4 if props['type'] == 'major_river' else 2
                ax.plot(lons_river, lats_river, color='#4169E1', linewidth=width, alpha=0.8)
                ax.plot(lons_river, lats_river, color='lightblue', linewidth=width-1, alpha=0.6)
            
            elif geom['type'] == 'MultiLineString':
                for line_coords in geom['coordinates']:
                    lons_line = [c[0] for c in line_coords]
                    lats_line = [c[1] for c in line_coords]
                    ax.plot(lons_line, lats_line, color='blue', linewidth=1, 
                           alpha=0.6, linestyle='--')
        
        # Add key locations
        for key, location in WALLA_WALLA_LOCATIONS.items():
            if key == 'eritage_resort':
                ax.plot(location['lon'], location['lat'], 'r*', markersize=18, 
                       markeredgecolor='white', markeredgewidth=2)
                ax.text(location['lon'], location['lat'] - 0.008, 'Eritage Resort',
                       ha='center', va='top', fontsize=12, fontweight='bold',
                       color='red',
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='white')])
            else:
                ax.plot(location['lon'], location['lat'], 'ko', markersize=8, 
                       markeredgecolor='white', markeredgewidth=1)
                ax.text(location['lon'], location['lat'] + 0.008, location['name'],
                       ha='center', va='bottom', fontsize=10, fontweight='bold',
                       color='black',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        # Add geological context annotations
        ax.text(-118.5, 46.13, 'BLUE MOUNTAINS\nFoothills', 
               ha='center', va='center', fontsize=12, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='darkblue', alpha=0.8))
        
        ax.text(-118.25, 46.02, 'COLUMBIA PLATEAU\nLoess Hills', 
               ha='center', va='center', fontsize=12, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='darkgreen', alpha=0.8))
        
        # Add wine region annotation
        ax.text(-118.38, 46.055, 'WALLA WALLA\nWine Country\nAVA', 
               ha='center', va='center', fontsize=11, fontweight='bold',
               color='gold', bbox=dict(boxstyle='round,pad=0.4', 
                                     facecolor='purple', alpha=0.8))
        
        # Style the map
        ax.set_xlim(WALLA_WALLA_BOUNDS['west'], WALLA_WALLA_BOUNDS['east'])
        ax.set_ylim(WALLA_WALLA_BOUNDS['south'], WALLA_WALLA_BOUNDS['north'])
        ax.set_aspect('equal')
        ax.set_facecolor('#2F4F4F')  # Dark slate gray base
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add comprehensive title
        fig.suptitle('Walla Walla Wine Country • Enhanced Geomorphological Context\n'
                    'Columbia Plateau Geology • Loess Hills • Basalt Bedrock Terroir • Agricultural Landscape', 
                    fontsize=16, fontweight='bold', color='white', y=0.95)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red', 
                      markersize=12, label='Eritage Resort'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                      markersize=8, label='Key Locations'),
            plt.Line2D([0], [0], color='#4169E1', linewidth=4, label='Walla Walla River'),
            plt.Line2D([0], [0], color='blue', linewidth=2, linestyle='--', label='Irrigation'),
            plt.Rectangle((0,0),1,1, facecolor='gold', alpha=0.3, label='Loess Deposits'),
            plt.Rectangle((0,0),1,1, facecolor='brown', alpha=0.3, label='Basalt Bedrock')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', 
                 facecolor='black', edgecolor='white', 
                 labelcolor='white', fontsize=9)
        
        # Save the enhanced map
        filename = "images/walla_walla_enhanced_geospatial.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#2F4F4F')
        plt.close()
        
        print(f"Enhanced Walla Walla map saved: {filename}")
        return filename
    
    def _get_geology_color(self, geology_type):
        """Get color for geological feature type."""
        colors = {
            'flood_basalt': '#8B4513',
            'wind_blown_sediment': '#DAA520',
            'fluvial_deposit': '#CD853F',
            'agricultural_geology': '#6B8E23'
        }
        return colors.get(geology_type, '#808080')

def main():
    """Create the enhanced Walla Walla wine country map."""
    mapper = WallaWallaGeoMapper()
    
    print("Walla Walla Wine Country Enhanced Geospatial Mapping")
    print("=" * 55)
    print("Integrating:")
    print("• Columbia Plateau basalt bedrock geology")
    print("• Palouse Formation loess hills")
    print("• Walla Walla River valley alluvium")
    print("• Wine terroir geological zones")
    print("• Agricultural landscape modifications")
    print("• Loess wind-blown sediment textures")
    print("")
    
    # Create the enhanced map
    filename = mapper.create_enhanced_map()
    
    print(f"\nEnhanced map created: {filename}")
    print("\nGeological Features Demonstrated:")
    print("• Columbia River Basalt Group - 15.6 Ma flood basalt foundation")
    print("• Palouse Formation - wind-blown glacial flour from Ice Age")
    print("• Loess hills - perfect wine growing terroir")
    print("• Walla Walla River - primary drainage system")
    print("• Agricultural terraces - human landscape modification")
    print("• Wine country geology - basalt bedrock with loess soils")

if __name__ == "__main__":
    main() 