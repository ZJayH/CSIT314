# scripts/seed_service_listings.py

import os
import sys
import random

# ensure project root is on the import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from entities.account_entity          import AccountEntity
from entities.service_category_entity import ServiceCategoryEntity
from entities.service_listing_entity  import ServiceListingEntity

def seed_service_listings(total=100):
    app = create_app()
    with app.app_context():
        # (optional) clear out existing listings
        db.session.query(ServiceListingEntity).delete()
        db.session.commit()

        # fetch all cleaner IDs
        cleaners = db.session.query(AccountEntity).filter_by(role='cleaner').all()
        cleaner_ids = [c.id for c in cleaners]

        # fetch all category IDs
        categories = db.session.query(ServiceCategoryEntity).all()
        category_ids = [c.id for c in categories]

        listings = []
        used = {cid: set() for cid in cleaner_ids}

        # give each cleaner one initial listing with a unique category
        for cid in cleaner_ids:
            cat = random.choice(category_ids)
            used[cid].add(cat)
            listings.append({
                'cleaner_id':  cid,
                'category_id': cat,
                'description': f"Service listing for category {cat}",
                'price':       round(random.uniform(20, 200), 2)
            })

        # fill up to `total`, ensuring no cleaner gets the same category twice
        while len(listings) < total:
            cid = random.choice(cleaner_ids)
            available = [cat for cat in category_ids if cat not in used[cid]]
            if not available:
                # this cleaner has exhausted all categories, pick another
                continue
            cat = random.choice(available)
            used[cid].add(cat)
            listings.append({
                'cleaner_id':  cid,
                'category_id': cat,
                'description': f"Service listing for category {cat}",
                'price':       round(random.uniform(20, 200), 2)
            })

        # bulk insert into the database
        db.session.bulk_insert_mappings(ServiceListingEntity, listings)
        db.session.commit()
        print(f"✅ Seeded {len(listings)} service listings (total requested: {total})")

if __name__ == '__main__':
    seed_service_listings()
