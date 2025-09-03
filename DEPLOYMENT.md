# 🚀 Magic Stocks Calendar - Deployment Guide

## 📋 Resumen del Proyecto

**Magic Stocks Calendar** es una aplicación de análisis de acciones con:
- ✅ Backend: FastAPI (Python)
- ✅ Frontend: React + Tailwind CSS
- ✅ APIs: Alpha Vantage, Yahoo Finance, IEX Cloud
- ✅ Pagos: PayPal integrado
- ✅ Datos: 5000+ acciones reales analizadas

## 🌐 Deployment Options

### Opción 1: Railway (Backend) + Vercel (Frontend) - RECOMENDADO

#### Backend en Railway:
1. **Crear cuenta en Railway**: https://railway.app
2. **Conectar GitHub**: Conecta tu repositorio
3. **Deploy automático**: Railway detectará el `railway.json`
4. **Variables de entorno**:
   ```
   ALPHA_VANTAGE_API_KEY=demo
   IEX_CLOUD_API_KEY=Tpk_018b97bce0a24c0d9c632c01c3c7c5c8
   FINNHUB_API_KEY=demo
   PAYPAL_CLIENT_ID=Af3gNb8926-JQj_yhlkytxhRb2k6IigPrzQoAwa9ifawMixPM5aS8t2IuaJ0aJA0eLTVFVrSTdE3d_Y6
   PAYPAL_CLIENT_SECRET=EFQLJ1moTHjkB3PhZm3LFzTK9ixq3KWMlV9A9S_e1VKFXWJvFuWzrdOQrAn5z27a2t4Yx_xzgdzbrmoI
   PAYPAL_MODE=live
   PAYPAL_EMAIL=malukelbasics@gmail.com
   ```

#### Frontend en Vercel:
1. **Crear cuenta en Vercel**: https://vercel.com
2. **Importar proyecto**: Conecta tu repositorio
3. **Configurar build**:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/build`
4. **Variables de entorno**:
   ```
   REACT_APP_API_URL=https://tu-backend.railway.app
   REACT_APP_PAYPAL_CLIENT_ID=Af3gNb8926-JQj_yhlkytxhRb2k6IigPrzQoAwa9ifawMixPM5aS8t2IuaJ0aJA0eLTVFVrSTdE3d_Y6
   ```

### Opción 2: Railway (Backend) + Netlify (Frontend)

#### Backend en Railway:
- Mismo proceso que Opción 1

#### Frontend en Netlify:
1. **Crear cuenta en Netlify**: https://netlify.com
2. **Conectar GitHub**: Conecta tu repositorio
3. **Configurar build**:
   - Build Command: `cd frontend && npm install && npm run build`
   - Publish Directory: `frontend/build`
4. **Variables de entorno**:
   ```
   REACT_APP_API_URL=https://tu-backend.railway.app
   REACT_APP_PAYPAL_CLIENT_ID=Af3gNb8926-JQj_yhlkytxhRb2k6IigPrzQoAwa9ifawMixPM5aS8t2IuaJ0aJA0eLTVFVrSTdE3d_Y6
   ```

### Opción 3: Heroku (Backend) + Vercel (Frontend)

#### Backend en Heroku:
1. **Crear cuenta en Heroku**: https://heroku.com
2. **Instalar Heroku CLI**
3. **Deploy**:
   ```bash
   heroku create magic-stocks-backend
   git push heroku main
   ```
4. **Variables de entorno**:
   ```bash
   heroku config:set ALPHA_VANTAGE_API_KEY=demo
   heroku config:set PAYPAL_CLIENT_ID=Af3gNb8926-JQj_yhlkytxhRb2k6IigPrzQoAwa9ifawMixPM5aS8t2IuaJ0aJA0eLTVFVrSTdE3d_Y6
   # ... etc
   ```

## 🔧 Configuración Post-Deployment

### 1. Actualizar URLs en el Frontend
Después del deployment, actualiza las URLs en:
- `netlify.toml` (línea 8)
- `vercel.json` (línea 12)
- Variables de entorno del frontend

### 2. Configurar PayPal
- ✅ PayPal ya está configurado con tus credenciales
- ✅ Modo: `live` (producción)
- ✅ Email: `malukelbasics@gmail.com`

### 3. Dominio Personalizado (Opcional)
- **Railway**: Configura dominio personalizado en el dashboard
- **Vercel/Netlify**: Configura dominio en las configuraciones del proyecto

## 📊 Monitoreo y Mantenimiento

### Health Checks:
- Backend: `https://tu-backend.railway.app/health`
- Frontend: Verifica que cargue correctamente

### Logs:
- **Railway**: Dashboard → Logs
- **Vercel**: Dashboard → Functions → Logs
- **Netlify**: Dashboard → Functions → Logs

### Actualizaciones:
- **Automáticas**: Cada push a `main` deploya automáticamente
- **Manuales**: Usa los dashboards de cada plataforma

## 🚨 Troubleshooting

### Backend no responde:
1. Verifica variables de entorno
2. Revisa logs en Railway/Heroku
3. Verifica que el puerto sea `$PORT`

### Frontend no conecta al backend:
1. Verifica `REACT_APP_API_URL`
2. Revisa CORS en el backend
3. Verifica que las funciones de Netlify estén funcionando

### PayPal no funciona:
1. Verifica credenciales en variables de entorno
2. Confirma que esté en modo `live`
3. Revisa logs de pago

## 💰 Costos Estimados

### Railway:
- **Gratis**: 500 horas/mes
- **Pro**: $5/mes por servicio

### Vercel:
- **Gratis**: 100GB bandwidth/mes
- **Pro**: $20/mes

### Netlify:
- **Gratis**: 100GB bandwidth/mes
- **Pro**: $19/mes

## 🎯 Próximos Pasos

1. **Deploy Backend** en Railway
2. **Deploy Frontend** en Vercel/Netlify
3. **Configurar variables de entorno**
4. **Probar funcionalidad completa**
5. **Configurar dominio personalizado** (opcional)
6. **Monitorear performance**

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en cada plataforma
2. Verifica las variables de entorno
3. Confirma que las URLs estén correctas
4. Contacta soporte de la plataforma si es necesario

---

**¡Tu aplicación estará online en menos de 30 minutos!** 🚀