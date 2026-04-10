import os
import PyPDF2

def read_pdfs():
    notas_dir = os.path.join(os.getcwd(), 'NOTAS')
    for file in os.listdir(notas_dir):
        if not file.endswith('.pdf'): continue
        
        path = os.path.join(notas_dir, file)
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
                
            print(f"--- Extracted from {file} ---")
            print(text[:1000]) # First 1000 chars to see format
            print("-" * 50)
            break

if __name__ == "__main__":
    read_pdfs()
