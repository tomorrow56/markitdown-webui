from app import app

# Vercel serverless function entry point
def handler(environ, start_response):
    return app(environ, start_response)

# Export for Vercel
app.handler = handler
