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

    // Generar datos de calendario simulados pero realistas
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

      // Generar señales para cada día del mes
      for (let day = 1; day <= daysInMonth; day++) {
        const date = `${currentYear}-${String(currentMonth + 1).padStart(2, "0")}-${String(day).padStart(2, "0")}`;
        const dayOfWeek = new Date(currentYear, currentMonth, day).getDay();

        // Solo días laborables (lunes a viernes)
        if (dayOfWeek >= 1 && dayOfWeek <= 5) {
          const signals = [];
          const numSignals = Math.floor(Math.random() * 8) + 2; // 2-9 señales por día

          for (let i = 0; i < numSignals; i++) {
            const signalTypes = ["BUY", "SELL", "HOLD"];
            const signalType = signalTypes[Math.floor(Math.random() * signalTypes.length)];

            const companies = ["AAPL", "GOOGL", "MSFT", "AMZN", "TSLA", "META", "NVDA", "NFLX"];
            const company = companies[Math.floor(Math.random() * companies.length)];

            signals.push({
              id: `signal_${day}_${i}`,
              company: company,
              signal: signalType,
              confidence: Math.floor(Math.random() * 30) + 70, // 70-99%
              price: (Math.random() * 500 + 50).toFixed(2),
              change: (Math.random() * 10 - 5).toFixed(2),
              volume: Math.floor(Math.random() * 1000000) + 100000,
              timestamp: `${date}T${String(Math.floor(Math.random() * 24)).padStart(2, "0")}:${String(Math.floor(Math.random() * 60)).padStart(2, "0")}:00Z`
            });
          }

          calendarData.days[date] = {
            date: date,
            day_of_week: ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][dayOfWeek - 1],
            signals: signals,
            total_signals: signals.length
          };

          calendarData.total_signals += signals.length;
        }
      }

      return calendarData;
    };

    const calendarData = generateCalendarData();

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
