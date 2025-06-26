from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

app = FastAPI()

# Import helper functions from your other files
from sheet_agent import load_subscribers    
from message_agent import send_whatsapp_message 
from scheduler import start_scheduler

# # # Load webhook URL from .env
# WHATSAPP_WEBHOOK_MANUAL = os.getenv("WHATSAPP_WEBHOOK_MANUAL")
# WHATSAPP_WEBHOOK_RENEWAL = os.getenv("WHATSAPP_WEBHOOK_RENEWAL")
# WHATSAPP_WEBHOOK_WORKSHOP = os.getenv("WHATSAPP_WEBHOOK_WORKSHOP")

# Schema for manual message testing
class MessageRequest(BaseModel):
    phone_number: str
    message: str

# Endpoint: Send a workshop alert to all users
@app.get("/send-workshop-alert")
def send_workshop_alert():
    try:
        subscribers = load_subscribers()  # From sheet_agent
        workshop_message = (
            "📣 New Workshop Alert!\n"
            "Join us for a Bollywood Fusion Workshop on July 15 at 5 PM.\n"
            "Reply 'JOIN' to reserve your spot! 💃🕺"
        )

        for user in subscribers:
            payload = {
                "phone_number": user["phone_number"],
                "message": workshop_message
            }
            # send_whatsapp_message(payload, webhook_url=WHATSAPP_WEBHOOK_WORKSHOP)
            send_whatsapp_message(payload, simulate=False)  # actual send   

        return {"status": "Workshop alerts sent to all users."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ✅ Endpoint: Send renewal reminders to users whose subscription ends in 3 days
@app.get("/send-renewal-reminders")
def send_renewal_reminders():
    try:
        subscribers = load_subscribers()  # From sheet_agent
        today = datetime.now().date()
        reminder_day = today + timedelta(days=2)

        count = 0
        for user in subscribers:
            raw_date = user.get("subscription_end")
            if not raw_date:
                continue
            try:
                end_date = datetime.strptime(raw_date, "%d-%m-%Y").date()
            except ValueError:
                print(f"[WARNING] Skipping invalid date: {raw_date}")
                continue

            print(f"[DEBUG] {user['name']} | end: {end_date} | reminder: {reminder_day}")

            if end_date == reminder_day:
                message = (
                    f"Hi {user['name']}, your subscription at King Cultural Spot "
                    f"ends on {end_date}. Renew now to continue your dance journey! 💃"
                )
                payload = {
                    "phone_number": user["phone_number"],
                    "message": message
                }
                # send_whatsapp_message(payload, webhook_url=WHATSAPP_WEBHOOK_RENEWAL)
                send_whatsapp_message(payload, simulate=False)
                count += 1

        return {"status": f"Renewal reminders sent to {count} users."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint: Send custom message manually
@app.post("/send-manual-message")
def send_manual_message(data: MessageRequest):
    try:
        payload = {
            "phone_number": data.phone_number,
            "message": data.message
        }
        # send_whatsapp_message(payload, webhook_url=WHATSAPP_WEBHOOK_MANUAL)
        send_whatsapp_message(payload, simulate=False)
        return {"status": "Message sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Start scheduler when FastAPI starts
@app.on_event("startup")
def startup_event():
    start_scheduler()
