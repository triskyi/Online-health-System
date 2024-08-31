# users/utils.py

import africastalking
import logging
import random

# Initialize AfricasTalking SDK
username = "Tresorafrica"
api_key = "atsk_d9337b34354ce42086c1509ec9cd5a39ae6d5fcd52f6e743e172cc00a8f0a7d3481612d6"
africastalking.initialize(username, api_key)
sms = africastalking.SMS

logger = logging.getLogger(__name__)

def generate_one_time_code(length=6):
    """Generate a random numeric one-time code"""
    return ''.join(random.choices('0123456789', k=length))

def send_registration_sms(phone_number, one_time_code):
    message = f"Welcome to the Health System. Your verification code is: {one_time_code}"
    try:
        response = sms.send(message, [phone_number])
        logger.info(f'SMS sent to {phone_number}: {response}')
        return True
    except Exception as e:
        logger.error(f'Error sending SMS to {phone_number}: {str(e)}')
        return False


