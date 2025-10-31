#!/usr/bin/env python3

from markitdown import MarkItDown
import sys
import tempfile
import os

def test_markitdown():
    try:
        md = MarkItDown()
        print("MarkItDown initialized successfully")
        
        # Test with a simple text file first
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            f.write("Hello World\nThis is a test document.")
            temp_file = f.name
        
        try:
            result = md.convert(temp_file)
            print("File conversion test passed")
            print(f"Result: {result.text_content}")
            return True
        finally:
            os.unlink(temp_file)
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_markitdown()
    sys.exit(0 if success else 1)
