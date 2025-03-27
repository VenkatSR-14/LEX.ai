from .base_parser import DocumentParser

class TextParser(DocumentParser):
    def parse(self, file_path: str) -> str:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return text
