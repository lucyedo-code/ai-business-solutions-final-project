import streamlit as st
import pandas as pd
from sqlalchemy import select
from database import SessionLocal
from models import CallRecord


def load_call_records(db):
    """
    Query all call records from the database and return as a list of dicts.
    """
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

    return records


def compute_avg_wait_by_day(df):
    """
    Computes average wait time grouped by day of the week.
    """
    return df.groupby("day_of_week")["wait_time_minutes"].mean().reset_index()


def compute_busiest_hours(df):
    """
    Returns the top 3 busiest hours by call volume.
    """
    return (
        df.groupby("hour_of_day")["call_id"]
        .count()
        .reset_index()
        .rename(columns={"call_id": "call_count"})
        .sort_values("call_count", ascending=False)
        .head(3)
    )


# --- Streamlit App ---
st.title("TechFlow Solutions — Customer Support Call Analysis")
st.markdown("Analyzing call volume and wait time patterns to recommend optimal staffing schedules.")

# Open DB session and load data
db = SessionLocal()
records = load_call_records(db)
db.close()

# Convert to DataFrame
df = pd.DataFrame(records)

# --- Full Call Records Table ---
st.subheader("Call Records")
st.dataframe(df)

# --- Average Wait Time by Day ---
st.subheader("Average Wait Time by Day of Week")
avg_wait = compute_avg_wait_by_day(df)
st.dataframe(avg_wait)

# --- Top 3 Busiest Hours ---
st.subheader("Top 3 Busiest Hours of the Day")
busiest = compute_busiest_hours(df)
st.dataframe(busiest)

# --- Summary Stats ---
st.subheader("Summary Statistics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Calls", len(df))
col2.metric("Avg Wait Time", f"{df['wait_time_minutes'].mean():.1f} min")
col3.metric("Resolution Rate", f"{df['resolution_status'].mean() * 100:.1f}%")