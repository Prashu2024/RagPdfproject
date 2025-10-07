# RAG Learning Assistant Backend

A comprehensive backend for an educational RAG (Retrieval-Augmented Generation) application that helps school students revise from their coursebooks using AI-powered features.

## Features

### Must-Have Features ✅
- **PDF Upload & Processing**: Upload PDF coursebooks, extract text, and process for analysis
- **Quiz Generation**: Generate MCQs, SAQs, and LAQs from uploaded PDFs using LLMs
- **Progress Tracking**: Monitor student progress, identify strengths/weaknesses
- **RAG-based Q&A**: Answer student questions with citations from source materials

### Nice-to-Have Features ✅
- **Chat Interface**: Virtual teaching companion with RAG capabilities
- **YouTube Recommendations**: Suggest relevant educational videos
- **Analytics Dashboard**: Comprehensive learning analytics and insights

## Tech Stack

- **Backend**: FastAPI
- **Database**: PostgreSQL (metadata) + ChromaDB (vector embeddings)
- **LLM Integration**: OpenAI GPT-3.5/4, Google Gemini
- **PDF Processing**: PyMuPDF (fitz)
- **Vector Database**: ChromaDB
- **Authentication**: JWT (ready for implementation)

## Project Structure

```
backend/
├── config/                 # Configuration files
│   ├── database.py        # Database connection and models
│   ├── settings.py        # Application settings
│   └── llm_config.py      # LLM service configurations
├── models/                # SQLAlchemy database models
│   └── pdf_model.py       # User, PDF, Quiz, Progress models
├── schemas/               # Pydantic schemas for validation
│   └── pdf_schema.py      # API request/response schemas
├── routes/                # API route definitions
│   ├── pdf_routes.py      # PDF upload, management, processing
│   ├── quiz_routes.py     # Quiz generation and submission
│   ├── chat_routes.py     # RAG-based Q&A and chat
│   └── progress_routes.py # Progress tracking and analytics
├── utils/                 # Utility functions
│   ├── pdf_processor.py   # PDF text extraction and chunking
│   ├── embeddings.py      # Vector embedding generation
│   ├── quiz_generator.py  # LLM-based quiz generation
│   └── youtube_recommender.py # YouTube video recommendations
├── services/              # Business logic services
│   ├── rag_service.py     # RAG retrieval and generation
│   └── analytics_service.py # Progress analytics and insights
├── uploads/               # File upload directory
│   └── pdfs/             # Uploaded PDF files
├── chroma/               # ChromaDB vector storage
├── main.py               # FastAPI application entry point
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
└── setup.py             # Setup and initialization script
```

## Installation & Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- OpenAI API Key
- Google API Key (for YouTube recommendations)

### Quick Setup

1. **Clone and navigate to the backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and database credentials
   ```

4. **Run the setup script:**
   ```bash
   python setup.py
   ```

5. **Start the server:**
   ```bash
   python -m uvicorn main:app --reload
   ```

### Manual Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up PostgreSQL database:**
   - Create a PostgreSQL database
   - Update `DATABASE_URL` in `.env`
   - Database tables will be created automatically on first run

3. **Set up ChromaDB:**
   - ChromaDB will be initialized automatically
   - Vector embeddings will be stored in `./chroma/` directory

4. **Configure API keys:**
   - Add your OpenAI API key to `.env`
   - Add your Google API key for YouTube recommendations

## API Documentation

### Base URL
```
http://localhost:8000/api
```

### Authentication
Currently using simplified authentication (user_id = 1). For production, implement proper JWT authentication.

### Endpoints

#### PDF Management
- `POST /api/pdfs/upload` - Upload and process a PDF
- `GET /api/pdfs/` - List all uploaded PDFs
- `GET /api/pdfs/{pdf_id}` - Get PDF details
- `DELETE /api/pdfs/{pdf_id}` - Delete PDF and associated data
- `GET /api/pdfs/{pdf_id}/chunks` - Get text chunks for a PDF

#### Quiz Generation
- `POST /api/quizzes/generate` - Generate a quiz from a PDF
- `GET /api/quizzes/{quiz_id}` - Get quiz details
- `POST /api/quizzes/{quiz_id}/submit` - Submit quiz answers
- `GET /api/quizzes/user/{user_id}/attempts` - Get user quiz attempts
- `GET /api/quizzes/pdf/{pdf_id}/attempts` - Get PDF quiz attempts
- `GET /api/quizzes/statistics` - Get quiz statistics

#### RAG Chat & Q&A
- `POST /api/chat/ask` - Ask a question using RAG
- `POST /api/chat/explain` - Explain a concept
- `GET /api/chat/similar-topics` - Find similar topics
- `POST /api/chat/recommend-videos` - Get YouTube recommendations

#### Progress Tracking
- `GET /api/progress/user/{user_id}` - Get user progress
- `GET /api/progress/user/{user_id}/insights` - Get learning insights
- `GET /api/progress/user/{user_id}/study-patterns` - Get study patterns
- `GET /api/progress/user/{user_id}/goals` - Get learning goals
- `GET /api/progress/leaderboard` - Get user leaderboard
- `GET /api/progress/stats/overview` - Get platform statistics

### API Usage Examples

#### Upload a PDF
```bash
curl -X POST "http://localhost:8000/api/pdfs/upload" \
  -H "Content-Type: application/pdf" \
  -d @file.pdf
```

#### Generate a Quiz
```bash
curl -X POST "http://localhost:8000/api/quizzes/generate" \
  -H "Content-Type: application/json" \
  -d '{"pdf_id": 1, "quiz_type": "MCQ", "num_questions": 5}'
```

#### Ask a Question
```bash
curl -X POST "http://localhost:8000/api/chat/ask" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Newton's first law of motion?", "pdf_id": 1}'
```

#### Get User Progress
```bash
curl -X GET "http://localhost:8000/api/progress/user/1"
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql://user:password@localhost/pdf_db` |
| `OPENAI_API_KEY` | OpenAI API key | Required |
| `GOOGLE_API_KEY` | Google API key | Optional |
| `CHROMA_PERSIST_DIRECTORY` | ChromaDB storage path | `./chroma` |
| `UPLOAD_DIR` | File upload directory | `./uploads/pdfs` |
| `MAX_FILE_SIZE` | Maximum file size (bytes) | `10485760` (10MB) |
| `DEBUG` | Debug mode | `True` |

### Database Schema

The application uses the following main tables:

- **users**: User accounts and authentication
- **pdfs**: Uploaded PDF file metadata
- **text_chunks**: Extracted text chunks from PDFs
- **quiz_attempts**: Quiz attempts and results
- **user_progress**: Learning progress and analytics

## Development

### Running Tests
```bash
# Add test files to tests/ directory
pytest tests/
```

### Code Structure
- **Models**: SQLAlchemy database models in `models/`
- **Schemas**: Pydantic validation schemas in `schemas/`
- **Routes**: FastAPI route definitions in `routes/`
- **Services**: Business logic in `services/`
- **Utils**: Utility functions in `utils/`

### Adding New Features
1. Create database models in `models/`
2. Add Pydantic schemas in `schemas/`
3. Implement business logic in `services/`
4. Create API endpoints in `routes/`
5. Update configuration if needed

## Production Deployment

### Environment Setup
1. Set production environment variables
2. Configure proper database credentials
3. Set up SSL/TLS certificates
4. Configure CORS for production domains
5. Set up proper authentication (JWT)

### Performance Optimization
- Use connection pooling for PostgreSQL
- Implement caching for frequently accessed data
- Optimize vector search parameters
- Use CDN for static assets

### Security Considerations
- Implement proper authentication and authorization
- Validate all user inputs
- Use HTTPS in production
- Implement rate limiting
- Secure API keys and sensitive data

## Troubleshooting

### Common Issues

1. **Database Connection Issues**
   - Verify PostgreSQL is running
   - Check DATABASE_URL configuration
   - Ensure database user has proper permissions

2. **ChromaDB Issues**
   - Check file permissions on `./chroma/` directory
   - Ensure sufficient disk space
   - Verify ChromaDB dependencies are installed

3. **OpenAI API Issues**
   - Verify API key is valid
   - Check API quota and billing
   - Ensure network connectivity

4. **PDF Processing Issues**
   - Verify PDF files are not corrupted
   - Check file size limits
   - Ensure PyMuPDF is properly installed

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export DEBUG=True
```