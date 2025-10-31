from app_minimal import app

# Vercel serverless function entry point
def handler(environ, start_response):
    try:
        return app(environ, start_response)
    except Exception as e:
        # Log error for debugging
        print(f"Handler error: {e}")
        # Return 500 error
        start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [b'Internal Server Error']

# Export for Vercel
app.handler = handler
