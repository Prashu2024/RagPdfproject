from .settings import settings

class LLMConfig:
    """Configuration for LLM services"""
    
    # OpenAI Configuration
    openai_api_key = settings.openai_api_key
    openai_model = "gpt-3.5-turbo"  # or "gpt-4"
    openai_temperature = 0.7
    openai_max_tokens = 2000
    
    # Google Gemini Configuration
    google_api_key = settings.google_api_key
    google_model = "gemini-pro"
    
    # Quiz Generation Prompts
    quiz_generation_prompt = """
    You are an educational quiz generator. Based on the provided text content, generate {question_type} questions.
    
    Content:
    {content}
    
    Requirements:
    - Generate {num_questions} questions
    - For MCQ: Provide 4 options with 1 correct answer
    - For SAQ: Provide 2-3 sentence answers
    - For LAQ: Provide detailed answers (5-7 sentences)
    - Include difficulty level (Easy/Medium/Hard)
    - Provide explanations for each answer
    
    Format the response as JSON:
    {{
        "questions": [
            {{
                "question": "Question text",
                "type": "MCQ/SAQ/LAQ",
                "difficulty": "Easy/Medium/Hard",
                "options": ["option1", "option2", "option3", "option4"], // Only for MCQ
                "correct_answer": "Correct answer",
                "explanation": "Explanation of the answer"
            }}
        ]
    }}
    """
    
    # RAG Prompt
    rag_prompt = """
    You are a helpful teaching assistant. Answer the user's question based on the provided context.
    
    Question: {question}
    
    Context:
    {context}
    
    Guidelines:
    - Provide accurate information based on the context
    - Include page citations when referencing specific information
    - Format citations as: "According to p. [page]: '[quote]'"
    - Keep the answer educational and student-friendly
    - If the context doesn't contain the answer, say so clearly
    
    Answer:
    """
    
    # YouTube Recommendation Prompt
    youtube_recommendation_prompt = """
    You are an educational content recommender. Based on the provided topic and content, suggest relevant YouTube videos.
    
    Topic: {topic}
    Content Summary: {content}
    
    Requirements:
    - Suggest 3-5 relevant educational videos
    - Focus on reputable educational channels
    - Include video titles, channel names, and brief descriptions
    - Explain why each video is relevant to the topic
    
    Format as JSON:
    {{
        "recommendations": [
            {{
                "title": "Video title",
                "channel": "Channel name",
                "url": "https://youtube.com/watch?v=...",
                "description": "Why this video is relevant"
            }}
        ]
    }}
    """

llm_config = LLMConfig()