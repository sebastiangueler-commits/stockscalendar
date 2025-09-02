# 💳 Configuración PayPal - Paso a Paso

## 1. 🏢 Crear Cuenta PayPal Business

### Pasos:
1. Ve a https://www.paypal.com/business
2. Haz clic en "Abrir cuenta Business"
3. Completa la información:
   - Nombre de la empresa
   - Dirección
   - Número de teléfono
   - Información fiscal

### Verificación:
- Sube documentos de identidad
- Verifica tu número de teléfono
- Completa la verificación fiscal

## 2. 🔑 Obtener Credenciales de Desarrollador

### Pasos:
1. Ve a https://developer.paypal.com
2. Inicia sesión con tu cuenta Business
3. Haz clic en "Create App"
4. Completa la información:
   - App Name: "Magic Stocks Calendar"
   - Merchant: Tu cuenta Business
   - Features: "Accept payments"

### Credenciales que obtienes:
- **Client ID**: Para el frontend
- **Client Secret**: Para el backend (¡NUNCA lo expongas!)
- **Merchant ID**: Para pagos directos

## 3. 🌐 Configurar URLs de Retorno

### URLs necesarias:
- **Return URL**: `https://tu-dominio.com/payment/success`
- **Cancel URL**: `https://tu-dominio.com/payment/cancel`
- **Webhook URL**: `https://tu-dominio.com/api/paypal/webhook`

## 4. 💰 Configurar Planes de Pago

### Planes actuales:
- **Basic**: $29.99/mes
- **Premium**: $99.99/mes  
- **Pro**: $199.99/mes

### Configuración en PayPal:
1. Ve a "Products & Services"
2. Crea productos para cada plan
3. Configura precios recurrentes
4. Obtén IDs de productos

## 5. 🔧 Implementación Técnica

### Backend (app.py):
```python
# Variables de entorno
PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID')
PAYPAL_CLIENT_SECRET = os.getenv('PAYPAL_CLIENT_SECRET')
PAYPAL_MODE = os.getenv('PAYPAL_MODE', 'sandbox')  # 'live' para producción
```

### Frontend:
```javascript
// Configuración PayPal
const paypalConfig = {
  clientId: process.env.REACT_APP_PAYPAL_CLIENT_ID,
  currency: 'USD',
  intent: 'subscription'
};
```

## 6. 🧪 Testing

### Sandbox (Desarrollo):
- Usa credenciales de sandbox
- Prueba con cuentas de prueba
- Verifica flujo completo

### Live (Producción):
- Cambia a credenciales live
- Prueba con montos pequeños
- Monitorea transacciones

## 7. 📊 Monitoreo y Analytics

### Métricas importantes:
- Tasa de conversión
- Abandonos en checkout
- Errores de pago
- Tiempo de procesamiento

### Herramientas:
- PayPal Dashboard
- Google Analytics
- Logs de aplicación

## 8. 🔒 Seguridad

### Mejores prácticas:
- Nunca expongas Client Secret
- Usa HTTPS en producción
- Valida webhooks de PayPal
- Implementa rate limiting
- Logs de auditoría

## 9. 💡 Tips Adicionales

### Optimización:
- Implementa retry logic
- Cachea respuestas de PayPal
- Usa webhooks para actualizaciones
- Implementa fallbacks

### UX:
- Loading states durante pago
- Mensajes de error claros
- Confirmación de pago
- Email de confirmación
