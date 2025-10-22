"""
Populate Initial Tags for Smart Canteen
=========================================
This script creates default tags for the menu tagging system.

Tags are organized into three categories:
1. Meal Type - What kind of dish (Main Course, Appetizer, Dessert, etc.)
2. Time of Day - When it's served (Breakfast, Lunch, Dinner, All-Day)
3. Temperature - How it's served (Hot, Cold, Frozen)

Run this script once after creating the Tag model migration:
    python populate_tags.py
"""

import os
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartcanteen.settings')
django.setup()

from core.models import Tag

def populate_tags():
    """Create default tags for the system"""
    
    print("🏷️  Populating Tags for Smart Canteen...")
    print("=" * 50)
    
    # Meal Type Tags
    meal_types = [
        {'name': 'Main Course', 'tag_type': 'meal_type', 'description': 'Primary dishes like rice, pasta, burgers'},
        {'name': 'Appetizer', 'tag_type': 'meal_type', 'description': 'Starters like salads, soups, spring rolls'},
        {'name': 'Dessert', 'tag_type': 'meal_type', 'description': 'Sweet endings like cakes, ice cream, pudding'},
        {'name': 'Beverage', 'tag_type': 'meal_type', 'description': 'Drinks like juice, soda, coffee, tea'},
        {'name': 'Snack', 'tag_type': 'meal_type', 'description': 'Light bites like chips, sandwiches, wraps'},
    ]
    
    # Time of Day Tags
    time_tags = [
        {'name': 'Breakfast', 'tag_type': 'time_of_day', 'description': 'Morning meals (7AM - 11AM)'},
        {'name': 'Lunch', 'tag_type': 'time_of_day', 'description': 'Midday meals (11AM - 3PM)'},
        {'name': 'Dinner', 'tag_type': 'time_of_day', 'description': 'Evening meals (5PM - 9PM)'},
        {'name': 'All-Day', 'tag_type': 'time_of_day', 'description': 'Available throughout the day'},
    ]
    
    # Temperature Tags
    temp_tags = [
        {'name': 'Hot', 'tag_type': 'temperature', 'description': 'Served hot or warm'},
        {'name': 'Cold', 'tag_type': 'temperature', 'description': 'Served cold or chilled'},
        {'name': 'Frozen', 'tag_type': 'temperature', 'description': 'Frozen items like ice cream'},
    ]
    
    # Combine all tags
    all_tags = meal_types + time_tags + temp_tags
    
    # Counters
    created_count = 0
    existing_count = 0
    
    # Create tags
    for tag_data in all_tags:
        tag, created = Tag.objects.get_or_create(
            name=tag_data['name'],
            tag_type=tag_data['tag_type'],
            defaults={'description': tag_data.get('description', '')}
        )
        
        if created:
            print(f"✅ Created: {tag.get_tag_type_display()}: {tag.name}")
            created_count += 1
        else:
            print(f"⚠️  Already exists: {tag.get_tag_type_display()}: {tag.name}")
            existing_count += 1
    
    print("=" * 50)
    print(f"\n📊 Summary:")
    print(f"   ✅ Created: {created_count} tags")
    print(f"   ⚠️  Already existed: {existing_count} tags")
    print(f"   📦 Total tags in database: {Tag.objects.count()}")
    
    # Show breakdown by type
    print(f"\n📋 Tags by Type:")
    for tag_type, display_name in Tag.TAG_TYPES:
        count = Tag.objects.filter(tag_type=tag_type).count()
        print(f"   - {display_name}: {count} tags")
    
    print("\n✨ Tag population complete!")
    print("\n💡 Next steps:")
    print("   1. Visit http://127.0.0.1:8000/admin/core/tag/ to manage tags")
    print("   2. API endpoint: http://127.0.0.1:8000/api/tags/")
    print("   3. Start assigning tags to menu items in Menu Management")

if __name__ == '__main__':
    try:
        populate_tags()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\n💡 Make sure:")
        print("   1. Django migrations are applied: python manage.py migrate")
        print("   2. You're in the backend directory")
        print("   3. Virtual environment is activated")
