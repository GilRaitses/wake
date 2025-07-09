#!/usr/bin/env python3
"""
Glacial Lake Missoula Timeline Visualization
Multi-panel geological storytelling for Pacific Northwest travel guide

Based on USGS research data:
- 40+ separate flood events over ~2500 years (20,000-15,000 years ago)
- Peak discharges up to 20+ million cubic meters per second
- Lake volume equivalent to Lake Erie + Lake Ontario combined
- Critical ice dam positions and failure mechanisms
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import Polygon, Circle, FancyBboxPatch
from scipy.ndimage import gaussian_filter
import json
from pathlib import Path

# Regional bounds for the visualization
REGION_BOUNDS = {
    'north': 49.0,
    'south': 44.0,
    'east': -110.0,
    'west': -125.0
}

class GlacialLakeMissoulaTimeline:
    def __init__(self):
        self.cache_dir = Path('geospatial_cache')
        self.cache_dir.mkdir(exist_ok=True)
        
        # Key geological events and data from USGS research
        self.geological_events = {
            'ice_sheet_advance': {
                'time': '20,000 years ago',
                'description': 'Cordilleran Ice Sheet advances south',
                'critical_points': ['Purcell Trench lobe formation', 'Clark Fork River blocked']
            },
            'lake_formation': {
                'time': '20,000-15,000 years ago',
                'description': 'Glacial Lake Missoula forms',
                'critical_points': ['Ice dam 2,500 feet high', 'Lake volume: 500 cubic miles', 'Water depth: 2,000 feet']
            },
            'dam_failure_cycle': {
                'time': 'Repeated over 2,500 years',
                'description': '40+ catastrophic dam failures',
                'critical_points': ['Peak discharge: 20+ million cubic meters/second', 'Flood speed: 65 mph', 'Complete drainage: 48 hours']
            },
            'scablands_formation': {
                'time': 'Each flood event',
                'description': 'Channeled Scablands carved',
                'critical_points': ['Stripped hundreds of feet of soil', 'Carved deep coulees', 'Created Grand Coulee']
            },
            'modern_landscape': {
                'time': 'Present day',
                'description': 'Geological legacy visible today',
                'critical_points': ['Flood deposits preserved', 'Scablands visible from space', 'Modern river valleys']
            }
        }
        
        # Ice sheet positions and critical failure points
        self.ice_positions = {
            'purcell_trench_lobe': (-116.5, 48.0),
            'okanogan_lobe': (-119.5, 48.5),
            'columbia_ice_dam': (-118.0, 47.5)
        }
        
        # Flood routing paths based on USGS flood modeling
        self.flood_routes = {
            'columbia_valley': [(-116.5, 48.0), (-119.0, 47.0), (-121.0, 45.5)],
            'grand_coulee': [(-119.0, 47.5), (-119.5, 47.0), (-119.0, 46.0)],
            'channeled_scablands': [(-118.0, 47.0), (-118.5, 46.5), (-119.0, 46.0)],
            'columbia_gorge': [(-121.0, 45.5), (-122.0, 45.7), (-123.5, 45.7)]
        }
        
    def create_base_geography(self, ax, time_period):
        """Create base geographical features for each time period."""
        lons = np.linspace(REGION_BOUNDS['west'], REGION_BOUNDS['east'], 200)
        lats = np.linspace(REGION_BOUNDS['south'], REGION_BOUNDS['north'], 160)
        lon_grid, lat_grid = np.meshgrid(lons, lats)
        
        # Base topography
        elevation = np.zeros_like(lon_grid)
        
        # Rocky Mountains (east)
        rocky_mask = (lon_grid > -115.0)
        elevation[rocky_mask] = 4000 + 2000 * np.exp(-((lon_grid[rocky_mask] + 112.0)**2 + (lat_grid[rocky_mask] - 46.5)**2) / 10)
        
        # Cascade Mountains (west)
        cascade_mask = (lon_grid < -120.0)
        elevation[cascade_mask] = 2000 + 3000 * np.exp(-((lon_grid[cascade_mask] + 121.5)**2 + (lat_grid[cascade_mask] - 46.0)**2) / 8)
        
        # Columbia River valley
        river_valley = ((lat_grid > 45.0) & (lat_grid < 46.5) & (lon_grid > -123.0) & (lon_grid < -115.0))
        elevation[river_valley] = 1000 + 500 * np.sin((lon_grid[river_valley] + 120.0) * 2)
        
        # Missoula valley
        missoula_valley = ((lat_grid > 46.5) & (lat_grid < 47.5) & (lon_grid > -114.5) & (lon_grid < -113.0))
        elevation[missoula_valley] = 3200
        
        # Color mapping based on time period
        if time_period == 'ice_age':
            colors = ['#E6F3FF', '#B8D4F0', '#8AB5E0', '#5C96D0', '#2E77C0']
        elif time_period == 'flood':
            colors = ['#2E77C0', '#5C96D0', '#8AB5E0', '#B8D4F0', '#E6F3FF']
        else:
            colors = ['#8FBC8F', '#98D982', '#A1F76C', '#AAD056', '#B3A940']
        
        cmap = LinearSegmentedColormap.from_list('topo', colors, N=256)
        
        # Add subtle texture
        texture = np.random.normal(0, 50, elevation.shape)
        enhanced_elevation = elevation + gaussian_filter(texture, sigma=1)
        
        contour = ax.contourf(lon_grid, lat_grid, enhanced_elevation, 
                             levels=20, cmap=cmap, alpha=0.7)
        
        return lon_grid, lat_grid, enhanced_elevation
    
    def add_ice_sheet(self, ax, extent='maximum'):
        """Add ice sheet coverage based on USGS glacial reconstructions."""
        if extent == 'maximum':
            # Maximum ice extent during dam formation
            ice_polygons = [
                # Purcell Trench lobe
                [(-117.0, 49.0), (-116.0, 49.0), (-116.0, 47.5), (-117.0, 47.5)],
                # Okanogan lobe
                [(-120.5, 49.0), (-118.5, 49.0), (-118.5, 47.0), (-120.5, 47.0)],
                # Main Cordilleran Ice Sheet
                [(-125.0, 49.0), (-115.0, 49.0), (-115.0, 48.0), (-125.0, 48.0)]
            ]
        else:
            # Retreating ice during flood events
            ice_polygons = [
                [(-117.0, 49.0), (-116.0, 49.0), (-116.0, 48.0), (-117.0, 48.0)],
                [(-120.0, 49.0), (-119.0, 49.0), (-119.0, 47.5), (-120.0, 47.5)]
            ]
        
        for polygon_coords in ice_polygons:
            ice_polygon = Polygon(polygon_coords, facecolor='#E6F7FF', 
                                edgecolor='#B8E6FF', linewidth=2, alpha=0.8)
            ax.add_patch(ice_polygon)
        
        # Add ice texture
        for x, y in [(lat, lon) for lat in np.arange(47.5, 49.0, 0.3) 
                     for lon in np.arange(-120.0, -115.0, 0.3)]:
            if any(self.point_in_polygon(x, y, poly) for poly in ice_polygons):
                ax.plot(y, x, 'o', color='#E6F7FF', markersize=2, alpha=0.6)
    
    def add_glacial_lake(self, ax, water_level='maximum'):
        """Add Glacial Lake Missoula based on USGS reconstruction."""
        if water_level == 'maximum':
            # Maximum lake extent - 4,250 feet elevation
            lake_bounds = [
                (-114.5, 47.8), (-113.0, 47.8), (-113.0, 46.5), 
                (-114.0, 46.5), (-114.5, 46.8), (-114.5, 47.8)
            ]
            lake_color = '#4A90E2'
            alpha = 0.8
        elif water_level == 'draining':
            # Partially drained lake
            lake_bounds = [
                (-114.0, 47.3), (-113.5, 47.3), (-113.5, 46.8), 
                (-114.0, 46.8), (-114.0, 47.3)
            ]
            lake_color = '#87CEEB'
            alpha = 0.6
        else:
            return
        
        lake_polygon = Polygon(lake_bounds, facecolor=lake_color, 
                              edgecolor='#2E5BDA', linewidth=2, alpha=alpha)
        ax.add_patch(lake_polygon)
        
        # Add lake label
        ax.text(-113.75, 47.2, 'GLACIAL LAKE\nMISSOULA', 
               fontsize=14, fontweight='bold', color='#2E5BDA', ha='center',
               path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
    
    def add_flood_paths(self, ax, active_routes=None):
        """Add flood pathways based on USGS flood routing research."""
        if active_routes is None:
            active_routes = ['columbia_valley', 'grand_coulee', 'channeled_scablands']
        
        route_colors = {
            'columbia_valley': '#FF4500',
            'grand_coulee': '#FF6B35',
            'channeled_scablands': '#FF8C69',
            'columbia_gorge': '#FFB347'
        }
        
        for route_name in active_routes:
            if route_name in self.flood_routes:
                route_coords = self.flood_routes[route_name]
                lons, lats = zip(*route_coords)
                
                ax.plot(lons, lats, color=route_colors[route_name], 
                       linewidth=6, alpha=0.8, zorder=10)
                
                # Add flow direction arrows
                for i in range(len(lons)-1):
                    mid_x = (lons[i] + lons[i+1]) / 2
                    mid_y = (lats[i] + lats[i+1]) / 2
                    dx = lons[i+1] - lons[i]
                    dy = lats[i+1] - lats[i]
                    
                    ax.annotate('', xy=(lons[i+1], lats[i+1]), 
                              xytext=(lons[i], lats[i]),
                              arrowprops=dict(arrowstyle='->', 
                                            color=route_colors[route_name],
                                            lw=3, alpha=0.7))
    
    def add_critical_points(self, ax, event_type):
        """Add critical failure points and geological features."""
        if event_type == 'dam_formation':
            # Ice dam location
            ax.plot(-116.5, 48.0, 's', color='#FF0000', markersize=15, 
                   markeredgecolor='white', markeredgewidth=2, zorder=15)
            ax.text(-116.5, 47.7, 'ICE DAM\n2,500 ft high', 
                   fontsize=12, fontweight='bold', color='#FF0000', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
            
        elif event_type == 'dam_failure':
            # Dam breach point
            ax.plot(-116.5, 48.0, 'X', color='#FF0000', markersize=20, 
                   markeredgecolor='white', markeredgewidth=2, zorder=15)
            ax.text(-116.5, 47.7, 'DAM BREACH\n20M m³/s', 
                   fontsize=12, fontweight='bold', color='#FF0000', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
            
        elif event_type == 'scablands':
            # Major scabland features
            scabland_features = [
                (-119.0, 46.8, 'Grand Coulee'),
                (-118.5, 46.5, 'Channeled Scablands'),
                (-119.5, 46.0, 'Dry Falls')
            ]
            
            for lon, lat, name in scabland_features:
                ax.plot(lon, lat, 'o', color='#8B4513', markersize=12, 
                       markeredgecolor='white', markeredgewidth=2, zorder=15)
                ax.text(lon, lat-0.2, name, 
                       fontsize=10, fontweight='bold', color='#8B4513', ha='center',
                       path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
    
    def point_in_polygon(self, x, y, polygon):
        """Check if point is inside polygon."""
        n = len(polygon)
        inside = False
        p1x, p1y = polygon[0]
        for i in range(1, n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
            p1x, p1y = p2x, p2y
        return inside
    
    def create_timeline_visualization(self):
        """Create the complete multi-panel timeline visualization."""
        fig = plt.figure(figsize=(24, 16))
        fig.patch.set_facecolor('#0F1419')
        
        # Define the 6 panels
        panels = [
            {'pos': (0, 0.67, 0.48, 0.3), 'title': 'Ice Sheet Advance (20,000 years ago)', 'type': 'ice_advance'},
            {'pos': (0.52, 0.67, 0.48, 0.3), 'title': 'Lake Formation (20,000-15,000 years ago)', 'type': 'lake_formation'},
            {'pos': (0, 0.34, 0.48, 0.3), 'title': 'Dam Failure & Megaflood (Repeated 40+ times)', 'type': 'dam_failure'},
            {'pos': (0.52, 0.34, 0.48, 0.3), 'title': 'Scablands Formation (Each flood event)', 'type': 'scablands'},
            {'pos': (0, 0.01, 0.48, 0.3), 'title': 'Modern Landscape Legacy (Present day)', 'type': 'modern'},
            {'pos': (0.52, 0.01, 0.48, 0.3), 'title': 'Your Travel Route Through Flood History', 'type': 'travel_route'}
        ]
        
        for i, panel in enumerate(panels):
            ax = fig.add_axes(panel['pos'])
            ax.set_facecolor('#0F1419')
            
            # Create base geography
            if panel['type'] == 'ice_advance':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'ice_age')
                self.add_ice_sheet(ax, extent='maximum')
                self.add_critical_points(ax, 'dam_formation')
                
            elif panel['type'] == 'lake_formation':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'ice_age')
                self.add_ice_sheet(ax, extent='maximum')
                self.add_glacial_lake(ax, water_level='maximum')
                
            elif panel['type'] == 'dam_failure':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'flood')
                self.add_ice_sheet(ax, extent='retreating')
                self.add_glacial_lake(ax, water_level='draining')
                self.add_flood_paths(ax, ['columbia_valley', 'grand_coulee'])
                self.add_critical_points(ax, 'dam_failure')
                
            elif panel['type'] == 'scablands':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'flood')
                self.add_flood_paths(ax, ['grand_coulee', 'channeled_scablands', 'columbia_gorge'])
                self.add_critical_points(ax, 'scablands')
                
            elif panel['type'] == 'modern':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'modern')
                # Add modern cities
                cities = [
                    (-113.99, 46.87, 'Missoula'),
                    (-116.10, 44.90, 'McCall'),
                    (-117.43, 45.49, 'Lostine'),
                    (-118.34, 45.70, 'Walla Walla')
                ]
                
                for lon, lat, name in cities:
                    ax.plot(lon, lat, 'o', color='#FF6B6B', markersize=10, 
                           markeredgecolor='white', markeredgewidth=2, zorder=10)
                    ax.text(lon, lat-0.2, name, 
                           fontsize=10, fontweight='bold', color='white', ha='center',
                           path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
                
            elif panel['type'] == 'travel_route':
                lon_grid, lat_grid, elevation = self.create_base_geography(ax, 'modern')
                
                # Add travel route
                route_coords = [(-113.99, 46.87), (-116.10, 44.90), (-117.43, 45.49), (-118.34, 45.70)]
                lons, lats = zip(*route_coords)
                ax.plot(lons, lats, color='#FFD700', linewidth=6, alpha=0.8, zorder=10)
                
                # Add cities with geological context
                geological_sites = [
                    (-113.99, 46.87, 'Missoula\n(Lake bottom deposits)'),
                    (-116.10, 44.90, 'McCall\n(Glacial cirque)'),
                    (-117.43, 45.49, 'Lostine\n(Wallowa granite)'),
                    (-118.34, 45.70, 'Walla Walla\n(Flood scablands)')
                ]
                
                for lon, lat, desc in geological_sites:
                    ax.plot(lon, lat, 'o', color='#FFD700', markersize=12, 
                           markeredgecolor='white', markeredgewidth=2, zorder=10)
                    ax.text(lon, lat-0.3, desc, 
                           fontsize=9, fontweight='bold', color='#FFD700', ha='center',
                           path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
            
            # Set panel properties
            ax.set_xlim(REGION_BOUNDS['west'], REGION_BOUNDS['east'])
            ax.set_ylim(REGION_BOUNDS['south'], REGION_BOUNDS['north'])
            ax.set_xlabel('Longitude', fontsize=10, color='white')
            ax.set_ylabel('Latitude', fontsize=10, color='white')
            ax.set_title(panel['title'], fontsize=14, fontweight='bold', color='white', pad=10)
            
            # Style the axes
            ax.tick_params(colors='white', labelsize=8)
            for spine in ax.spines.values():
                spine.set_color('white')
        
        # Add main title and timeline
        fig.suptitle('GLACIAL LAKE MISSOULA MEGAFLOODS\nGeological Timeline & Modern Travel Context', 
                    fontsize=24, fontweight='bold', color='white', y=0.98)
        
        # Add timeline bar
        timeline_ax = fig.add_axes([0.1, 0.0, 0.8, 0.02])
        timeline_ax.set_xlim(0, 20000)
        timeline_ax.set_ylim(0, 1)
        timeline_ax.barh(0.5, 5000, left=15000, height=0.3, color='#FF4500', alpha=0.7)
        timeline_ax.text(17500, 0.5, '40+ Flood Events\n(20,000-15,000 years ago)', 
                        ha='center', va='center', fontsize=12, fontweight='bold', color='white')
        timeline_ax.text(10000, 0.5, 'Your trip experiences\nthe geological legacy', 
                        ha='center', va='center', fontsize=10, fontweight='bold', color='#FFD700')
        timeline_ax.set_xlabel('Years Ago', fontsize=12, color='white')
        timeline_ax.tick_params(colors='white')
        timeline_ax.set_facecolor('#0F1419')
        for spine in timeline_ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Save the visualization
        filename = 'images/glacial_lake_missoula_timeline.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        print(f"Glacial Lake Missoula timeline visualization saved: {filename}")
        return filename
    
    def create_critical_events_summary(self):
        """Create a summary of critical geological events."""
        summary = {
            'geological_timeline': self.geological_events,
            'critical_datasets': {
                'usgs_flood_modeling': 'Digital terrain models (185m resolution)',
                'stratigraphic_evidence': 'Dozens of separate flood beds',
                'paleoclimate_data': 'Varve counts and radiocarbon dating',
                'ice_sheet_modeling': 'Cordilleran Ice Sheet reconstruction'
            },
            'key_statistics': {
                'total_floods': '40+ separate events',
                'time_period': '20,000-15,000 years ago',
                'peak_discharge': '20+ million cubic meters per second',
                'flood_speed': '65 miles per hour',
                'drainage_time': '48 hours complete drainage',
                'lake_volume': '500 cubic miles (Lake Erie + Ontario combined)'
            }
        }
        
        # Save summary
        with open('geospatial_cache/glacial_lake_missoula_summary.json', 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary

def main():
    timeline = GlacialLakeMissoulaTimeline()
    
    # Create the timeline visualization
    timeline_file = timeline.create_timeline_visualization()
    
    # Create summary of critical events
    summary = timeline.create_critical_events_summary()
    
    print(f"Timeline visualization created: {timeline_file}")
    print(f"Geological events summary saved to: geospatial_cache/glacial_lake_missoula_summary.json")
    
    return timeline_file

if __name__ == "__main__":
    main() 