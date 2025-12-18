from flask import request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app import app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Endpoint to receive WhatsApp messages from Twilio
    """
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')

    logger.info(f"Received message from {from_number}: {incoming_msg}")

    # Process the message (placeholder for now)
    response_msg = process_message(incoming_msg)

    # Create TwiML response
    resp = MessagingResponse()
    resp.message(response_msg)

    return str(resp)

def process_message(message):
    """
    Process the incoming message and generate a response
    """
    # Placeholder logic - to be implemented
    return f"Echo: {message}"
