from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return jsonify({
        'message': 'Stocks Calendar API',
        'status': 'running',
        'version': '1.0.0'
    })

@app.route('/api/health')
def health():
    return jsonify({
        'status': 'ok',
        'message': 'Server is running'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'Test endpoint working',
        'status': 'success'
    })

# For Vercel
handler = app

if __name__ == '__main__':
    app.run(debug=True)
