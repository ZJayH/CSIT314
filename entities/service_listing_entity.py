import random

from sqlalchemy import Column, Integer, ForeignKey, Text, Float, or_
from sqlalchemy.orm import relationship
from extensions import db
from entities.service_category_entity import ServiceCategoryEntity
from entities.account_entity         import AccountEntity

class ServiceListingEntity(db.Model):
    __tablename__ = 'service_listings'

    listing_id   = Column(Integer, primary_key=True)
    cleaner_id   = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    description  = Column(Text,    nullable=False)
    price        = Column(Float,   nullable=False)
    category_id  = Column(Integer, ForeignKey('service_categories.id'), nullable=False)
    views           = Column(Integer, nullable=False, default=0)
    shortlist_count = Column(Integer, nullable=False, default=0)

    category     = relationship('ServiceCategoryEntity', lazy='joined')
    cleaner  = relationship('AccountEntity',          lazy='joined')


    @classmethod
    def create(cls,
               cleaner_id: int, 
               description: str,
               price: float,
               category_id: int) -> 'ServiceListingEntity':
        sl = cls(
            cleaner_id  = cleaner_id,
            description = description,
            price       = price,
            category_id = category_id
        )
        db.session.add(sl)
        db.session.commit()
        return sl
    
    @classmethod
    def list_by_cleaner(cls, cleaner_id: int) -> list['ServiceListingEntity']:
        """"""
        return (
            db.session
            .query(cls)
            .filter_by(cleaner_id=cleaner_id)
            .order_by(cls.listing_id)
            .all()
        )
    
    @classmethod
    def update(cls, listing_id, description, price, category_id):
        sl = db.session.get(cls, listing_id)
        sl.description = description
        sl.price       = price
        sl.category_id = category_id
        db.session.commit()
        return sl

    @classmethod
    def delete(cls, listing_id):
        sl = db.session.get(cls, listing_id)
        db.session.delete(sl)
        db.session.commit()

    @classmethod
    def search_by_cleaner(cls, cleaner_id: int, keyword: str):
        pattern = f"%{keyword}%"
        return (
            db.session.query(cls)
                      .join(ServiceCategoryEntity)
                      .filter(cls.cleaner_id == cleaner_id)
                      .filter(or_(
                          cls.description.ilike(pattern),
                          ServiceCategoryEntity.name.ilike(pattern)
                      ))
                      .order_by(cls.listing_id)
                      .all()
        )
    
    @classmethod
    def     list_all(cls):
        """List every service listing."""
        return (
            db.session
            .query(cls)
            .order_by(cls.listing_id)
            .all()
        )

    @classmethod
    def search_all(cls, keyword: str):
        """
        Search across description or category name (case-insensitive).
        """
        pattern = f"%{keyword}%"
        return (
            db.session
            .query(cls)
            .join(ServiceCategoryEntity)
            .filter(or_(
                cls.description.ilike(pattern),
                ServiceCategoryEntity.name.ilike(pattern)
            ))
            .order_by(cls.listing_id)
            .all()
        )
    
    @classmethod
    def seed_random_views(cls, listing_id: int, floor: int = 10, ceiling: int = 100) -> int:
        """
        """
        sl = db.session.get(cls, listing_id)
        if not sl:
            raise ValueError(f"Listing {listing_id} not found")
        if sl.views < floor:
            sl.views = random.randint(floor, ceiling)
            db.session.commit()
        return sl.views

    @classmethod
    def refresh_shortlist_count(cls, listing_id: int) -> int:
        """

        """
        from entities.shortlist_entity       import ShortlistEntity

        sl = db.session.get(cls, listing_id)
        if not sl:
            raise ValueError(f"Listing {listing_id} not found")
        count = db.session.query(ShortlistEntity) \
                         .filter_by(listing_id=listing_id) \
                         .count()
        sl.shortlist_count = count
        db.session.commit()
        return count
    
    @classmethod
    def list_one(cls, listing_id: int) -> 'ServiceListingEntity':
        """
        """
        return (
            db.session
            .query(cls)
            .filter_by(listing_id=listing_id)
            .first()
        )

