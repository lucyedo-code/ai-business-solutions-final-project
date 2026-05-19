import pandas as pd
from sqlalchemy import select
from database import SessionLocal
from models import CallRecord


def export_call_records_to_csv(filepath: str = "call_records.csv"):
    """
    Queries all call records from the database and exports them to a CSV file
    to be used in Lovable for dashboard creation.
    """
    db = SessionLocal()

    try:
        statement = select(CallRecord)
        results = db.execute(statement).scalars().all()

        records = []
        for record in results:
            records.append({
                "call_id": record.call_id,
                "customer_name": record.customer_name,
                "call_timestamp": record.call_timestamp,
                "day_of_week": record.day_of_week,
                "hour_of_day": record.hour_of_day,
                "wait_time_minutes": record.wait_time_minutes,
                "issue_category": record.issue_category,
                "resolution_status": record.resolution_status,
            })

        # Create DataFrame and export to CSV
        df = pd.DataFrame(records)
        df.to_csv(filepath, index=False)

        print(f"Successfully exported {len(df)} records to '{filepath}'")
        print("\nPreview of exported data:")
        print(df.head())

    except Exception as e:
        print(f"Error exporting data: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    export_call_records_to_csv()