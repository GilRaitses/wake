#!/usr/bin/env python3
"""
Hotel Rate Finder for Pacific Northwest Trip
Helps find current rates for specific hotels in the itinerary
"""

import requests
import json
from datetime import datetime, timedelta

# Hotel search information
hotels = {
    "shore_lodge": {
        "name": "Shore Lodge",
        "location": "McCall, Idaho",
        "dates": "August 7-8, 2025",
        "phone": "(800) 657-6464",
        "website": "https://shorelodge.com",
        "estimated_rate": "$400-600/night",
        "features": "Luxury lakefront resort, 77 suites, spa, dining"
    },
    "jennings_hotel": {
        "name": "Jennings Hotel",
        "location": "Joseph, Oregon",
        "dates": "August 9, 2025",
        "phone": "Contact needed",
        "website": "Search needed",
        "estimated_rate": "$200-300/night",
        "features": "Historic downtown location, near Wallowa Lake"
    },
    "eritage_resort": {
        "name": "Eritage Resort",
        "location": "Walla Walla, Washington",
        "dates": "August 10, 2025",
        "phone": "Contact needed",
        "website": "Search needed",
        "estimated_rate": "$300-500/night",
        "features": "Wine country resort, vineyard views, spa"
    },
    "under_canvas": {
        "name": "Under Canvas Columbia River",
        "location": "Columbia River Gorge, Washington",
        "dates": "August 11, 2025",
        "phone": "Contact needed",
        "website": "https://undercanvas.com",
        "estimated_rate": "$200-400/night",
        "features": "Luxury glamping, furnished tents, scenic location"
    }
}

def print_hotel_search_guide():
    """Print a guide for manually searching hotel rates."""
    print("="*60)
    print("HOTEL RATE SEARCH GUIDE - Pacific Northwest Trip")
    print("="*60)
    print()
    
    for hotel_key, hotel_info in hotels.items():
        print(f"🏨 {hotel_info['name']}")
        print(f"   Location: {hotel_info['location']}")
        print(f"   Dates: {hotel_info['dates']}")
        print(f"   Estimated Rate: {hotel_info['estimated_rate']}")
        print(f"   Features: {hotel_info['features']}")
        
        if hotel_info['phone'] != "Contact needed":
            print(f"   Phone: {hotel_info['phone']}")
        if hotel_info['website'] != "Search needed":
            print(f"   Website: {hotel_info['website']}")
        
        print()
        print("   SEARCH SUGGESTIONS:")
        print(f"   • Google: '{hotel_info['name']} {hotel_info['location']} August 2025 rates'")
        print(f"   • Booking.com: Search for '{hotel_info['name']}' in {hotel_info['location']}")
        print(f"   • Hotels.com: Search location '{hotel_info['location']}' for August 7-9, 2025")
        print()
        print("-" * 60)
        print()

def create_booking_checklist():
    """Create a booking checklist for parents."""
    print("📋 BOOKING CHECKLIST FOR PARENTS")
    print("=" * 40)
    print()
    print("IMMEDIATE ACTIONS:")
    print("□ Book August 3rd flights JFK→BZN (~$109/person)")
    print("□ Book August 12th return flights SEA→JFK (~$249/person)")
    print()
    print("HOTEL RESERVATIONS (in order of priority):")
    print("□ Shore Lodge, McCall ID - August 7-8")
    print("  Phone: (800) 657-6464")
    print("  Website: shorelodge.com")
    print("  Priority: HIGH (luxury property, books early)")
    print()
    print("□ Bozeman, MT hotel - August 3-5")
    print("  Search: Downtown Bozeman hotels")
    print("  Budget: $150-250/night")
    print()
    print("□ Jennings Hotel, Joseph OR - August 9")
    print("  Search: 'Jennings Hotel Joseph Oregon'")
    print("  Budget: $200-300/night")
    print()
    print("□ Eritage Resort, Walla Walla WA - August 10")
    print("  Search: 'Eritage Resort Walla Walla'")
    print("  Budget: $300-500/night")
    print()
    print("□ Under Canvas Columbia River - August 11")
    print("  Website: undercanvas.com")
    print("  Budget: $200-400/night")
    print()
    print("□ Seattle hotel - August 12")
    print("  Search: Downtown Seattle hotels")
    print("  Budget: $200-400/night")
    print()
    print("TOTAL ESTIMATED COST: $4,366-4,866 per couple")
    print("(Including flights, hotels, meals/activities)")

def main():
    """Main function to run the hotel search guide."""
    print_hotel_search_guide()
    print()
    create_booking_checklist()
    
    # Save search results to file
    with open('hotel_search_results.json', 'w') as f:
        json.dump(hotels, f, indent=2)
    
    print("\n" + "="*60)
    print("Hotel information saved to: hotel_search_results.json")
    print("For current rates, use the search suggestions above")
    print("or call the hotels directly for best availability.")
    print("="*60)

if __name__ == "__main__":
    main() 