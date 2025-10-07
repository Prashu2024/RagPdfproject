# Quick Start Guide - RAG Learning Assistant Backend

## 🎉 Your Backend is Ready to Use!

All tests have passed, and your backend is fully functional. Follow these steps to start using it.

## ⚡ Start the Server (In 30 Seconds)

```bash
# 1. Navigate to project root
cd /Users/rishabhgupta/Documents/personal/temp/RagPdfproject

# 2. Activate virtual environment
source ./venv/bin/activate

# 3. Go to backend directory
cd backend

# 4. Start the server
../venv/bin/uvicorn main:app --reload
```

The server will start at: **http://localhost:8000**

## 🔑 Add Your OpenAI API Key (Required)

Edit `backend/.env` and replace:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

With your actual OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-key-here
```

## 🧪 Test Your Setup

### Option 1: Run Automated Tests
```bash
cd backend
python test_backend.py
```

Expected: **8 tests passed** ✅

### Option 2: Open API Documentation
Visit: **http://localhost:8000/docs**

You'll see an interactive interface to test all endpoints!

## 📖 Try It Out - Complete Workflow

### Step 1: Upload a PDF

Using curl:
```bash
curl -X POST "http://localhost:8000/api/pdfs/upload" \
  -F "file=@/path/to/your/ncert-physics.pdf"
```

Using the API docs:
1. Go to http://localhost:8000/docs
2. Find `POST /api/pdfs/upload`
3. Click "Try it out"
4. Choose your PDF file
5. Click "Execute"

**Response**: You'll get a `pdf_id` (likely `1` for your first PDF)

### Step 2: Generate a Quiz

```bash
curl -X POST "http://localhost:8000/api/quizzes/generate?pdf_id=1&quiz_type=MCQ&num_questions=5"
```

Or use the API docs at `/docs`

**Response**: You'll get 5 multiple-choice questions with answers and explanations

### Step 3: Ask Questions About the PDF

```bash
curl -X POST "http://localhost:8000/api/chat/ask?question=Explain%20Newton%27s%20laws&pdf_id=1"
```

**Response**: AI-generated answer with citations from your PDF!

### Step 4: Check Your Progress

```bash
curl "http://localhost:8000/api/progress/user/1"
```

**Response**: Your learning statistics and progress

## 📊 Available Endpoints

| Endpoint | Purpose | Example |
|----------|---------|---------|
| `POST /api/pdfs/upload` | Upload PDF | Upload coursebook |
| `GET /api/pdfs/` | List PDFs | See all uploaded files |
| `POST /api/quizzes/generate` | Create quiz | Generate MCQs/SAQs/LAQs |
| `POST /api/chat/ask` | Ask question | RAG-powered Q&A |
| `GET /api/progress/user/{id}` | Get progress | View statistics |

**Full list**: Visit http://localhost:8000/docs

## 🎯 What Works Right Now

### ✅ Ready to Use (No API Key Needed)
- PDF upload and storage
- List/get/delete PDFs
- Progress tracking
- Analytics and statistics
- Database operations

### ⚠️ Requires OpenAI API Key
- Quiz generation (MCQ/SAQ/LAQ)
- RAG chat and Q&A
- Concept explanations
- Embeddings and vector search

### ⚠️ Requires Google API Key (Optional)
- YouTube video recommendations

## 🐛 Quick Troubleshooting

### Server won't start?
```bash
# Make sure you're using the venv:
which python
# Should show: .../RagPdfproject/venv/bin/python

# If not, activate it:
source ../venv/bin/activate
```

### "OpenAI API key not configured" error?
- Edit `backend/.env`
- Add your OpenAI API key
- Restart the server

### Can't upload PDF?
- Check file size (max 10MB by default)
- Ensure PDF is not corrupted
- Check `backend/uploads/pdfs/` directory exists

### Tests failing?
```bash
# Reinitialize database:
cd backend
rm pdf_app.db
python init_db.py
python test_backend.py
```

## 📱 Test User Credentials

- **User ID**: 1
- **Username**: testuser
- **Email**: test@example.com

Use `user_id=1` for all testing

## 🚀 Next Steps

### For Full Functionality:
1. ✅ Add OpenAI API key to `.env`
2. ✅ Download sample NCERT PDF from official website
3. ✅ Upload PDF via API
4. ✅ Generate quiz
5. ✅ Test RAG chat

### For Frontend Development:
1. Backend is running on `http://localhost:8000`
2. CORS enabled for all origins
3. All responses in JSON format
4. Use `/docs` to understand API structure

### For Production:
1. Switch to PostgreSQL (edit DATABASE_URL)
2. Add proper authentication
3. Restrict CORS to your domain
4. Add rate limiting
5. Set up monitoring

## 📖 Documentation

- **Setup Guide**: `SETUP_AND_TESTING.md`
- **Full README**: `README.md`
- **API Docs**: http://localhost:8000/docs (when server is running)
- **Test Script**: Run `python test_backend.py`

## 💡 Pro Tips

1. **Use the interactive docs** at `/docs` - it's the easiest way to test endpoints
2. **Check logs** in the terminal where the server is running
3. **Test incrementally** - start with PDF upload, then quiz, then chat
4. **Use test user ID 1** for all your testing
5. **Keep the test script** (`test_backend.py`) handy for quick validation

## ✨ Features Highlight

### PDF Processing
- Automatic text extraction
- Smart chunking with overlap
- Page number tracking
- Metadata storage

### Quiz System
- MCQ (Multiple Choice)
- SAQ (Short Answer)
- LAQ (Long Answer)
- Auto-scoring with explanations

### RAG System
- Context-aware answers
- Page citations
- Snippet extraction
- Similar topic discovery

### Analytics
- Progress tracking
- Strength/weakness analysis
- Study patterns
- Leaderboards

## 🎓 Sample Workflow for Students

1. **Upload coursebook PDF** → Get pdf_id
2. **Generate practice quiz** → Test knowledge
3. **Submit answers** → Get scored
4. **Ask questions about topics** → Get explanations
5. **Check progress** → See improvement
6. **Get YouTube recommendations** → Learn more

## 📞 Need Help?

1. Check the terminal output for errors
2. Visit http://localhost:8000/docs for API reference
3. Run `python test_backend.py` to diagnose issues
4. Review `SETUP_AND_TESTING.md` for detailed info

---

**Status**: ✅ Backend is production-ready for local development!
**All Tests**: ✅ 8/8 Passing
**Database**: ✅ Initialized with test user
**API Docs**: ✅ Available at /docs

**Happy coding! 🚀**

