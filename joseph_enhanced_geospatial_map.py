#!/usr/bin/env python3
"""
Joseph Enhanced Geospatial Mapping
Wallowa Mountains "Alps of Oregon" - alpine glacial terrain & granite batholith
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

# Joseph study area bounds - includes Wallowa Lake and surrounding peaks
JOSEPH_BOUNDS = {
    'north': 45.45,
    'south': 45.20,
    'east': -117.0,
    'west': -117.4
}

# Key locations in Joseph area
JOSEPH_LOCATIONS = {
    'jennings_hotel': {'lat': 45.3514, 'lon': -117.2314, 'name': 'The Jennings Hotel'},
    'downtown_joseph': {'lat': 45.3514, 'lon': -117.2314, 'name': 'Downtown Joseph'},
    'wallowa_lake': {'lat': 45.2738, 'lon': -117.2094, 'name': 'Wallowa Lake'},
    'chief_joseph_mtn': {'lat': 45.3200, 'lon': -117.1500, 'name': 'Chief Joseph Mountain'},
    'wallowa_lake_lodge': {'lat': 45.2738, 'lon': -117.2094, 'name': 'Wallowa Lake Lodge'},
    'valley_bronze': {'lat': 45.3520, 'lon': -117.2310, 'name': 'Valley Bronze'},
    'tramway_base': {'lat': 45.2800, 'lon': -117.1950, 'name': 'Tramway Base'}
}

class JosephGeoMapper:
    """Enhanced mapping for Joseph with Wallowa Mountains alpine glacial terrain."""
    
    def __init__(self):
        self.cache_dir = CACHE_DIR
        
    def get_elevation_data(self):
        """Generate realistic elevation data for Joseph and Wallowa Mountains."""
        cache_file = self.cache_dir / 'joseph_elevation.json'
        
        if cache_file.exists():
            print("Loading cached elevation data...")
            with open(cache_file, 'r') as f:
                return json.load(f)
        
        print("Generating elevation data for Joseph and Wallowa Mountains...")
        
        # Create elevation grid
        lats = np.linspace(JOSEPH_BOUNDS['south'], JOSEPH_BOUNDS['north'], 50)
        lons = np.linspace(JOSEPH_BOUNDS['west'], JOSEPH_BOUNDS['east'], 60)
        
        elevations = np.zeros((50, 60))
        
        for i, lat in enumerate(lats):
            for j, lon in enumerate(lons):
                # Valley floor base elevation (~1300m/4265ft)
                base_elevation = 1300
                
                # Joseph is in the valley center
                joseph_lat, joseph_lon = 45.3514, -117.2314
                
                # Distance from Joseph (valley center)
                dist_from_joseph = np.sqrt((lat - joseph_lat)**2 + (lon - joseph_lon)**2)
                
                # Wallowa Lake depression (glacial lake)
                lake_lat, lake_lon = 45.2738, -117.2094
                dist_from_lake = np.sqrt((lat - lake_lat)**2 + (lon - lake_lon)**2)
                
                # Base valley elevation
                elevation = base_elevation
                
                # Valley walls rising dramatically to alpine peaks
                if dist_from_joseph > 0.02:  # Outside immediate valley
                    # Steep granite walls
                    elevation += (dist_from_joseph ** 1.5) * 15000
                
                # Wallowa Lake depression (terminal moraine dam)
                if dist_from_lake < 0.02:
                    elevation = base_elevation - 50  # Lake level
                    
                # Major peaks (granite batholith)
                # Chief Joseph Mountain area
                if lat > 45.30 and lon > -117.20:
                    peak_effect = (lat - 45.30) * 8000 + (lon + 117.20) * 6000
                    elevation += peak_effect
                
                # Wallowa peaks to the south
                if lat < 45.30 and lon > -117.25:
                    alpine_effect = (45.30 - lat) * 10000 + (lon + 117.25) * 8000
                    elevation += alpine_effect
                
                # Glacial cirques (bowl-shaped depressions)
                cirque_pattern = np.sin((lat - 45.35) * 50) * np.cos((lon + 117.15) * 40)
                if elevation > 2000:  # High elevation areas
                    elevation += cirque_pattern * 200
                
                # Hanging valleys
                if lat > 45.35 and -117.2 < lon < -117.1:
                    hanging_valley = np.sin((lon + 117.15) * 30) * 300
                    elevation += hanging_valley
                
                # Add realistic terrain variation
                elevation += np.random.normal(0, 30)
                
                # Keep valley floor and lake relatively flat
                if dist_from_joseph < 0.01:
                    elevation = base_elevation + np.random.normal(0, 10)
                elif dist_from_lake < 0.01:
                    elevation = base_elevation - 50 + np.random.normal(0, 5)
                
                elevations[i, j] = max(elevation, base_elevation - 50)
        
        # Strong exaggeration for alpine drama
        elevations = elevations * 1.5
        
        elevation_data = {
            'elevations': elevations.tolist(),
            'lats': lats.tolist(),
            'lons': lons.tolist(),
            'bounds': JOSEPH_BOUNDS
        }
        
        # Cache the data
        with open(cache_file, 'w') as f:
            json.dump(elevation_data, f)
        
        return elevation_data
    
    def get_geological_features(self):
        """Get geological features specific to Joseph Wallowa Mountains."""
        cache_file = self.cache_dir / 'joseph_geology.json'
        
        geological_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wallowa Granite Batholith",
                        "age": "165 Ma",
                        "type": "granite_intrusion",
                        "description": "Jurassic granite intrusion - 'Alps of Oregon'"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.4, 45.20], [-117.0, 45.20], 
                            [-117.0, 45.45], [-117.4, 45.45], 
                            [-117.4, 45.20]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Alpine Glacial Cirques",
                        "age": "Pleistocene",
                        "type": "glacial_erosion",
                        "description": "Bowl-shaped amphitheaters carved by glaciers"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.25, 45.35], [-117.10, 45.35],
                            [-117.10, 45.42], [-117.25, 45.42],
                            [-117.25, 45.35]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wallowa Lake Terminal Moraine",
                        "age": "Late Pleistocene",
                        "type": "glacial_deposit",
                        "description": "Natural dam creating Wallowa Lake"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.23, 45.25], [-117.19, 45.25],
                            [-117.19, 45.28], [-117.23, 45.28],
                            [-117.23, 45.25]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Hanging Valleys",
                        "age": "Pleistocene",
                        "type": "glacial_erosion",
                        "description": "Tributary valleys left hanging by main glacier"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.20, 45.38], [-117.12, 45.38],
                            [-117.12, 45.42], [-117.20, 45.42],
                            [-117.20, 45.38]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Joseph Valley Floor",
                        "age": "Holocene",
                        "type": "alluvial_deposit",
                        "description": "Modern valley floor with historic settlement"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.25, 45.34], [-117.22, 45.34],
                            [-117.22, 45.37], [-117.25, 45.37],
                            [-117.25, 45.34]
                        ]]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(geological_features, f)
        
        return geological_features
    
    def get_hydrological_features(self):
        """Get hydrological features of Joseph area."""
        cache_file = self.cache_dir / 'joseph_hydrology.json'
        
        hydro_features = {
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wallowa Lake",
                        "type": "glacial_lake",
                        "area_acres": 1562,
                        "importance": "Glacial lake dammed by terminal moraine"
                    },
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [[
                            [-117.22, 45.26], [-117.20, 45.26],
                            [-117.20, 45.29], [-117.22, 45.29],
                            [-117.22, 45.26]
                        ]]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Wallowa River",
                        "type": "glacial_river",
                        "flow_direction": "northeast",
                        "importance": "Primary drainage from Wallowa Lake"
                    },
                    "geometry": {
                        "type": "LineString",
                        "coordinates": [
                            [-117.21, 45.28], [-117.22, 45.32],
                            [-117.23, 45.35], [-117.235, 45.38]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Alpine Waterfalls",
                        "type": "waterfall",
                        "importance": "Hanging valley cascades"
                    },
                    "geometry": {
                        "type": "MultiPoint",
                        "coordinates": [
                            [-117.15, 45.40], [-117.18, 45.38], [-117.13, 45.42]
                        ]
                    }
                },
                {
                    "type": "Feature",
                    "properties": {
                        "name": "Snowmelt Creeks",
                        "type": "seasonal_stream",
                        "importance": "Spring snowmelt from granite peaks"
                    },
                    "geometry": {
                        "type": "MultiLineString",
                        "coordinates": [
                            [[-117.12, 45.42], [-117.21, 45.28]],
                            [[-117.08, 45.40], [-117.20, 45.29]],
                            [[-117.15, 45.38], [-117.22, 45.30]]
                        ]
                    }
                }
            ]
        }
        
        with open(cache_file, 'w') as f:
            json.dump(hydro_features, f)
        
        return hydro_features
    
    def create_subglacial_texture(self, shape, intensity=0.3):
        """Create alpine glacial texture for Joseph area."""
        height, width = shape
        
        # Create texture layers
        texture = np.zeros((height, width))
        
        # Large scale features - glacial striations (valley orientation)
        x = np.linspace(0, 3*np.pi, width)
        y = np.linspace(0, 4*np.pi, height)
        X, Y = np.meshgrid(x, y)
        
        # Glacial striations (southwest to northeast)
        glacial_striae = np.sin((X + Y)*2) * 0.8
        
        # Granite exfoliation joints (concentric patterns)
        granite_joints = np.sin(X*8) * np.cos(Y*6) * 0.5
        
        # Cirque patterns (bowl-shaped)
        cirque_texture = np.sin(X*3) * np.sin(Y*4) * 0.4
        
        # Alpine scree patterns
        scree_texture = np.sin((X*2 + Y*3)*1.5) * 0.3
        
        # Combine patterns
        texture = glacial_striae + granite_joints + cirque_texture + scree_texture
        
        # Apply smoothing
        texture = gaussian_filter(texture, sigma=1.0)
        
        # Normalize and apply intensity
        texture = (texture - texture.min()) / (texture.max() - texture.min())
        texture = texture * intensity
        
        return texture
    
    def create_alpine_colormap(self):
        """Create custom colormap for Joseph alpine environment."""
        colors = [
            '#003f5c',  # Deep lake blue
            '#2f4b7c',  # Wallowa Lake
            '#665191',  # Valley forests
            '#a05195',  # Alpine meadows
            '#d45087',  # Granite walls
            '#f95d6a',  # High granite peaks
            '#ff7c43',  # Scree slopes
            '#ffa600',  # Summit granite
            '#ffffff'   # Snow and ice
        ]
        return LinearSegmentedColormap.from_list('joseph_alpine', colors)
    
    def create_enhanced_map(self):
        """Create the complete enhanced Joseph alpine map."""
        print("Creating enhanced Joseph alpine map...")
        
        # Get all data layers
        elevation_data = self.get_elevation_data()
        geological_features = self.get_geological_features()
        hydro_features = self.get_hydrological_features()
        
        # Create figure
        fig, ax = plt.subplots(figsize=(20, 14), dpi=200)
        
        # Get data arrays
        elevations = np.array(elevation_data['elevations'])
        lats = np.array(elevation_data['lats'])
        lons = np.array(elevation_data['lons'])
        
        # Create extent
        extent = (JOSEPH_BOUNDS['west'], JOSEPH_BOUNDS['east'], 
                 JOSEPH_BOUNDS['south'], JOSEPH_BOUNDS['north'])
        
        # Create custom colormap
        alpine_cmap = self.create_alpine_colormap()
        
        # Plot elevation with alpine colors
        terrain = ax.imshow(elevations, extent=extent, cmap=alpine_cmap, 
                           alpha=0.9, interpolation='bilinear', aspect='auto')
        
        # Add glacial texture overlay
        texture = self.create_subglacial_texture(elevations.shape, intensity=0.25)
        ax.imshow(texture, extent=extent, cmap='gray', alpha=0.4, 
                 interpolation='bilinear', aspect='auto')
        
        # Add dramatic contour lines for alpine relief
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        contours = ax.contour(lon_grid, lat_grid, elevations, levels=15, 
                             colors='white', alpha=0.6, linewidths=1.0)
        
        # Plot geological features
        for feature in geological_features['features']:
            geom = feature['geometry']
            props = feature['properties']
            
            if geom['type'] == 'Polygon':
                coords = geom['coordinates'][0]
                polygon = Polygon(coords, alpha=0.3, 
                                facecolor=self._get_geology_color(props['type']),
                                edgecolor='black', linewidth=1.5)
                ax.add_patch(polygon)
                
                # Add label for major features
                if props['type'] in ['granite_intrusion', 'glacial_erosion']:
                    center_lon = np.mean([c[0] for c in coords])
                    center_lat = np.mean([c[1] for c in coords])
                    ax.text(center_lon, center_lat, props['name'], 
                           ha='center', va='center', fontsize=10, fontweight='bold',
                           color='white', 
                           path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])
        
        # Plot hydrological features
        for feature in hydro_features['features']:
            geom = feature['geometry']
            props = feature['properties']
            
            if geom['type'] == 'Polygon':  # Wallowa Lake
                coords = geom['coordinates'][0]
                lake_polygon = Polygon(coords, facecolor='darkblue', 
                                     edgecolor='lightblue', linewidth=3, alpha=0.8)
                ax.add_patch(lake_polygon)
                
                # Lake label
                center_lon = np.mean([c[0] for c in coords])
                center_lat = np.mean([c[1] for c in coords])
                ax.text(center_lon, center_lat, 'WALLOWA\nLAKE', 
                       ha='center', va='center', fontsize=12, fontweight='bold',
                       color='white', 
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='darkblue')])
            
            elif geom['type'] == 'LineString':  # Wallowa River
                coords = geom['coordinates']
                lons_river = [c[0] for c in coords]
                lats_river = [c[1] for c in coords]
                
                ax.plot(lons_river, lats_river, color='#1E90FF', linewidth=6, alpha=0.9)
                ax.plot(lons_river, lats_river, color='lightblue', linewidth=4, alpha=0.8)
            
            elif geom['type'] == 'MultiLineString':  # Snowmelt creeks
                for line_coords in geom['coordinates']:
                    lons_line = [c[0] for c in line_coords]
                    lats_line = [c[1] for c in line_coords]
                    ax.plot(lons_line, lats_line, color='cyan', linewidth=2, alpha=0.7)
            
            elif geom['type'] == 'MultiPoint':  # Alpine waterfalls
                for point_coords in geom['coordinates']:
                    ax.plot(point_coords[0], point_coords[1], '*', color='cyan', 
                           markersize=12, markeredgecolor='white', markeredgewidth=1)
        
        # Add key locations
        for key, location in JOSEPH_LOCATIONS.items():
            if key == 'jennings_hotel':
                ax.plot(location['lon'], location['lat'], 'r*', markersize=20, 
                       markeredgecolor='white', markeredgewidth=2)
                ax.text(location['lon'], location['lat'] - 0.012, 'The Jennings Hotel',
                       ha='center', va='top', fontsize=13, fontweight='bold',
                       color='red',
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='white')])
            elif key == 'wallowa_lake':
                pass  # Already labeled with lake
            elif key == 'chief_joseph_mtn':
                ax.plot(location['lon'], location['lat'], '^', color='white', 
                       markersize=15, markeredgecolor='black', markeredgewidth=2)
                ax.text(location['lon'], location['lat'] + 0.012, 'Chief Joseph\nMountain',
                       ha='center', va='bottom', fontsize=11, fontweight='bold',
                       color='white',
                       path_effects=[path_effects.withStroke(linewidth=3, foreground='black')])
            else:
                ax.plot(location['lon'], location['lat'], 'ko', markersize=8, 
                       markeredgecolor='white', markeredgewidth=1)
                ax.text(location['lon'], location['lat'] + 0.008, location['name'],
                       ha='center', va='bottom', fontsize=9, fontweight='bold',
                       color='black',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        # Add geological context annotations
        ax.text(-117.05, 45.42, 'WALLOWA GRANITE\nBatholith\n165 Ma\n"Alps of Oregon"', 
               ha='center', va='center', fontsize=12, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.4', 
                                      facecolor='darkred', alpha=0.9))
        
        ax.text(-117.35, 45.22, 'GLACIAL VALLEY\nTerminal Moraine\nPleistocene Ice Age', 
               ha='center', va='center', fontsize=11, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.4', 
                                      facecolor='darkblue', alpha=0.9))
        
        ax.text(-117.17, 45.40, 'ALPINE CIRQUES\nGlacial Amphitheaters\nHanging Valleys', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='white', bbox=dict(boxstyle='round,pad=0.3', 
                                      facecolor='purple', alpha=0.9))
        
        # Add elevation reference
        ax.text(-117.08, 45.25, '4,000+ ft\nElevation\nGain', 
               ha='center', va='center', fontsize=10, fontweight='bold',
               color='yellow', bbox=dict(boxstyle='round,pad=0.3', 
                                       facecolor='green', alpha=0.8))
        
        # Style the map
        ax.set_xlim(JOSEPH_BOUNDS['west'], JOSEPH_BOUNDS['east'])
        ax.set_ylim(JOSEPH_BOUNDS['south'], JOSEPH_BOUNDS['north'])
        ax.set_aspect('equal')
        ax.set_facecolor('#0a0a0a')  # Near black base for alpine drama
        
        # Remove axes
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Add comprehensive title
        fig.suptitle('Joseph & Wallowa Mountains • Enhanced Alpine Geomorphological Context\n'
                    '"Alps of Oregon" • Granite Batholith • Glacial Cirques • Terminal Moraine Lake • Alpine Glacial Terrain', 
                    fontsize=17, fontweight='bold', color='white', y=0.95)
        
        # Add legend
        legend_elements = [
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='red', 
                      markersize=14, label='The Jennings Hotel'),
            plt.Line2D([0], [0], marker='^', color='w', markerfacecolor='white', 
                      markersize=12, label='Mountain Peaks'),
            plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='black', 
                      markersize=8, label='Town Features'),
            plt.Line2D([0], [0], color='#1E90FF', linewidth=4, label='Wallowa River'),
            plt.Line2D([0], [0], color='cyan', linewidth=2, label='Alpine Streams'),
            plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='cyan', 
                      markersize=10, label='Alpine Waterfalls'),
            plt.Rectangle((0,0),1,1, facecolor='darkblue', alpha=0.8, label='Wallowa Lake'),
            plt.Rectangle((0,0),1,1, facecolor='darkred', alpha=0.3, label='Granite Batholith'),
            plt.Rectangle((0,0),1,1, facecolor='purple', alpha=0.3, label='Glacial Cirques')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 facecolor='black', edgecolor='white', 
                 labelcolor='white', fontsize=10)
        
        # Save the enhanced map
        filename = "images/joseph_enhanced_geospatial.png"
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight', facecolor='#0a0a0a')
        plt.close()
        
        print(f"Enhanced Joseph map saved: {filename}")
        return filename
    
    def _get_geology_color(self, geology_type):
        """Get color for geological feature type."""
        colors = {
            'granite_intrusion': '#A0522D',
            'glacial_erosion': '#4169E1',
            'glacial_deposit': '#696969',
            'alluvial_deposit': '#CD853F'
        }
        return colors.get(geology_type, '#808080')

def main():
    """Create the enhanced Joseph alpine map."""
    mapper = JosephGeoMapper()
    
    print("Joseph Alpine Enhanced Geospatial Mapping")
    print("=" * 42)
    print("Integrating:")
    print("• Wallowa granite batholith (165 Ma)")
    print("• Alpine glacial cirques and hanging valleys")
    print("• Wallowa Lake terminal moraine")
    print("• Glacial striations and alpine terrain")
    print("• Joseph valley floor historic settlement")
    print("• 'Alps of Oregon' mountain environment")
    print("")
    
    # Create the enhanced map
    filename = mapper.create_enhanced_map()
    
    print(f"\nEnhanced map created: {filename}")
    print("\nGeological Features Demonstrated:")
    print("• Wallowa Granite - 165 Ma Jurassic granite batholith")
    print("• Alpine cirques - bowl-shaped glacial amphitheaters")
    print("• Wallowa Lake - glacial lake dammed by terminal moraine")
    print("• Hanging valleys - tributary valleys left hanging by main glacier")
    print("• Glacial striations - ice flow directional patterns")
    print("• Joseph valley - historic town in glacial valley floor")
    print("• Alpine waterfalls - cascades from hanging valleys")

if __name__ == "__main__":
    main() 