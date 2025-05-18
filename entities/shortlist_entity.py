# entities/shortlist_entity.py

from sqlalchemy import Column, Integer, ForeignKey, or_
from sqlalchemy.orm import relationship
from .service_listing_entity import ServiceListingEntity
from .service_category_entity import ServiceCategoryEntity
from .account_entity         import AccountEntity
from extensions import db

class ShortlistEntity(db.Model):
    __tablename__ = 'shortlists'

    id           = Column(Integer, primary_key=True, autoincrement=True)
    homeowner_id = Column(Integer, ForeignKey('accounts.id'), nullable=False)
    listing_id   = Column(Integer, ForeignKey('service_listings.listing_id'), nullable=False)

    homeowner    = relationship('AccountEntity',         lazy='joined')
    listing      = relationship('ServiceListingEntity', lazy='joined')

    @classmethod
    def add_to_shortlist(cls, homeowner_id: int, listing_id: int):
        exists = db.session.query(cls) \
                           .filter_by(homeowner_id=homeowner_id, listing_id=listing_id) \
                           .first()
        if exists:
            raise ValueError()
        sl = cls(homeowner_id=homeowner_id, listing_id=listing_id)
        db.session.add(sl)
        db.session.commit()
   

    @classmethod
    def remove_from_shortlist(cls, homeowner_id: int, listing_id: int):
        sl = db.session.query(cls) \
                       .filter_by(homeowner_id=homeowner_id, listing_id=listing_id) \
                       .first()
        if not sl:
            raise ValueError()
        db.session.delete(sl)
        db.session.commit()

    @classmethod
    def get_shortlist_for_homeowner(cls, homeowner_id: int):
        return db.session.query(cls) \
                         .filter_by(homeowner_id=homeowner_id) \
                         .order_by(cls.id) \
                         .all()
    
    @classmethod
    def search_for_homeowner(cls, homeowner_id: int, keyword: str):
        """
        """
        pattern = f"%{keyword}%"
        return (
            db.session.query(cls)
                      .join(ServiceListingEntity, cls.listing)
                      .join(ServiceCategoryEntity, ServiceListingEntity.category)
                      .filter(cls.homeowner_id == homeowner_id)
                      .filter(or_(
                          ServiceListingEntity.description.ilike(pattern),
                          ServiceCategoryEntity.name.ilike(pattern)
                      ))
                      .order_by(cls.id)
                      .all()
        )
