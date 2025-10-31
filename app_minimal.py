from flask import Flask, render_template, request, jsonify, send_file
import os
import tempfile
from markitdown import MarkItDown
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')

app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max file size
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Limited file extensions for minimal deployment
ALLOWED_EXTENSIONS = {'txt', 'md', 'html', 'htm', 'csv', 'json', 'xml'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    type_map = {
        'txt': 'text/plain',
        'md': 'text/markdown',
        'html': 'text/html',
        'htm': 'text/html',
        'csv': 'text/csv',
        'json': 'application/json',
        'xml': 'application/xml'
    }
    return type_map.get(ext, 'text/plain')

@app.route('/')
def index():
    return render_template('index_minimal.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Supported formats: txt, md, html, csv, json, xml'}), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Initialize MarkItDown
        md = MarkItDown(enable_plugins=False)
        
        # Convert file
        result = md.convert(file_path)
        
        # Generate output filename
        base_name = os.path.splitext(filename)[0]
        output_filename = f"{base_name}_converted.md"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Save converted content
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(result.text_content)
        
        # Clean up input file
        os.remove(file_path)
        
        return jsonify({
            'success': True,
            'output_filename': output_filename,
            'download_url': f'/download/{output_filename}',
            'content_preview': result.text_content[:500] + '...' if len(result.text_content) > 500 else result.text_content,
            'file_type': get_file_type(unique_filename)
        })
        
    except Exception as e:
        # Clean up on error
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        error_msg = f'Conversion failed: {str(e)}'
        return jsonify({'error': error_msg}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(
            os.path.join(app.config['UPLOAD_FOLDER'], filename),
            as_attachment=True,
            download_name=filename
        )
    except Exception as e:
        return jsonify({'error': 'File not found'}), 404

@app.route('/cleanup', methods=['POST'])
def cleanup_files():
    try:
        # Clean up files older than 1 hour
        current_time = datetime.now()
        for filename in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            if os.path.isfile(file_path):
                file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if (current_time - file_time).seconds > 3600:  # 1 hour
                    os.remove(file_path)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Cleanup failed: {str(e)}'}), 500

# Vercel serverless function entry point
def handler(environ, start_response):
    return app(environ, start_response)

app.handler = handler

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
