exports.handler = async (event, context) => {
  // CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'POST, OPTIONS'
  };

  // Handle preflight requests
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers,
      body: ''
    };
  }

  if (event.httpMethod !== 'POST') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  try {
    const { plan_id, user_id } = JSON.parse(event.body);

    // Planes de pago
    const payment_plans = [
      {
        id: "monthly",
        name: "Monthly Plan",
        price: 9.99,
        period: "month",
        features: ["Full access to all signals", "Premium features included", "Real-time updates"]
      },
      {
        id: "yearly",
        name: "Yearly Plan",
        price: 99.99,
        period: "year",
        features: ["Full access to all signals", "Premium features included", "Save 17% vs monthly", "Real-time updates"]
      },
      {
        id: "lifetime",
        name: "Lifetime Plan",
        price: 300,
        period: "lifetime",
        features: ["Full access to all signals", "Premium features included", "Best value - One payment forever", "Real-time updates"]
      }
    ];

    const plan = payment_plans.find(p => p.id === plan_id);
    if (!plan) {
      return {
        statusCode: 404,
        headers,
        body: JSON.stringify({ success: false, error: "Plan no encontrado" })
      };
    }

    // Generar enlace de PayPal
    const payment_id = `pay_${Date.now()}`;

    // URL de PayPal para pagos reales
    const paypal_url = `https://www.paypal.com/paypalme/malukelbasics@gmail.com/${plan.price}`;

    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        success: true,
        payment_id: payment_id,
        plan: plan,
        user_id: user_id,
        status: "pending",
        amount: plan.price,
        paypal_url: paypal_url,
        message: "Redirigiendo a PayPal para completar el pago"
      })
    };
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        error: `Error en pago: ${error.message}`
      })
    };
  }
};
