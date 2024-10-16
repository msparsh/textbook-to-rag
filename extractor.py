import re
import fitz  # ie pymupdf
from PyPDF2 import PdfReader


class Extractor:

    def write_out(self, text, out_file_path):
        with open(out_file_path, 'w+') as text_file:
            text_file.write(text)
        print(f"Text extracted and saved to {out_file_path}")

    def extract_text_from_pdf(self, pdf_path, output_text_path):
        with fitz.open(pdf_path) as pdf:
            text = ''
            for page_num in range(len(pdf)):
                page = pdf.load_page(page_num)
                text += page.get_text()
        self.write_out(text, output_text_path)

    def extract_text(self, file_name, output_text_path):
        with open(file_name, 'rb') as file:
            reader = PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        # text = re.sub(r"\n", "\n\n", text)
        self.write_out(text, output_text_path)

    def extract_text_alternative(self, pdf_path, output_text_path):
        reader = PdfReader(pdf_path)
        text_content = []

        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text = page.extract_text()
            if text:
                text_content.append(text)

        text = "\n".join(text_content)
        self.write_out(text, output_text_path)


if __name__ == "__main__":
    file_name = "Introduction to Computation and Programming Using Python by John V. Guttag (z-lib.org).pdf"

    extractor = Extractor()
    extractor.extract_text_from_pdf(file_name, "out/textfile.txt")
