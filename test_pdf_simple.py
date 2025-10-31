#!/usr/bin/env python3

import tempfile
import os
from markitdown import MarkItDown

def test_pdf_with_real_file():
    try:
        # Create a simple test PDF content
        test_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF"
        
        # Create temporary PDF file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as f:
            f.write(test_content)
            temp_pdf = f.name
        
        try:
            # Test MarkItDown conversion
            md = MarkItDown(enable_plugins=False)
            print("MarkItDown initialized successfully")
            
            result = md.convert(temp_pdf)
            print("PDF conversion successful!")
            print(f"Result: {result.text_content}")
            
            return True
        finally:
            os.unlink(temp_pdf)
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pdf_with_real_file()
    print(f"Test {'passed' if success else 'failed'}")
