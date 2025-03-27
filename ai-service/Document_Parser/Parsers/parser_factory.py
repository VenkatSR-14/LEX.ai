from .base_parser import DocumentParser
from .pdf_parser import PDFParser
from .word_parser import WordParser
from .text_parser import TextParser


class DocumentParserFactory:
    @staticmethod
    def get_parser(file_type: str) -> DocumentParser:
        if file_type == "pdf":
            return PDFParser()
        elif file_type in ['docx', 'doc']:
            return WordParser()
        elif file_type in ['text', 'txt']:
            return TextParser()
        else:
            raise ValueError(f"Unsupported file type: {file_type}")
