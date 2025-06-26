# message_agent.py

import requests
import os
from dotenv import load_dotenv

load_dotenv()

WHATSAPP_WEBHOOK_URL = os.getenv("WHATSAPP_WEBHOOK_URL")


def send_whatsapp_message(payload: dict, simulate: bool = False):
    """
    Sends a message to the WhatsApp webhook.
    Set simulate=True to avoid actually sending (for testing).
    """
    phone = str(payload.get("phone_number", "")).strip()
    if not phone.startswith("+"):
        phone = "+91" + phone  # Default to Indian numbers if not present
    payload["phone_number"] = phone

    if simulate:
        print(f"Simulating send: {payload}")

    else:
        if not WHATSAPP_WEBHOOK_URL:
            raise ValueError("WHATSAPP_WEBHOOK_URL not set")
        print("📡 Sending to:", WHATSAPP_WEBHOOK_URL)
        response = requests.post(WHATSAPP_WEBHOOK_URL, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to send message: {response.text}")