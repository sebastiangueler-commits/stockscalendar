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

    // Generar enlace de pago
    const payment_id = `pay_${Date.now()}`;

    // URL de Stripe (más confiable que PayPal)
    const stripe_url = `https://buy.stripe.com/test_28o5kK0Xj0Xj0Xj6op?prefilled_email=${user_id}@example.com&client_reference_id=${payment_id}`;

    // URL alternativa de PayPal (formato más simple)
    const paypal_url = `https://www.paypal.me/malukelbasics/${plan.price}`;

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
        stripe_url: stripe_url,
        paypal_url: paypal_url,
        message: "Choose your payment method: Stripe (recommended) or PayPal"
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
