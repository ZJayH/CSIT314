from sqlalchemy import Column, Integer, String, or_
from extensions import db
from exceptions import CreateError,UpdateError
class ServiceCategoryEntity(db.Model):
    __tablename__ = 'service_categories'

    id          = Column(Integer, primary_key=True)
    name        = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), nullable=True)

    @classmethod
    def create(cls, name: str, description: str = None) -> 'ServiceCategoryEntity':
        """
        data keys: name, description
        """
        existing = db.session.query(cls).filter_by(name=name).first()
        if existing:
            raise CreateError(f"Category name '{name}' already exists.")
        sc = cls(name=name, description=description)
        db.session.add(sc)
        db.session.commit()
        return sc
    
    @classmethod
    def list_all(cls) -> list['ServiceCategoryEntity']:
        return db.session.query(cls).order_by(cls.id).all()
    
    @classmethod
    def update(cls, sc_id: int, name: str, description: str = None) -> 'ServiceCategoryEntity':
        sc = cls.query.get(sc_id)
        if name != sc.name:
            duplicate = db.session.query(cls).filter(cls.name == name, cls.id != sc_id).first()
            if duplicate:
                raise UpdateError(f"Category name '{name}' already exists.")
        sc.name = name
        sc.description = description
        db.session.commit()
        return sc

    @classmethod
    def delete(cls, sc_id: int) -> None:
        sc = cls.query.get(sc_id)
        db.session.delete(sc)
        db.session.commit()

    @classmethod
    def search(cls, keyword: str) -> list['ServiceCategoryEntity']:
        """
        """
        q = keyword.strip()
        if not q:
            return cls.list_all()
        pattern = f"%{q}%"
        return (
            db.session.query(cls)
            .filter(or_(cls.name.ilike(pattern),
                        cls.description.ilike(pattern)))
            .order_by(cls.id)
            .all()
        )
