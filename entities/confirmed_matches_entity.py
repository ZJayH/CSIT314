from sqlalchemy import Column, Integer, ForeignKey, DateTime, or_
from sqlalchemy.orm import relationship
from extensions import db
import datetime

from entities.account_entity         import AccountEntity
from entities.service_listing_entity import ServiceListingEntity
from entities.service_category_entity import ServiceCategoryEntity

class ConfirmedMatchEntity(db.Model):
    __tablename__ = 'confirmed_matches'

    match_id       = Column(Integer, primary_key=True, autoincrement=True)
    homeowner_id   = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    listing_id     = Column(Integer, ForeignKey('service_listings.listing_id'), nullable=False)
    cleaner_id     = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    confirmed_date = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)

    # relationships
    homeowner = relationship('AccountEntity', foreign_keys=[homeowner_id], lazy='joined')
    listing   = relationship('ServiceListingEntity', foreign_keys=[listing_id], lazy='joined')
    cleaner   = relationship('AccountEntity', foreign_keys=[cleaner_id], lazy='joined')

    @classmethod
    def list_by_cleaner(cls, cleaner_id: int) -> list['ConfirmedMatchEntity']:
        """
        """
        return (
            db.session
            .query(cls)
            .filter(cls.cleaner_id == cleaner_id)
            .order_by(cls.confirmed_date.desc())
            .all()
        )

    @classmethod
    def search_by_cleaner(cls, cleaner_id: int, keyword: str):
        pattern = f"%{keyword}%"
        q = (
        db.session.query(cls)
        .filter(cls.cleaner_id == cleaner_id)
        )
        q = q.filter(
        or_(
            cls.homeowner.has(AccountEntity.name.ilike(pattern)),
            cls.listing.has(ServiceListingEntity.description.ilike(pattern)),
            cls.listing.has(ServiceListingEntity.category.has(
            ServiceCategoryEntity.name.ilike(pattern)
            ))
        )
        )
        return q.order_by(cls.confirmed_date.desc()).all()
    
    @classmethod
    def list_by_homeowner(cls, homeowner_id: int) -> list['ConfirmedMatchEntity']:
        """
        """
        return (
            db.session.query(cls)
            .filter(cls.homeowner_id == homeowner_id)
            .order_by(cls.confirmed_date.desc())
            .all()
        )

    @classmethod
    def search_by_homeowner(cls, homeowner_id: int, keyword: str) -> list['ConfirmedMatchEntity']:
        """
        """
        pattern = f"%{keyword}%"
        return (
            db.session.query(cls)
            .filter(cls.homeowner_id == homeowner_id)
            .filter(or_(
                cls.cleaner.has(AccountEntity.name.ilike(pattern)),
                cls.listing.has(ServiceListingEntity.description.ilike(pattern)),
                cls.listing.has(ServiceListingEntity.category.has(
                    ServiceCategoryEntity.name.ilike(pattern)
                ))
            ))
            .order_by(cls.confirmed_date.desc())
            .all()
        )
    
    @classmethod
    def list_one(cls, match_id: int) -> list['ConfirmedMatchEntity']:
        """
        """
        return ( db.session.query(cls).filter_by(match_id=match_id).first()
            
        )