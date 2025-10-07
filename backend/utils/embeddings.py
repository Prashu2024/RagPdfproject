import os
import uuid
from typing import List, Dict, Optional
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document # Import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from config.settings import settings
from config.llm_config import llm_config

class EmbeddingService:
    """Service for generating and managing embeddings with ChromaDB"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=llm_config.openai_api_key,
            model="text-embedding-ada-002"
        )
        self.persist_directory = settings.chroma_persist_directory
        self.vector_store = None
        self._initialize_vector_store()
    
    def _initialize_vector_store(self):
        """Initialize ChromaDB vector store"""
        try:
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
        except Exception as e:
            print(f"Warning: Could not initialize ChromaDB: {e}")
            print("Will create new vector store when needed")
    
    def create_embeddings_for_chunks(self, chunks: List[Dict]) -> List[str]:
        """
        Create embeddings for text chunks
        
        Args:
            chunks: List of dictionaries containing chunk data
            
        Returns:
            List of embedding IDs
        """
        if not chunks:
            return []
        
        try:
            # Extract texts for embedding
            texts = [chunk['chunk_text'] for chunk in chunks]
            
            # Generate embeddings
            embeddings = self.embeddings.embed_documents(texts)
            
            # Create embedding IDs
            embedding_ids = [str(uuid.uuid4()) for _ in embeddings]
            
            return embedding_ids
            
        except Exception as e:
            raise Exception(f"Error creating embeddings: {str(e)}")
    
    def store_embeddings(self, chunks: List[Dict], embedding_ids: List[str], pdf_id: int):
        """
        Store embeddings in ChromaDB
        
        Args:
            chunks: List of chunk data
            embedding_ids: List of corresponding embedding IDs
            pdf_id: PDF ID for metadata
        """
        if not chunks or not embedding_ids:
            return
        
        try:
            # Prepare documents for ChromaDB
            documents = []
            metadatas = []
            ids = []
            
            for chunk, embedding_id in zip(chunks, embedding_ids):
                # Create a Document object for each chunk
                doc = Document(
                    page_content=chunk['chunk_text'],
                    metadata={
                        'pdf_id': pdf_id,
                        'page_number': chunk['page_number'],
                        'chunk_order': chunk['chunk_order']
                    }
                )
                documents.append(doc)
                ids.append(embedding_id)
            
            # Add to vector store
            self.vector_store.add_documents(
                documents=documents,
                ids=ids
            )
            
            print(f"Stored {len(documents)} embeddings for PDF {pdf_id}")
            
        except Exception as e:
            raise Exception(f"Error storing embeddings: {str(e)}")
    
    def search_similar_content(self, query: str, pdf_id: Optional[int] = None, top_k: int = 5) -> List[Dict]:
        """
        Search for similar content using vector similarity
        
        Args:
            query: Search query
            pdf_id: Optional PDF ID to filter results
            top_k: Number of results to return
            
        Returns:
            List of similar content with metadata
        """
        try:
            # Build filter if PDF ID is specified
            filter_dict = None
            if pdf_id is not None:
                filter_dict = {"pdf_id": pdf_id}
            
            # Perform similarity search
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=top_k,
                filter=filter_dict
            )
            
            # Format results
            formatted_results = []
            for doc, score in results:
                formatted_results.append({
                    'content': doc.page_content,
                    'metadata': doc.metadata,
                    'score': score,
                    'page_number': doc.metadata.get('page_number'),
                    'chunk_order': doc.metadata.get('chunk_order')
                })
            
            return formatted_results
            
        except Exception as e:
            raise Exception(f"Error searching similar content: {str(e)}")
    
    def get_content_with_citations(self, query: str, pdf_id: Optional[int] = None) -> Dict:
        """
        Get relevant content with proper citations
        
        Args:
            query: Search query
            pdf_id: Optional PDF ID to filter results
            
        Returns:
            Dictionary with content and citations
        """
        try:
            # Search for similar content
            results = self.search_similar_content(query, pdf_id, top_k=3)
            
            if not results:
                return {
                    'content': "No relevant content found.",
                    'citations': []
                }
            
            # Group content by page for better citations
            pages_content = {}
            for result in results:
                page_num = result['page_number']
                if page_num not in pages_content:
                    pages_content[page_num] = []
                pages_content[page_num].append(result['content'])
            
            # Create citations
            citations = []
            for page_num, contents in pages_content.items():
                # Take first few lines as snippet
                snippet = ' '.join(contents[:2])
                if len(snippet) > 200:
                    snippet = snippet[:200] + '...'
                
                citations.append({
                    'page_number': page_num,
                    'snippet': snippet
                })
            
            # Combine all content
            combined_content = ' '.join([result['content'] for result in results])
            
            return {
                'content': combined_content,
                'citations': citations
            }
            
        except Exception as e:
            raise Exception(f"Error getting content with citations: {str(e)}")
    
    def delete_pdf_embeddings(self, pdf_id: int):
        """
        Delete all embeddings for a specific PDF
        
        Args:
            pdf_id: PDF ID to delete embeddings for
        """
        try:
            # Get all embeddings for this PDF
            results = self.vector_store.get(
                where={"pdf_id": pdf_id}
            )
            
            if results['ids']:
                # Delete embeddings
                self.vector_store.delete(ids=results['ids'])
                print(f"Deleted {len(results['ids'])} embeddings for PDF {pdf_id}")
            
        except Exception as e:
            print(f"Warning: Could not delete embeddings for PDF {pdf_id}: {e}")
    
    def get_collection_stats(self) -> Dict:
        """
        Get statistics about the vector store
        
        Returns:
            Dictionary with collection statistics
        """
        try:
            # Get all documents
            all_docs = self.vector_store.get()
            
            # Group by PDF
            pdf_counts = {}
            for metadata in all_docs['metadatas']:
                pdf_id = metadata.get('pdf_id', 'unknown')
                pdf_counts[pdf_id] = pdf_counts.get(pdf_id, 0) + 1
            
            return {
                'total_documents': len(all_docs['ids']),
                'unique_pdfs': len(pdf_counts),
                'pdf_document_counts': pdf_counts
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'total_documents': 0,
                'unique_pdfs': 0
            }

# Global embedding service instance
embedding_service = EmbeddingService()
