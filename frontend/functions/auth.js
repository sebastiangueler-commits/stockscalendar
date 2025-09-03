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

  console.log('Auth function called with method:', event.httpMethod);

  // Simple demo login
  if (event.httpMethod === 'POST') {
    try {
      console.log('Auth function body:', event.body);
      const { username, password } = JSON.parse(event.body);
      console.log('Login attempt for username:', username);
      
      if (username === 'demo' && password === 'demo123') {
        console.log('Login successful for demo user');
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
            message: 'Login successful'
          })
        };
      } else {
        console.log('Login failed - invalid credentials');
        return {
          statusCode: 401,
          headers,
          body: JSON.stringify({
            success: false,
            message: 'Invalid credentials. Use demo/demo123'
          })
        };
      }
    } catch (error) {
      console.error('Auth function error:', error);
      return {
        statusCode: 500,
        headers,
        body: JSON.stringify({
          success: false,
          message: `Login error: ${error.message}`
        })
      };
    }
  }

  return {
    statusCode: 405,
    headers,
    body: JSON.stringify({ error: 'Method not allowed' })
  };
};
