import re
from datetime import datetime

def validate_dni(dni):
    """Validate DNI format (8 digits)"""
    if not dni:
        return False
    # Remove any spaces or dots
    dni = re.sub(r'[.\s]', '', dni)
    return bool(re.match(r'^\d{8}$', dni))

def validate_phone(phone):
    """Validate phone number format"""
    if not phone:
        return False
    # Remove spaces, dashes, parentheses
    phone = re.sub(r'[()\s\-]', '', phone)
    # Allow + prefix and digits
    return bool(re.match(r'^\+?\d{8,15}$', phone))

def validate_email(email):
    """Validate email format"""
    if not email:
        return False
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_date(date_str):
    """Validate date format (DD/MM/YYYY)"""
    if not date_str:
        return False
    try:
        datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False