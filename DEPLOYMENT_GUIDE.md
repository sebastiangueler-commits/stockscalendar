# 🚀 Magic Stocks Calendar - Guía de Deployment

## 📋 Configuración PayPal para Producción

### 1. Cuenta PayPal Business
- Crear cuenta en https://developer.paypal.com
- Verificar identidad y datos fiscales
- Activar cuenta Business

### 2. Aplicación PayPal
- Crear nueva aplicación en PayPal Developer
- Obtener Client ID y Client Secret
- Configurar URLs de retorno:
  - Return URL: `https://tu-dominio.com/payment/success`
  - Cancel URL: `https://tu-dominio.com/payment/cancel`

### 3. Variables de Entorno
```env
PAYPAL_CLIENT_ID=tu_client_id_aqui
PAYPAL_CLIENT_SECRET=tu_client_secret_aqui
PAYPAL_MODE=sandbox  # o 'live' para producción
PAYPAL_MERCHANT_ID=tu_merchant_id_aqui
```

### 4. Configuración en el Backend
- Actualizar `paypal_config.json` con credenciales reales
- Configurar webhooks para notificaciones
- Implementar verificación de pagos

### 5. Frontend
- Actualizar URLs de PayPal en el frontend
- Configurar manejo de respuestas de PayPal
- Implementar redirección después del pago

## 🌐 Deployment Options

### Frontend (React)
- **Vercel**: https://vercel.com
- **Netlify**: https://netlify.com
- **GitHub Pages**: Gratis

### Backend (FastAPI)
- **Railway**: https://railway.app
- **Heroku**: https://heroku.com
- **DigitalOcean**: https://digitalocean.com
- **AWS**: https://aws.amazon.com

### Base de Datos
- **PostgreSQL**: Railway, Heroku, AWS RDS
- **MongoDB**: MongoDB Atlas
- **SQLite**: Para desarrollo local

## 📝 Checklist de Deployment

### Pre-deployment
- [ ] Configurar variables de entorno
- [ ] Actualizar URLs en el código
- [ ] Configurar CORS para dominio de producción
- [ ] Preparar base de datos
- [ ] Configurar PayPal

### Post-deployment
- [ ] Verificar que todas las APIs funcionen
- [ ] Probar login y registro
- [ ] Probar pagos con PayPal
- [ ] Verificar calendarios
- [ ] Probar admin dashboard

## 🔧 Comandos de Build

### Frontend
```bash
cd frontend
npm run build
```

### Backend
```bash
pip freeze > requirements.txt
```

## 📊 Monitoreo
- Configurar logs de aplicación
- Monitorear errores de PayPal
- Tracking de conversiones
- Analytics de uso
