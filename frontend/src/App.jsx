import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import PDFViewer from './pages/PDFViewer';
import QuizPage from './pages/QuizPage';
import ChatPage from './pages/ChatPage';
import ProgressPage from './pages/ProgressPage';
import { pdfAPI } from './services/api';

function App() {
  const [pdfs, setPdfs] = useState([]);
  const [selectedPDF, setSelectedPDF] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sidebarOpen, setSidebarOpen] = useState(true);

  useEffect(() => {
    loadPDFs();
  }, []);

  const loadPDFs = async () => {
    try {
      setLoading(true);
      const response = await pdfAPI.getAllPDFs();
      if (response.success) {
        setPdfs(response.data.pdfs);
        if (response.data.pdfs.length > 0 && !selectedPDF) {
          setSelectedPDF(response.data.pdfs[0].id);
        }
      }
    } catch (error) {
      console.error('Error loading PDFs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handlePDFUpload = async (file) => {
    try {
      const response = await pdfAPI.uploadPDF(file);
      if (response.success) {
        await loadPDFs();
        setSelectedPDF(response.data.pdf_id);
        return response.data;
      }
    } catch (error) {
      console.error('Error uploading PDF:', error);
      throw error;
    }
  };

  const handlePDFDelete = async (pdfId) => {
    try {
      await pdfAPI.deletePDF(pdfId);
      await loadPDFs();
      if (selectedPDF === pdfId) {
        setSelectedPDF(pdfs.length > 1 ? pdfs.find(p => p.id !== pdfId)?.id : null);
      }
    } catch (error) {
      console.error('Error deleting PDF:', error);
    }
  };

  return (
    <Router>
      <div className="flex h-screen bg-gray-50">
        <Sidebar
          pdfs={pdfs}
          selectedPDF={selectedPDF}
          onSelectPDF={setSelectedPDF}
          onUploadPDF={handlePDFUpload}
          onDeletePDF={handlePDFDelete}
          isOpen={sidebarOpen}
          onToggle={() => setSidebarOpen(!sidebarOpen)}
        />
        
        <main className={`flex-1 overflow-auto transition-all duration-300 ${sidebarOpen ? 'md:ml-64' : 'ml-0'}`}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route 
              path="/dashboard" 
              element={<Dashboard pdfs={pdfs} selectedPDF={selectedPDF} onSelectPDF={setSelectedPDF} />} 
            />
            <Route 
              path="/pdf-viewer" 
              element={<PDFViewer pdfs={pdfs} selectedPDF={selectedPDF} />} 
            />
            <Route 
              path="/quiz" 
              element={<QuizPage selectedPDF={selectedPDF} pdfs={pdfs} />} 
            />
            <Route 
              path="/chat" 
              element={<ChatPage selectedPDF={selectedPDF} pdfs={pdfs} />} 
            />
            <Route 
              path="/progress" 
              element={<ProgressPage />} 
            />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
