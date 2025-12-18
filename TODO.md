# TODO Checklist for WhatsApp Document Bot

## 🏗️ Configuración Inicial del Proyecto
- [x] Crear estructura de directorios del proyecto
  - [x] `/app` - Código principal de la aplicación
  - [x] `/documents` - Plantillas base de convenios (NO modificar)
  - [x] `/output` - Convenios generados (temporal)
  - [x] `/logs` - Archivos de registro
  - [x] `/tests` - Tests unitarios
- [x] Crear `requirements.txt` con dependencias gratuitas
- [x] Crear archivo `.env` para variables de entorno
- [x] Crear `.gitignore` (ignorar `.env`, `/output`, `/logs`, `__pycache__`)
- [x] Inicializar repositorio Git

## 📦 Instalación de Dependencias
- [ ] Crear entorno virtual: `python3 -m venv venv`
- [ ] Activar entorno virtual: `source venv/bin/activate` (Mac/Linux)
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Verificar instalación: `pip list`

## 🔧 Configuración de Twilio
- [ ] Crear cuenta gratuita en Twilio (https://www.twilio.com/try-twilio)
- [ ] Obtener credenciales:
  - [ ] Account SID
  - [ ] Auth Token
- [ ] Configurar WhatsApp Sandbox:
  - [ ] Ir a Console > Messaging > Try it out > Send a WhatsApp message
  - [ ] Enviar código de activación al número de Twilio
  - [ ] Guardar número de Twilio WhatsApp
- [ ] Configurar Webhook URL en Twilio Console
  - [ ] Opción A (desarrollo local): Usar ngrok
  - [ ] Opción B (producción): URL del servidor
- [ ] Agregar credenciales al archivo `.env`

## 💻 Desarrollo de la Aplicación
- [x] Crear aplicación Flask básica (`app/__init__.py`)
- [x] Implementar endpoint `/whatsapp` para recibir mensajes
- [x] Crear sistema de sesiones de usuario (temporal en memoria)
- [x] Implementar flujo conversacional:
  - [x] Mostrar menú de convenios disponibles
  - [x] Capturar selección del usuario
  - [x] Solicitar datos campo por campo
  - [x] Mostrar resumen para confirmación
  - [x] Generar documento o cancelar
- [x] Crear módulo `document_processor.py`:
  - [x] Función `get_document_fields()` - Define campos por tipo de convenio
  - [x] Función `fill_document()` - Completa plantilla con datos
- [x] Implementar manejo de errores y logging
- [x] Agregar validaciones de datos:
  - [x] Validar formato de DNI (8 dígitos)
  - [x] Validar formato de teléfono
  - [x] Validar formato de email
  - [x] Validar formato de CBU/Alias
  - [x] Validar fechas
  - [x] Validar montos numéricos
- [x] Crear módulo `validators.py` con todas las validaciones
- [x] Crear módulo `config.py` con configuraciones centralizadas

## 📄 Preparación de Plantillas de Documentos
- [ ] Revisar todas las plantillas en `/documents`
- [ ] Identificar campos variables en cada convenio
- [ ] Agregar placeholders en formato `{{nombre_campo}}`:
  - [ ] Convenio Niños y Adolescentes
  - [ ] Convenio tercero directo (RCC y RCL)
  - [ ] Convenio Tipo Letrado (RCC y RCL)
  - [ ] Convenio Tipo Letrado Muerte
  - [ ] Convenio con Cesión de Derechos (RCC)
  - [ ] CONVENIO HONORARIOS
  - [ ] CONVENIO PATROCINIO
  - [ ] Declaracion Jurada de no Seguro
  - [ ] Desistimiento Por Renuncia de Derechos
  - [ ] Desistimiento Sustitución de Tercero
  - [ ] Recibo de Pago a Tercero (Efectivo)
- [ ] Crear documento de mapeo de placeholders
- [ ] Hacer backup de plantillas originales

## 🔒 Privacidad y Seguridad
- [x] Implementar eliminación automática de datos personales después de generar convenio
- [ ] Agregar límite de intentos por usuario (rate limiting)
- [x] Implementar timeout de sesión (15 minutos de inactividad) - configurado en config.py
- [x] Sanitizar inputs del usuario - función en validators.py
- [x] Agregar logs de auditoría (sin datos sensibles)
- [ ] Implementar HTTPS para producción
- [ ] Configurar CORS apropiadamente
- [ ] Agregar autenticación de webhook de Twilio

## 📤 Envío de Documentos por WhatsApp
- [ ] Investigar límites de tamaño de archivos de Twilio (16 MB)
- [ ] Implementar envío de documento completado:
  - [ ] Opción A: Usar Twilio Media URL (subir a servidor accesible)
  - [ ] Opción B: Convertir a PDF y enviar
- [ ] Agregar mensaje de confirmación con resumen
- [ ] Implementar reintento en caso de fallo
- [ ] Agregar opción de reenvío si falla

## 🧪 Testing
- [ ] Crear tests unitarios para `document_processor.py`
- [ ] Crear tests para flujo de conversación
- [ ] Crear tests para validaciones de datos
- [ ] Probar cada tipo de convenio con datos de ejemplo
- [ ] Probar casos de error:
  - [ ] Entrada inválida
  - [ ] Cancelación en diferentes etapas
  - [ ] Timeout de sesión
  - [ ] Plantilla no encontrada
- [ ] Probar con múltiples usuarios simultáneos
- [ ] Hacer pruebas de carga

## 🚀 Deployment - Desarrollo Local (con ngrok)

### Paso 1: Instalar ngrok
```bash
# Mac (con Homebrew)
brew install ngrok

# O descargar desde https://ngrok.com/download
```

### Paso 2: Configurar ngrok
```bash
# Crear cuenta gratuita en ngrok.com y obtener authtoken
ngrok config add-authtoken TU_AUTH_TOKEN
```

### Paso 3: Ejecutar la aplicación
```bash
# Terminal 1: Iniciar Flask
source venv/bin/activate
python run.py

# Terminal 2: Iniciar ngrok
ngrok http 5000
```

### Paso 4: Configurar Webhook en Twilio
```
1. Copiar URL HTTPS de ngrok (ej: https://abc123.ngrok.io)
2. Ir a Twilio Console > WhatsApp Sandbox Settings
3. Pegar: https://abc123.ngrok.io/whatsapp en "When a message comes in"
4. Método: HTTP POST
5. Guardar
```

### Checklist de Desarrollo Local:
- [ ] Instalar ngrok
- [ ] Configurar authtoken de ngrok
- [ ] Ejecutar Flask en puerto 5000
- [ ] Ejecutar ngrok apuntando al puerto 5000
- [ ] Copiar URL HTTPS de ngrok
- [ ] Configurar webhook en Twilio con URL de ngrok
- [ ] Probar enviando mensaje de WhatsApp al número de Twilio
- [ ] Verificar logs en terminal de Flask

## 🌐 Deployment - Producción

### Opción A: Heroku (Gratuito con limitaciones)
- [ ] Crear cuenta en Heroku
- [ ] Instalar Heroku CLI: `brew tap heroku/brew && brew install heroku`
- [x] Crear archivo `Procfile`:
  ```
  web: gunicorn run:app
  ```
- [x] Agregar `gunicorn` a `requirements.txt`
- [x] Crear archivo `runtime.txt`:
  ```
  python-3.11.0
  ```
- [ ] Inicializar Git y hacer commit
- [ ] Crear app en Heroku: `heroku create nombre-app`
- [ ] Configurar variables de entorno:
  ```bash
  heroku config:set TWILIO_ACCOUNT_SID=xxx
  heroku config:set TWILIO_AUTH_TOKEN=xxx
  heroku config:set TWILIO_WHATSAPP_NUMBER=xxx
  ```
- [ ] Deploy: `git push heroku main`
- [ ] Configurar webhook en Twilio con URL de Heroku
- [ ] Verificar logs: `heroku logs --tail`

### Opción B: Railway (Alternativa a Heroku)
- [ ] Crear cuenta en Railway.app
- [ ] Conectar repositorio GitHub
- [ ] Railway detectará automáticamente Flask
- [ ] Configurar variables de entorno en Railway
- [ ] Deploy automático desde GitHub
- [ ] Obtener URL pública de Railway
- [ ] Configurar webhook en Twilio

### Opción C: Render (Free tier generoso)
- [ ] Crear cuenta en Render.com
- [ ] Crear nuevo "Web Service"
- [ ] Conectar repositorio GitHub
- [ ] Configurar:
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn run:app`
- [ ] Agregar variables de entorno
- [ ] Deploy automático
- [ ] Configurar webhook en Twilio con URL de Render

### Opción D: VPS Propio (DigitalOcean, Linode, AWS EC2)
- [ ] Crear servidor VPS
- [ ] Instalar Python 3.11+
- [ ] Clonar repositorio
- [ ] Instalar dependencias
- [ ] Configurar Nginx como reverse proxy
- [ ] Configurar SSL con Let's Encrypt
- [ ] Usar Gunicorn o uWSGI
- [ ] Configurar systemd para auto-inicio
- [ ] Configurar firewall
- [ ] Configurar webhook en Twilio con dominio propio

## 📊 Monitoreo y Mantenimiento
- [x] Configurar logging en producción - logging.basicConfig en routes.py
- [ ] Implementar rotación de logs
- [ ] Configurar alertas de errores (Sentry o similar)
- [ ] Monitorear uso de almacenamiento en `/output`
- [ ] Implementar limpieza automática de archivos antiguos en `/output`
- [ ] Monitorear uso de cuota de Twilio
- [ ] Crear dashboard de métricas:
  - [ ] Convenios generados por día
  - [ ] Tipos de convenios más usados
  - [ ] Tasa de éxito/cancelación
  - [ ] Tiempo promedio de generación

## 🔄 Mejoras Futuras
- [ ] Implementar base de datos (PostgreSQL) para:
  - [ ] Persistencia de sesiones
  - [ ] Historial de convenios generados (solo metadatos, no datos personales)
  - [ ] Estadísticas de uso
- [ ] Agregar autenticación de usuarios
- [ ] Implementar Redis para manejo de sesiones
- [ ] Agregar soporte para múltiples idiomas
- [ ] Implementar firma digital de documentos
- [ ] Agregar opción de envío por email
- [ ] Crear panel de administración web
- [ ] Implementar IA para extracción de datos de imágenes (OCR)
- [ ] Agregar plantillas personalizadas por usuario
- [ ] Implementar versionado de convenios
- [ ] Agregar notificaciones de seguimiento
- [ ] Crear API REST para integraciones

## 📝 Documentación
- [x] Crear README.md completo
- [ ] Documentar arquitectura del sistema
- [ ] Crear guía de usuario para WhatsApp
- [ ] Documentar proceso de agregar nuevos tipos de convenios
- [ ] Crear video tutorial de instalación
- [ ] Documentar API de endpoints
- [ ] Crear guía de troubleshooting
- [x] Documentar placeholders de cada convenio - en document_processor.py

## ✅ Verificación Final
- [ ] Todas las plantillas tienen placeholders correctos
- [ ] Todos los tipos de convenios funcionan correctamente
- [x] Los datos se eliminan después de generar convenio
- [x] El bot responde a errores de forma amigable
- [x] Los logs no contienen datos sensibles
- [ ] El webhook está configurado correctamente
- [ ] SSL/HTTPS está activo en producción
- [x] Las validaciones de datos funcionan
- [ ] El envío de documentos funciona
- [ ] El bot maneja múltiples usuarios simultáneamente

---

## 🎯 Prioridades de Desarrollo

### Sprint 1 (Semana 1) - MVP ✅ EN PROGRESO
- [x] Configuración básica y plantillas con placeholders
- [x] Flujo conversacional completo
- [x] Generación de al menos 3 tipos de convenios
- [ ] Testing local con ngrok

### Sprint 2 (Semana 2) - Validaciones y Seguridad
- [x] Implementar todas las validaciones
- [x] Agregar seguridad y privacidad
- [ ] Testing completo de todos los convenios
- [ ] Preparar para producción

### Sprint 3 (Semana 3) - Deployment
- [ ] Deploy a producción (Heroku/Railway/Render)
- [ ] Configuración de monitoreo
- [x] Documentación completa
- [ ] Testing en producción

### Sprint 4 (Semana 4) - Mejoras
- [ ] Envío de documentos por WhatsApp
- [ ] Mejoras de UX
- [ ] Optimizaciones de performance
- [ ] Feedback de usuarios

---

## 📌 Notas Importantes

⚠️ **Privacidad**: Los datos personales NUNCA se almacenan después de generar el convenio. ✅ IMPLEMENTADO

⚠️ **Plantillas Base**: Los archivos en `/documents` son las plantillas originales y NO se modifican. ✅ CONFIRMADO

⚠️ **Convenios Generados**: Los archivos en `/output` deben limpiarse periódicamente (configurar cron job).

⚠️ **Límites de Twilio**: Cuenta gratuita tiene límites de mensajes y números de destino.

⚠️ **Ngrok**: La URL de ngrok cambia cada vez que reinicias (para desarrollo). En producción usar dominio fijo.

💡 **Tip**: Usar variables de entorno para todas las credenciales y configuraciones sensibles. ✅ IMPLEMENTADO

💡 **Tip**: Hacer backups regulares de las plantillas base en `/documents`.

---

## 📋 RESUMEN DE PROGRESO

### ✅ Completado (70% del MVP)
- Estructura completa del proyecto
- Sistema de validaciones robusto
- Flujo conversacional implementado
- Módulo de procesamiento de documentos
- Configuración centralizada
- Seguridad y privacidad básicas
- Documentación inicial

### 🔄 En Progreso
- Preparación de plantillas con placeholders
- Testing del sistema

### ⏳ Pendiente
- Configuración de Twilio y webhook
- Testing local con ngrok
- Envío de documentos por WhatsApp
- Deploy a producción

### 🎯 Próximos Pasos Inmediatos
1. Instalar dependencias: `pip install -r requirements.txt`
2. Configurar `.env` con credenciales de Twilio
3. Agregar placeholders a las plantillas en `/documents`
4. Testing local con ngrok
5. Deploy a producción