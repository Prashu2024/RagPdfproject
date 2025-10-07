import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Home, FileText, MessageSquare, TrendingUp, BookOpen, Upload, X, ChevronLeft, ChevronRight, Trash2 } from 'lucide-react';

const Sidebar = ({ pdfs, selectedPDF, onSelectPDF, onUploadPDF, onDeletePDF, isOpen, onToggle }) => {
  const location = useLocation();
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState({ current: 0, total: 0, currentFile: '' });
  const [uploadError, setUploadError] = useState('');
  const [uploadSuccess, setUploadSuccess] = useState('');

  const navigationItems = [
    { name: 'Dashboard', path: '/dashboard', icon: Home },
    { name: 'PDF Viewer', path: '/pdf-viewer', icon: FileText },
    { name: 'Quiz', path: '/quiz', icon: BookOpen },
    { name: 'Chat', path: '/chat', icon: MessageSquare },
    { name: 'Progress', path: '/progress', icon: TrendingUp },
  ];

  const handleFileUpload = async (event) => {
    const files = Array.from(event.target.files);
    if (!files.length) return;

    // Validate all files are PDFs
    const invalidFiles = files.filter(file => file.type !== 'application/pdf');
    if (invalidFiles.length > 0) {
      setUploadError(`Please upload only PDF files. ${invalidFiles.length} file(s) are not PDFs.`);
      return;
    }

    try {
      setUploading(true);
      setUploadError('');
      setUploadSuccess('');
      setUploadProgress({ current: 0, total: files.length, currentFile: '' });
      
      // Upload files one by one
      for (let i = 0; i < files.length; i++) {
        setUploadProgress({ 
          current: i + 1, 
          total: files.length, 
          currentFile: files[i].name 
        });
        await onUploadPDF(files[i]);
      }
      
      // Show success message
      setUploadSuccess(`Successfully uploaded ${files.length} PDF(s)!`);
      setTimeout(() => setUploadSuccess(''), 3000); // Clear after 3 seconds
    } catch (error) {
      setUploadError('Upload failed. Please try again.');
    } finally {
      setUploading(false);
      setUploadProgress({ current: 0, total: 0, currentFile: '' });
      event.target.value = '';
    }
  };

  if (!isOpen) {
    return (
      <button
        onClick={onToggle}
        className="fixed top-4 left-4 z-50 p-2 bg-white rounded-lg shadow-lg hover:bg-gray-50"
      >
        <ChevronRight className="w-6 h-6" />
      </button>
    );
  }

  return (
    <div className="fixed left-0 top-0 h-screen w-64 bg-white border-r border-gray-200 flex flex-col z-40">
      {/* Header */}
      <div className="p-4 border-b border-gray-200 flex items-center justify-between">
        <h1 className="text-xl font-bold text-primary-600">RAG Learning</h1>
        <button
          onClick={onToggle}
          className="p-1 hover:bg-gray-100 rounded"
        >
          <ChevronLeft className="w-5 h-5" />
        </button>
      </div>

      {/* PDF Upload */}
      <div className="p-4 border-b border-gray-200">
        <label className="btn-primary w-full cursor-pointer flex items-center justify-center gap-2">
          <Upload className="w-4 h-4" />
          {uploading 
            ? `Uploading... (${uploadProgress.current}/${uploadProgress.total})` 
            : 'Upload PDF(s)'
          }
          <input
            type="file"
            accept=".pdf"
            multiple
            onChange={handleFileUpload}
            className="hidden"
            disabled={uploading}
          />
        </label>
        {uploadError && (
          <p className="text-red-500 text-sm mt-2">{uploadError}</p>
        )}
        {uploadSuccess && (
          <p className="text-green-600 text-sm mt-2">{uploadSuccess}</p>
        )}
        {uploading && uploadProgress.currentFile && (
          <p className="text-blue-600 text-xs mt-1 truncate">
            Uploading: {uploadProgress.currentFile}
          </p>
        )}
      </div>

      {/* PDF Selection */}
      <div className="flex-1 overflow-y-auto p-4">
        <h3 className="text-sm font-semibold text-gray-500 uppercase mb-2">Your PDFs</h3>
        {pdfs.length === 0 ? (
          <p className="text-gray-400 text-sm">No PDFs uploaded yet</p>
        ) : (
          <div className="space-y-2">
            <button
              onClick={() => onSelectPDF(null)}
              className={`w-full text-left px-3 py-2 rounded-lg transition-colors ${
                selectedPDF === null
                  ? 'bg-primary-50 text-primary-700 font-medium'
                  : 'hover:bg-gray-50'
              }`}
            >
              All PDFs
            </button>
            {pdfs.map((pdf) => (
              <div
                key={pdf.id}
                className={`group relative px-3 py-2 rounded-lg transition-colors ${
                  selectedPDF === pdf.id
                    ? 'bg-primary-50 text-primary-700'
                    : 'hover:bg-gray-50'
                }`}
              >
                <button
                  onClick={() => onSelectPDF(pdf.id)}
                  className="w-full text-left pr-8"
                >
                  <p className="text-sm font-medium truncate">{pdf.filename}</p>
                  <p className="text-xs text-gray-500">
                    {pdf.page_count} pages
                  </p>
                </button>
                <button
                  onClick={() => onDeletePDF(pdf.id)}
                  className="absolute right-2 top-1/2 -translate-y-1/2 p-1 opacity-0 group-hover:opacity-100 hover:bg-red-50 rounded transition-all"
                >
                  <Trash2 className="w-4 h-4 text-red-500" />
                </button>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="border-t border-gray-200 p-4">
        <nav className="space-y-1">
          {navigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path;
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                  isActive
                    ? 'bg-primary-50 text-primary-700 font-medium'
                    : 'text-gray-700 hover:bg-gray-50'
                }`}
              >
                <Icon className="w-5 h-5" />
                <span>{item.name}</span>
              </Link>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;

