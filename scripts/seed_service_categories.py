# scripts/seed_service_categories.py

import os
import sys

# 将项目根目录加入路径，以便导入 app 和实体
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from entities.service_category_entity import ServiceCategoryEntity

def seed_service_categories():
    app = create_app()
    with app.app_context():
        # （可选）先清空旧数据
        db.session.query(ServiceCategoryEntity).delete()
        db.session.commit()

        categories = [
            {"name": "Window Cleaning",             "description": "Cleaning interior and exterior windows"},
            {"name": "Carpet Cleaning",             "description": "Removing stains and dirt from carpets"},
            {"name": "Upholstery Cleaning",         "description": "Cleaning sofas, chairs and other upholstery"},
            {"name": "Floor Polishing",             "description": "Polishing and shining hard floors"},
            {"name": "Tile and Grout Cleaning",     "description": "Deep cleaning tile surfaces and grout lines"},
            {"name": "Pressure Washing",            "description": "High-pressure exterior surface washing"},
            {"name": "Post-Construction Cleaning",  "description": "Removing debris and dust after construction"},
            {"name": "Move-In Cleaning",            "description": "Preparing homes for moving in"},
            {"name": "Move-Out Cleaning",           "description": "Thorough cleaning after moving out"},
            {"name": "Office Cleaning",             "description": "Daily or weekly office maintenance"},
            {"name": "Deep Cleaning",               "description": "Intensive whole-home or whole-office cleaning"},
            {"name": "Green Cleaning",              "description": "Eco-friendly, non-toxic cleaning services"},
            {"name": "Oven Cleaning",               "description": "Deep cleaning of kitchen ovens"},
            {"name": "Refrigerator Cleaning",       "description": "Cleaning interior and shelves of refrigerators"},
            {"name": "Gutter Cleaning",             "description": "Clearing leaves and debris from gutters"},
            {"name": "Duct Cleaning",               "description": "Cleaning HVAC ducts and vents"},
            {"name": "Trash Removal",               "description": "Collection and disposal of household trash"},
            {"name": "Garage Cleaning",             "description": "Cleaning and organizing garages"},
            {"name": "Pet Area Cleaning",           "description": "Sanitizing areas used by pets"},
            {"name": "Laundry Services",            "description": "Washing, drying, and folding laundry"},
        ]

        for cat in categories:
            db.session.add(ServiceCategoryEntity(
                name        = cat["name"],
                description = cat["description"]
            ))
        db.session.commit()
        print("✅ Seeded 20 service categories.")

if __name__ == '__main__':
    seed_service_categories()
