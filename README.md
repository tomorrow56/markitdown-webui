# MarkItDown Web UI

A modern web interface for Microsoft's MarkItDown document conversion tool.

## Features

- **Drag & Drop Upload**: Intuitive file upload with drag-and-drop support
- **Multiple Format Support**: Convert PDF, Word, PowerPoint, Excel, Images, Audio, HTML, and more
- **Live Preview**: See a preview of your converted Markdown before downloading
- **Modern UI**: Clean, responsive interface built with Tailwind CSS
- **Error Handling**: Comprehensive error reporting and validation
- **File Management**: Automatic cleanup of temporary files

## Supported File Formats

- **Documents**: PDF, DOCX, DOC, PPTX, PPT, XLSX, XLS
- **Images**: JPG, JPEG, PNG, GIF, BMP, TIFF, WebP (with OCR)
- **Audio**: WAV, MP3 (with transcription)
- **Web**: HTML, HTM
- **Data**: CSV, JSON, XML
- **Archives**: ZIP (iterates over contents)
- **Books**: EPUB
- **Text**: TXT, MD

## Local Installation

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

## Vercel Deployment

### Option 1: Using Vercel CLI

1. Install Vercel CLI:
   ```bash
   npm i -g vercel
   ```

2. Deploy to Vercel:
   ```bash
   vercel
   ```

3. Follow the prompts to deploy your application

### Option 2: Using GitHub Integration

1. Push your code to GitHub
2. Connect your repository to [Vercel](https://vercel.com)
3. Vercel will automatically deploy your application

### Deployment Notes

- The application automatically detects Vercel environment
- Files are stored in `/tmp/uploads` on Vercel (serverless limitation)
- Maximum file size: 50MB
- Function timeout: 30 seconds
- Some large documents may timeout due to Vercel's limitations

## Configuration

- **Maximum file size**: 50MB (configurable in `app.py`)
- **Supported formats**: Defined in `ALLOWED_EXTENSIONS` in `app.py`
- **Cleanup interval**: Files older than 1 hour are automatically deleted

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

## Limitations

- **Vercel**: 30-second function timeout may limit large document processing
- **File Storage**: Temporary files only (serverless limitation)
- **Memory Usage**: Large files may exceed serverless memory limits

## License

This project is built using Microsoft's MarkItDown library. Please refer to the original MarkItDown license for usage terms.

## Contributing

Feel free to submit issues and enhancement requests!
