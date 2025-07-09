#!/usr/bin/env python3
"""
Lostine Enhanced Geospatial Mapping
Wallowa Mountains foothills - granite batholith & glacial valley
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Polygon
import matplotlib.patheffects as path_effects
from scipy.ndimage import gaussian_filter

# Create cache directory
CACHE_DIR = Path('geospatial_cache')
CACHE_DIR.mkdir(exist_ok=True)

# Lostine study area bounds (smaller scope as specified)
LOSTINE_BOUNDS = {
    'north': 45.45,
    'south': 45.35,
    'east': -117.35,
    'west': -117.50
}

# Key locations in Lostine
LOSTINE_LOCATIONS = {
    'town_center': {'lat': 45.4055, 'lon': -117.4255, 'name': 'Lostine Town'},
    'mcrow_store': {'lat': 45.4055, 'lon': -117.4255, 'name': 'M. Crow & Co.'},
    'lostine_tavern': {'lat': 45.4050, 'lon': -117.4250, 'name': 'Lostine Tavern'},
    'river_access': {'lat': 45.4000, 'lon': -117.4200, 'name': 'River Access'},
    'wallowa_foothills': {'lat': 45.4200, 'lon': -117.3800, 'name': 'Wallowa Foothills'}
}

class LostineGeoMapper:
    """Enhanced mapping for Lostine glacial valley with Wallowa granite geology."""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        
    def get_elevation_data(self):
        """Generate realistic elevation data for Lostine glacial valley."""
        cache_file = self.cache_dir / 'lostine_elevation.json'
        
        if cache_file.exists():
            print("Loading cached elevation data...")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        print("Generating elevation data for Lostine glacial valley...")
        
        # Create elevation grid
        lats = np.linspace(LOSTINE_BOUNDS['south'], LOSTINE_BOUNDS['north'], 30)
        lons = np.linspace(LOSTINE_BOUNDS['west'], LOSTINE_BOUNDS['east'], 40)
        
        elevations = np.zeros((30, 40))
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                # Valley floor base elevation (~1000m/3280ft)
                base_elevation = 1000
                
                # Lostine River runs north-south through valley center
                river_lon = -117.425
                dist_from_river = abs(lon - river_lon)
                
                # U-shaped glacial valley profile
                # Valley walls rise steeply to granite peaks
                valley_elevation = base_elevation + (dist_from_river ** 2) * 8000
                
                # Wallowa granite peaks to the east (getting higher)
                if lon > -117.4:
                    mountain_effect = (lon + 117.4) * 4000  # Rising to granite peaks
                    valley_elevation += mountain_effect
                
                # Foothills to the west (more gradual)
                if lon < -117.45:
                    foothill_effect = (-117.45 - lon) * 2000
                    valley_elevation += foothill_effect
                
                # Glacial valley floor terraces
                if dist_from_river < 0.01:  # Near river
                    # Alluvial terraces
                    terrace_pattern = np.sin((lat - 45.4) * 100) * 50
                    valley_elevation = base_elevation + terrace_pattern
                
                # Add realistic terrain variation
                valley_elevation += np.random.normal(0, 25)
                
                # Ensure valley floor stays relatively flat
                if dist_from_river < 0.005:
                    valley_elevation = base_elevation + np.random.normal(0, 10)
                
                elevations[i, j] = max(valley_elevation, base_elevation)
        
        # Moderate exaggeration for glacial valley effect
        elevations = elevations * 1.3
        
        elevation_data = {
            'elevations': elevations.tolist(),
            'lats': lats.tolist(),
            'lons': lons.tolist(),
            'bounds': LOSTINE_BOUNDS
        }
        
        # Cache the data
        with open(cache_file, 'w') as f:
            json.dump(elevation_data, f)
        
        return elevation_data
    
    def get_geological_features(self):
        """Get geological features specific to Lostine Wallowa granite."""
        cache_file = self.cache_dir / 'lostine_geology.json'
        
        geological_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wallowa Granite Batholith",
                        "age": "165-150 Ma",
                        "type": "granite_intrusion",
                        "description": "Jurassic granite intrusion - 'Alps of Oregon'"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.45, 45.35], [-117.35, 45.35], 
                            [-117.35, 45.45], [-117.45, 45.45], 
                            [-117.45, 45.35]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Glacial Valley Floor",
                        "age": "Pleistocene",
                        "type": "glacial_erosion",
                        "description": "U-shaped valley carved by alpine glaciers"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.44, 45.38], [-117.41, 45.38],
                            [-117.41, 45.43], [-117.44, 45.43],
                            [-117.44, 45.38]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Alluvial Terraces",
                        "age": "Holocene",
                        "type": "fluvial_deposit",
                        "description": "Modern river terraces on valley floor"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.43, 45.40], [-117.42, 45.40],
                            [-117.42, 45.41], [-117.43, 45.41],
                            [-117.43, 45.40]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Glacial Moraines",
                        "age": "Late Pleistocene",
                        "type": "glacial_deposit",
                        "description": "Terminal and lateral moraines"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.44, 45.36], [-117.40, 45.36],
                            [-117.40, 45.38], [-117.44, 45.38],
                            [-117.44, 45.36]
                        ]]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(geological_features, f)
        
        return geological_features
    
    def get_hydrological_features(self):
        """Get hydrological features of Lostine valley."""
        cache_file = self.cache_dir / 'lostine_hydrology.json'
        
        hydro_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Lostine River",
                        "type": "alpine_river",
                        "flow_direction": "north",
                        "importance": "Primary drainage from Wallowa peaks"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-117.425, 45.35], [-117.425, 45.38],
                            [-117.425, 45.42], [-117.425, 45.45]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Seasonal Creeks",
                        "type": "tributary",
                        "importance": "Spring snowmelt drainage"
                    },
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [
                            [[-117.40, 45.42], [-117.425, 45.41]],
                            [[-117.45, 45.40], [-117.425, 45.405]]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Alpine Springs",
                        "type": "groundwater",
                        "importance": "Granite bedrock springs"
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [-117.40, 45.42]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(hydro_features, f)
        
        return hydro_features
    
    def create_subglacial_texture(self, shape, intensity=0.3):
        """Create glacial valley texture for Lostine."""
        height, width = shape
        
        # Create texture layers
        texture = np.zeros((height, width))
        
        # Large scale features - glacial striations (north-south)
        x = np.linspace(0, 2*np.pi, width)
        y = np.linspace(0, 4*np.pi, height)
        X, Y = np.meshgrid(x, y)
        
        # Glacial striations (north-south valley orientation)
        glacial_striae = np.sin(Y*3) * 0.7
        
        # Granite joint patterns (blocky)
        granite_joints = np.sin(X*6) * np.cos(Y*4) * 0.4
        
        # U-shaped valley profile texture
        valley_texture = np.sin(X*2) * 0.3
        
        # Combine patterns
        texture = glacial_striae + granite_joints + valley_texture
        
        # Apply smoothing
        texture = gaussian_filter(texture, sigma=1.0)
        
        # Normalize and apply intensity
        texture = (texture - texture.min()) / (texture.max() - texture.min())
        texture = texture * intensity
        
        return texture
    
    def create_alpine_colormap(self):
        """Create custom colormap for Lostine alpine valley."""
        colors = [
            '#4169E1',  # Lostine River (royal blue)
            '#87CEEB',  # Valley floor (sky blue)
            '#228B22',  # Riparian vegetation (forest green)
            '#9ACD32',  # Meadows (yellow green)
            '#CD853F',  # Granite outcrops (peru)
            '#A0522D',  # Granite peaks (sienna)
            '#696969',  # High granite (dim gray)
            '#F5F5DC'   # Snow patches (beige)
        ]
        return LinearSegmentedColormap.from_list('lostine_alpine', colors)
    
    def create_enhanced_map(self):
        """Create the complete enhanced Lostine glacial valley map."""
        print("Creating enhanced Lostine glacial valley map...")
        
        # Get all data layers
        elevation_data = self.get_elevation_data()
        geological_features = self.get_geological_features()
        hydro_features = self.get_hydrological_features()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(16, 10), dpi=200)
        
        # Get data arrays
        elevations = np.array(elevation_data['elevations'])
        lats = np.array(elevation_data['lats'])
        lons = np.array(elevation_data['lons'])
        
        # Create extent
        extent = (LOSTINE_BOUNDS['west'], LOSTINE_BOUNDS['east'], 
                 LOSTINE_BOUNDS['south'], LOSTINE_BOUNDS['north'])
        
        # Create custom colormap
        alpine_cmap = self.create_alpine_colormap()
        
        # Plot elevation with alpine colors
        terrain = ax.imshow(elevations, extent=extent, cmap=alpine_cmap, 
                           alpha=0.9, interpolation='bilinear', aspect='auto')
        
        # Add glacial texture overlay
        texture = self.create_subglacial_texture(elevations.shape, intensity=0.2)
        ax.imshow(texture, extent=extent, cmap='gray', alpha=0.3, 
                 interpolation='bilinear', aspect='auto')
        
        # Add contour lines for U-shaped valley
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        contours = ax.contour(lon_grid, lat_grid, elevations, levels=10, 
                             colors='white', alpha=0.5, linewidths=0.8)
        
        # Plot geological features
        for feature in geological_features['features']:
            geom = feature['geometry']
            props = feature['properties']
            
            if geom['type'] == 'Polygon':
                coords = geom['coordinates'][0]
                polygon = Polygon(coords, alpha=0.3, 
                                facecolor=self._get_geology_color(props['type']),
                                edgecolor='black', linewidth=1)
                ax.add_patch(polygon)
                
                # Add label for major features
                if props['type'] in ['granite_intrusion', 'glacial_erosion']:
                    center_lon = np.mean([c[0] for c in coords])
                    center_lat = np.mean([c[1] for c in coords])
                    ax.text(center_lon, center_lat, props['name'], 
                           ha='center', va='center', fontsize=9, fontweight='bold',
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
                
                # Lostine River - prominent alpine stream
                ax.plot(lons_river, lats_river, color='#1E90FF', linewidth=5, alpha=0.8)
                ax.plot(lons_river, lats_river, color='lightblue', linewidth=3, alpha=0.7)
            
            elif geom['type'] == 'MultiLineString':
                for line_coords in geom['coordinates']:
                    lons_line = [c[0] for c in line_coords]
                    lats_line = [c[1] for c in line_coords]
                    ax.plot(lons_line, lats_line, color='cyan', linewidth=2, alpha=0.6)
            
            elif geom['type'] == 'Point':
                coords = geom['coordinates']
                ax.plot(coords[0], coords[1], 'o', color='aqua', markersize=8, 
                       markeredgecolor='blue', markeredgewidth=1)
        
        # Add key locations
        for key, location in LOSTINE_LOCATIONS.items():
            if key == 'mcrow_store':
                ax.plot(location['lon'], location['lat'], 'r*', markersize=16, 
                       markeredgecolor='white', markeredgewidth=2)
                ax.text(location['lon'], location['lat'] - 0.006, 'M. Crow & Co.',
                       ha='center', va='top', fontsize=11, fontweight='bold',
                       color='red',
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='white')])
            else:
                ax.plot(location['lon'], location['lat'], 'ko', markersize=6, 
                       markeredgecolor='white', markeredgewidth=1)
                ax.text(location['lon'], location['lat'] + 0.006, location['name'],
                       ha='center', va='bottom', fontsize=9, fontweight='bold',
                       color='black',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        # Add geological context annotations
        ax.text(-117.37, 45.44, 'WALLOWA GRANITE\nBatholith\n165 Ma', 
               ha='center', va='center', fontsize=11, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='darkred', alpha=0.8))
        
        ax.text(-117.47, 45.37, 'GLACIAL VALLEY\nU-Shaped Profile\nPleistocene', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='darkblue', alpha=0.8))
        
        # Add directional indicator
        ax.text(-117.36, 45.36, 'To Wallowa\nPeaks →', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='yellow', bbox=dict(boxstyle='round,pad=0.3', 
                                       facecolor='green', alpha=0.8))
        
        # Style the map
        ax.set_xlim(LOSTINE_BOUNDS['west'], LOSTINE_BOUNDS['east'])
        ax.set_ylim(LOSTINE_BOUNDS['south'], LOSTINE_BOUNDS['north'])
        ax.set_aspect('equal')
        ax.set_facecolor('#1e3d59')  # Dark blue base
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add comprehensive title
        fig.suptitle('Lostine Glacial Valley • Enhanced Geomorphological Context\n'
                    'Wallowa Granite Batholith • U-Shaped Valley • Alpine Glacial Carving • Mountain Town', 
                    fontsize=15, fontweight='bold', color='white', y=0.95)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red', 
                      markersize=12, label='M. Crow & Co.'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                      markersize=8, label='Town Features'),
            plt.Line2D([0], [0], color='#1E90FF', linewidth=4, label='Lostine River'),
            plt.Line2D([0], [0], color='cyan', linewidth=2, label='Seasonal Creeks'),
            plt.Rectangle((0,0),1,1, facecolor='darkred', alpha=0.3, label='Granite Batholith'),
            plt.Rectangle((0,0),1,1, facecolor='darkblue', alpha=0.3, label='Glacial Valley')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 facecolor='black', edgecolor='white', 
                 labelcolor='white', fontsize=9)
        
        # Save the enhanced map
        filename = "images/lostine_enhanced_geospatial.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#1e3d59')
        plt.close()
        
        print(f"Enhanced Lostine map saved: {filename}")
        return filename
    
    def _get_geology_color(self, geology_type):
        """Get color for geological feature type."""
        colors = {
            'granite_intrusion': '#A0522D',
            'glacial_erosion': '#4169E1',
            'fluvial_deposit': '#CD853F',
            'glacial_deposit': '#696969'
        }
        return colors.get(geology_type, '#808080')

def main():
    """Create the enhanced Lostine glacial valley map."""
    mapper = LostineGeoMapper()
    
    print("Lostine Glacial Valley Enhanced Geospatial Mapping")
    print("=" * 50)
    print("Integrating:")
    print("• Wallowa granite batholith (165 Ma)")
    print("• U-shaped glacial valley profile")
    print("• Lostine River alpine drainage")
    print("• Glacial striations and moraines")
    print("• Historic mountain town setting")
    print("• Alpine to valley floor transitions")
    print("")
    
    # Create the enhanced map
    filename = mapper.create_enhanced_map()
    
    print(f"\nEnhanced map created: {filename}")
    print("\nGeological Features Demonstrated:")
    print("• Wallowa Granite - 165 Ma Jurassic granite intrusion")
    print("• Glacial valley - U-shaped profile carved by ice")
    print("• Lostine River - primary alpine drainage")
    print("• Glacial moraines - Pleistocene ice deposits")
    print("• Valley floor terraces - Holocene alluvial deposits")
    print("• Mountain town - historic settlement on granite")

if __name__ == "__main__":
    main() 