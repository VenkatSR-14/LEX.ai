import docx
from .base_parser import DocumentParser

class WordParser(DocumentParser):
    def parse(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text

