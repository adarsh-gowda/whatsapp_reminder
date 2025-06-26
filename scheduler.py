# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Your FastAPI server (it must be running for this to work)
BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Function to call the FastAPI endpoints
def call_workshop_alert():
    try:
        response = requests.get(f"{BASE_URL}/send-workshop-alert")
        print("Workshop alert status:", response.json())
    except Exception as e:
        print("Failed to call /send-workshop-alert:", e)

def call_renewal_reminders():
    try:
        response = requests.get(f"{BASE_URL}/send-renewal-reminders")
        print("Renewal reminder status:", response.json())
    except Exception as e:
        print("Failed to call /send-renewal-reminders:", e)

# Start and schedule jobs
def start_scheduler():
    scheduler = BackgroundScheduler()
    
    # Schedule: Workshop alerts - every Monday at 10 AM
    scheduler.add_job(call_workshop_alert, 'cron', day_of_week='mon', hour=10, minute=0)

    # Schedule: Subscription reminders - daily at 9 AM
    # scheduler.add_job(call_renewal_reminders, 'cron', hour=9, minute=0)
    # In scheduler.py, for testing:
    scheduler.add_job(call_renewal_reminders, 'interval', seconds=30)


    scheduler.start()
    print("🔁 APScheduler started...")

