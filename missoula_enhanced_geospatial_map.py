#!/usr/bin/env python3
"""
Enhanced Geospatial Mapping: Missoula, Montana
Glacial Lake Missoula deposits and Clark Fork River valley

Geological Context:
- Glacial Lake Missoula - Massive ice-dammed lake (Late Pleistocene)
- Missoula Floods - Catastrophic drainage events (~15,000 years ago)
- Clark Fork River - Modern drainage following flood scablands
- Surrounding mountains - Belt Supergroup and Precambrian rocks
- Quaternary lake sediments and flood deposits
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

# Missoula location bounds
MISSOULA_BOUNDS = {
    'north': 46.95,
    'south': 46.80,
    'east': -113.85,
    'west': -114.15
}

class MissoulaGeoMapper:
    def __init__(self):
        self.cache_dir = Path('geospatial_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
    def get_elevation_data(self):
        """Generate realistic elevation data based on Missoula valley geology."""
        # Missoula valley floor ~3,200 ft, surrounding mountains ~6,000-7,000 ft
        lons = np.linspace(MISSOULA_BOUNDS['west'], MISSOULA_BOUNDS['east'], 400)
        lats = np.linspace(MISSOULA_BOUNDS['south'], MISSOULA_BOUNDS['north'], 300)
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Base elevation - Missoula valley
        base_elevation = np.full_like(lon_grid, 3200)
        
        # Clark Fork River valley (lower elevation)
        river_mask = (lat_grid > 46.85) & (lat_grid < 46.88) & (lon_grid > -114.05) & (lon_grid < -113.95)
        base_elevation[river_mask] = 3150
        
        # Surrounding mountains
        # Rattlesnake Mountains (north)
        north_mountains = (lat_grid > 46.90) & (lon_grid > -114.05)
        base_elevation[north_mountains] += 2000 + 1000 * np.exp(-(lat_grid[north_mountains] - 46.92)**2 / 0.001)
        
        # Bitterroot Mountains (south)
        south_mountains = (lat_grid < 46.84) & (lon_grid < -114.00)
        base_elevation[south_mountains] += 1500 + 800 * np.exp(-(lat_grid[south_mountains] - 46.82)**2 / 0.001)
        
        # Sapphire Mountains (east)
        east_mountains = (lon_grid > -113.95) & (lat_grid > 46.85)
        base_elevation[east_mountains] += 1000 + 600 * np.exp(-(lon_grid[east_mountains] + 113.90)**2 / 0.001)
        
        # University of Montana area (slight elevation)
        university_area = (lat_grid > 46.86) & (lat_grid < 46.87) & (lon_grid > -114.00) & (lon_grid < -113.98)
        base_elevation[university_area] += 100
        
        # Add topographic noise
        noise = np.random.normal(0, 50, base_elevation.shape)
        elevation = base_elevation + gaussian_filter(noise, sigma=2)
        
        return lon_grid, lat_grid, elevation
    
    def get_geological_features(self):
        """Define geological formations for Missoula area."""
        return {
            'glacial_lake_deposits': {
                'description': 'Glacial Lake Missoula sediments',
                'color': '#B8860B',
                'age': 'Late Pleistocene (~15,000 years)',
                'bounds': [(-114.10, 46.82), (-113.90, 46.90)]
            },
            'belt_supergroup': {
                'description': 'Belt Supergroup metamorphic rocks',
                'color': '#8B4513',
                'age': 'Mesoproterozoic (1.4-1.0 Ga)',
                'bounds': [(-114.15, 46.90), (-113.85, 46.95)]
            },
            'flood_deposits': {
                'description': 'Missoula Flood scablands',
                'color': '#CD853F',
                'age': 'Late Pleistocene (~15,000 years)',
                'bounds': [(-114.05, 46.85), (-113.95, 46.88)]
            },
            'quaternary_alluvium': {
                'description': 'Modern river deposits',
                'color': '#F4A460',
                'age': 'Holocene (recent)',
                'bounds': [(-114.08, 46.85), (-113.92, 46.89)]
            }
        }
    
    def get_hydrological_features(self):
        """Define water features for Missoula area."""
        return {
            'clark_fork_river': {
                'type': 'major_river',
                'coordinates': [(-114.05, 46.86), (-113.95, 46.87)],
                'description': 'Clark Fork River - main drainage'
            },
            'rattlesnake_creek': {
                'type': 'creek',
                'coordinates': [(-114.02, 46.91), (-114.00, 46.87)],
                'description': 'Rattlesnake Creek'
            },
            'bitterroot_river': {
                'type': 'river',
                'coordinates': [(-114.08, 46.83), (-114.05, 46.86)],
                'description': 'Bitterroot River confluence'
            }
        }
    
    def create_subglacial_texture(self, shape, intensity=0.3):
        """Create glacial lake and flood-specific textures."""
        # Glacial lake bottom textures - rhythmic sediment patterns
        lake_texture = np.zeros(shape)
        
        # Varved sediment patterns (annual layers)
        y, x = np.mgrid[0:shape[0], 0:shape[1]]
        varve_pattern = np.sin(y * 0.1) * 0.5
        
        # Flood scabland textures - chaotic drainage
        flood_texture = np.random.random(shape) * 0.3
        flood_channels = gaussian_filter(flood_texture, sigma=3)
        
        # Combine textures
        combined_texture = varve_pattern + flood_channels * 0.7
        
        return gaussian_filter(combined_texture, sigma=1.5) * intensity
    
    def create_enhanced_map(self):
        """Create the complete enhanced Missoula map."""
        # Create figure
        fig, ax = plt.subplots(1, 1, figsize=(18, 12))
        fig.patch.set_facecolor('#0F1419')
        ax.set_facecolor('#0F1419')
        
        # Get data
        lon_grid, lat_grid, elevation = self.get_elevation_data()
        geological_features = self.get_geological_features()
        hydrological_features = self.get_hydrological_features()
        
        # Create subglacial texture
        texture = self.create_subglacial_texture(elevation.shape, intensity=0.25)
        
        # Enhanced elevation with texture
        enhanced_elevation = elevation + texture * 200
        
        # Create geological colormap
        geological_colors = ['#0F1419', '#2D1B14', '#4A2C1A', '#8B4513', '#CD853F', '#F4A460', '#FFEAA7', '#FFFFFF']
        geological_cmap = LinearSegmentedColormap.from_list('geological', geological_colors, N=256)
        
        # Plot enhanced elevation
        elevation_plot = ax.contourf(lon_grid, lat_grid, enhanced_elevation, 
                                   levels=50, cmap=geological_cmap, alpha=0.6)
        
        # Add geological formation overlays
        for formation, data in geological_features.items():
            if formation == 'glacial_lake_deposits':
                # Special highlighting for glacial lake area
                bounds = data['bounds']
                rect = Rectangle((bounds[0][0], bounds[0][1]), 
                               bounds[1][0] - bounds[0][0], 
                               bounds[1][1] - bounds[0][1],
                               facecolor=data['color'], alpha=0.15, 
                               edgecolor=data['color'], linewidth=1.5, linestyle='-')
                ax.add_patch(rect)
        
        # Add hydrological features
        for feature, data in hydrological_features.items():
            coords = data['coordinates']
            if data['type'] == 'major_river':
                ax.plot([coords[0][0], coords[1][0]], [coords[0][1], coords[1][1]], 
                       color='#4A90E2', linewidth=4, alpha=0.8, label='Clark Fork River')
            elif data['type'] == 'river':
                ax.plot([coords[0][0], coords[1][0]], [coords[0][1], coords[1][1]], 
                       color='#4A90E2', linewidth=3, alpha=0.7)
            elif data['type'] == 'creek':
                ax.plot([coords[0][0], coords[1][0]], [coords[0][1], coords[1][1]], 
                       color='#4A90E2', linewidth=2, alpha=0.6)
        
        # Add key locations
        locations = {
            'Downtown Missoula': (-113.996, 46.872),
            'University of Montana': (-113.985, 46.865),
            'Rattlesnake Wilderness': (-114.02, 46.91),
            'Bitterroot Confluence': (-114.05, 46.86),
            'DoubleTree Hotel': (-113.995, 46.870)
        }
        
        for name, (lon, lat) in locations.items():
            if name == 'DoubleTree Hotel':
                # Hotel marker
                ax.plot(lon, lat, 'o', color='#FF6B6B', markersize=12, 
                       markeredgecolor='white', markeredgewidth=2, zorder=10)
                ax.text(lon + 0.008, lat + 0.005, name, fontsize=11, 
                       fontweight='bold', color='white',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
            else:
                ax.plot(lon, lat, 'o', color='#FFF', markersize=8, 
                       markeredgecolor='black', markeredgewidth=1, zorder=10)
                ax.text(lon + 0.008, lat + 0.002, name, fontsize=10, 
                       color='white', fontweight='bold',
                       path_effects=[path_effects.withStroke(linewidth=1.5, foreground='black')])
        
        # Add geological story annotations
        ax.text(-114.12, 46.94, 'GLACIAL LAKE MISSOULA', 
               fontsize=16, fontweight='bold', color='#B8860B',
               path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
        
        ax.text(-114.12, 46.92, 'Ice-dammed lake\n~15,000 years ago\nCatastrophic drainage', 
               fontsize=11, color='white', fontweight='bold',
               path_effects=[path_effects.withStroke(linewidth=1.5, foreground='black')])
        
        # Add elevation contours
        contour_lines = ax.contour(lon_grid, lat_grid, enhanced_elevation, 
                                 levels=15, colors='white', alpha=0.3, linewidths=0.5)
        
        # Set map bounds and labels
        ax.set_xlim(MISSOULA_BOUNDS['west'], MISSOULA_BOUNDS['east'])
        ax.set_ylim(MISSOULA_BOUNDS['south'], MISSOULA_BOUNDS['north'])
        ax.set_xlabel('Longitude', fontsize=12, color='white', fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, color='white', fontweight='bold')
        ax.set_title('MISSOULA, MONTANA\nGlacial Lake Deposits & Clark Fork Valley', 
                    fontsize=20, fontweight='bold', color='white', pad=20)
        
        # Create legend
        legend_elements = [
            mpatches.Patch(color='#B8860B', alpha=0.7, label='Glacial Lake Deposits'),
            mpatches.Patch(color='#8B4513', alpha=0.7, label='Belt Supergroup'),
            mpatches.Patch(color='#CD853F', alpha=0.7, label='Flood Scablands'),
            Line2D([0], [0], color='#4A90E2', linewidth=3, label='Clark Fork River'),
            Line2D([0], [0], marker='o', color='#FF6B6B', markersize=10, 
                      label='DoubleTree Hotel', linestyle='None')
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
        filename = 'images/missoula_enhanced_geospatial.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        print(f"Enhanced Missoula map saved: {filename}")
        return filename

def main():
    mapper = MissoulaGeoMapper()
    filename = mapper.create_enhanced_map()
    print(f"Enhanced Missoula map created: {filename}")

if __name__ == "__main__":
    main() 