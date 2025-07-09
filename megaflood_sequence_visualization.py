#!/usr/bin/env python3
"""
Missoula Megaflood Sequence Visualization
Critical failure points and flood routing based on USGS research

Key scientific findings:
- Ice dam failure mechanisms (subglacial drainage vs catastrophic breach)
- Multiple flood pathways depending on ice sheet positions
- Flood routing through Columbia River system
- Peak discharge estimates and flow velocities
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

class MegafloodSequenceVisualization:
    def __init__(self):
        # Critical failure sequence based on USGS research
        self.failure_sequence = {
            'ice_dam_buildup': {
                'duration': 'Decades to centuries',
                'mechanism': 'Cordilleran Ice Sheet advance',
                'water_level': 'Rising to 4,250 ft elevation',
                'pressure': 'Increasing hydrostatic pressure'
            },
            'critical_failure_point': {
                'trigger': 'Ice dam flotation or subglacial drainage',
                'location': 'Purcell Trench, northern Idaho',
                'mechanism': 'Catastrophic breach or jökulhlaup-style release',
                'peak_discharge': '20+ million cubic meters per second'
            },
            'flood_routing': {
                'primary_paths': ['Columbia Valley', 'Grand Coulee', 'Channeled Scablands'],
                'ice_controls': 'Okanogan lobe position determines routing',
                'flow_velocity': '65 mph (30-50 mph typical)',
                'drainage_time': '48 hours for complete lake emptying'
            },
            'geological_impact': {
                'erosion': 'Hundreds of feet of loess stripped',
                'carving': 'Deep coulees and scabland channels',
                'deposition': 'Boulder bars and flood sediments',
                'legacy': 'Modern landscape features'
            }
        }
        
        # Flood routing based on ice sheet positions (USGS modeling)
        self.ice_scenarios = {
            'early_floods': {
                'okanogan_position': 'Minimal advance',
                'primary_route': 'Columbia Valley',
                'secondary_routes': ['Moses Coulee'],
                'characteristics': 'Direct routing to Pacific'
            },
            'mid_period_floods': {
                'okanogan_position': 'Advanced - blocking Columbia',
                'primary_route': 'Grand Coulee',
                'secondary_routes': ['Channeled Scablands', 'Telford-Crab Creek'],
                'characteristics': 'Diverted through scablands'
            },
            'late_floods': {
                'okanogan_position': 'Maximum advance',
                'primary_route': 'Channeled Scablands',
                'secondary_routes': ['Cheney-Palouse'],
                'characteristics': 'Most complex routing'
            }
        }
        
    def create_failure_mechanism_diagram(self):
        """Create detailed diagram of ice dam failure mechanisms."""
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(20, 16))
        fig.patch.set_facecolor('#0F1419')
        
        # Panel 1: Ice dam buildup
        ax1.set_facecolor('#0F1419')
        
        # Draw ice dam cross-section
        x_profile = np.linspace(0, 10, 100)
        
        # Bedrock profile
        bedrock = 2 + 0.5 * np.sin(x_profile)
        ax1.fill_between(x_profile, 0, bedrock, color='#8B4513', alpha=0.8, label='Bedrock')
        
        # Ice dam profile
        ice_dam = bedrock + 6 * np.exp(-((x_profile - 5)**2) / 4)
        ax1.fill_between(x_profile, bedrock, ice_dam, color='#E6F7FF', alpha=0.8, label='Ice Dam')
        
        # Water level
        water_level = np.full_like(x_profile, 6.5)
        water_mask = x_profile < 5
        ax1.fill_between(x_profile[water_mask], bedrock[water_mask], water_level[water_mask], 
                        color='#4A90E2', alpha=0.7, label='Glacial Lake Missoula')
        
        # Annotations
        ax1.text(2.5, 4, 'GLACIAL LAKE\nMISSOULA\n500 cubic miles', 
                fontsize=12, fontweight='bold', color='#4A90E2', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        ax1.text(5, 8, 'ICE DAM\n2,500 ft high', 
                fontsize=12, fontweight='bold', color='#E6F7FF', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
        
        # Pressure arrows
        for i in range(1, 5):
            ax1.arrow(i, 6.5, 0, -1.5, head_width=0.1, head_length=0.1, 
                     fc='red', ec='red', linewidth=2)
        
        ax1.text(2.5, 3, 'HYDROSTATIC\nPRESSURE', 
                fontsize=11, fontweight='bold', color='red', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        ax1.set_xlim(0, 10)
        ax1.set_ylim(0, 10)
        ax1.set_title('ICE DAM BUILDUP\nHydrostatic Pressure Increases', 
                     fontsize=14, fontweight='bold', color='white')
        ax1.tick_params(colors='white')
        for spine in ax1.spines.values():
            spine.set_color('white')
        
        # Panel 2: Critical failure point
        ax2.set_facecolor('#0F1419')
        
        # Show failure mechanism
        ax2.fill_between(x_profile, 0, bedrock, color='#8B4513', alpha=0.8)
        
        # Failing ice dam
        failing_ice = bedrock + 3 * np.exp(-((x_profile - 5)**2) / 4)
        ax2.fill_between(x_profile, bedrock, failing_ice, color='#B8E6FF', alpha=0.6)
        
        # Breach point
        breach_x = np.linspace(4.5, 5.5, 10)
        breach_y = bedrock[45:55] + 0.5
        ax2.fill_between(breach_x, bedrock[45:55], breach_y, color='#FF0000', alpha=0.8)
        
        # Flood water rushing out
        flood_x = np.linspace(5.5, 10, 45)
        flood_y = 2 + 2 * np.exp(-((flood_x - 6)**2) / 2)
        ax2.fill_between(flood_x, bedrock[55:], flood_y, color='#FF4500', alpha=0.8)
        
        # Velocity arrows
        for i in range(6, 10):
            ax2.arrow(i, 3, 0.5, 0, head_width=0.2, head_length=0.1, 
                     fc='#FF4500', ec='#FF4500', linewidth=3)
        
        ax2.text(7.5, 4, '20+ MILLION\nCUBIC METERS\nPER SECOND', 
                fontsize=11, fontweight='bold', color='#FF4500', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        ax2.text(5, 5, 'DAM BREACH', 
                fontsize=12, fontweight='bold', color='#FF0000', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        ax2.set_xlim(0, 10)
        ax2.set_ylim(0, 10)
        ax2.set_title('CATASTROPHIC DAM FAILURE\nPeak Discharge: 20+ Million m³/s', 
                     fontsize=14, fontweight='bold', color='white')
        ax2.tick_params(colors='white')
        for spine in ax2.spines.values():
            spine.set_color('white')
        
        # Panel 3: Flood routing scenarios
        ax3.set_facecolor('#0F1419')
        
        # Simplified regional map
        x_map = np.linspace(0, 10, 100)
        y_map = np.linspace(0, 8, 80)
        X, Y = np.meshgrid(x_map, y_map)
        
        # Topography
        topo = 2 + 0.5 * np.sin(X * 0.5) + 0.3 * np.cos(Y * 0.7)
        ax3.contourf(X, Y, topo, levels=10, cmap='terrain', alpha=0.6)
        
        # Flood routes
        routes = {
            'Columbia Valley': ([1, 3, 5, 7, 9], [4, 4, 4, 4, 4]),
            'Grand Coulee': ([3, 4, 5, 6, 7], [5, 4, 3, 2, 1]),
            'Channeled Scablands': ([3, 4, 5, 6, 8], [3, 2.5, 2, 1.5, 1])
        }
        
        colors = ['#FF4500', '#FF6B35', '#FF8C69']
        for i, (route_name, (x_coords, y_coords)) in enumerate(routes.items()):
            ax3.plot(x_coords, y_coords, color=colors[i], linewidth=4, 
                    label=route_name, alpha=0.8)
            
            # Add arrows
            for j in range(len(x_coords)-1):
                ax3.annotate('', xy=(x_coords[j+1], y_coords[j+1]), 
                            xytext=(x_coords[j], y_coords[j]),
                            arrowprops=dict(arrowstyle='->', color=colors[i], lw=3))
        
        # Ice sheet positions
        ice_positions = [
            Rectangle((0.5, 6), 2, 1.5, facecolor='#E6F7FF', alpha=0.8),
            Rectangle((4, 5.5), 3, 2, facecolor='#E6F7FF', alpha=0.8)
        ]
        
        for ice_patch in ice_positions:
            ax3.add_patch(ice_patch)
        
        ax3.text(1.5, 6.7, 'Purcell\nTrench\nLobe', fontsize=10, fontweight='bold', 
                color='#2E5BDA', ha='center')
        ax3.text(5.5, 6.5, 'Okanogan\nLobe', fontsize=10, fontweight='bold', 
                color='#2E5BDA', ha='center')
        
        ax3.set_xlim(0, 10)
        ax3.set_ylim(0, 8)
        ax3.set_title('FLOOD ROUTING SCENARIOS\nIce Sheet Positions Control Flow Paths', 
                     fontsize=14, fontweight='bold', color='white')
        ax3.legend(loc='upper right', facecolor='black', edgecolor='white', 
                  framealpha=0.8, labelcolor='white')
        ax3.tick_params(colors='white')
        for spine in ax3.spines.values():
            spine.set_color('white')
        
        # Panel 4: Geological impact
        ax4.set_facecolor('#0F1419')
        
        # Before and after landscape profiles
        x_landscape = np.linspace(0, 10, 100)
        
        # Pre-flood landscape
        original_surface = 5 + 0.5 * np.sin(x_landscape * 0.5)
        ax4.fill_between(x_landscape, 0, original_surface, color='#8FBC8F', alpha=0.7, 
                        label='Original Landscape (Loess-covered)')
        
        # Post-flood landscape (eroded)
        eroded_surface = 3 + 0.8 * np.sin(x_landscape * 0.5) + 0.5 * np.sin(x_landscape * 2)
        ax4.fill_between(x_landscape, 0, eroded_surface, color='#8B4513', alpha=0.8, 
                        label='Post-flood Landscape (Scablands)')
        
        # Flood deposits
        deposit_locations = [2, 4, 6, 8]
        for loc in deposit_locations:
            deposit_x = np.linspace(loc-0.3, loc+0.3, 10)
            deposit_y = eroded_surface[int(loc*10):int(loc*10)+10] + 0.3
            ax4.fill_between(deposit_x, eroded_surface[int(loc*10):int(loc*10)+10], 
                            deposit_y, color='#DEB887', alpha=0.8)
        
        # Annotations
        ax4.text(5, 6, 'HUNDREDS OF FEET\nOF SOIL STRIPPED', 
                fontsize=12, fontweight='bold', color='#FF4500', ha='center',
                path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        ax4.text(2, 2.5, 'Boulder\nBars', fontsize=10, fontweight='bold', 
                color='#DEB887', ha='center')
        ax4.text(6, 2.5, 'Flood\nDeposits', fontsize=10, fontweight='bold', 
                color='#DEB887', ha='center')
        
        ax4.set_xlim(0, 10)
        ax4.set_ylim(0, 7)
        ax4.set_title('GEOLOGICAL IMPACT\nChanneled Scablands Formation', 
                     fontsize=14, fontweight='bold', color='white')
        ax4.legend(loc='upper right', facecolor='black', edgecolor='white', 
                  framealpha=0.8, labelcolor='white')
        ax4.tick_params(colors='white')
        for spine in ax4.spines.values():
            spine.set_color('white')
        
        # Main title
        fig.suptitle('MISSOULA MEGAFLOOD FAILURE SEQUENCE\nCritical Points of Catastrophic Dam Failure', 
                    fontsize=20, fontweight='bold', color='white', y=0.95)
        
        plt.tight_layout()
        
        # Save the diagram
        filename = 'images/megaflood_failure_sequence.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        return filename
    
    def create_flood_routing_map(self):
        """Create detailed map of flood routing through Columbia River system."""
        fig, ax = plt.subplots(1, 1, figsize=(18, 12))
        fig.patch.set_facecolor('#0F1419')
        ax.set_facecolor('#0F1419')
        
        # Regional topography
        x_region = np.linspace(-125, -110, 150)
        y_region = np.linspace(44, 49, 100)
        X, Y = np.meshgrid(x_region, y_region)
        
        # Elevation model
        elevation = np.zeros_like(X)
        
        # Mountain ranges
        cascades = ((X < -120) & (Y > 45) & (Y < 48))
        elevation[cascades] = 3000 + 2000 * np.exp(-((X[cascades] + 121)**2 + (Y[cascades] - 46.5)**2) / 4)
        
        rockies = ((X > -117) & (Y > 46))
        elevation[rockies] = 4000 + 3000 * np.exp(-((X[rockies] + 114)**2 + (Y[rockies] - 47)**2) / 8)
        
        # Columbia River valley
        river_valley = ((Y > 45) & (Y < 46.5) & (X > -123) & (X < -117))
        elevation[river_valley] = 1000 + 300 * np.sin((X[river_valley] + 120) * 2)
        
        # Topographic colormap
        topo_colors = ['#2E77C0', '#5C96D0', '#8AB5E0', '#B8D4F0', '#E6F3FF', '#F0F8FF']
        topo_cmap = LinearSegmentedColormap.from_list('topo', topo_colors, N=256)
        
        contour = ax.contourf(X, Y, elevation, levels=25, cmap=topo_cmap, alpha=0.7)
        
        # Ice sheet positions
        ice_sheets = [
            # Purcell Trench lobe
            [(-117.5, 49.0), (-116.0, 49.0), (-116.0, 47.0), (-117.5, 47.0)],
            # Okanogan lobe
            [(-120.5, 49.0), (-118.0, 49.0), (-118.0, 46.5), (-120.5, 46.5)]
        ]
        
        for ice_coords in ice_sheets:
            ice_polygon = Polygon(ice_coords, facecolor='#E6F7FF', 
                                edgecolor='#B8E6FF', linewidth=2, alpha=0.8)
            ax.add_patch(ice_polygon)
        
        # Glacial Lake Missoula
        lake_coords = [(-114.5, 47.8), (-113.0, 47.8), (-113.0, 46.0), (-114.5, 46.0)]
        lake_polygon = Polygon(lake_coords, facecolor='#4A90E2', 
                             edgecolor='#2E5BDA', linewidth=2, alpha=0.8)
        ax.add_patch(lake_polygon)
        
        # Flood routing paths
        flood_routes = {
            'Columbia Valley Route': {
                'coords': [(-116.5, 48.0), (-119.0, 47.0), (-121.0, 45.5), (-123.0, 45.7)],
                'color': '#FF4500',
                'width': 8,
                'label': 'Early floods (Columbia Valley open)'
            },
            'Grand Coulee Route': {
                'coords': [(-116.5, 48.0), (-119.0, 47.5), (-119.5, 47.0), (-119.0, 46.0), (-121.0, 45.5)],
                'color': '#FF6B35',
                'width': 6,
                'label': 'Mid-period floods (Okanogan lobe blocks Columbia)'
            },
            'Channeled Scablands Route': {
                'coords': [(-116.5, 48.0), (-118.0, 47.0), (-118.5, 46.5), (-119.0, 46.0), (-121.0, 45.5)],
                'color': '#FF8C69',
                'width': 4,
                'label': 'Late floods (Maximum ice advance)'
            }
        }
        
        for route_name, route_data in flood_routes.items():
            coords = route_data['coords']
            lons, lats = zip(*coords)
            
            ax.plot(lons, lats, color=route_data['color'], 
                   linewidth=route_data['width'], alpha=0.8, 
                   label=route_data['label'], zorder=10)
            
            # Add directional arrows
            for i in range(len(lons)-1):
                ax.annotate('', xy=(lons[i+1], lats[i+1]), 
                           xytext=(lons[i], lats[i]),
                           arrowprops=dict(arrowstyle='->', 
                                         color=route_data['color'],
                                         lw=3, alpha=0.8))
        
        # Major geological features
        features = [
            (-116.5, 48.0, 'ICE DAM\nBreach Point', '#FF0000'),
            (-119.0, 47.0, 'Grand Coulee\nFormation', '#8B4513'),
            (-118.5, 46.5, 'Channeled\nScablands', '#8B4513'),
            (-121.0, 45.5, 'Wallula Gap\nBottleneck', '#8B4513'),
            (-122.5, 45.7, 'Columbia River\nGorge', '#4A90E2')
        ]
        
        for lon, lat, label, color in features:
            ax.plot(lon, lat, 'o', color=color, markersize=10, 
                   markeredgecolor='white', markeredgewidth=2, zorder=15)
            ax.text(lon, lat-0.2, label, 
                   fontsize=9, fontweight='bold', color=color, ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='white')])
        
        # Modern cities for reference
        cities = [
            (-113.99, 46.87, 'Missoula'),
            (-116.10, 44.90, 'McCall'),
            (-117.43, 45.49, 'Lostine'),
            (-118.34, 45.70, 'Walla Walla')
        ]
        
        for lon, lat, name in cities:
            ax.plot(lon, lat, 's', color='#FFD700', markersize=8, 
                   markeredgecolor='white', markeredgewidth=1, zorder=15)
            ax.text(lon, lat+0.2, name, 
                   fontsize=9, fontweight='bold', color='#FFD700', ha='center',
                   path_effects=[path_effects.withStroke(linewidth=2, foreground='black')])
        
        # Set map bounds and labels
        ax.set_xlim(-125, -110)
        ax.set_ylim(44, 49)
        ax.set_xlabel('Longitude', fontsize=12, color='white', fontweight='bold')
        ax.set_ylabel('Latitude', fontsize=12, color='white', fontweight='bold')
        ax.set_title('MISSOULA MEGAFLOOD ROUTING SYSTEM\nIce Sheet Positions Control Flow Pathways', 
                    fontsize=18, fontweight='bold', color='white', pad=20)
        
        # Create legend
        legend_elements = [
            Line2D([0], [0], color='#FF4500', linewidth=6, label='Early floods (Columbia Valley)'),
            Line2D([0], [0], color='#FF6B35', linewidth=6, label='Mid-period floods (Grand Coulee)'),
            Line2D([0], [0], color='#FF8C69', linewidth=6, label='Late floods (Channeled Scablands)'),
            mpatches.Patch(color='#E6F7FF', alpha=0.8, label='Cordilleran Ice Sheet'),
            mpatches.Patch(color='#4A90E2', alpha=0.8, label='Glacial Lake Missoula'),
            Line2D([0], [0], marker='s', color='#FFD700', markersize=8, 
                   label='Modern cities (your route)', linestyle='None')
        ]
        
        ax.legend(handles=legend_elements, loc='upper left', 
                 fancybox=True, shadow=True, fontsize=11,
                 facecolor='black', edgecolor='white', framealpha=0.8)
        
        # Style the axes
        ax.tick_params(colors='white', labelsize=10)
        for spine in ax.spines.values():
            spine.set_color('white')
        
        plt.tight_layout()
        
        # Save the map
        filename = 'images/megaflood_routing_map.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight', 
                   facecolor='#0F1419', edgecolor='none')
        plt.close()
        
        return filename

def main():
    visualizer = MegafloodSequenceVisualization()
    
    # Create failure sequence diagram
    sequence_file = visualizer.create_failure_mechanism_diagram()
    print(f"Megaflood failure sequence diagram created: {sequence_file}")
    
    # Create flood routing map
    routing_file = visualizer.create_flood_routing_map()
    print(f"Flood routing map created: {routing_file}")
    
    return sequence_file, routing_file

if __name__ == "__main__":
    main() 