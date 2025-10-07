import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// PDF APIs
export const pdfAPI = {
  uploadPDF: async (file) => {
    const formData = new FormData();
    formData.append('file', file);
    const response = await axios.post(`${API_BASE_URL}/pdfs/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return response.data;
  },
  
  getAllPDFs: async () => {
    const response = await api.get('/pdfs/');
    return response.data;
  },
  
  getPDF: async (pdfId) => {
    const response = await api.get(`/pdfs/${pdfId}`);
    return response.data;
  },
  
  deletePDF: async (pdfId) => {
    const response = await api.delete(`/pdfs/${pdfId}`);
    return response.data;
  },
  
  getPDFChunks: async (pdfId) => {
    const response = await api.get(`/pdfs/${pdfId}/chunks`);
    return response.data;
  },
};

// Quiz APIs
export const quizAPI = {
  generateQuiz: async (pdfId, quizType = 'MCQ', numQuestions = 5) => {
    // Handle "All PDFs" case where pdfId is null
    const url = pdfId 
      ? `/quizzes/generate?pdf_id=${pdfId}&quiz_type=${quizType}&num_questions=${numQuestions}`
      : `/quizzes/generate?quiz_type=${quizType}&num_questions=${numQuestions}`;
    const response = await api.post(url);
    return response.data;
  },
  
  getQuiz: async (quizId) => {
    const response = await api.get(`/quizzes/${quizId}`);
    return response.data;
  },
  
  submitQuiz: async (quizId, answers) => {
    // Answers are already in the correct format from QuizPage
    const response = await api.post(`/quizzes/${quizId}/submit`, { 
      quiz_id: quizId.toString(), // Convert to string as expected by backend
      answers: answers // Use answers as-is since they're already formatted correctly
    });
    return response.data;
  },
  
  getUserAttempts: async (userId) => {
    const response = await api.get(`/quizzes/user/${userId}/attempts`);
    return response.data;
  },
  
  getStatistics: async () => {
    const response = await api.get('/quizzes/statistics');
    return response.data;
  },
};

// Chat APIs
export const chatAPI = {
  askQuestion: async (question, pdfId = null) => {
    const url = pdfId 
      ? `/chat/ask?question=${encodeURIComponent(question)}&pdf_id=${pdfId}`
      : `/chat/ask?question=${encodeURIComponent(question)}`;
    const response = await api.post(url);
    return response.data;
  },
  
  explainConcept: async (concept, pdfId = null) => {
    const url = pdfId
      ? `/chat/explain?concept=${encodeURIComponent(concept)}&pdf_id=${pdfId}`
      : `/chat/explain?concept=${encodeURIComponent(concept)}`;
    const response = await api.post(url);
    return response.data;
  },
  
  getSimilarTopics: async (query, pdfId = null, topK = 5) => {
    const url = pdfId
      ? `/chat/similar-topics?query=${encodeURIComponent(query)}&pdf_id=${pdfId}&top_k=${topK}`
      : `/chat/similar-topics?query=${encodeURIComponent(query)}&top_k=${topK}`;
    const response = await api.get(url);
    return response.data;
  },
};

// Progress APIs
export const progressAPI = {
  getUserProgress: async (userId) => {
    const response = await api.get(`/progress/user/${userId}`);
    return response.data;
  },
  
  getInsights: async (userId) => {
    const response = await api.get(`/progress/user/${userId}/insights`);
    return response.data;
  },
  
  getStudyPatterns: async (userId) => {
    const response = await api.get(`/progress/user/${userId}/study-patterns`);
    return response.data;
  },
  
  getOverviewStats: async () => {
    const response = await api.get('/progress/stats/overview');
    return response.data;
  },
};

export default api;

