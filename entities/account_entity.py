from datetime import datetime
from extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from entities.profile_entity import ProfileEntity
from sqlalchemy import or_
from exceptions import DuplicateEmailError, DuplicatePhoneError, LoginError, UpdateError, CreateError

class AccountEntity(db.Model):
    __tablename__ = 'accounts'
    
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(128), nullable=False)
    phone      = db.Column(db.String(20), unique=True, nullable=True)
    role       = db.Column(db.String(20), db.ForeignKey('profiles.role'), nullable=False)
    is_active  = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, name: str, email: str, password: str,
               phone: str = None, role: str = 'homeowner',
               is_active: bool = True) -> "AccountEntity":
        """Create a new account with hashed password."""

        if cls.query.filter_by(email=email).first():
            raise CreateError("This email is already registered.")
        if phone and cls.query.filter_by(phone=phone).first():
            raise CreateError("This phone is already in use.")

        hashed = generate_password_hash(password)
        acct = cls(
            name=name,
            email=email,
            password=hashed,
            phone=phone,
            role=role,
            is_active=is_active
        )
        db.session.add(acct)
        db.session.commit()
        return acct

    @classmethod
    def authenticate(cls, email: str, password: str) -> "AccountEntity":
        """
        """
        acct = cls.query.filter_by(email=email).first()
        if not acct:
            raise LoginError("Invalid credentials.")
        if not check_password_hash(acct.password, password):
            raise LoginError("Invalid credentials.")

        # 用户被禁用
        if not acct.is_active:
            raise LoginError("Your account is suspended.")

        # Profile 被挂起
        prof = ProfileEntity.query.get(acct.role)
        if prof and not prof.is_active:
            raise LoginError("Your user role has been suspended.")

        return acct

    @classmethod
    def update(cls, id: int, **fields) -> "AccountEntity":
        """
        Update allowed fields for the given account ID.
        Allowed: name, email, phone, role, is_active.
        """
        acct = cls.query.get(id)
        if 'email' in fields:
            new_email = fields['email']
            if new_email != acct.email and cls.query \
                    .filter(cls.email == new_email, cls.id != id) \
                    .first():
                raise UpdateError("This email address is already registered.")
            acct.email = new_email

        if 'phone' in fields:
            new_phone = fields['phone']
            if new_phone and new_phone != acct.phone and cls.query \
                    .filter(cls.phone == new_phone, cls.id != id) \
                    .first():
                raise UpdateError("This phone number is already in use.")
            acct.phone = new_phone
        for key in ('name', 'email', 'phone', 'role', 'is_active'):
            if key in fields:
                setattr(acct, key, fields[key])
        db.session.commit()
        return acct
        
    
    @classmethod
    def list_all(cls) -> list['AccountEntity']:
        """
        """
        return cls.query.order_by(cls.id).all()
    
    @classmethod
    def search(cls, keyword: str) -> list['AccountEntity']:
        """
        """
        kw = f"%{keyword}%"
        return (
            cls.query
               .filter(or_(
                   cls.name.ilike(kw),
                   cls.email.ilike(kw)
               ))
               .order_by(cls.id)
               .all()
        )
