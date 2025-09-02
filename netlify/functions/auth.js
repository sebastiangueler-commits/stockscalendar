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
    const { username, password } = JSON.parse(event.body);

    // Usuario demo para pruebas
    if (username === 'demo' && password === 'demo123') {
      return {
        statusCode: 200,
        headers,
        body: JSON.stringify({
          success: true,
          token: `token_${username}_${Date.now()}`,
          user: {
            username: username,
            email: 'demo@magicstocks.com',
            role: 'user',
            plan: 'premium'
          },
          message: 'Login exitoso'
        })
      };
    } else {
      return {
        statusCode: 401,
        headers,
        body: JSON.stringify({
          success: false,
          message: 'Credenciales inválidas'
        })
      };
    }
  } catch (error) {
    return {
      statusCode: 500,
      headers,
      body: JSON.stringify({
        success: false,
        message: `Error en login: ${error.message}`
      })
    };
  }
};
