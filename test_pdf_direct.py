#!/usr/bin/env python3

from markitdown import MarkItDown
import tempfile
import os

def test_pdf_conversion():
    try:
        # Create a simple PDF content test
        md = MarkItDown()
        print("MarkItDown initialized successfully")
        
        # Check if PDF converter is available
        converters = md._converters
        print(f"Available converters: {[type(c).__name__ for c in converters]}")
        
        # Test PDF dependency
        from markitdown._markitdown import PdfConverter
        print("PDF converter import successful")
        
        return True
    except ImportError as e:
        print(f"PDF converter import failed: {e}")
        return False
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_conversion()
    print(f"Test {'passed' if success else 'failed'}")
