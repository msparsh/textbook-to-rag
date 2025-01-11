import os
import fitz  # PyMuPDF

class Extractor:

    def _write_out(self, text, out_file_path):
        os.makedirs(os.path.dirname(out_file_path), exist_ok=True)
        
        try:
            with open(out_file_path, 'w+', encoding='utf-8') as text_file:
                text_file.write(text)
            print(f"Text extracted and saved to {out_file_path}")
        except IOError as e:
            raise RuntimeError(f"An error occurred while writing to the file: {e}")

    def extract_text_from_pdf(self, pdf_path, output_text_path):
        try:
            with fitz.open(pdf_path) as pdf:
                text = ''
                for page_num in range(len(pdf)):
                    page = pdf.load_page(page_num)
                    text += page.get_text()
            self._write_out(text, output_text_path)
        except Exception as e:
            raise RuntimeError(f"An error occurred while extracting text from the PDF: {e}")

