from typing import Dict, List, Optional
from utils.embeddings import embedding_service
from config.llm_config import llm_config
import openai

class RAGService:
    """Service for Retrieval-Augmented Generation (RAG)"""
    
    def __init__(self):
        self.openai_client = openai.OpenAI(api_key=llm_config.openai_api_key)
    
    def ask_question(self, question: str, pdf_id: Optional[int] = None) -> Dict:
        """
        Answer a question using RAG with PDF content
        
        Args:
            question: User question
            pdf_id: Optional PDF ID to search within
            
        Returns:
            Dictionary with answer and citations
        """
        try:
            # Get relevant content with citations
            content_with_citations = embedding_service.get_content_with_citations(question, pdf_id)
            
            # Prepare context for LLM
            context = content_with_citations['content']
            citations = content_with_citations['citations']
            
            # Generate answer using LLM
            answer = self._generate_answer(question, context)
            
            # Format citations
            formatted_citations = self._format_citations(citations)
            
            return {
                'question': question,
                'answer': answer,
                'citations': formatted_citations,
                'context_used': context[:500] + '...' if len(context) > 500 else context
            }
            
        except Exception as e:
            return {
                'question': question,
                'answer': f"I apologize, but I encountered an error while processing your question: {str(e)}",
                'citations': [],
                'context_used': ""
            }
    
    def _generate_answer(self, question: str, context: str) -> str:
        """Generate answer using LLM with provided context"""
        try:
            prompt = llm_config.rag_prompt.format(
                question=question,
                context=context
            )
            
            response = self.openai_client.chat.completions.create(
                model=llm_config.openai_model,
                messages=[
                    {"role": "system", "content": "You are a helpful teaching assistant. Answer questions based on the provided context and include proper citations."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,  # Lower temperature for more factual answers
                max_tokens=1000
            )
            
            answer = response.choices[0].message.content.strip()
            
            # Ensure citations are included
            citations = self._extract_citations_from_context(context)
            if "According to" not in answer and citations:
                answer += f"\n\n{citations}"
            
            return answer
            
        except Exception as e:
            return f"I apologize, but I couldn't generate an answer to your question. Error: {str(e)}"
    
    def _format_citations(self, citations: List[Dict]) -> str:
        """Format citations for display"""
        if not citations:
            return ""
        
        citation_text = "Sources:\n"
        for citation in citations:
            citation_text += f"- Page {citation['page_number']}: {citation['snippet']}\n"
        
        return citation_text.strip()
    
    def _extract_citations_from_context(self, context: str) -> str:
        """Extract potential citations from context"""
        # Simple extraction - in production, this would be more sophisticated
        lines = context.split('\n')
        citations = []
        
        for line in lines[:5]:  # Check first 5 lines
            if len(line.strip()) > 20:  # Reasonable length for citation
                citations.append(line.strip())
        
        if citations:
            return "Relevant information found in the text: " + "; ".join(citations[:2])
        
        return ""
    
    def get_similar_topics(self, query: str, pdf_id: Optional[int] = None, top_k: int = 5) -> List[Dict]:
        """
        Find similar topics or content in the PDF
        
        Args:
            query: Search query
            pdf_id: Optional PDF ID to search within
            top_k: Number of results to return
            
        Returns:
            List of similar content with metadata
        """
        try:
            results = embedding_service.search_similar_content(query, pdf_id, top_k)
            
            # Format results for topic similarity
            similar_topics = []
            for result in results:
                similar_topics.append({
                    'content': result['content'][:200] + '...' if len(result['content']) > 200 else result['content'],
                    'page_number': result['page_number'],
                    'relevance_score': result['score'],
                    'full_content': result['content']
                })
            
            return similar_topics
            
        except Exception as e:
            print(f"Error finding similar topics: {e}")
            return []
    
    def explain_concept(self, concept: str, pdf_id: Optional[int] = None) -> Dict:
        """
        Explain a concept using the PDF content
        
        Args:
            concept: Concept to explain
            pdf_id: Optional PDF ID to search within
            
        Returns:
            Dictionary with explanation and examples
        """
        try:
            # Search for relevant content about the concept
            similar_content = self.get_similar_topics(concept, pdf_id, top_k=3)
            
            if not similar_content:
                return {
                    'concept': concept,
                    'explanation': f"I couldn't find specific information about '{concept}' in the available content.",
                    'examples': [],
                    'related_topics': []
                }
            
            # Combine content for explanation
            combined_content = " ".join([item['full_content'] for item in similar_content])
            
            # Generate explanation
            explanation_prompt = f"""
            Based on the following content, explain the concept of '{concept}' in simple terms.
            Provide a clear explanation and 2-3 examples if possible.
            
            Content:
            {combined_content}
            
            Please provide:
            1. A simple definition of {concept}
            2. 2-3 examples or applications
            3. Any important related concepts
            """
            
            response = self.openai_client.chat.completions.create(
                model=llm_config.openai_model,
                messages=[
                    {"role": "system", "content": "You are an educational explainer. Provide clear, simple explanations of concepts."},
                    {"role": "user", "content": explanation_prompt}
                ],
                temperature=0.4,
                max_tokens=800
            )
            
            explanation = response.choices[0].message.content.strip()
            
            # Extract related topics
            related_topics = [item['content'][:100] for item in similar_content[:2]]
            
            return {
                'concept': concept,
                'explanation': explanation,
                'examples': self._extract_examples(explanation),
                'related_topics': related_topics,
                'source_pages': [item['page_number'] for item in similar_content]
            }
            
        except Exception as e:
            return {
                'concept': concept,
                'explanation': f"I apologize, but I couldn't generate an explanation for '{concept}'. Error: {str(e)}",
                'examples': [],
                'related_topics': []
            }
    
    def _extract_examples(self, explanation: str) -> List[str]:
        """Extract examples from explanation text"""
        examples = []
        lines = explanation.split('\n')
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ['example:', 'for example:', 'instance:', 'such as:']):
                examples.append(line.strip())
        
        return examples[:3]  # Return up to 3 examples

# Global RAG service instance
rag_service = RAGService()