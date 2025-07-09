#!/usr/bin/env python3
"""
Modern Travel Route Through Glacial Lake Missoula Geological Legacy
Connecting ancient megafloods to present-day travel destinations

This visualization shows how the modern Pacific Northwest travel route
passes through the geological features created by the Glacial Lake Missoula
megafloods 15,000-20,000 years ago.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patheffects as path_effects
from matplotlib.patches import Polygon, Circle, FancyBboxPatch, Rectangle
from scipy.ndimage import gaussian_filter
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

class ModernTravelGeologicalContext:
    def __init__(self):
        # Modern travel destinations and their geological context
        self.travel_destinations = {
            'missoula': {
                'coords': (-113.99, 46.87),
                'accommodation': 'DoubleTree Hotel',
                'geological_context': 'Glacial Lake Bottom',
                'ancient_feature': 'Lake bed sediments & varved deposits',
                'modern_evidence': 'Glacial Lake Missoula high-water marks',
                'description': 'Built on ancient lake floor deposits'
            },
            'mccall': {
                'coords': (-116.10, 44.90),
                'accommodation': 'Shore Lodge',
                'geological_context': 'Glacial Cirque Lake',
                'ancient_feature': 'Payette Lake formed by glacial scouring',
                'modern_evidence': 'U-shaped valley and glacial moraines',
                'description': 'Alpine glacial landscape - untouched by floods'
            },
            'lostine': {
                'coords': (-117.43, 45.49),
                'accommodation': 'Day trip from Joseph',
                'geological_context': 'Wallowa Mountains Foothills',
                'ancient_feature': 'Granite batholith and glacial carving',
                'modern_evidence': 'Glacial valley morphology',
                'description': 'Upstream from flood paths - preserved landscape'
            },
            'joseph': {
                'coords': (-117.43, 45.49),
                'accommodation': 'The Jennings Hotel',
                'geological_context': 'Wallowa Mountains Base',
                'ancient_feature': 'Glacial lake and alpine terrain',
                'modern_evidence': 'Wallowa Lake and glacial features',
                'description': 'Mountain refuge from flood devastation'
            },
            'walla_walla': {
                'coords': (-118.34, 45.70),
                'accommodation': 'Eritage Resort',
                'geological_context': 'Columbia Plateau Loess Hills',
                'ancient_feature': 'Flood-deposited loess and wine terroir',
                'modern_evidence': 'Palouse loess formation',
                'description': 'Wine country built on flood-deposited soils'
            },
            'columbia_gorge': {
                'coords': (-122.0, 45.7),
                'accommodation': 'Under Canvas Glamping',
                'geological_context': 'Major Flood Conduit',
                'ancient_feature': 'Primary megaflood pathway to Pacific',
                'modern_evidence': 'Carved gorge walls and flood terraces',
                'description': 'The great drain - floods rushed through here'
            },
            'seattle': {
                'coords': (-122.33, 47.61),
                'accommodation': 'Fairmont Olympic',
                'geological_context': 'Puget Sound Lowlands',
                'ancient_feature': 'Glacial Lake Columbia overflow',
                'modern_evidence': 'Puget Sound carved by glacial advance',
                'description': 'Northern terminus - beyond flood impact'
            }
        }
        
        # Geological timeline connecting ancient events to modern features
        self.geological_timeline = {
            '20000_years_ago': {
                'event': 'Cordilleran Ice Sheet advance',
                'modern_evidence': 'Puget Sound formation, glacial valleys'
            },
            '18000_years_ago': {
                'event': 'Glacial Lake Missoula at maximum',
                'modern_evidence': 'High water marks visible in Missoula'
            },
            '15000_years_ago': {
                'event': '40+ catastrophic megafloods',
                'modern_evidence': 'Channeled Scablands, Columbia River Gorge'
            },
            '12000_years_ago': {
                'event': 'Ice retreat and landscape stabilization',
                'modern_evidence': 'Modern river systems established'
            },
            'present_day': {
                'event': 'Your travel route through geological history',
                'modern_evidence': 'Hotels built on ancient flood deposits'
            }
        }
        
    def create_travel_geological_map(self):
        """Create main map showing travel route through geological context."""
        fig, ax = plt.subplots(1, 1, figsize=(20, 14))
        fig.patch.set_facecolor('#0F1419')
        ax.set_facecolor('#0F1419')
        
        # Regional topography
        x_region = np.linspace(-125, -112, 200)
        y_region = np.linspace(44, 49, 150)
        X, Y = np.meshgrid(x_region, y_region)
        
        # Create geological base map
        elevation = np.zeros_like(X)
        
        # Major geological provinces
        cascade_range = ((X < -120) & (Y > 45) & (Y < 48.5))
        elevation[cascade_range] = 2000 + 3000 * np.exp(-((X[cascade_range] + 121.5)**2 + (Y[cascade_range] - 46.5)**2) / 8)
        
        rocky_mountains = ((X > -117) & (Y > 46))
        elevation[rocky_mountains] = 3000 + 4000 * np.exp(-((X[rocky_mountains] + 114)**2 + (Y[rocky_mountains] - 47)**2) / 12)
        
        columbia_plateau = ((X > -120) & (X < -116) & (Y > 45) & (Y < 47))
        elevation[columbia_plateau] = 1500 + 500 * np.sin((X[columbia_plateau] + 118) * 3) * np.cos((Y[columbia_plateau] - 46) * 4)
        
        # Glacial Lake Missoula basin
        lake_basin = ((X > -114.5) & (X < -113) & (Y > 46) & (Y < 47.8))
        elevation[lake_basin] = 3200 + 200 * np.random.random(lake_basin.shape)[lake_basin]
        
        # Create geological color scheme
        geo_colors = ['#2E4B8B', '#4A6FA5', '#6B8FBC', '#8FAACD', '#B8CDE6', '#E6F3FF']
        geo_cmap = LinearSegmentedColormap.from_list('geological', geo_colors, N=256)
        
        # Plot base topography
        contour = ax.contourf(X, Y, elevation, levels=30, cmap=geo_cmap, alpha=0.6)
        
        # Add geological provinces as overlays
        provinces = {
            'Channeled Scablands': {
                'coords': [(-119.5, 47.5), (-117.5, 47.5), (-117.5, 46.0), (-119.5, 46.0)],
                'color': '#CD853F',
                'alpha': 0.3,
                'label': 'Megaflood erosion zone'
            },
            'Columbia River Gorge': {
                'coords': [(-123.0, 46.0), (-121.0, 46.0), (-121.0, 45.5), (-123.0, 45.5)],
                'color': '#FF6B35',
                'alpha': 0.4,
                'label': 'Primary flood conduit'
            },
            'Glacial Lake Basin': {
                'coords': [(-114.5, 47.8), (-113.0, 47.8), (-113.0, 46.0), (-114.5, 46.0)],
                'color': '#4A90E2',
                'alpha': 0.3,
                'label': 'Ancient lake bottom'
            },
            'Wallowa Mountains': {
                'coords': [(-117.8, 45.8), (-117.0, 45.8), (-117.0, 45.0), (-117.8, 45.0)],
                'color': '#8B4513',
                'alpha': 0.3,
                'label': 'Granite batholith - flood refuge'
            }
        }
        
        for province, data in provinces.items():
            polygon = Polygon(data['coords'], facecolor=data['color'], 
                            alpha=data['alpha'], edgecolor=data['color'], 
                            linewidth=2, linestyle='--')
            ax.add_patch(polygon)
        
        # Add travel route
        destinations = ['missoula', 'mccall', 'joseph', 'walla_walla', 'columbia_gorge', 'seattle']
        route_coords = [self.travel_destinations[dest]['coords'] for dest in destinations]
        
        # Draw travel route
        lons, lats = zip(*route_coords)
        ax.plot(lons, lats, color='#FFD700', linewidth=6, alpha=0.9, 
               zorder=10, label='Your Travel Route')
        
        # Add directional arrows
        for i in range(len(lons)-1):
            ax.annotate('', xy=(lons[i+1], lats[i+1]), 
                       xytext=(lons[i], lats[i]),
                       arrowprops=dict(arrowstyle='->', color='#FFD700',
                                     lw=4, alpha=0.8))
        
        # Add destination markers and geological context
        for i, dest_key in enumerate(destinations):
            dest = self.travel_destinations[dest_key]
            lon, lat = dest['coords']
            
            # Marker style based on geological context
            if 'Lake' in dest['geological_context']:
                marker_style = 'o'
                marker_color = '#4A90E2'
            elif 'Flood' in dest['geological_context'] or 'Scab' in dest['geological_context']:
                marker_style = 's'
                marker_color = '#FF6B35'
            elif 'Mountain' in dest['geological_context']:
                marker_style = '^'
                marker_color = '#8B4513'
            else:
                marker_style = 'o'
                marker_color = '#FFD700'
            
            # Plot destination marker
            ax.plot(lon, lat, marker_style, color=marker_color, markersize=15, 
                   markeredgecolor='white', markeredgewidth=2, zorder=15)
            
            # Add geological context annotation
            ax.text(lon, lat-0.25, f"{dest['accommodation']}\n{dest['geological_context']}", 
                   fontsize=10, fontweight='bold', color='white', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
            
            # Add day number
            ax.text(lon+0.3, lat+0.3, f"Day {i+1}", 
                   fontsize=12, fontweight='bold', color='#FFD700', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
        
        # Add ancient flood pathways for context
        ancient_routes = [
            # Columbia Valley route
            [(-116.5, 48.0), (-119.0, 47.0), (-121.0, 45.5), (-123.0, 45.7)],
            # Grand Coulee route  
            [(-116.5, 48.0), (-119.0, 47.5), (-119.5, 47.0), (-121.0, 45.5)],
            # Channeled Scablands route
            [(-116.5, 48.0), (-118.0, 47.0), (-118.5, 46.5), (-121.0, 45.5)]
        ]
        
        flood_colors = ['#FF4500', '#FF6B35', '#FF8C69']
        for i, route in enumerate(ancient_routes):
            lons_flood, lats_flood = zip(*route)
            ax.plot(lons_flood, lats_flood, color=flood_colors[i], 
                   linewidth=3, alpha=0.5, linestyle=':', zorder=5)
        
        # Add ice dam breach point
        ax.plot(-116.5, 48.0, 'X', color='#FF0000', markersize=20, 
               markeredgecolor='white', markeredgewidth=3, zorder=20)
        ax.text(-116.5, 47.6, 'ICE DAM\nBREACH POINT\n(20,000-15,000 years ago)', 
               fontsize=11, fontweight='bold', color='#FF0000', ha='center',
               path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        # Set map properties
        ax.set_xlim(-125, -112)
        ax.set_ylim(44, 49)
        ax.set_xlabel('Longitude', fontsize=14, color='white', fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=14, color='white', fontweight='bold')
        ax.set_title('MODERN TRAVEL ROUTE THROUGH ANCIENT MEGAFLOOD TERRAIN\n' + 
                    'Your Hotels Built on 15,000-Year-Old Geological Features', 
                    fontsize=18, fontweight='bold', color='white', pad=20)
        
        # Create comprehensive legend
        legend_elements = [
            Line2D([0], [0], color='#FFD700', linewidth=6, label='Your Travel Route'),
            Line2D([0], [0], color='#FF4500', linewidth=3, linestyle=':', 
                   label='Ancient Megaflood Pathways'),
            Line2D([0], [0], marker='o', color='#4A90E2', markersize=12, 
                   label='Lake Bottom Destinations', linestyle='None'),
            Line2D([0], [0], marker='s', color='#FF6B35', markersize=12, 
                   label='Flood Zone Destinations', linestyle='None'),
            Line2D([0], [0], marker='^', color='#8B4513', markersize=12, 
                   label='Mountain Refuge Destinations', linestyle='None'),
            Line2D([0], [0], marker='X', color='#FF0000', markersize=15, 
                   label='Ice Dam Breach Point', linestyle='None'),
            mpatches.Patch(color='#CD853F', alpha=0.3, label='Channeled Scablands'),
            mpatches.Patch(color='#4A90E2', alpha=0.3, label='Ancient Lake Basin')
        ]
        
        ax.legend(handles=legend_elements, loc='upper right', 
                 fancybox=True, shadow=True, fontsize=11,
                 facecolor='black', edgecolor='white', framealpha=0.8)
        
        # Style the axes
        ax.tick_params(colors='white', labelsize=12)
        for spine in ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Save the map
        filename = 'images/modern_travel_geological_context.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        return filename
    
    def create_timeline_comparison(self):
        """Create timeline comparing ancient events to modern travel."""
        fig, ax = plt.subplots(1, 1, figsize=(20, 8))
        fig.patch.set_facecolor('#0F1419')
        ax.set_facecolor('#0F1419')
        
        # Timeline data
        timeline_events = [
            (20000, 'Cordilleran Ice Sheet Advance', '#87CEEB', 'Ice dams Clark Fork River'),
            (18000, 'Glacial Lake Missoula Forms', '#4A90E2', 'Lake reaches maximum size'),
            (17000, 'First Megafloods Begin', '#FF4500', '40+ catastrophic floods'),
            (15000, 'Peak Flood Activity', '#FF6B35', 'Channeled Scablands carved'),
            (13000, 'Last Megafloods', '#FF8C69', 'Final dam failures'),
            (12000, 'Ice Retreat Complete', '#98FB98', 'Modern landscape emerges'),
            (0, 'Your Trip - August 2025', '#FFD700', 'Experience geological legacy')
        ]
        
        # Plot timeline
        for i, (year, event, color, description) in enumerate(timeline_events):
            y_pos = 0.5
            
            # Event marker
            ax.plot(year, y_pos, 'o', color=color, markersize=20, 
                   markeredgecolor='white', markeredgewidth=2, zorder=10)
            
            # Event label
            ax.text(year, y_pos + 0.15, event, 
                   fontsize=12, fontweight='bold', color=color, ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
            
            # Description
            ax.text(year, y_pos - 0.15, description, 
                   fontsize=10, color='white', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=1, foreground='black')])
            
            # Timeline line
            if i < len(timeline_events) - 1:
                next_year = timeline_events[i+1][0]
                ax.plot([year, next_year], [y_pos, y_pos], 
                       color='white', linewidth=2, alpha=0.6, zorder=5)
        
        # Highlight flood period
        ax.axvspan(17000, 13000, alpha=0.2, color='#FF6B35', 
                  label='Peak Megaflood Activity')
        
        # Add modern travel destinations
        modern_destinations = [
            (0, 'Missoula\n(Lake bottom)', '#4A90E2'),
            (0, 'McCall\n(Glacial cirque)', '#98FB98'),
            (0, 'Joseph\n(Mountain refuge)', '#8B4513'),
            (0, 'Walla Walla\n(Flood deposits)', '#CD853F'),
            (0, 'Columbia Gorge\n(Flood conduit)', '#FF6B35'),
            (0, 'Seattle\n(Beyond floods)', '#87CEEB')
        ]
        
        for i, (year, dest, color) in enumerate(modern_destinations):
            y_offset = 0.8 - (i * 0.05)
            ax.text(year + 500, y_offset, dest, 
                   fontsize=9, fontweight='bold', color=color, ha='left',
                   path_effects=[path_effects.withStroke(linewidth=1, foreground='black')])
        
        # Set axes properties
        ax.set_xlim(21000, -1000)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Years Ago', fontsize=14, color='white', fontweight='bold')
        ax.set_title('GEOLOGICAL TIMELINE: From Ancient Megafloods to Modern Travel\n' + 
                    'Your August 2025 Trip Through 20,000 Years of Geological History', 
                    fontsize=16, fontweight='bold', color='white', pad=20)
        
        # Remove y-axis
        ax.set_yticks([])
        
        # Style the axes
        ax.tick_params(colors='white', labelsize=12)
        for spine in ax.spines.values():
            spine.set_color('white')
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        
        plt.tight_layout()
        
        # Save the timeline
        filename = 'images/geological_timeline_comparison.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        return filename

def main():
    context = ModernTravelGeologicalContext()
    
    # Create main travel geological map
    travel_map = context.create_travel_geological_map()
    print(f"Modern travel geological context map created: {travel_map}")
    
    # Create timeline comparison
    timeline_map = context.create_timeline_comparison()
    print(f"Geological timeline comparison created: {timeline_map}")
    
    return travel_map, timeline_map

if __name__ == "__main__":
    main() 