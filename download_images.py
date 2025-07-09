#!/usr/bin/env python3
"""
Generate professional travel images for the Pacific Northwest trip itinerary.
Creates clean, gradient-based images with professional typography.
"""

import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

# Create images directory if it doesn't exist
os.makedirs('images', exist_ok=True)

def create_gradient_background(width, height, color1, color2, direction='horizontal'):
    """Create a smooth gradient background."""
    if direction == 'horizontal':
        gradient = np.linspace(0, 1, width)
        gradient = np.tile(gradient, (height, 1))
    else:  # vertical
        gradient = np.linspace(0, 1, height)
        gradient = np.tile(gradient, (width, 1)).T
    
    # Convert colors to RGB arrays
    c1 = np.array(color1)
    c2 = np.array(color2)
    
    # Create gradient for each channel
    image_array = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(3):
        image_array[:, :, i] = c1[i] + gradient * (c2[i] - c1[i])
    
    return Image.fromarray(image_array)

def create_professional_location_image(location_name, subtitle, gradient_colors, width=800, height=500):
    """Create a professional-looking location image with gradients."""
    
    # Create gradient background
    img = create_gradient_background(width, height, gradient_colors[0], gradient_colors[1])
    draw = ImageDraw.Draw(img)
    
    # Try to load professional fonts
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 56)
        subtitle_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 24)
    except:
        try:
            title_font = ImageFont.truetype("arial.ttf", 56)
            subtitle_font = ImageFont.truetype("arial.ttf", 24)
        except:
            title_font = ImageFont.load_default()
            subtitle_font = ImageFont.load_default()
    
    # Add subtle overlay for text readability
    overlay = Image.new('RGBA', (width, height), (0, 0, 0, 40))
    img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
    draw = ImageDraw.Draw(img)
    
    # Calculate text positions
    title_bbox = draw.textbbox((0, 0), location_name, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_height = title_bbox[3] - title_bbox[1]
    
    subtitle_bbox = draw.textbbox((0, 0), subtitle, font=subtitle_font)
    subtitle_width = subtitle_bbox[2] - subtitle_bbox[0]
    
    # Position text in center
    title_x = (width - title_width) // 2
    title_y = (height - title_height) // 2 - 20
    
    subtitle_x = (width - subtitle_width) // 2
    subtitle_y = title_y + title_height + 15
    
    # Draw text with subtle shadow
    shadow_offset = 2
    draw.text((title_x + shadow_offset, title_y + shadow_offset), location_name, 
              fill=(0, 0, 0, 100), font=title_font)
    draw.text((title_x, title_y), location_name, fill="white", font=title_font)
    
    draw.text((subtitle_x + shadow_offset, subtitle_y + shadow_offset), subtitle, 
              fill=(0, 0, 0, 80), font=subtitle_font)
    draw.text((subtitle_x, subtitle_y), subtitle, fill="white", font=subtitle_font)
    
    return img

def create_route_overview_image():
    """Create a clean route overview with professional styling."""
    width, height = 1000, 600
    
    # Mountain-inspired gradient
    img = create_gradient_background(width, height, (135, 206, 235), (25, 25, 112), 'vertical')
    draw = ImageDraw.Draw(img)
    
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 42)
        location_font = ImageFont.truetype("/System/Library/Fonts/Avenir Next.ttc", 18)
    except:
        title_font = ImageFont.load_default()
        location_font = ImageFont.load_default()
    
    # Title
    title = "Pacific Northwest Adventure Route"
    title_bbox = draw.textbbox((0, 0), title, font=title_font)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    
    # Draw title with shadow
    draw.text((title_x + 2, 52), title, fill=(0, 0, 0, 100), font=title_font)
    draw.text((title_x, 50), title, fill="white", font=title_font)
    
    # Route points with better positioning
    route_points = [
        ("Bozeman, MT", "Aug 3-4", 150, 150),
        ("Missoula, MT", "Aug 5", 120, 220),
        ("Jerry Johnson HS", "Aug 6", 180, 290),
        ("McCall, ID", "Aug 7-8", 250, 360),
        ("Joseph, OR", "Aug 9", 120, 430),
        ("Walla Walla, WA", "Aug 10", 350, 400),
        ("Columbia Gorge", "Aug 11", 500, 350),
        ("Seattle, WA", "Aug 12-14", 650, 200)
    ]
    
    # Draw connecting lines
    for i in range(len(route_points) - 1):
        x1, y1 = route_points[i][2], route_points[i][3]
        x2, y2 = route_points[i+1][2], route_points[i+1][3]
        draw.line([(x1, y1), (x2, y2)], fill="white", width=3)
    
    # Draw points and labels
    for location, date, x, y in route_points:
        # Draw circle with border
        radius = 12
        draw.ellipse([x-radius-2, y-radius-2, x+radius+2, y+radius+2], 
                    fill="white", outline="navy", width=2)
        draw.ellipse([x-radius, y-radius, x+radius, y+radius], 
                    fill="#FF6B35")
        
        # Draw location labels with background
        text = f"{location}\n{date}"
        text_bbox = draw.textbbox((0, 0), text, font=location_font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Position text to avoid overlap
        text_x = x + 20
        text_y = y - text_height // 2
        
        # Draw text background
        draw.rectangle([text_x-3, text_y-3, text_x+text_width+3, text_y+text_height+3],
                      fill=(0, 0, 0, 120))
        draw.text((text_x, text_y), text, fill="white", font=location_font)
    
    return img

# Generate all location images
locations = {
    "route_overview": {
        "title": "Pacific Northwest Adventure Route",
        "subtitle": "August 3-14, 2025 • 1,200 miles",
        "colors": [(135, 206, 235), (25, 25, 112)]
    },
    "bozeman_montana": {
        "title": "Bozeman, Montana",
        "subtitle": "Gateway to Big Sky Country",
        "colors": [(218, 165, 32), (139, 69, 19)]
    },
    "missoula_montana": {
        "title": "Missoula, Montana", 
        "subtitle": "University Town & Riverfront",
        "colors": [(144, 238, 144), (34, 139, 34)]
    },
    "jerry_johnson_hot_springs": {
        "title": "Jerry Johnson Hot Springs",
        "subtitle": "Natural Wilderness Springs",
        "colors": [(70, 130, 180), (25, 25, 112)]
    },
    "shore_lodge_mccall": {
        "title": "Shore Lodge, McCall",
        "subtitle": "Luxury Lakefront Resort",
        "colors": [(0, 191, 255), (30, 144, 255)]
    },
    "wallowa_lake": {
        "title": "Joseph & Wallowa Lake",
        "subtitle": "Oregon's Alpine Paradise",
        "colors": [(34, 139, 34), (0, 100, 0)]
    },
    "walla_walla_vineyards": {
        "title": "Walla Walla Wine Country",
        "subtitle": "Premier Washington Wine Region",
        "colors": [(128, 0, 128), (75, 0, 130)]
    },
    "columbia_river_gorge": {
        "title": "Columbia River Gorge",
        "subtitle": "Waterfalls & Scenic Beauty",
        "colors": [(65, 105, 225), (25, 25, 112)]
    },
    "seattle_waterfront": {
        "title": "Seattle, Washington",
        "subtitle": "Emerald City Adventures",
        "colors": [(105, 105, 105), (47, 79, 79)]
    }
}

def main():
    """Generate all professional travel images."""
    print("Generating professional travel images...")
    
    # Create route overview
    route_img = create_route_overview_image()
    route_img.save('images/route_overview.jpg', quality=95)
    print(f"✓ Created: images/route_overview.jpg")
    
    # Create location images
    for location_key, data in locations.items():
        if location_key != "route_overview":
            img = create_professional_location_image(
                data["title"], 
                data["subtitle"], 
                data["colors"]
            )
            filename = f"images/{location_key}.jpg"
            img.save(filename, quality=95)
            print(f"✓ Created: {filename}")
    
    print(f"\n✨ Generated {len(locations)} professional travel images")
    print("All images use clean gradients and professional typography!")

if __name__ == "__main__":
    main() 