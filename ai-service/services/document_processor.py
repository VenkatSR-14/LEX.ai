from fastapi import FastAPI, APIRouter, UploadFile, File
import PyPDF2
from PyPDF2 import PdfReader, PdfFileReader
from Interfaces import IDocumentService
from models import Document, Topic

"""
The Document service behaves as a one stop solution
to process the document entities
"""
class DocumentService(IDocumentService):

    def retrieve_list_of_contents(self, current_document: Document):
        file_path = current_document.file_path
        

    @abstractmethod
    def parse_pdf(self, file_path):
        pass

    @abstractmethod
    def parse_word_doc(self, file_path):
        pass

    @abstractmethod
    def parse_text_file(self, file_path):
        pass
