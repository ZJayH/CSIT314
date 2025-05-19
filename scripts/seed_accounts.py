# scripts/seed_accounts.py
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import random
from app import create_app, db
from werkzeug.security import generate_password_hash
from entities.account_entity import AccountEntity

def seed_accounts():
    app = create_app()
    with app.app_context():
        # 先删除已有数据（可选）
        AccountEntity.query.delete()
        db.session.commit()
        hashed_pw = generate_password_hash("123456")
        accounts = []

        # 1 x Admin
        accounts.append(AccountEntity(
            name="Admin User",
            email="a1@1.com",
            password=hashed_pw,
            phone="13800000001",
            role="user admin",
            is_active=True
        ))

        # 1 x Platform Manager
        accounts.append(AccountEntity(
            name="Platform Manager",
            email="p1@1.com",
            password=hashed_pw,
            phone="13800000002",
            role="platform manager",
            is_active=True
        ))

        # 40 x Cleaner (c1…c40)
        for i in range(1, 41):
            accounts.append(AccountEntity(
                name=f"Cleaner {i}",
                email=f"c{i}@1.com",
                password=hashed_pw,
                phone=f"1380000{str(100 + i)[1:]}",  # e.g. 13800000103 for i=3
                role="cleaner",
                is_active=True
            ))

        # 60 x Homeowner (h1…h60)
        for i in range(1, 61):
            accounts.append(AccountEntity(
                name=f"Homeowner {i}",
                email=f"h{i}@1.com",
                password=hashed_pw,
                phone=f"1380001{str(100 + i)[1:]}",
                role="homeowner",
                is_active=True
            ))

        db.session.add_all(accounts)
        db.session.commit()
        total = len(accounts)
        print(f"✅ Seeded {total} accounts (1 admin, 1 pm, 40 cleaners, 60 homeowners).")

if __name__ == '__main__':
    seed_accounts()
