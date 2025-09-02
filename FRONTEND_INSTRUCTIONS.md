# 🎯 INSTRUCCIONES PARA FRONTEND - CALENDARIOS VISUALES

## 📅 Endpoints Disponibles para Calendarios Visuales

### 1. **Calendario Mensual** (Como la imagen - RECOMENDADO)
```
GET /api/calendar/monthly
```
**Formato de respuesta:**
```json
{
  "monthly_calendar": {
    "month": "09",
    "year": "2025",
    "month_name": "SEPTIEMBRE",
    "days": {
      "01": {
        "date": "2025-09-01",
        "day": "01",
        "signals": [
          {
            "symbol": "MA",
            "type": "SELL",
            "source": "fundamental",
            "price": 404.26,
            "target_price": 445.61,
            "stop_loss": 352.63,
            "confidence": 0.81,
            "reason": "P/E: 17.8, ROE: 21.4%, Debt/Equity: 0.3"
          }
        ],
        "buy_signals": [],
        "sell_signals": [...],
        "total_signals": 2,
        "total_buy": 0,
        "total_sell": 2
      }
    },
    "total_days": 29,
    "total_signals": 140,
    "total_buy": 15,
    "total_sell": 125
  }
}
```

### 2. **Calendario Visual Completo** (Para FullCalendar.js)
```
GET /api/calendar/visual
```
**Formato de respuesta:**
```json
{
  "events": [
    {
      "id": "AAPL_2025-09-01_BUY",
      "title": "AAPL - BUY",
      "date": "2025-09-01",
      "start": "2025-09-01T09:00:00",
      "end": "2025-09-01T17:00:00",
      "symbol": "AAPL",
      "type": "BUY",
      "source": "fundamental",
      "price": 172.06,
      "target_price": 195.46,
      "stop_loss": 149.90,
      "confidence": 0.78,
      "reason": "P/E: 12.6, ROE: 15.7%, Debt/Equity: 0.1",
      "backgroundColor": "#28a745",
      "borderColor": "#28a745",
      "textColor": "#ffffff"
    }
  ],
  "total_events": 140,
  "buy_events": 15,
  "sell_events": 125,
  "fundamental_events": 70,
  "technical_events": 70
}
```

### 2. **Calendario Fundamental Diario**
```
GET /api/calendar/fundamental/daily
```

### 3. **Calendario Histórico Diario**
```
GET /api/calendar/historical/daily
```

### 4. **Calendario Completo Diario**
```
GET /api/calendar/daily
```

## 🎨 Colores para el Calendario

- **BUY (Comprar)**: Verde (#28a745)
- **SELL (Vender)**: Rojo (#dc3545)
- **Fundamental**: Azul (#007bff)
- **Técnico**: Naranja (#fd7e14)

## 📊 Datos Disponibles por Evento

Cada evento incluye:
- **symbol**: Símbolo de la acción (AAPL, MSFT, etc.)
- **type**: BUY o SELL
- **source**: fundamental o technical
- **price**: Precio actual
- **target_price**: Precio objetivo
- **stop_loss**: Stop loss
- **confidence**: Nivel de confianza (0-1)
- **reason**: Razón del análisis (P/E, ROE, etc.)
- **volume**: Volumen de trading

## 🚀 Implementación Recomendada

1. **Usar `/api/calendar/monthly`** para calendario tipo imagen (como enero 2025)
2. **Mostrar acciones dentro de cada día** con símbolos y tipos
3. **Usar colores** para distinguir BUY/SELL (verde/rojo)
4. **Mostrar tooltip** con detalles al hacer hover
5. **Filtrar por source** para mostrar fundamental vs histórico

## 📱 Ejemplo de Uso en React

### Para Calendario Mensual (Recomendado)
```javascript
// Obtener calendario mensual
const response = await fetch('/api/calendar/monthly');
const data = await response.json();

const monthlyData = data.monthly_calendar;

// Renderizar calendario tipo imagen
const renderCalendar = () => {
  return (
    <div className="calendar-grid">
      <h2>{monthlyData.month_name} {monthlyData.year}</h2>
      <div className="calendar-days">
        {Object.entries(monthlyData.days).map(([day, dayData]) => (
          <div key={day} className="calendar-day">
            <div className="day-number">{day}</div>
            <div className="day-signals">
              {dayData.signals.map((signal, index) => (
                <div 
                  key={index} 
                  className={`signal ${signal.type.toLowerCase()}`}
                  title={`${signal.symbol} - ${signal.type} - $${signal.price}`}
                >
                  {signal.symbol} {signal.type}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
```

### Para FullCalendar.js
```javascript
// Obtener eventos del calendario
const response = await fetch('/api/calendar/visual');
const data = await response.json();

// Para FullCalendar.js
const events = data.events.map(event => ({
  id: event.id,
  title: event.title,
  start: event.start,
  end: event.end,
  backgroundColor: event.backgroundColor,
  borderColor: event.borderColor,
  textColor: event.textColor,
  extendedProps: {
    symbol: event.symbol,
    type: event.type,
    price: event.price,
    target_price: event.target_price,
    stop_loss: event.stop_loss,
    confidence: event.confidence,
    reason: event.reason
  }
}));
```

## ✅ Datos Reales Disponibles

- **29 días** de trading
- **140 eventos** totales
- **70 eventos fundamentales**
- **70 eventos técnicos**
- **15 señales de compra**
- **125 señales de venta**

¡Los calendarios ahora muestran acciones reales día por día! 🎉
