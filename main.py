from fastapi import FastAPI, HTTPException
from datetime import datetime, timedelta
from pydantic import BaseModel
import os
import json
from typing import List
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = FastAPI()

# Dummy user data, replace with DB or Google Sheet integration
SUBSCRIBERS_FILE = "subscribers.json"

# Webhook URLs to trigger WhatsApp messages via N8N or other service
WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL")

# Pydantic model for manual testing
class MessageRequest(BaseModel):
    phone_number: str
    message: str

# Load subscriber data
def load_subscribers():
    with open(SUBSCRIBERS_FILE, "r") as file:
        return json.load(file)

# Endpoint 1: Send Workshop Alert
@app.get("/send-workshop-alert")
def send_workshop_alert():
    try:
        subscribers = load_subscribers()
        workshop_message = "📣 New Workshop Alert!\nJoin us for a Bollywood Fusion Workshop on July 15 at 5 PM.\nReply 'JOIN' to reserve your spot! 💃🕺"

        for user in subscribers:
            payload = {
                "phone_number": user["phone_number"],
                "message": workshop_message
            }
            # requests.post(WHATSAPP_WEBHOOK_URL, json=payload)
            print(f"Simulating send: {payload}")


        return {"status": "Workshop alerts sent to all users."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint 2: Send Subscription Renewal Reminders
@app.get("/send-renewal-reminders")
def send_renewal_reminders():
    try:
        subscribers = load_subscribers()
        today = datetime.now().date()
        reminder_day = today + timedelta(days=3)

        count = 0
        for user in subscribers:
            end_date = datetime.strptime(user["subscription_end"], "%Y-%m-%d").date()
            if end_date == reminder_day:
                message = f"Hi {user['name']}, your subscription at King Cultural Spot ends on {end_date}. Renew now to continue your dance journey! 💃"
                payload = {
                    "phone_number": user["phone_number"],
                    "message": message
                }
                # requests.post(WHATSAPP_WEBHOOK_URL, json=payload)
                print(f"Simulating send: {payload}")

                count += 1

        return {"status": f"Renewal reminders sent to {count} users."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Optional test endpoint
@app.post("/send-manual-message")
def send_manual_message(data: MessageRequest):
    try:
        payload = {
            "phone_number": data.phone_number,
            "message": data.message
        }
        # requests.post(WHATSAPP_WEBHOOK_URL, json=payload)
        print(f"Simulating send: {payload}")

        return {"status": "Message sent."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
