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
git clone https://github.com/Prashu2024/RagPdfproject
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


