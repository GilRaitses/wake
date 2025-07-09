#!/usr/bin/env python3
"""
Enhanced Geospatial Mapping: McCall, Idaho
Payette Lake glacial cirque and Brundage Mountain geology

Geological Context:
- Payette Lake - Glacial cirque lake in glacially carved valley
- Brundage Mountain - Idaho Batholith granite (Mesozoic)
- Payette National Forest - Granitic terrain with glacial sculpturing
- Valley glaciation - U-shaped valley morphology from Pleistocene glaciation
- Modern alpine environment with remnant glacial features
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Polygon, Rectangle
import matplotlib.patheffects as path_effects
from scipy.ndimage import gaussian_filter
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# McCall location bounds
MCCALL_BOUNDS = {
    'north': 44.95,
    'south': 44.85,
    'east': -116.05,
    'west': -116.15
}

class McCallGeoMapper:
    def __init__(self):
        self.cache_dir = Path('geospatial_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_elevation_data(self):
        """Generate realistic elevation data based on McCall alpine geology."""
        # Payette Lake ~5,000 ft, surrounding peaks ~7,000-8,000 ft
        lons = np.linspace(MCCALL_BOUNDS['west'], MCCALL_BOUNDS['east'], 400)
        lats = np.linspace(MCCALL_BOUNDS['south'], MCCALL_BOUNDS['north'], 300)
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Base elevation - McCall valley
        base_elevation = np.full_like(lon_grid, 5000)
        
        # Payette Lake (slightly lower)
        lake_center_lon, lake_center_lat = -116.10, 44.90
        lake_radius = 0.025
        lake_mask = ((lon_grid - lake_center_lon)**2 + (lat_grid - lake_center_lat)**2) < lake_radius**2
        base_elevation[lake_mask] = 4980
        
        # Brundage Mountain (west side)
        brundage_center_lon, brundage_center_lat = -116.13, 44.92
        brundage_distance = np.sqrt((lon_grid - brundage_center_lon)**2 + (lat_grid - brundage_center_lat)**2)
        brundage_elevation = 2500 * np.exp(-brundage_distance**2 / 0.002)
        base_elevation += brundage_elevation
        
        # East side mountains
        east_mountains = (lon_grid > -116.08) & (lat_grid > 44.87)
        east_distance = np.sqrt((lon_grid[east_mountains] + 116.06)**2 + (lat_grid[east_mountains] - 44.92)**2)
        east_elevation = 1800 * np.exp(-east_distance**2 / 0.003)
        base_elevation[east_mountains] += east_elevation
        
        # North side ridges
        north_ridges = (lat_grid > 44.92) & (lon_grid < -116.08)
        north_distance = np.sqrt((lon_grid[north_ridges] + 116.11)**2 + (lat_grid[north_ridges] - 44.94)**2)
        north_elevation = 1500 * np.exp(-north_distance**2 / 0.004)
        base_elevation[north_ridges] += north_elevation
        
        # South side slopes
        south_slopes = (lat_grid < 44.88) & (lon_grid > -116.12)
        south_distance = np.sqrt((lon_grid[south_slopes] + 116.09)**2 + (lat_grid[south_slopes] - 44.86)**2)
        south_elevation = 1200 * np.exp(-south_distance**2 / 0.005)
        base_elevation[south_slopes] += south_elevation
        
        # Add realistic topographic noise
        noise = np.random.normal(0, 80, base_elevation.shape)
        elevation = base_elevation + gaussian_filter(noise, sigma=2)
        
        return lon_grid, lat_grid, elevation
    
    def get_geological_features(self):
        """Define geological formations for McCall area."""
        return {
            'idaho_batholith': {
                'description': 'Idaho Batholith granite',
                'color': '#CD853F',
                'age': 'Mesozoic (100-80 Ma)',
                'bounds': [(-116.15, 44.85), (-116.05, 44.95)]
            },
            'glacial_cirque': {
                'description': 'Glacial cirque deposits',
                'color': '#B8860B',
                'age': 'Pleistocene (~20,000 years)',
                'bounds': [(-116.13, 44.88), (-116.07, 44.92)]
            },
            'quaternary_alluvium': {
                'description': 'Modern lake and stream deposits',
                'color': '#F4A460',
                'age': 'Holocene (recent)',
                'bounds': [(-116.12, 44.89), (-116.08, 44.91)]
            },
            'alpine_drift': {
                'description': 'Glacial drift and moraines',
                'color': '#DEB887',
                'age': 'Pleistocene (~15,000 years)',
                'bounds': [(-116.14, 44.87), (-116.06, 44.93)]
            }
        }
    
    def get_hydrological_features(self):
        """Define water features for McCall area."""
        return {
            'payette_lake': {
                'type': 'glacial_lake',
                'center': (-116.10, 44.90),
                'radius': 0.025,
                'description': 'Payette Lake - glacial cirque lake'
            },
            'payette_river': {
                'type': 'outlet_river',
                'coordinates': [(-116.08, 44.88), (-116.06, 44.86)],
                'description': 'Payette River outlet'
            },
            'lake_fork': {
                'type': 'creek',
                'coordinates': [(-116.12, 44.93), (-116.10, 44.91)],
                'description': 'Lake Fork Creek'
            },
            'brundage_creek': {
                'type': 'creek',
                'coordinates': [(-116.13, 44.92), (-116.11, 44.90)],
                'description': 'Brundage Creek'
            }
        }
    
    def create_subglacial_texture(self, shape, intensity=0.3):
        """Create alpine glacial and cirque-specific textures."""
        # Glacial cirque textures - radial scouring patterns
        y, x = np.mgrid[0:shape[0], 0:shape[1]]
        center_y, center_x = shape[0] // 2, shape[1] // 2
        
        # Radial glacial flow patterns
        angle = np.arctan2(y - center_y, x - center_x)
        radius = np.sqrt((y - center_y)**2 + (x - center_x)**2)
        
        # Cirque scouring texture
        cirque_texture = np.sin(angle * 8) * np.exp(-radius / 50) * 0.4
        
        # U-shaped valley texture
        valley_texture = np.sin(x * 0.05) * np.exp(-np.abs(y - center_y) / 20) * 0.3
        
        # Combine textures
        combined_texture = cirque_texture + valley_texture
        
        return gaussian_filter(combined_texture, sigma=2.0) * intensity
    
    def create_enhanced_map(self):
        """Create the complete enhanced McCall map."""
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(18, 12))
        fig.patch.set_facecolor('#0F1419')
        ax.set_facecolor('#0F1419')
        
        # Get data
        lon_grid, lat_grid, elevation = self.get_elevation_data()
        geological_features = self.get_geological_features()
        hydrological_features = self.get_hydrological_features()
        
        # Create subglacial texture
        texture = self.create_subglacial_texture(elevation.shape, intensity=0.28)
        
        # Enhanced elevation with texture
        enhanced_elevation = elevation + texture * 250
        
        # Create alpine colormap
        alpine_colors = ['#0F1419', '#1A2B3D', '#2D4A5C', '#4A6741', '#6B8E23', '#8FBC8F', '#F0E68C', '#FFFFFF']
        alpine_cmap = LinearSegmentedColormap.from_list('alpine', alpine_colors, N=256)
        
        # Plot enhanced elevation
        elevation_plot = ax.contourf(lon_grid, lat_grid, enhanced_elevation, 
                                   levels=50, cmap=alpine_cmap, alpha=0.6)
        
        # Add Payette Lake
        lake_data = hydrological_features['payette_lake']
        lake_circle = Circle(lake_data['center'], lake_data['radius'], 
                           facecolor='#4A90E2', alpha=0.6, edgecolor='#2E5BDA', linewidth=1.5)
        ax.add_patch(lake_circle)
        
        # Add geological formation overlays
        for formation, data in geological_features.items():
            if formation == 'glacial_cirque':
                # Special highlighting for glacial cirque
                bounds = data['bounds']
                rect = Rectangle((bounds[0][0], bounds[0][1]), 
                               bounds[1][0] - bounds[0][0], 
                               bounds[1][1] - bounds[0][1],
                               facecolor=data['color'], alpha=0.15, 
                               edgecolor=data['color'], linewidth=1.5,
                               linestyle='-')
                ax.add_patch(rect)
        
        # Add hydrological features
        for feature, data in hydrological_features.items():
            if data['type'] == 'outlet_river':
                coords = data['coordinates']
                ax.plot([coords[0][0], coords[1][0]], [coords[0][1], coords[1][1]], 
                       color='#4A90E2', linewidth=4, alpha=0.8, label='Payette River')
            elif data['type'] == 'creek':
                coords = data['coordinates']
                ax.plot([coords[0][0], coords[1][0]], [coords[0][1], coords[1][1]], 
                       color='#4A90E2', linewidth=2, alpha=0.6)
        
        # Add key locations
        locations = {
            'McCall Downtown': (-116.099, 44.901),
            'Shore Lodge': (-116.095, 44.895),
            'Brundage Mountain': (-116.13, 44.92),
            'Payette Lake': (-116.10, 44.90),
            'Payette National Forest': (-116.12, 44.93)
        }
        
        for name, (lon, lat) in locations.items():
            if name == 'Shore Lodge':
                # Hotel marker
                ax.plot(lon, lat, 'o', color='#FF6B6B', markersize=12, 
                       markeredgecolor='white', markeredgewidth=2, zorder=10)
                ax.text(lon + 0.008, lat + 0.008, name, fontsize=11, 
                       fontweight='bold', color='white',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
            elif name == 'Payette Lake':
                # Lake label
                ax.text(lon, lat - 0.015, name, fontsize=12, 
                       fontweight='bold', color='#4A90E2', ha='center',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
            else:
                ax.plot(lon, lat, 'o', color='#FFF', markersize=8, 
                       markeredgecolor='black', markeredgewidth=1, zorder=10)
                ax.text(lon + 0.008, lat + 0.003, name, fontsize=10, 
                       color='white', fontweight='bold',
                       path_effects=[path_effects.withStroke(linewidth=1.5, foreground='black')])
        
        # Add geological story annotations
        ax.text(-116.14, 44.94, 'GLACIAL CIRQUE LAKE', 
               fontsize=16, fontweight='bold', color='#B8860B',
               path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
        
        ax.text(-116.14, 44.92, 'Alpine glaciation\n~20,000 years ago\nU-shaped valley', 
               fontsize=11, color='white', fontweight='bold',
               path_effects=[path_effects.withStroke(linewidth=1.5, foreground='black')])
        
        # Add elevation contours
        contour_lines = ax.contour(lon_grid, lat_grid, enhanced_elevation, 
                                 levels=15, colors='white', alpha=0.3, linewidths=0.5)
        
        # Set map bounds and labels
        ax.set_xlim(MCCALL_BOUNDS['west'], MCCALL_BOUNDS['east'])
        ax.set_ylim(MCCALL_BOUNDS['south'], MCCALL_BOUNDS['north'])
        ax.set_xlabel('Longitude', fontsize=12, color='white', fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, color='white', fontweight='bold')
        ax.set_title('MCCALL, IDAHO\nPayette Lake Glacial Cirque & Idaho Batholith', 
                    fontsize=20, fontweight='bold', color='white', pad=20)
        
        # Create legend
        legend_elements = [
            mpatches.Patch(color='#CD853F', alpha=0.7, label='Idaho Batholith Granite'),
            mpatches.Patch(color='#B8860B', alpha=0.7, label='Glacial Cirque'),
            mpatches.Patch(color='#DEB887', alpha=0.7, label='Glacial Drift'),
            mpatches.Patch(color='#4A90E2', alpha=0.8, label='Payette Lake'),
            Line2D([0], [0], color='#4A90E2', linewidth=3, label='Payette River'),
            Line2D([0], [0], marker='o', color='#FF6B6B', markersize=10, 
                      label='Shore Lodge', linestyle='None')
        ]
        
        ax.legend(handles=legend_elements, loc='lower right', 
                 fancybox=True, shadow=True, fontsize=11,
                 facecolor='black', edgecolor='white', framealpha=0.6)
        
        # Style the axes
        ax.tick_params(colors='white', labelsize=10)
        for spine in ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Save the map
        filename = 'images/mccall_enhanced_geospatial.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        print(f"Enhanced McCall map saved: {filename}")
        return filename

def main():
    mapper = McCallGeoMapper()
    filename = mapper.create_enhanced_map()
    print(f"Enhanced McCall map created: {filename}")

if __name__ == "__main__":
    main() 