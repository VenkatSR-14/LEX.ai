from .base_parser import DocumentParser
import PyPDF2

class PDFParser(DocumentParser):
    def parse(self, file_path: str) -> str:
        text = ""
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text()
        return text
    