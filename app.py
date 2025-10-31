from flask import Flask, render_template, request, jsonify, send_file, send_from_directory
import os
import tempfile
from markitdown import MarkItDown
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {
    'pdf', 'docx', 'doc', 'pptx', 'ppt', 'xlsx', 'xls', 
    'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp',
    'wav', 'mp3', 'html', 'htm', 'csv', 'json', 'xml', 
    'zip', 'epub', 'txt', 'md'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_type(filename):
    # Simple file type detection based on extension
    ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    type_map = {
        'pdf': 'application/pdf',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'doc': 'application/msword',
        'pptx': 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
        'ppt': 'application/vnd.ms-powerpoint',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'xls': 'application/vnd.ms-excel',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'bmp': 'image/bmp',
        'tiff': 'image/tiff',
        'webp': 'image/webp',
        'wav': 'audio/wav',
        'mp3': 'audio/mpeg',
        'html': 'text/html',
        'htm': 'text/html',
        'csv': 'text/csv',
        'json': 'application/json',
        'xml': 'application/xml',
        'zip': 'application/zip',
        'epub': 'application/epub+zip',
        'txt': 'text/plain',
        'md': 'text/markdown'
    }
    return type_map.get(ext, 'application/octet-stream')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        print(f"Received file: {file.filename}")
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported'}), 400
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        print(f"File saved to: {file_path}")
        
        # Initialize MarkItDown
        try:
            # Force import of PDF dependencies
            import pdfminer
            md = MarkItDown(enable_plugins=False)
            print(f"MarkItDown initialized successfully")
            
            # Check available converters
            converters = [type(c).__name__ for c in md._converters]
            print(f"Available converters: {converters}")
            
        except Exception as e:
            print(f"Failed to initialize MarkItDown: {e}")
            raise
        
        # Convert file
        try:
            print(f"Converting file: {file_path}")
            result = md.convert(file_path)
            print(f"Conversion successful")
        except Exception as e:
            print(f"Conversion failed: {e}")
            import traceback
            traceback.print_exc()
            raise
        
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
        print(error_msg)
        import traceback
        traceback.print_exc()
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)
