from flask import request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app import app
import logging

# Try to import optional modules
try:
    from app.config import DOCUMENT_TYPES
    from app.validators import validate_dni, validate_phone, validate_email
    from app.document_processor import fill_document_naturally
    IMPORTS_SUCCESSFUL = True
except ImportError as e:
    logging.error(f"Import error: {e}")
    IMPORTS_SUCCESSFUL = False
    DOCUMENT_TYPES = {}
    validate_dni = lambda x: True
    validate_phone = lambda x: True
    validate_email = lambda x: True
    fill_document_naturally = lambda x, y: None
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory session storage (for demo purposes)
user_sessions = {}

@app.route('/whatsapp', methods=['POST'])
def whatsapp_webhook():
    """
    Endpoint to receive WhatsApp messages from Twilio
    """
    incoming_msg = request.values.get('Body', '').strip().lower()
    from_number = request.values.get('From', '')

    logger.info(f"Received message from {from_number}: {incoming_msg}")

    # Process the message
    response_msg = process_message(incoming_msg, from_number)

    # Create TwiML response
    resp = MessagingResponse()
    resp.message(response_msg)

    return str(resp)

def process_message(message, from_number):
    """
    Process the incoming message and generate a response
    """
    logger.info(f"Processing message: '{message}' from {from_number}")
    logger.info(f"Imports successful: {IMPORTS_SUCCESSFUL}")

    # Simple response for testing
    if message == 'hola':
        return "¡Hola! El bot está funcionando. Envía 'convenio' para ver el menú."
    elif message == 'convenio':
        if IMPORTS_SUCCESSFUL:
            return get_convenio_menu()
        else:
            return "Sistema de convenios no disponible (error de importación)"
    else:
        return f"Recibí: {message}. Envía 'hola' o 'convenio'."

def get_convenio_menu():
    """Generate the convenio type selection menu"""
    if not DOCUMENT_TYPES:
        return "No hay tipos de convenio disponibles."
    
    menu = "📄 Selecciona el tipo de convenio:\n\n"
    for i, (key, name) in enumerate(DOCUMENT_TYPES.items(), 1):
        menu += f"{i}. {name}\n"
    menu += "\nEnvía el número de tu opción:"
    return menu

def get_convenio_menu():
    """Generate the convenio type selection menu"""
    menu = "📄 Selecciona el tipo de convenio:\n\n"
    for i, (key, name) in enumerate(DOCUMENT_TYPES.items(), 1):
        menu += f"{i}. {name}\n"
    menu += "\nEnvía el número de tu opción:"
    return menu

def collect_next_field(session):
    """Get the next field to collect from user"""
    fields = [
        ('nombre_demandante', 'Nombre completo del demandante'),
        ('dni_demandante', 'DNI del demandante'),
        ('domicilio_demandante', 'Domicilio del demandante'),
        ('telefono_demandante', 'Teléfono del demandante'),
        ('email_demandante', 'Email del demandante'),
        ('nombre_demandado', 'Nombre completo del demandado'),
        ('dni_demandado', 'DNI del demandado'),
        ('domicilio_demandado', 'Domicilio del demandado'),
        ('telefono_demandado', 'Teléfono del demandado'),
        ('email_demandado', 'Email del demandado')
    ]

    if session['current_field'] < len(fields):
        field_key, field_name = fields[session['current_field']]
        return f"Ingresa {field_name}:"
    else:
        session['state'] = 'confirm'
        return show_summary(session)

def handle_data_collection(message, session):
    """Handle data collection for document fields"""
    fields = [
        ('nombre_demandante', 'Nombre completo del demandante'),
        ('dni_demandante', 'DNI del demandante'),
        ('domicilio_demandante', 'Domicilio del demandante'),
        ('telefono_demandante', 'Teléfono del demandante'),
        ('email_demandante', 'Email del demandante'),
        ('nombre_demandado', 'Nombre completo del demandado'),
        ('dni_demandado', 'DNI del demandado'),
        ('domicilio_demandado', 'Domicilio del demandado'),
        ('telefono_demandado', 'Teléfono del demandado'),
        ('email_demandado', 'Email del demandado')
    ]

    current_field = session['current_field']
    field_key, field_name = fields[current_field]

    # Validate input based on field type
    if 'dni' in field_key:
        if not validate_dni(message):
            return f"DNI inválido. Debe tener 8 dígitos. Ingresa {field_name}:"
    elif 'telefono' in field_key:
        if not validate_phone(message):
            return f"Teléfono inválido. Ingresa {field_name}:"
    elif 'email' in field_key:
        if not validate_email(message):
            return f"Email inválido. Ingresa {field_name}:"

    # Store the data
    session['data'][field_key] = message
    session['current_field'] += 1

    return collect_next_field(session)

def show_summary(session):
    """Show summary of collected data for confirmation"""
    data = session['data']
    summary = "📋 Resumen de datos:\n\n"
    summary += f"📄 Tipo: {DOCUMENT_TYPES[data['document_type']]}\n\n"
    summary += f"👤 Demandante:\n"
    summary += f"   Nombre: {data.get('nombre_demandante', 'N/A')}\n"
    summary += f"   DNI: {data.get('dni_demandante', 'N/A')}\n"
    summary += f"   Domicilio: {data.get('domicilio_demandante', 'N/A')}\n"
    summary += f"   Teléfono: {data.get('telefono_demandante', 'N/A')}\n"
    summary += f"   Email: {data.get('email_demandante', 'N/A')}\n\n"
    summary += f"👤 Demandado:\n"
    summary += f"   Nombre: {data.get('nombre_demandado', 'N/A')}\n"
    summary += f"   DNI: {data.get('dni_demandado', 'N/A')}\n"
    summary += f"   Domicilio: {data.get('domicilio_demandado', 'N/A')}\n"
    summary += f"   Teléfono: {data.get('telefono_demandado', 'N/A')}\n"
    summary += f"   Email: {data.get('email_demandado', 'N/A')}\n\n"
    summary += "¿Los datos son correctos? Responde 'sí' para generar el documento o 'no' para cancelar."

    return summary

def generate_document(session, from_number):
    """Generate the document and send it via WhatsApp"""
    try:
        data = session['data']
        doc_type = data['document_type']

        # Generate document
        output_path = fill_document_naturally(doc_type, data)

        # Reset session
        session['state'] = 'initial'
        session['data'] = {}

        # For now, just return success message (document sending would require additional setup)
        return f"✅ Documento generado exitosamente!\n\nTipo: {DOCUMENT_TYPES[doc_type]}\n\nEl documento ha sido procesado y está listo. En un entorno completo, se enviaría por WhatsApp."

    except Exception as e:
        logger.error(f"Error generating document: {e}")
        return "❌ Error al generar el documento. Por favor intenta de nuevo."
