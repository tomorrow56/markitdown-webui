from app_minimal import app

# Vercel serverless function entry point
def handler(environ, start_response):
    return app(environ, start_response)

app.handler = handler
