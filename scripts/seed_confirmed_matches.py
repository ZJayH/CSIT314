#!/usr/bin/env python3
import random
import os
import sys
from datetime import datetime, timedelta

# make project root available
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from entities.confirmed_matches_entity import ConfirmedMatchEntity
from entities.service_listing_entity import ServiceListingEntity
from entities.account_entity import AccountEntity


def seed_confirmed_matches():
    """
    Seed confirmed matches with the following rules:
      1. One future match (>2025-05-25) per homeowner (IDs 13-22).
      2. Then 90 additional matches randomly assigned among these homeowners, with dates NOT in the future relative to 2025-05-25.
      3. Constraint: each cleaner can only serve one homeowner per day.
    """
    app = create_app()
    with app.app_context():
        # Homeowner IDs 13–22
        homeowner_ids = list(range(13, 23))
        # Fetch listings 1–100
        listings = db.session.query(ServiceListingEntity) \
                             .filter(ServiceListingEntity.listing_id.between(1, 100)) \
                             .all()

        # Clear existing data
        db.session.query(ConfirmedMatchEntity).delete()
        db.session.commit()

        base_date = datetime(2025, 5, 25)
        used_cleaner_dates = set()
        matches = []

        # 1) One future match per homeowner
        for homeowner_id in homeowner_ids:
            while True:
                listing = random.choice(listings)
                cleaner_id = listing.cleaner_id
                # random date between 2025-05-26 and 2025-06-25
                delta = random.randint(1, 30)
                confirmed_date = base_date + timedelta(days=delta)
                date_only = confirmed_date.date()
                key = (cleaner_id, date_only)
                if key in used_cleaner_dates:
                    continue
                used_cleaner_dates.add(key)
                match = ConfirmedMatchEntity(
                    homeowner_id=homeowner_id,
                    listing_id=listing.listing_id,
                    cleaner_id=cleaner_id,
                    confirmed_date=confirmed_date
                )
                matches.append(match)
                break

        # 2) 90 additional matches with past dates (<= base_date)
        target_total = len(homeowner_ids) + 90
        past_range_days = 90  # up to 90 days before base_date
        while len(matches) < target_total:
            homeowner_id = random.choice(homeowner_ids)
            listing = random.choice(listings)
            cleaner_id = listing.cleaner_id
            # random date between base_date - 90 days and base_date (not future)
            delta = random.randint(1, past_range_days)
            confirmed_date = base_date - timedelta(days=delta)
            date_only = confirmed_date.date()
            key = (cleaner_id, date_only)
            if key in used_cleaner_dates:
                continue
            used_cleaner_dates.add(key)
            match = ConfirmedMatchEntity(
                homeowner_id=homeowner_id,
                listing_id=listing.listing_id,
                cleaner_id=cleaner_id,
                confirmed_date=confirmed_date
            )
            matches.append(match)

        # Bulk save and commit
        db.session.bulk_save_objects(matches)
        db.session.commit()

        # Print results
        all_matches = db.session.query(ConfirmedMatchEntity) \
                                .order_by(ConfirmedMatchEntity.match_id) \
                                .all()
        print(f"Seeded {len(all_matches)} confirmed matches:")
        for m in all_matches:
            homeowner = db.session.get(AccountEntity, m.homeowner_id)
            cleaner   = db.session.get(AccountEntity, m.cleaner_id)
            listing   = db.session.get(ServiceListingEntity, m.listing_id)
            print(
                f"Match ID: {m.match_id} | "
                f"Homeowner: {homeowner.name} (ID {m.homeowner_id}) | "
                f"Cleaner: {cleaner.name} (ID {m.cleaner_id}) | "
                f"Listing: {listing.description!r} | "
                f"Category: {listing.category.name} | "
                f"Date: {m.confirmed_date.strftime('%Y-%m-%d')}"
            )

if __name__ == '__main__':
    seed_confirmed_matches()
