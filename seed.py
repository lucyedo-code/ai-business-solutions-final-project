import random
import numpy as np
from faker import Faker
from database import engine, SessionLocal
from models import CallRecord, DBModelBase

# Initialize Faker and set a seed for reproducibility (optional — remove for fresh data each run)
fake = Faker()

# Issue categories as defined in the case study
ISSUE_CATEGORIES = ["Billing", "Technical", "Service", "Account"]


def generate_call_records(num_records: int = 1000) -> list[dict]:
    """
    Generates a list of simulated customer support call records.

    Rules applied:
    - Work hours (9–17): wait time between 10–45 minutes
    - Off hours: wait time between 2–15 minutes
    - Monday or Friday: add 5–15 extra minutes (peak days)
    """
    call_records = []

    for _ in range(num_records):
        # Generate the call timestamp using Faker
        call_timestamp = fake.date_time_this_year()

        # Derive day of week and hour from the timestamp
        day_of_week = call_timestamp.strftime("%A")   # e.g. "Monday"
        hour_of_day = call_timestamp.hour              # 0–23

        # Determine base wait time based on work hours (9 AM–5 PM)
        if 9 <= hour_of_day < 17:
            wait_time = random.randint(10, 45)
        else:
            wait_time = random.randint(2, 15)

        # Increase wait time on peak days (Monday and Friday)
        if day_of_week in ("Monday", "Friday"):
            wait_time += int(np.random.randint(5, 16))  # 5–15 extra minutes

        # Build the record dictionary
        call_records.append({
            "call_id": fake.uuid4(),
            "customer_name": fake.name(),
            "call_timestamp": call_timestamp,
            "day_of_week": day_of_week,
            "hour_of_day": hour_of_day,
            "wait_time_minutes": wait_time,
            "issue_category": ISSUE_CATEGORIES[random.randint(0, len(ISSUE_CATEGORIES) - 1)],
            "resolution_status": random.choice([True, False]),
        })

    return call_records


def seed_database():
    """
    Creates all tables and populates the call_records table with 1000 generated records.
    """
    print("Creating database tables...")
    DBModelBase.metadata.create_all(bind=engine)

    print("Generating 1000 call records...")
    records = generate_call_records(1000)

    db = SessionLocal()
    try:
        # Convert each dict into a CallRecord ORM object and add to session
        for record in records:
            call = CallRecord(**record)
            db.add(call)

        db.commit()
        print(f"Successfully seeded {len(records)} records into the database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()