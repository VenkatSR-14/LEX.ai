from abc import ABC, abstractmethod

class IDocumentService(ABC):
    @abstractmethod
    def retrieve_list_of_contents(self, document_id, document_type):
        pass

    @abstractmethod
    def parse_pdf(self, file_path: str):
        pass

    @abstractmethod
    def parse_word_doc(self, file_path: str):
        pass

    @abstractmethod
    def parse_text_file(self, file_path: str):
        pass

    @abstractmethod
    def upload_document(self, file_path: str, file_type: str):
        pass