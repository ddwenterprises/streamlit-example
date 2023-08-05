import streamlit as st
from datetime import datetime, timedelta
from collections import defaultdict

def calculate_completion_date(start_date, calendar_days, winter_shutdown):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    completion_date = start_date
    days_added = 0
    days_per_month = defaultdict(int)

    while days_added < calendar_days:
        if winter_shutdown == "Yes":
            if (completion_date.month < 12 or completion_date.day < 1) and (completion_date.month > 3 or completion_date.day > 31):
                days_added += 1
                days_per_month[completion_date.strftime("%Y-%m")] += 1
        else:
            days_added += 1
            days_per_month[completion_date.strftime("%Y-%m")] += 1
        completion_date += timedelta(days=1)

    # subtract one day because the day of start is considered a working day
    completion_date -= timedelta(days=1)


    return completion_date.strftime("%B %d, %Y"), dict(days_per_month)

st.title("Contract Completion Date Calculator")

start_date = st.date_input("Contract Start Date",format="MM/DD/YYYY")
calendar_days = st.number_input("Calendar Days",min_value=1,step=1)
winter_shutdown = st.selectbox("Winter Shutdown", ["Yes", "No"])

if st.button("Calculate Completion Date"):
    completion_date, days_per_month = calculate_completion_date(str(start_date), calendar_days, winter_shutdown)
    st.write("The Contract Completion Date is **", completion_date,"**.")
    st.write("Days per month:")
    total_days = 0
    for month, days in sorted(days_per_month.items()):
        month_name = datetime.strptime(month, "%Y-%m").strftime("%B %Y")
        total_days += days
        st.write(f"{month_name}: {days} Days ({total_days} Days Total)")
