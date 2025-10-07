import fitz  # PyMuPDF
import os
import re
from typing import List, Dict, Tuple
from models.pdf_model import TextChunk
from schemas.pdf_schema import TextChunkCreate

class PDFProcessor:
    """Handles PDF text extraction and chunking"""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Extract text from PDF with page information
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            List of dictionaries containing text and page info
        """
        try:
            doc = fitz.open(pdf_path)
            pages_data = []
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                text = page.get_text()
                
                # Clean up text
                text = self._clean_text(text)
                
                pages_data.append({
                    'page_number': page_num + 1,
                    'text': text,
                    'word_count': len(text.split())
                })
            
            doc.close()
            return pages_data
            
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")
    
    def chunk_text(self, pages_data: List[Dict]) -> List[TextChunkCreate]:
        """
        Chunk extracted text into manageable pieces
        
        Args:
            pages_data: List of page data from PDF extraction
            
        Returns:
            List of TextChunkCreate objects
        """
        chunks = []
        chunk_order = 0
        
        for page_data in pages_data:
            page_text = page_data['text']
            page_number = page_data['page_number']
            
            # Split text into sentences for better chunking
            sentences = self._split_into_sentences(page_text)
            
            # Create chunks from sentences
            current_chunk = ""
            current_sentence_count = 0
            
            for sentence in sentences:
                # Check if adding this sentence would exceed chunk size
                if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                    # Save current chunk
                    chunks.append(TextChunkCreate(
                        pdf_id=0,  # Will be set when creating actual chunks
                        chunk_text=current_chunk.strip(),
                        page_number=page_number,
                        chunk_order=chunk_order
                    ))
                    chunk_order += 1
                    
                    # Start new chunk with overlap
                    overlap_sentences = sentences[max(0, current_sentence_count - 3):current_sentence_count]
                    current_chunk = " ".join(overlap_sentences) + " " + sentence
                    current_sentence_count = len(overlap_sentences) + 1
                else:
                    current_chunk += sentence + " "
                    current_sentence_count += 1
            
            # Add the last chunk if it has content
            if current_chunk.strip():
                chunks.append(TextChunkCreate(
                    pdf_id=0,  # Will be set when creating actual chunks
                    chunk_text=current_chunk.strip(),
                    page_number=page_number,
                    chunk_order=chunk_order
                ))
                chunk_order += 1
        
        return chunks
    
    def get_pdf_info(self, pdf_path: str) -> Dict:
        """
        Get basic information about the PDF
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with PDF information
        """
        try:
            doc = fitz.open(pdf_path)
            file_size = os.path.getsize(pdf_path)
            
            info = {
                'page_count': len(doc),
                'file_size': file_size,
                'filename': os.path.basename(pdf_path)
            }
            
            doc.close()
            return info
            
        except Exception as e:
            raise Exception(f"Error getting PDF info: {str(e)}")
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize extracted text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters that might cause issues
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)\[\]\{\}\"\'\/\@\#\$\%\^\&\*\+\=\~\`]', '', text)
        return text.strip()
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        # Simple sentence splitting based on punctuation
        sentences = re.split(r'(?<=[.!?])\s+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def process_pdf(self, pdf_path: str, pdf_id: int) -> Tuple[List[TextChunkCreate], Dict]:
        """
        Complete PDF processing pipeline
        
        Args:
            pdf_path: Path to the PDF file
            pdf_id: Database ID of the PDF
            
        Returns:
            Tuple of (chunks, pdf_info)
        """
        # Get PDF info
        pdf_info = self.get_pdf_info(pdf_path)
        
        # Extract text
        pages_data = self.extract_text_from_pdf(pdf_path)
        
        # Create chunks
        chunks = self.chunk_text(pages_data)
        
        # Update PDF IDs in chunks
        for chunk in chunks:
            chunk.pdf_id = pdf_id
        
        return chunks, pdf_info