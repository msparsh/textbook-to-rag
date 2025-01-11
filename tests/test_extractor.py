import pytest
from unittest.mock import patch, MagicMock
from extractor import Extractor

class TestExtractor:

    @patch("fitz.open")
    @patch.object(Extractor, '_write_out')
    def test_extract_text_from_pdf_success(self, mock_write_out, mock_fitz_open):
        extractor = Extractor()
        pdf_path = "sample.pdf"
        output_text_path = "out/textfile.txt"
        
        # Mocking the PDF content
        mock_pdf = MagicMock()
        mock_pdf.__enter__.return_value = mock_pdf
        mock_pdf.__len__.return_value = 2  # Two pages
        mock_pdf.load_page.return_value.get_text.return_value = "Page text\n"

        mock_fitz_open.return_value = mock_pdf

        extractor.extract_text_from_pdf(pdf_path, output_text_path)

        mock_fitz_open.assert_called_once_with(pdf_path)
        assert mock_pdf.load_page.call_count == 2
        mock_write_out.assert_called_once()
