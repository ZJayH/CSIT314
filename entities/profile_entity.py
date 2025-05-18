from extensions import db
from sqlalchemy import Column, String, Text, Boolean, or_
from exceptions import CreateError

class ProfileEntity(db.Model):
    __tablename__ = 'profiles'

    # role is now primary key: one row per role definition
    role        = db.Column(db.String(20), primary_key=True)
    description = db.Column(db.Text, default='')
    is_active   = db.Column(db.Boolean, default=True)

    @classmethod
    def all_roles(cls) -> list[str]:
        """Return all active roles."""
        rows = (
            db.session.query(cls.role)
                      .filter_by(is_active=True)
                      .order_by(cls.role)
                      .all()
        )
        return [r[0] for r in rows]

    @classmethod
    def seed_defaults(cls):
        """
        Seed the 4 base roles if they don’t exist.
        Call this at app startup after create_all().
        """
        base = {
            'homeowner':        'Homeowner role',
            'cleaner':          'Cleaner role',
            'user admin':       'Can manage user accounts',
            'platform manager': 'Can manage platform settings'
        }
        for role, desc in base.items():
            if cls.query.get(role) is None:
                db.session.add(
                    cls(role=role, description=desc, is_active=True)
                )
        db.session.commit()

    @classmethod
    def create(cls, role: str, description: str = '', is_active: bool = True) -> "ProfileEntity":
        """
        Insert a new role definition.
        Raises ValueError if this role already exists.
        """
        if cls.query.get(role):
            raise CreateError(f"Role '{role}' already exists.")
        prof = cls(role=role, description=description, is_active=is_active)
        db.session.add(prof)
        db.session.commit()
        return prof
    
    @classmethod
    def update(cls, role: str, **attrs) -> "ProfileEntity":
        prof = cls.query.get(role)
        for k, v in attrs.items():
            setattr(prof, k, v)
        db.session.commit()
        return prof
    
    @classmethod
    def list_all(cls):
        return cls.query.order_by(cls.role).all()
    
    @classmethod
    def search(cls, keyword: str) -> list['ProfileEntity']:
        """
        """
        kw = f"%{keyword}%"
        return (
            cls.query
               .filter(or_(
                   cls.role.ilike(kw),
                   cls.description.ilike(kw)
               ))
               .order_by(cls.role)
               .all()
        )
    
