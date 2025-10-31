from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({
        'message': 'MarkItDown Web UI (Test)',
        'status': 'working',
        'version': '1.0.0'
    })

@app.route('/test')
def test():
    return jsonify({
        'test': 'success',
        'environment': 'vercel' if __name__ != '__main__' else 'local'
    })

# Vercel serverless function entry point
def handler(environ, start_response):
    try:
        return app(environ, start_response)
    except Exception as e:
        print(f"Handler error: {e}")
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Internal Server Error']

app.handler = handler

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
