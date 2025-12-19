import os

class Config:
    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
    TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')

# Document types mapping
DOCUMENT_TYPES = {
    'niños_adolescentes': 'Convenio Niños y Adolescentes',
    'tercero_directo_rcc_rcl': 'Convenio Tercero Directo (RCC y RCL)',
    'tipo_letrado_rcc_rcl': 'Convenio Tipo Letrado (RCC y RCL)',
    'tipo_letrado_muerte': 'Convenio Tipo Letrado Muerte',
    'cesion_derechos_rcc': 'Convenio con Cesión de Derechos (RCC)',
    'honorarios': 'Convenio Honorarios',
    'patrocinio': 'Convenio Patrocinio',
    'desistimiento_renuncia': 'Desistimiento por Renuncia de Derechos',
    'desistimiento_sustitucion': 'Desistimiento Sustitución de Tercero',
    'recibo_pago_tercero': 'Recibo de Pago a Tercero',
    'declaracion_no_seguro': 'Declaración Jurada de No Seguro'
}