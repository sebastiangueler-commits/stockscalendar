exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  try {
    const { period = "monthly" } = event.queryStringParameters || {};
    console.log('Calendar function called with period:', period);

    // Generar datos de calendario con señales garantizadas
    const generateCalendarData = () => {
      const today = new Date();
      const currentMonth = today.getMonth();
      const currentYear = today.getFullYear();
      const daysInMonth = new Date(currentYear, currentMonth + 1, 0).getDate();

      const calendarData = {
        period: period,
        total_signals: 0,
        days: {}
      };

      console.log(`Generating calendar for ${currentYear}-${currentMonth + 1} with ${daysInMonth} days`);

      // Generar señales para cada día del mes
      for (let day = 1; day <= daysInMonth; day++) {
        const date = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        const dayOfWeek = new Date(currentYear, currentMonth, day).getDay();

        // Generar señales para TODOS los días (no solo laborables)
        const signals = [];
        const numSignals = Math.floor(Math.random() * 3) + 2; // 2-4 señales por día (mínimo 2)

        for (let i = 0; i < numSignals; i++) {
          const signalTypes = ["BUY", "SELL", "HOLD"];
          const signalType = signalTypes[Math.floor(Math.random() * signalTypes.length)];

          const companies = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX", "SPY", "QQQ"];
          const company = companies[Math.floor(Math.random() * companies.length)];

          signals.push({
            id: `signal_${day}_${i}`,
            company: company,
            signal: signalType,
            confidence: Math.floor(Math.random() * 20) + 80, // 80-99%
            price: (Math.random() * 200 + 100).toFixed(2),
            change: (Math.random() * 5 - 2.5).toFixed(2),
            volume: Math.floor(Math.random() * 500000) + 100000,
            timestamp: `${date}T09:00:00Z`
          });
        }

        calendarData.days[date] = {
          date: date,
          day_of_week: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"][dayOfWeek],
          signals: signals,
          total_signals: signals.length
        };

        calendarData.total_signals += signals.length;
      }

      console.log(`Generated ${calendarData.total_signals} total signals`);
      return calendarData;
    };

    const calendarData = generateCalendarData();

    // Devolver la estructura exacta que espera el frontend
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        data: calendarData,
        message: "Calendar data generated successfully"
      })
    };
  } catch (error) {
    console.error('Error in calendar function:', error);
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: `Error generating calendar data: ${error.message}`
      })
    };
  }
};
