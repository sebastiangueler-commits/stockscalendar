from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        'message': 'Hello from Vercel!',
        'status': 'working'
    })

@app.route('/api/test')
def test():
    return jsonify({
        'message': 'API is working',
        'status': 'success'
    })

# For Vercel
handler = app

if __name__ == '__main__':
    app.run(debug=True)
