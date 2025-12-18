from flask import request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from app import app
from app.config import DOCUMENT_TYPES
from app.validators import validate_dni, validate_phone, validate_email
from app.document_processor import fill_document_naturally
import logging
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
    # Get or create user session
    if from_number not in user_sessions:
        user_sessions[from_number] = {
            'state': 'initial',
            'data': {}
        }

    session = user_sessions[from_number]

    # Main conversation flow
    if session['state'] == 'initial':
        if message in ['hola', 'hello', 'hi']:
            return "¡Hola! Soy tu asistente para generar convenios legales. Envía 'convenio' para comenzar."
        elif message == 'convenio':
            session['state'] = 'select_type'
            return get_convenio_menu()
        else:
            return "Envía 'convenio' para comenzar a generar un documento legal."

    elif session['state'] == 'select_type':
        try:
            choice = int(message)
            if 1 <= choice <= len(DOCUMENT_TYPES):
                doc_type = list(DOCUMENT_TYPES.keys())[choice - 1]
                session['data']['document_type'] = doc_type
                session['state'] = 'collect_data'
                session['current_field'] = 0
                return f"Seleccionaste: {DOCUMENT_TYPES[doc_type]}\n\n{collect_next_field(session)}"
            else:
                return f"Opción inválida. {get_convenio_menu()}"
        except ValueError:
            return f"Por favor ingresa un número. {get_convenio_menu()}"

    elif session['state'] == 'collect_data':
        return handle_data_collection(message, session)

    elif session['state'] == 'confirm':
        if message.lower() in ['si', 'sí', 'yes', 'y']:
            return generate_document(session, from_number)
        elif message.lower() in ['no', 'n']:
            session['state'] = 'initial'
            return "Operación cancelada. Envía 'convenio' para comenzar de nuevo."
        else:
            return "Por favor responde 'sí' o 'no' para confirmar los datos."

    return f"Echo: {message}"

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
