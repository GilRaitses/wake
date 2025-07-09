#!/bin/bash
# Pacific Northwest Travel Guide Generator
# This script generates all maps, images, and renders the final PDF

echo "🏔️  Pacific Northwest Travel Guide Generator"
echo "============================================"

# Check if Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is required but not installed. Please install Python3 first."
    exit 1
fi

# Check if Quarto is installed
if ! command -v quarto &> /dev/null; then
    echo "⚠️  Quarto not found. Install from: https://quarto.org/docs/get-started/"
    echo "    Or install with: brew install quarto"
    echo "    Continuing without PDF generation..."
    QUARTO_AVAILABLE=false
else
    QUARTO_AVAILABLE=true
fi

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

# Create images directory if it doesn't exist
mkdir -p images

# Generate route maps and data
echo "🗺️  Generating route maps and driving times..."
python3 generate_route_maps.py

# Generate location images
echo "🖼️  Creating location images..."
python3 download_images.py

# Generate hotel search guide
echo "🏨 Generating hotel rate finder..."
python3 find_hotel_rates.py

# List generated files
echo "📁 Generated files:"
ls -la images/
echo ""
echo "📄 Travel documents:"
ls -la *.md *.qmd *.json 2>/dev/null || echo "No additional documents found"

# Render the PDF if Quarto is available
if [ "$QUARTO_AVAILABLE" = true ]; then
    echo "📄 Rendering PDF travel guide..."
    quarto render trip_itinerary_august_2025.qmd --to pdf
    
    if [ $? -eq 0 ]; then
        echo "✅ PDF generated successfully: trip_itinerary_august_2025.pdf"
    else
        echo "❌ PDF generation failed. Check the Quarto output above."
    fi
else
    echo "⚠️  Skipping PDF generation (Quarto not available)"
    echo "   You can still render manually with: quarto render trip_itinerary_august_2025.qmd"
fi

# Generate HTML version
echo "🌐 Generating HTML version..."
if [ "$QUARTO_AVAILABLE" = true ]; then
    quarto render trip_itinerary_august_2025.qmd --to html
    if [ $? -eq 0 ]; then
        echo "✅ HTML generated successfully: trip_itinerary_august_2025.html"
    fi
fi

echo ""
echo "🎉 Travel guide generation complete!"
echo "Files created:"
echo "   - trip_itinerary_august_2025.qmd (Quarto source)"
echo "   - trip_itinerary_august_2025.html (HTML version)"
echo "   - trip_itinerary_august_2025.pdf (PDF version - if Quarto available)"
echo "   - parent_travel_summary.md (Parent travel guide)"
echo "   - hotel_search_results.json (Hotel search data)"
echo "   - images/ directory with all maps and photos"
echo ""
echo "✈️  PARENT TRAVEL SUMMARY:"
echo "   - Flight recommendation: Aug 3 to BZN (~$109/person)"
echo "   - Return flight: Aug 12 from SEA (~$249/person)"
echo "   - Total trip cost: $4,366-4,866 per couple"
echo "   - Priority booking: Shore Lodge (800) 657-6464"
echo ""
echo "🚀 Open the HTML file in your browser to view the interactive travel guide!"
echo "📋 Check parent_travel_summary.md for booking checklist and budget details!" 