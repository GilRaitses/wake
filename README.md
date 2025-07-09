# Pacific Northwest Summer Adventure Travel Guide

This project generates a comprehensive travel guide for your August 2025 Pacific Northwest trip, complete with interactive maps, route information, visual location guides, and detailed parent travel information.

## 🗺️ Trip Overview

**Route:** Montana → Idaho → Oregon → Washington  
**Duration:** August 3-14, 2025  
**Highlights:** Hot springs, luxury lodging, wine country, alpine lakes, and scenic drives

## 🚀 Quick Start

### One-Command Setup
```bash
./generate_travel_guide.sh
```

This script will:
- Install all required Python packages
- Generate route maps and driving times
- Create location images and visual guides
- Render the final PDF and HTML travel guide

### Manual Steps

1. **Install Python dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Generate maps and route data:**
   ```bash
   python3 generate_route_maps.py
   ```

3. **Create location images:**
   ```bash
   python3 download_images.py
   ```

4. **Find current hotel rates:**
   ```bash
   python3 find_hotel_rates.py
   ```

5. **Render the travel guide:**
   ```bash
   quarto render trip_itinerary_august_2025.qmd --to pdf
   ```

## 📁 Generated Files

- **`trip_itinerary_august_2025.qmd`** - Quarto source document
- **`trip_itinerary_august_2025.pdf`** - Final PDF travel guide
- **`trip_itinerary_august_2025.html`** - Interactive HTML version
- **`parent_travel_summary.md`** - Concise parent travel guide
- **`images/`** - Directory containing all generated maps and photos

## ✈️ Parent Travel Information

The travel guide includes a dedicated section for parents with:

### Flight Recommendations
- **To Bozeman (Aug 3):** ~$109/person (save $140-240 vs Aug 4)
- **From Seattle (Aug 12):** ~$249/person (same-day return to NY)

### Hotel Budget Estimates
- **Total trip cost:** $4,366-4,866 per couple
- **Lodging:** $2,650 for 8 nights
- **Key property:** Shore Lodge McCall (~$500/night)

### Booking Priorities
1. **URGENT:** August 3rd flights (significant savings)
2. **HIGH:** Shore Lodge reservation (luxury property)
3. **RECOMMENDED:** All other hotels for August dates

## 🖼️ Visual Elements

The generated travel guide includes:

### Maps & Routes
- Interactive route map with all waypoints
- Elevation profile showing terrain changes
- Driving times and distances between locations

### Location Images
- Shore Lodge, McCall (luxury lakefront resort)
- Jerry Johnson Hot Springs (natural wilderness springs)
- Wallowa Lake, Oregon (alpine lake setting)
- Columbia River Gorge (waterfall scenery)
- Walla Walla wine country vineyards
- Bozeman and Missoula, Montana
- Seattle waterfront

### Visual Guides
- Hot springs comparison chart
- Route overview with key stops
- Elevation profile across the journey

## 🏔️ Key Destinations

1. **Bozeman, MT** - Gateway to Big Sky country
2. **Missoula, MT** - University town on the Clark Fork River
3. **Jerry Johnson Hot Springs** - Natural hot springs on Highway 12
4. **McCall, ID** - Shore Lodge luxury resort + hot springs tours
5. **Joseph, OR** - Wallowa Lake and alpine scenery
6. **Walla Walla, WA** - Premier wine region
7. **Columbia River Gorge** - Glamping with waterfall views
8. **Seattle, WA** - Urban exploration and departure

## 🌊 Hot Springs Guide

The trip includes access to multiple hot springs:
- **Jerry Johnson** - Free, natural wilderness springs
- **Trail Creek** - Roadside access, creek-side pools
- **Burgdorf** - Historic resort ($20/adult)
- **Gold Fork** - Family-friendly, tiered pools ($10/adult)

## 🛠️ Requirements

- **Python 3.7+** with pip
- **Quarto** for document rendering (install from [quarto.org](https://quarto.org))
- **Required Python packages** (auto-installed):
  - folium (interactive maps)
  - geopy (geocoding)
  - matplotlib (charts)
  - requests (web requests)
  - beautifulsoup4 (web scraping)
  - pillow (image processing)
  - numpy (numerical computing)

## 📱 Usage Tips

- The HTML version includes interactive elements
- PDF is optimized for printing and offline use
- All images are embedded for standalone viewing
- Route maps include clickable waypoints
- Hot springs guide provides practical information
- Parent section includes booking checklist and budget estimates

## 🎯 Customization

To modify the itinerary:
1. Edit `trip plans` (original YAML)
2. Update `trip_itinerary_august_2025.qmd`
3. Modify location data in `download_images.py`
4. Adjust route points in `generate_route_maps.py`
5. Update hotel information in `find_hotel_rates.py`
6. Re-run `./generate_travel_guide.sh`

## 📊 Hotel Rate Finder

Use the hotel rate finder to get current pricing:
```bash
python3 find_hotel_rates.py
```

This generates:
- Search suggestions for each hotel
- Contact information and websites
- Estimated rate ranges
- Booking priority checklist

## 🚗 Driving Information

- **Total Distance:** ~1,200 miles
- **Key Scenic Drive:** Highway 12 (Northwest Passage Scenic Byway)
- **Elevation Range:** Sea level (Seattle) to 5,021 ft (McCall)
- **Mountain Passes:** Allow extra time for curvy roads

## 💰 Budget Summary

### Parent Trip Costs (per couple):
- **Flights:** $716 (Aug 3 + Aug 12)
- **Hotels:** $2,650 (8 nights)
- **Meals/Activities:** $1,000-1,500
- **Total:** $4,366-4,866

### Money-Saving Tips:
- Book August 3rd flights (save $280+ per couple)
- Reserve hotels early for better rates
- Consider Shore Lodge packages for dining credits
- Look for wine country tour packages in Walla Walla

---

*Created with love for an epic Pacific Northwest adventure! 🏔️* 