"""
Seed the PostgreSQL database with realistic enterprise sample data.
Generates customers, orders, and support interactions with embedded churn signal.
"""
import random
import os
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_SYNC_URL", "postgresql://insightflow:insightflow@localhost:5432/insightflow")

REGIONS = ["North America", "Europe", "APAC", "LATAM", "Middle East"]
SEGMENTS = ["SMB", "Mid-Market", "Enterprise"]
PRODUCTS = ["InsightFlow Pro", "InsightFlow Analytics", "InsightFlow Basic", "Data Connector Pack", "ML Suite"]
CHANNELS = ["email", "call", "chat"]
NAMES = [
    "Acme Corp", "TechNova", "GlobalSync", "Meridian Analytics", "DataPeak", "NovaStar",
    "BluePath", "OmniCore", "SkyBridge", "IronCrest", "Valence Systems", "Nexus Dynamics",
    "Quasar Tech", "Apex Intelligence", "Stratos Data", "Orison Labs", "Crestline Solutions",
    "Pinnacle Analytics", "Tidal Systems", "ClearView Data"
]


def seed():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Import models
    import sys
    sys.path.insert(0, "/app")
    from app.db.models import Customer, Order, Interaction
    from app.db.database import Base
    Base.metadata.create_all(engine)

    print("Seeding customers...")
    customers = []
    for i, name in enumerate(NAMES * 5):  # 100 customers
        churned = random.random() < 0.25  # 25% churn rate
        created_at = datetime.utcnow() - timedelta(days=random.randint(30, 730))
        c = Customer(
            name=f"{name} {i+1}",
            email=f"contact{i+1}@{name.lower().replace(' ', '')}.com",
            region=random.choice(REGIONS),
            segment=random.choice(SEGMENTS),
            contract_value=random.choice([500, 1200, 2500, 5000, 10000, 25000]),
            created_at=created_at,
            is_churned=churned,
        )
        session.add(c)
        customers.append((c, churned, created_at))

    session.flush()

    print("Seeding orders...")
    for c, churned, c_created in customers:
        n_orders = random.randint(0, 3) if churned else random.randint(2, 15)
        for _ in range(n_orders):
            order_date = c_created + timedelta(days=random.randint(1, 400))
            session.add(Order(
                customer_id=c.id,
                product=random.choice(PRODUCTS),
                amount=round(random.uniform(100, 5000), 2),
                region=c.region,
                status=random.choice(["completed", "completed", "completed", "refunded", "pending"]),
                created_at=order_date,
            ))

    print("Seeding interactions...")
    for c, churned, c_created in customers:
        n_int = random.randint(1, 4) if churned else random.randint(1, 8)
        for _ in range(n_int):
            session.add(Interaction(
                customer_id=c.id,
                channel=random.choice(CHANNELS),
                sentiment=random.uniform(-0.8, -0.1) if churned else random.uniform(-0.2, 0.9),
                resolved=random.choice([False, False, True]) if churned else True,
                created_at=c_created + timedelta(days=random.randint(1, 300)),
            ))

    session.commit()
    session.close()
    print(f"Done! Seeded {len(customers)} customers.")


if __name__ == "__main__":
    seed()
