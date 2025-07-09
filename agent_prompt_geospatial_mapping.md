# Enhanced Geospatial Mapping Agent Prompt
## Pacific Northwest Travel Guide Project

### **CONTEXT & BACKGROUND**

You are working on a **Pacific Northwest travel booking guide** project that creates scientifically accurate, artistically enhanced maps combining:
- **Real geospatial data** (USGS geological, hydrological, elevation)
- **Subglacial fluvial textures** (artistic geological interpretation)
- **Art Nouveau decorative elements** (subtle organic patterns)
- **3D exaggerated topography** for dramatic landscape visualization

### **PROJECT STATUS**

**✅ COMPLETED:**
- Columbia River Gorge (enhanced geospatial map)
- Bozeman, Montana (basic geomorphological map)
- Seattle, Washington (basic geomorphological map)
- All basic walking maps for all locations

**🎯 YOUR ASSIGNMENT (work bottom-up):**
1. **Walla Walla, Washington** - Columbia Plateau loess hills & wine country
2. **Lostine, Oregon** - Small mountain town (simpler scope)
3. **Joseph, Oregon** - Wallowa Mountains alpine glacial terrain

**🎯 OTHER AGENT (working top-down):**
1. **Missoula, Montana** - Glacial Lake Missoula deposits
2. **McCall, Idaho** - Payette Lake glacial cirque

### **TECHNICAL SETUP**

**Required Files (already exist):**
- `columbia_river_gorge_enhanced_map.py` - Reference implementation
- `geospatial_data_integration.py` - Data source framework
- `smadar_booking_booklet_redesigned.qmd` - LaTeX document to update

**Required Libraries (already installed):**
```bash
pip3 install matplotlib numpy scipy requests geopandas contextily pillow
```

**Directory Structure:**
```
PNW_summer25/
├── images/                    # Map outputs
├── geospatial_cache/         # Data caching
└── smadar_booking_booklet_redesigned.qmd
```

### **YOUR SPECIFIC LOCATIONS & GEOLOGICAL CONTEXT**

#### **1. WALLA WALLA, WASHINGTON**
**Geological Context:**
- **Columbia Plateau** - Flood basalt province
- **Loess Hills** - Wind-blown glacial sediment deposits
- **Walla Walla River Valley** - Agricultural drainage
- **Wine terroir geology** - Basalt bedrock with loess soils

**Key Features to Include:**
- Blue Mountains to the east
- Columbia River Basalt Group bedrock
- Quaternary loess deposits (Palouse Formation)
- Modern agricultural landscape on geological foundation
- Wine region geological terroir

**Accommodation:** Eritage Resort (1319 Bergevin Springs Road)

#### **2. LOSTINE, OREGON** 
**Geological Context:**
- **Wallowa Mountains foothills** - Granite batholith
- **Lostine River** - Alpine drainage
- **Glacial valley** - U-shaped profile
- **Small scope** - Focus on valley morphology

**Key Features to Include:**
- Lostine River valley glacial carving
- Wallowa granite intrusions
- Alpine to valley floor elevation gradient
- Historic settlement on alluvial terraces

**Accommodation:** Day trip from Joseph

#### **3. JOSEPH, OREGON**
**Geological Context:**
- **Wallowa Mountains** - "Alps of Oregon"
- **Alpine glacial terrain** - Cirques, moraines, U-valleys
- **Granite batholith** - Mesozoic intrusion
- **Wallowa Lake** - Glacial lake in terminal moraine

**Key Features to Include:**
- Wallowa granite (165 Ma)
- Quaternary glacial features
- Alpine cirques and hanging valleys
- Wallowa Lake glacial dam
- Modern alpine environment

**Accommodation:** The Jennings Hotel (100 Main St)

### **IMPLEMENTATION TEMPLATE**

Create files following this pattern:
```python
#!/usr/bin/env python3
"""
Enhanced Geospatial Mapping: [LOCATION NAME]
[Geological description]
"""

import matplotlib.pyplot as plt
import numpy as np
import json
from pathlib import Path
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Circle, Polygon
import matplotlib.patheffects as path_effects
from scipy.ndimage import gaussian_filter

# Location-specific bounds
LOCATION_BOUNDS = {
    'north': [latitude],
    'south': [latitude], 
    'east': [longitude],
    'west': [longitude]
}

class [Location]GeoMapper:
    def __init__(self):
        self.cache_dir = Path('geospatial_cache')
        self.cache_dir.mkdir(exist_ok=True)
    
    def get_elevation_data(self):
        """Generate realistic elevation data based on geological knowledge."""
        # Implement location-specific topography
        pass
    
    def get_geological_features(self):
        """Define geological formations for the area."""
        # Location-specific geology
        pass
    
    def get_hydrological_features(self):
        """Define water features."""
        # Rivers, lakes, watersheds
        pass
    
    def create_subglacial_texture(self, shape, intensity=0.25):
        """Location-appropriate fluvial textures."""
        # Geological process-specific patterns
        pass
    
    def create_enhanced_map(self):
        """Create the complete enhanced map."""
        # Full implementation following Columbia Gorge pattern
        pass

def main():
    mapper = [Location]GeoMapper()
    filename = mapper.create_enhanced_map()
    print(f"Enhanced {location} map created: {filename}")

if __name__ == "__main__":
    main()
```

### **GEOLOGICAL DATA SOURCES**

**For Each Location, Include:**
1. **Bedrock Geology** - Major formations and ages
2. **Surficial Geology** - Quaternary deposits, glacial features
3. **Structural Features** - Faults, folds if relevant
4. **Hydrological Features** - Rivers, lakes, watersheds
5. **Elevation Profile** - Realistic topographic relief

**Geological Time Periods to Reference:**
- **Precambrian** - Basement rocks
- **Paleozoic-Mesozoic** - Marine sediments, intrusions
- **Miocene** - Columbia River Basalt Group (~15 Ma)
- **Quaternary** - Glacial features, modern landforms

### **VISUAL STYLE REQUIREMENTS**

**Essential Elements:**
1. **Subglacial fluvial textures** - Organic flow patterns
2. **3D exaggerated elevation** - Dramatic landscape relief
3. **Scientific color schemes** - Geological/ecological
4. **Art Nouveau decorative borders** - Subtle organic elements
5. **High contrast labels** - White text with clean stroke effects

**CRITICAL TRANSPARENCY GUIDELINES:**
- **Elevation contours:** alpha=0.6 (NOT 0.9 - too opaque!)
- **Geological overlays:** alpha=0.15 (subtle highlighting only)
- **Water features:** alpha=0.6 (lakes), alpha=0.8 (rivers)
- **Legend backgrounds:** framealpha=0.6 (readable but not overwhelming)

**STROKE EFFECT GUIDELINES:**
- **Hotel/accommodation text:** linewidth=2 (NOT 3 - too thick!)
- **Location labels:** linewidth=1.5 (clean and readable)
- **Title text:** linewidth=2 (prominent but not overwhelming)
- **Geological boundaries:** linewidth=1.5, solid lines (NOT dashed)
- **All strokes:** Use black foreground for white text, white foreground for colored text

**Technical Specifications:**
- **Figure size:** (18, 12) inches for consistent scaling
- **DPI:** 300 for high quality
- **Color depth:** Scientific accuracy with artistic enhancement
- **File format:** PNG with dark background (#0F1419)

### **INTEGRATION REQUIREMENTS**

**LaTeX Booklet Integration:**
Each completed map needs to replace the basic walking map in `smadar_booking_booklet_redesigned.qmd`:

```latex
\begin{figure}[h]
\centering
\includegraphics[width=0.9\textwidth]{images/[location]_enhanced_geospatial.png}
\caption{\textbf{\textcolor{primary}{[LOCATION] • Enhanced Geomorphological Context}} \\ 
\textbf{\textcolor{secondary}{Accommodation:}} \textcolor{mapred}{●} [Hotel Name] \\
\textbf{\textcolor{secondary}{Geological Features:}} \\
[Location-specific geological features with colors and descriptions]
\textbf{\textcolor{secondary}{Key Locations:}} \\
[Important landmarks and features]}
\end{figure}
```

### **DELIVERABLES**

**For Each Location:**
1. **Enhanced geospatial map** - High-quality PNG file
2. **Python script** - Documented implementation
3. **LaTeX integration** - Updated booklet section
4. **Data cache files** - Geological/elevation data

**File Naming Convention:**
- `[location]_enhanced_geospatial_map.py`
- `images/[location]_enhanced_geospatial.png`
- Cache: `geospatial_cache/[location]_[datatype].json`

### **SUCCESS CRITERIA**

**Each map should demonstrate:**
✅ Scientific geological accuracy for the region  
✅ Artistic enhancement with subglacial textures  
✅ Functional accommodation and landmark information  
✅ Educational geological storytelling  
✅ Integration with existing LaTeX document  
✅ High visual quality for print production  

### **COORDINATION**

**Progress Tracking:**
- Start with **Walla Walla** (wine country geology)
- Move to **Lostine** (simplest scope)
- Finish with **Joseph** (most complex alpine terrain)

**When Complete:**
- Update the main LaTeX document
- Generate final PDF with all enhanced maps
- Verify all geological data is scientifically accurate

### **REFERENCE MATERIALS**

**Use Columbia River Gorge implementation as template:**
- File: `columbia_river_gorge_enhanced_map.py`
- Success pattern: Real data + artistic enhancement
- Integration example: Already in booking booklet

**Geological Resources:**
- USGS geological maps for each state
- Quaternary research for glacial features  
- Regional geological surveys
- Academic literature on Pacific Northwest geology

---

**START WITH WALLA WALLA AND WORK YOUR WAY UP THE LIST!** 