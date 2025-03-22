import os
import uuid
from typing import List, Dict, Any
import PyPDF2
import docx
from langchain_openai import OpenAI, OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

class DocumentProcessor:
    def __init__(self):
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set.")
        os.environ["OPENAI_API_KEY"] = self.openai_api_key
        
        # Initialize LangChain components
        self.llm = OpenAI(temperature=0.2)  # Lower temperature for more deterministic results
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=200
        )

    def analyze_document(self, file_path: str) -> Dict[str, Any]:
        """Analyze document content and extract structure using AI"""
        # Extract text from document
        content = self._extract_text(file_path)
        
        # Split text into chunks for processing
        chunks = self.text_splitter.split_text(content)
        
        # Create vector store from chunks
        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        retriever = vectorstore.as_retriever()
        
        # Create QA chain for document analysis
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        # Extract chapters and structure
        chapters = self._extract_chapters(qa_chain, content)
        
        # Extract document metadata
        metadata = self._extract_metadata(qa_chain, content)
        
        return {
            "content_length": len(content),
            "potential_chapters": chapters,
            "metadata": metadata
        }
    
    def analyze_chapter(self, content: str, document_type: str = "textbook") -> Dict[str, Any]:
        """Analyze a chapter's content and extract key information using AI"""
        # Split chapter content into chunks
        chunks = self.text_splitter.split_text(content)
        
        # Create vector store from chunks
        vectorstore = FAISS.from_texts(chunks, self.embeddings)
        retriever = vectorstore.as_retriever()
        
        # Create QA chain for chapter analysis
        qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=retriever
        )
        
        # Extract key concepts
        key_concepts = self._extract_key_concepts(qa_chain)
        
        # Extract main topics
        topics = self._extract_topics(qa_chain)
        
        # Generate summary if it's a textbook
        summary = ""
        if document_type == "textbook":
            summary = self._generate_summary(qa_chain)
        
        return {
            "key_concepts": key_concepts,
            "topics": topics,
            "summary": summary
        }
    
    def match_syllabus_to_chapters(self, textbook_chapters: List[Dict[str, Any]], 
                                   syllabus_topics: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Match syllabus topics to textbook chapters using AI"""
        matches = []
        
        # Create prompt template for matching
        match_prompt = PromptTemplate(
            input_variables=["topic", "chapter"],
            template="""
            On a scale of 0 to 1, how well does the textbook chapter match the syllabus topic?
            
            Syllabus Topic: {topic}
            Textbook Chapter: {chapter}
            
            Provide only a number between 0 and 1 as your answer, where 1 means perfect match and 0 means no match.
            """
        )
        
        for topic in syllabus_topics:
            topic_text = topic.get("title", "")
            best_match = None
            best_score = 0
            
            for chapter in textbook_chapters:
                chapter_title = chapter.get("title", "")
                
                # Use LLM to calculate similarity score
                match_chain = match_prompt | self.llm
                response = match_chain.invoke({"topic": topic_text, "chapter": chapter_title})
                
                try:
                    # Check response type and extract content appropriately
                    if isinstance(response, dict):
                        # Extract the text content from the dictionary
                        response_text = response.get('text', '')
                        if not response_text:
                            # Try other common keys if 'text' is not present
                            response_text = str(response.get('content', str(response)))
                    else:
                        response_text = str(response)
                        
                    # Now use strip() on the string
                    score = float(response_text.strip())
                    if score > best_score and score > 0.6:
                        best_score = score
                        best_match = chapter
                except ValueError:
                    # If response is not a valid float, skip this match
                    continue
                        
            if best_match:
                matches.append({
                    "syllabus_topic": topic,
                    "textbook_chapter": best_match,
                    "confidence": best_score
                })
        
        return matches
    
    def _extract_text(self, file_path: str) -> str:
        """Extract text from various document formats"""
        file_extension = os.path.splitext(file_path)[1].lower()
        
        if file_extension == '.pdf':
            return self._extract_from_pdf(file_path)
        elif file_extension in ['.docx', '.doc']:
            return self._extract_from_docx(file_path)
        elif file_extension == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                return file.read()
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file"""
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text
    
    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file"""
        doc = docx.Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        return text
    
    def _extract_chapters(self, qa_chain: RetrievalQA, content: str) -> List[Dict[str, Any]]:
        """Extract chapters from document using AI"""
        # Create prompt for chapter extraction
        query = """
        Analyze this document and identify all chapters or major sections.
        For each chapter, provide:
        1. The chapter number (if available)
        2. The chapter title
        3. The approximate position in the document (beginning, middle, or end)
        
        Format your response as a numbered list with each chapter on a new line.
        """
        
        response = qa_chain.invoke({"query": query})
        print(response)
        # Process the response to extract chapters
        chapters = []

# Handle response based on its type
        if isinstance(response, dict):
            # Extract text from the dictionary based on its structure
            response_text = response.get('result', '')
            if not response_text:
                # Try other common keys if 'result' is not present
                response_text = response.get('answer', '')
            if not response_text:
                # If still not found, convert the whole dict to string
                response_text = str(response)
        else:
            response_text = str(response)

        lines = response_text.strip().split('\n')
        
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue
                
            # Try to extract chapter information
            try:
                # Remove numbering if present
                if '. ' in line:
                    line = line.split('. ', 1)[1]
                
                # Extract chapter number and title
                if ':' in line:
                    parts = line.split(':', 1)
                    title_parts = parts[0].split()
                    
                    if len(title_parts) >= 2 and title_parts[0].lower() in ['chapter', 'unit', 'section']:
                        number = title_parts[1]
                        title = parts[1].strip()
                    else:
                        number = ""
                        title = line.strip()
                else:
                    number = ""
                    title = line.strip()
                
                # Create chapter entry
                chapter = {
                    "id": str(uuid.uuid4()),
                    "number": number,
                    "title": title,
                    "start_position": content.find(title) if title in content else 0,
                }
                
                chapters.append(chapter)
            except Exception as e:
                # Skip problematic lines
                continue
        
        # Sort chapters by position in document
        chapters.sort(key=lambda x: x['start_position'])
        
        # Calculate chapter boundaries
        for i in range(len(chapters) - 1):
            start = chapters[i]['start_position']
            end = chapters[i+1]['start_position']
            chapters[i]['content_range'] = (start, end)
            chapters[i]['estimated_pages'] = self._estimate_pages(end - start)
        
        # Handle the last chapter
        if chapters:
            start = chapters[-1]['start_position']
            chapters[-1]['content_range'] = (start, len(content))
            chapters[-1]['estimated_pages'] = self._estimate_pages(len(content) - start)
        
        return chapters
    
    def _extract_metadata(self, qa_chain: RetrievalQA, content: str) -> Dict[str, str]:
        """Extract metadata from document using AI"""
        query = """
        Extract the following metadata from this document:
        1. Title
        2. Author(s)
        3. Publication date (if available)
        4. Subject or field
        5. Keywords or main topics
        
        Format your response as key-value pairs, one per line.
        """
        
        response = qa_chain.invoke({"query": query})
        
        # Process the response to extract metadata
        metadata = {}
        
        # Handle response based on its type
        if isinstance(response, dict):
            # Extract text from the dictionary based on its structure
            response_text = response.get('result', '')
            if not response_text:
                # Try other common keys if 'result' is not present
                response_text = response.get('answer', '')
                if not response_text:
                    # If still not found, convert the whole dict to string
                    response_text = str(response)
        else:
            response_text = str(response)
        
        lines = response_text.strip().split('\n')
        
        for line in lines:
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip()
        
        return metadata

    
    def _extract_key_concepts(self, qa_chain: RetrievalQA) -> List[str]:
        """Extract key concepts from chapter using AI"""
        query = """
        What are the 5-10 most important concepts or terms in this chapter?
        List each concept on a new line without numbering or bullet points.
        """
        
        response = qa_chain.invoke({"query": query})
        
        # Handle response based on its type
        if isinstance(response, dict):
            # Extract text from the dictionary based on its structure
            response_text = response.get('result', '')
            if not response_text:
                # Try other common keys if 'result' is not present
                response_text = response.get('answer', '')
                if not response_text:
                    # If still not found, convert the whole dict to string
                    response_text = str(response)
        else:
            response_text = str(response)
        
        # Process the response to extract concepts
        concepts = []
        for line in response_text.strip().split('\n'):
            concept = line.strip()
            if concept and not concept.isdigit():
                concepts.append(concept)
        
        return concepts[:10]  # Limit to top 10

    
    def _extract_topics(self, qa_chain: RetrievalQA) -> List[str]:
        """Extract main topics from chapter using AI"""
        query = """
        What are the main topics or sections covered in this chapter?
        List each topic on a new line without numbering or bullet points.
        """
        
        response = qa_chain.invoke({"query": query})
        
        # Handle response based on its type
        if isinstance(response, dict):
            response_text = response.get('result', '')
            if not response_text:
                response_text = response.get('answer', '')
                if not response_text:
                    response_text = str(response)
        else:
            response_text = str(response)
        
        # Process the response to extract topics
        topics = []
        for line in response_text.strip().split('\n'):
            topic = line.strip()
            if topic and not topic.isdigit():
                topics.append(topic)
        
        return topics[:15]  # Limit to top 15

    def _generate_summary(self, qa_chain: RetrievalQA) -> str:
        """Generate a summary of the chapter using AI"""
        query = """
        Provide a concise summary of this chapter in 3-5 sentences.
        Focus on the main points and key takeaways.
        """
        
        response = qa_chain.invoke({"query": query})
        
        # Handle response based on its type
        if isinstance(response, dict):
            summary = response.get('result', '')
            if not summary:
                summary = response.get('answer', '')
                if not summary:
                    summary = str(response)
        else:
            summary = str(response)
        
        return summary.strip()
    
    def _estimate_pages(self, char_count: int) -> int:
        """Estimate page count based on character count"""
        # Rough estimation: assume 3000 characters per page
        return max(1, char_count // 3000)
