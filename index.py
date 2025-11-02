from app import app as application

# Vercel serverless function entry point
# @vercel/python expects either 'app' or 'handler' to be exported
# Using 'app' as the standard name for WSGI applications
app = application
