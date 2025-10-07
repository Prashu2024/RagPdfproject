# RAG Learning Assistant

A comprehensive educational platform that helps school students revise from their coursebooks using AI-powered features. The application combines PDF processing, quiz generation, RAG-based Q&A, and progress tracking to create an interactive learning experience.

## 🚀 Features

### Must-Have Features ✅
- **📚 PDF Management**: Upload and manage multiple PDF coursebooks
- **📖 PDF Viewer**: View PDFs with zoom, page navigation, and search
- **🧠 Quiz Generator**: Generate MCQs, SAQs, and LAQs from uploaded PDFs
- **📊 Progress Tracking**: Monitor learning progress and identify strengths/weaknesses
- **💬 RAG Chat**: Ask questions and get answers with citations from source materials

### Nice-to-Have Features ✅
- **🎯 Smart Quiz Generation**: Generate quizzes from specific PDFs or all PDFs combined
- **📈 Analytics Dashboard**: Comprehensive learning analytics and insights
- **🔍 Similar Topics**: Discover related concepts and topics
- **📺 YouTube Integration**: Get relevant educational video recommendations
- **📱 Responsive Design**: Works seamlessly on desktop and mobile devices

## 🏗️ Architecture

```
RagPdfproject/
├── backend/                 # FastAPI backend server
│   ├── config/             # Configuration files
│   ├── models/             # Database models
│   ├── routes/             # API endpoints
│   ├── services/           # Business logic
│   ├── utils/              # Utility functions
│   └── uploads/            # PDF storage
├── frontend/               # React frontend application
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   └── services/       # API integration
│   └── public/             # Static assets
└── venv/                   # Python virtual environment
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLite (development) / PostgreSQL (production)
- **Vector Database**: ChromaDB
- **LLM**: OpenAI GPT-3.5/4
- **PDF Processing**: PyMuPDF (fitz)
- **Authentication**: JWT (ready for implementation)

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **PDF Viewer**: react-pdf
- **HTTP Client**: Axios
- **Routing**: React Router DOM

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API Key

### 1. Clone the Repository
```bash
git clone <repository-url>
cd RagPdfproject
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv ../venv
source ../venv/bin/activate  # On Windows: ..\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenAI API key

# Initialize database
python init_db.py

# Start the backend server
python -m uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

### 3. Frontend Setup
```bash
# Navigate to frontend directory (in a new terminal)
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

### 4. Access the Application
Open your browser and navigate to `http://localhost:5173`

## 📖 Usage Guide

### 1. Upload PDFs
- Click "Upload PDF(s)" in the sidebar
- Select one or multiple PDF files
- Wait for processing to complete
- PDFs will appear in the sidebar

### 2. View PDFs
- Select a PDF from the sidebar
- Navigate to "PDF Viewer" page
- Use zoom and page navigation controls
- Download PDFs if needed

### 3. Generate Quizzes
- Select a PDF or "All PDFs"
- Navigate to "Quiz" page
- Choose quiz type (MCQ, SAQ, LAQ)
- Set number of questions
- Click "Generate Quiz"
- Answer questions and submit

### 4. Ask Questions
- Select a PDF or "All PDFs"
- Navigate to "Chat" page
- Type your question
- Get AI-powered answers with citations
- Explore similar topics

### 5. Track Progress
- Navigate to "Progress" page
- View learning analytics
- Monitor quiz performance
- Identify areas for improvement

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the `backend/` directory:

```env
# Database
DATABASE_URL=sqlite:///./pdf_app.db

# OpenAI
OPENAI_API_KEY=your_openai_api_key_here

# ChromaDB
CHROMA_PERSIST_DIRECTORY=./chroma

# Upload
UPLOAD_DIR=./uploads/pdfs
MAX_FILE_SIZE=10485760

# App
DEBUG=True
```

### API Endpoints

The backend provides a comprehensive REST API:

- **PDF Management**: `/api/pdfs/*`
- **Quiz Generation**: `/api/quizzes/*`
- **Chat & Q&A**: `/api/chat/*`
- **Progress Tracking**: `/api/progress/*`

Full API documentation available at `http://localhost:8000/docs`

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_backend.py
```

### Frontend Testing
```bash
cd frontend
npm test
```

## 📦 Deployment

### Backend Deployment
1. Set up production database (PostgreSQL)
2. Configure environment variables
3. Install dependencies: `pip install -r requirements.txt`
4. Run migrations: `python init_db.py`
5. Start server: `uvicorn main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment
1. Build the application: `npm run build`
2. Serve the `dist/` directory with a web server
3. Configure API endpoints for production

### Docker Deployment
```bash
# Build and run with Docker Compose
docker-compose up -d
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Commit your changes: `git commit -m 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## 📝 Development Notes

### Backend Development
- Follow FastAPI best practices
- Use type hints and Pydantic models
- Write comprehensive tests
- Document API endpoints

### Frontend Development
- Follow React best practices
- Use functional components with hooks
- Implement responsive design
- Write unit tests for components

## 🐛 Troubleshooting

### Common Issues

1. **PDF Upload Fails**
   - Check file size limits
   - Ensure PDF is not corrupted
   - Verify file permissions

2. **Quiz Generation Issues**
   - Check OpenAI API key
   - Verify PDF processing completed
   - Check API quota limits

3. **RAG Chat Not Working**
   - Ensure PDFs are processed
   - Check ChromaDB is running
   - Verify embeddings are generated

4. **Frontend Build Issues**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

### Debug Mode
Enable debug mode for detailed error messages:
```bash
export DEBUG=True
```
