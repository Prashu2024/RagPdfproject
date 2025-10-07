import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FileText, MessageSquare, BookOpen, TrendingUp, Clock, CheckCircle } from 'lucide-react';
import { progressAPI, quizAPI } from '../services/api';

const Dashboard = ({ pdfs, selectedPDF, onSelectPDF }) => {
  const [stats, setStats] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [progressData, statsData] = await Promise.all([
        progressAPI.getUserProgress(1),
        progressAPI.getOverviewStats()
      ]);
      
      if (progressData.success) {
        setStats(progressData.data);
      }
    } catch (error) {
      console.error('Error loading dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Generate Quiz',
      description: 'Test your knowledge with MCQs, SAQs, or LAQs',
      icon: BookOpen,
      link: '/quiz',
      color: 'bg-blue-500',
      disabled: !selectedPDF && pdfs.length === 0
    },
    {
      title: 'Ask Questions',
      description: 'Get instant answers with citations',
      icon: MessageSquare,
      link: '/chat',
      color: 'bg-green-500',
      disabled: !selectedPDF && pdfs.length === 0
    },
    {
      title: 'View PDF',
      description: 'Read your coursebook with AI assistance',
      icon: FileText,
      link: '/pdf-viewer',
      color: 'bg-purple-500',
      disabled: !selectedPDF && pdfs.length === 0
    },
    {
      title: 'Track Progress',
      description: 'Monitor your learning journey',
      icon: TrendingUp,
      link: '/progress',
      color: 'bg-orange-500',
      disabled: false
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Welcome back! 👋
        </h1>
        <p className="text-gray-600">
          {pdfs.length === 0 
            ? 'Upload a PDF to get started with your learning journey'
            : selectedPDF 
              ? `Currently studying: ${pdfs.find(p => p.id === selectedPDF)?.filename || 'All PDFs'}`
              : 'Select a PDF from the sidebar to begin'
          }
        </p>
      </div>

      {/* Stats Cards */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Total Quizzes</p>
                <p className="text-2xl font-bold mt-1">{stats.total_quizzes || 0}</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <BookOpen className="w-6 h-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Average Score</p>
                <p className="text-2xl font-bold mt-1">{stats.average_score || 0}%</p>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <CheckCircle className="w-6 h-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">PDFs Uploaded</p>
                <p className="text-2xl font-bold mt-1">{pdfs.length}</p>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <FileText className="w-6 h-6 text-purple-600" />
              </div>
            </div>
          </div>

          <div className="card">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-gray-500 text-sm">Study Streak</p>
                <p className="text-2xl font-bold mt-1">0 days</p>
              </div>
              <div className="p-3 bg-orange-100 rounded-lg">
                <Clock className="w-6 h-6 text-orange-600" />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Quick Actions */}
      <div className="mb-8">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {quickActions.map((action) => {
            const Icon = action.icon;
            return (
              <Link
                key={action.title}
                to={action.disabled ? '#' : action.link}
                className={`card hover:shadow-md transition-all ${
                  action.disabled ? 'opacity-50 cursor-not-allowed' : 'hover:-translate-y-1'
                }`}
                onClick={(e) => action.disabled && e.preventDefault()}
              >
                <div className={`${action.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4`}>
                  <Icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="font-semibold mb-1">{action.title}</h3>
                <p className="text-sm text-gray-600">{action.description}</p>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Recent PDFs */}
      {pdfs.length > 0 && (
        <div>
          <h2 className="text-xl font-semibold mb-4">Your PDFs</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {pdfs.map((pdf) => (
              <div key={pdf.id} className="card hover:shadow-md transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className="p-2 bg-primary-100 rounded-lg">
                    <FileText className="w-5 h-5 text-primary-600" />
                  </div>
                  {pdf.processed && (
                    <span className="text-xs bg-green-100 text-green-700 px-2 py-1 rounded-full">
                      Processed
                    </span>
                  )}
                </div>
                <h3 className="font-medium mb-2 truncate">{pdf.filename}</h3>
                <p className="text-sm text-gray-600 mb-4">
                  {pdf.page_count} pages • {(pdf.file_size / 1024 / 1024).toFixed(2)} MB
                </p>
                <button
                  onClick={() => onSelectPDF(pdf.id)}
                  className="btn-primary w-full text-sm"
                >
                  Select PDF
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Empty State */}
      {pdfs.length === 0 && (
        <div className="card text-center py-12">
          <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold mb-2">No PDFs uploaded yet</h3>
          <p className="text-gray-600 mb-6">
            Upload your first PDF coursebook to start learning
          </p>
          <button className="btn-primary">
            Upload PDF from Sidebar
          </button>
        </div>
      )}
    </div>
  );
};

export default Dashboard;

