# MarkItDown Web UI

A modern web interface for Microsoft's MarkItDown document conversion tool.

## 🚀 Live Demo

**https://markitdown-webui-fawn.vercel.app/**

## Features

- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support
- **Document Conversion**: Convert PDF, Word, PowerPoint, Excel files
- **Web Content**: Convert HTML and web pages to Markdown
- **Data Formats**: Support for CSV, JSON, XML conversion
- **Live Preview**: See a preview of your converted Markdown before downloading
- **Modern UI**: Clean, responsive interface built with Tailwind CSS
- **Error Handling**: Comprehensive error reporting and validation
- **File Management**: Automatic cleanup of temporary files

## Supported File Formats

- **Documents**: PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS
- **Web**: HTML, HTM
- **Data**: CSV, JSON, XML
- **Text**: TXT, MD

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tomorrow56/markitdown-webui.git
   cd markitdown-webui
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5001`

## Usage

1. **Upload a file**: Drag and drop a file onto the upload area or click "Browse Files"
2. **Wait for conversion**: The file will be automatically converted to Markdown
3. **Preview the result**: See a preview of the converted content
4. **Download**: Click "Download Markdown" to save the converted file

## Configuration

- **Maximum file size**: 50MB (configurable in `app.py`)
- **Supported formats**: Defined in `ALLOWED_EXTENSIONS` in `app.py`
- **Cleanup interval**: Files older than 1 hour are automatically deleted
- **Port**: Application runs on port 5001

## Requirements

- Python 3.10 or higher
- MarkItDown library with all dependencies
- Flask web framework

## API Endpoints

- `GET /`: Main web interface
- `POST /convert`: Convert uploaded file to Markdown
- `GET /download/<filename>`: Download converted file
- `POST /cleanup`: Clean up old temporary files

## Error Handling

The application includes comprehensive error handling for:
- Invalid file formats
- File size limits
- Conversion failures
- Network errors
- File system errors

## Security Features

- File type validation
- Secure filename handling
- Automatic cleanup of temporary files
- File size limits
- Input sanitization

## Troubleshooting

### PDF Conversion Issues
If you encounter PDF conversion errors:
1. Ensure all dependencies are installed: `pip install -r requirements.txt`
2. Try reinstalling MarkItDown: `pip uninstall markitdown -y && pip install 'markitdown[all]'`
3. Check that pdfminer-six is properly installed

### Port Already in Use
If port 5001 is already in use:
```bash
# Kill existing process
lsof -ti:5001 | xargs kill -9
# Or change port in app.py
```

## License

This project is built using Microsoft's MarkItDown library. Please refer to the original MarkItDown license for usage terms.

## Contributing

Feel free to submit issues and enhancement requests!
