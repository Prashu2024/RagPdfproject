import React, { useState, useRef } from 'react';
import { FileText, ZoomIn, ZoomOut, Download, Loader2, RotateCcw, ChevronLeft, ChevronRight } from 'lucide-react';
import { Document, Page, pdfjs } from 'react-pdf';

// Set up PDF.js worker with version matching
console.log('Setting up PDF.js worker...');
console.log('PDF.js version:', pdfjs.version);

// Set worker to match the exact version
console.log('PDF.js API version:', pdfjs.version);
pdfjs.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjs.version}/build/pdf.worker.min.mjs`;
console.log('PDF.js worker configured with version:', pdfjs.version);

// Add some basic styles for react-pdf
const pdfStyles = `
  .react-pdf__Document {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .react-pdf__Page {
    max-width: calc(100% - 2em);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    margin: 1em;
  }
  
  .react-pdf__Page__canvas {
    display: block;
    max-width: 100%;
    max-height: 100%;
  }
  
  .pdf-page {
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    overflow: hidden;
  }
`;

const PDFViewer = ({ pdfs, selectedPDF }) => {
  const [zoom, setZoom] = useState(1);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [numPages, setNumPages] = useState(null);
  const [pageNumber, setPageNumber] = useState(1);
  const [pdfBlobUrl, setPdfBlobUrl] = useState(null);
  const currentBlobUrlRef = useRef(null);

  const currentPDF = pdfs.find(p => p.id === selectedPDF);

  // Add styles to document head
  React.useEffect(() => {
    const style = document.createElement('style');
    style.textContent = pdfStyles;
    document.head.appendChild(style);
    
    return () => {
      document.head.removeChild(style);
    };
  }, []);

  // Reset state when PDF changes
  React.useEffect(() => {
    if (currentPDF) {
      setLoading(true);
      setError(null);
      setPageNumber(1);
      setNumPages(null);
      
      // Clean up previous blob URL
      if (currentBlobUrlRef.current) {
        URL.revokeObjectURL(currentBlobUrlRef.current);
        setPdfBlobUrl(null);
      }
      
      // Fetch PDF as blob and create blob URL
      const fetchPDF = async () => {
        try {
          console.log('Fetching PDF as blob...');
          const response = await fetch(`http://localhost:8000/api/pdfs/${currentPDF.id}/file`);
          if (!response.ok) {
            throw new Error(`HTTP ${response.status}: ${response.statusText}`);
          }
          
          const blob = await response.blob();
          console.log('PDF blob created:', blob.size, 'bytes, type:', blob.type);
          
          const blobUrl = URL.createObjectURL(blob);
          console.log('Blob URL created:', blobUrl);
          currentBlobUrlRef.current = blobUrl;
          setPdfBlobUrl(blobUrl);
          setLoading(false);
        } catch (error) {
          console.error('Error fetching PDF:', error);
          setError(`Failed to load PDF: ${error.message}`);
          setLoading(false);
        }
      };
      
      fetchPDF();
      
      // Set a timeout to stop loading after 30 seconds
      const timeout = setTimeout(() => {
        console.log('PDF loading timeout reached');
        console.log('PDF URL:', `http://localhost:8000/api/pdfs/${currentPDF.id}/file`);
        console.log('Worker source:', pdfjs.GlobalWorkerOptions.workerSrc);
        setLoading(false);
        setError('PDF loading timeout - please try again');
      }, 30000);
      
      return () => {
        clearTimeout(timeout);
        if (currentBlobUrlRef.current) {
          URL.revokeObjectURL(currentBlobUrlRef.current);
        }
      };
    }
  }, [currentPDF]);

  const onDocumentLoadSuccess = ({ numPages }) => {
    console.log('PDF loaded successfully, pages:', numPages);
    setNumPages(numPages);
    setLoading(false);
    setError(null);
  };

  const onDocumentLoadError = (error) => {
    console.error('PDF load error:', error);
    console.error('Error details:', error.message, error.name);
    console.error('PDF URL:', `http://localhost:8000/api/pdfs/${currentPDF.id}/file`);
    console.error('Worker source:', pdfjs.GlobalWorkerOptions.workerSrc);
    setError(`Failed to load PDF: ${error.message}`);
    setLoading(false);
  };

  const onDocumentLoadProgress = ({ loaded, total }) => {
    console.log('PDF loading progress:', loaded, '/', total);
  };

  const goToPrevPage = () => {
    setPageNumber(prev => Math.max(prev - 1, 1));
  };

  const goToNextPage = () => {
    setPageNumber(prev => Math.min(prev + 1, numPages || 1));
  };

  if (!selectedPDF || !currentPDF) {
    return (
      <div className="p-8 max-w-4xl mx-auto">
        <div className="card text-center py-12">
          <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold mb-2">No PDF Selected</h2>
          <p className="text-gray-600">
            Please select a PDF from the sidebar to view it
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Toolbar */}
      <div className="bg-white border-b border-gray-200 p-4">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <div>
            <h2 className="text-lg font-semibold">{currentPDF.filename}</h2>
            <p className="text-sm text-gray-600">{currentPDF.page_count} pages</p>
          </div>
          
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 bg-gray-100 rounded-lg p-2">
              <button
                onClick={() => setZoom(Math.max(0.5, zoom - 0.1))}
                className="p-2 hover:bg-gray-200 rounded transition-colors"
                disabled={loading}
              >
                <ZoomOut className="w-4 h-4" />
              </button>
              <span className="text-sm font-medium px-2">{Math.round(zoom * 100)}%</span>
              <button
                onClick={() => setZoom(Math.min(2, zoom + 0.1))}
                className="p-2 hover:bg-gray-200 rounded transition-colors"
                disabled={loading}
              >
                <ZoomIn className="w-4 h-4" />
              </button>
            </div>
            
            <a
              href={`http://localhost:8000/api/pdfs/${currentPDF.id}/file`}
              target="_blank"
              rel="noopener noreferrer"
              className="btn-secondary flex items-center gap-2"
            >
              <Download className="w-4 h-4" />
              Open PDF
            </a>
          </div>
        </div>
      </div>

      {/* PDF Display */}
      <div className="flex-1 overflow-auto bg-gray-100">
        <div className="h-full w-full flex flex-col">

            {/* PDF Content */}
            <div className="flex-1 overflow-auto p-4">
              {loading ? (
                <div className="flex flex-col items-center gap-4 py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-blue-600" />
                  <p className="text-gray-600">Loading PDF...</p>
                </div>
              ) : error ? (
                <div className="p-8 text-center text-gray-600 bg-white rounded-lg shadow-lg max-w-md mx-auto">
                  <FileText className="w-16 h-16 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-semibold mb-2">Error Loading PDF</h3>
                  <p className="mb-4">{error}</p>
                  <button
                    onClick={() => {
                      setError(null);
                      setLoading(true);
                    }}
                    className="btn-primary inline-flex items-center gap-2 mb-2"
                  >
                    <RotateCcw className="w-4 h-4" />
                    Retry
                  </button>
                  <br />
                  <a 
                    href={`http://localhost:8000/api/pdfs/${currentPDF.id}/file`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="btn-secondary inline-flex items-center gap-2"
                  >
                    <Download className="w-4 h-4" />
                    Open PDF in New Tab
                  </a>
                </div>
              ) : (
                <div className="flex flex-col items-center">
                  {/* Page Navigation */}
                  {numPages && (
                    <div className="flex items-center gap-4 mb-4 bg-white rounded-lg shadow-sm p-3">
                      <button
                        onClick={goToPrevPage}
                        disabled={pageNumber <= 1}
                        className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <ChevronLeft className="w-4 h-4" />
                      </button>
                      <span className="text-sm font-medium">
                        Page {pageNumber} of {numPages}
                      </span>
                      <button
                        onClick={goToNextPage}
                        disabled={pageNumber >= numPages}
                        className="p-2 rounded hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  )}

                  {/* PDF Document */}
                  {pdfBlobUrl && (
                    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                      <Document
                        file={pdfBlobUrl}
                        onLoadSuccess={onDocumentLoadSuccess}
                        onLoadError={onDocumentLoadError}
                        onLoadProgress={onDocumentLoadProgress}
                        loading={
                          <div className="flex items-center justify-center p-8">
                            <Loader2 className="w-6 h-6 animate-spin text-blue-600" />
                          </div>
                        }
                      >
                        <Page
                          pageNumber={pageNumber}
                          scale={zoom}
                          renderTextLayer={false}
                          renderAnnotationLayer={false}
                          className="pdf-page"
                        />
                      </Document>
                    </div>
                  )}

                  {/* Download Link and Test Button */}
                  <div className="mt-4 flex gap-2 justify-center">
                    <a 
                      href={`http://localhost:8000/api/pdfs/${currentPDF.id}/file`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="btn-secondary inline-flex items-center gap-2 text-sm"
                    >
                      <Download className="w-4 h-4" />
                      Open PDF in New Tab
                    </a>
                    <button
                      onClick={async () => {
                        try {
                          console.log('Testing PDF fetch...');
                          console.log('PDF URL:', `http://localhost:8000/api/pdfs/${currentPDF.id}/file`);
                          const response = await fetch(`http://localhost:8000/api/pdfs/${currentPDF.id}/file`);
                          console.log('PDF fetch response:', response.status, response.headers.get('content-type'));
                          if (response.ok) {
                            const blob = await response.blob();
                            console.log('PDF blob size:', blob.size, 'type:', blob.type);
                            console.log('PDF fetch successful!');
                          } else {
                            console.error('PDF fetch failed with status:', response.status);
                          }
                        } catch (error) {
                          console.error('PDF fetch error:', error);
                        }
                      }}
                      className="btn-primary inline-flex items-center gap-2 text-sm"
                    >
                      Test PDF Fetch
                    </button>
                  </div>
                </div>
              )}
            </div>
        </div>
      </div>
    </div>
  );
};

export default PDFViewer;

