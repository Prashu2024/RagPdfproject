import React, { useState, useEffect } from 'react';
import { TrendingUp, Award, Target, Brain, BarChart3 } from 'lucide-react';
import { progressAPI } from '../services/api';

const ProgressPage = () => {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadProgress();
  }, []);

  const loadProgress = async () => {
    try {
      setLoading(true);
      const response = await progressAPI.getUserProgress(1);
      if (response.success) {
        setProgress(response.data);
      }
    } catch (error) {
      console.error('Error loading progress:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  const getTrendColor = (trend) => {
    switch (trend) {
      case 'improving': return 'text-green-600';
      case 'stable': return 'text-blue-600';
      case 'declining': return 'text-orange-600';
      default: return 'text-gray-600';
    }
  };

  const getTrendText = (trend) => {
    switch (trend) {
      case 'improving': return '📈 Improving';
      case 'stable': return '➡️ Stable';
      case 'declining': return '📉 Needs Attention';
      default: return '📊 Insufficient Data';
    }
  };

  return (
    <div className="p-8 max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold mb-2">Your Learning Progress</h1>
        <p className="text-gray-600">Track your performance and identify areas for improvement</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-blue-100 rounded-lg">
              <BarChart3 className="w-5 h-5 text-blue-600" />
            </div>
            <span className="text-gray-600 text-sm">Total Quizzes</span>
          </div>
          <p className="text-3xl font-bold">{progress?.total_quizzes || 0}</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-green-100 rounded-lg">
              <Award className="w-5 h-5 text-green-600" />
            </div>
            <span className="text-gray-600 text-sm">Average Score</span>
          </div>
          <p className="text-3xl font-bold">{progress?.average_score || 0}%</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-purple-100 rounded-lg">
              <Brain className="w-5 h-5 text-purple-600" />
            </div>
            <span className="text-gray-600 text-sm">Strengths</span>
          </div>
          <p className="text-3xl font-bold">{progress?.strengths?.length || 0}</p>
        </div>

        <div className="card">
          <div className="flex items-center gap-3 mb-2">
            <div className="p-2 bg-orange-100 rounded-lg">
              <Target className="w-5 h-5 text-orange-600" />
            </div>
            <span className="text-gray-600 text-sm">Areas to Improve</span>
          </div>
          <p className="text-3xl font-bold">{progress?.weaknesses?.length || 0}</p>
        </div>
      </div>

      {/* Improvement Trend */}
      {progress && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-4">Learning Trend</h2>
          <div className="flex items-center gap-4">
            <div className={`text-2xl font-semibold ${getTrendColor(progress.improvement_trend)}`}>
              {getTrendText(progress.improvement_trend)}
            </div>
            <p className="text-gray-600">
              {progress.improvement_trend === 'improving' && 'Keep up the great work!'}
              {progress.improvement_trend === 'stable' && 'Maintain consistency for better results'}
              {progress.improvement_trend === 'declining' && 'Focus on reviewing weak areas'}
              {progress.improvement_trend === 'insufficient_data' && 'Take more quizzes to see your trend'}
            </p>
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Strengths */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Award className="w-5 h-5 text-green-600" />
            Your Strengths
          </h2>
          {progress?.strengths && progress.strengths.length > 0 ? (
            <div className="space-y-3">
              {progress.strengths.map((strength, index) => (
                <div key={index} className="bg-green-50 border border-green-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-green-900">{strength.topic}</h3>
                    <span className="text-green-700 font-bold">{strength.score.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-green-200 rounded-full h-2">
                    <div
                      className="bg-green-600 h-2 rounded-full transition-all"
                      style={{ width: `${strength.score}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-green-700 mt-2">
                    {strength.attempts} quiz{strength.attempts > 1 ? 'zes' : ''} attempted
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              Take more quizzes to identify your strengths
            </p>
          )}
        </div>

        {/* Weaknesses */}
        <div className="card">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <Target className="w-5 h-5 text-orange-600" />
            Areas to Improve
          </h2>
          {progress?.weaknesses && progress.weaknesses.length > 0 ? (
            <div className="space-y-3">
              {progress.weaknesses.map((weakness, index) => (
                <div key={index} className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-2">
                    <h3 className="font-medium text-orange-900">{weakness.topic}</h3>
                    <span className="text-orange-700 font-bold">{weakness.score.toFixed(1)}%</span>
                  </div>
                  <div className="w-full bg-orange-200 rounded-full h-2">
                    <div
                      className="bg-orange-600 h-2 rounded-full transition-all"
                      style={{ width: `${weakness.score}%` }}
                    ></div>
                  </div>
                  <p className="text-sm text-orange-700 mt-2">
                    {weakness.attempts} quiz{weakness.attempts > 1 ? 'zes' : ''} attempted
                  </p>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-gray-500 text-center py-8">
              Great! No weak areas identified yet
            </p>
          )}
        </div>
      </div>

      {/* Recommendations */}
      {progress?.weaknesses && progress.weaknesses.length > 0 && (
        <div className="card mt-8">
          <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
            <TrendingUp className="w-5 h-5 text-primary-600" />
            Recommendations
          </h2>
          <div className="space-y-3">
            {progress.weaknesses.slice(0, 3).map((weakness, index) => (
              <div key={index} className="flex items-start gap-3 p-4 bg-blue-50 border border-blue-200 rounded-lg">
                <span className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold">
                  {index + 1}
                </span>
                <div>
                  <p className="font-medium text-blue-900">
                    Focus on {weakness.topic}
                  </p>
                  <p className="text-sm text-blue-700 mt-1">
                    Review the material and take practice quizzes to improve your score from {weakness.score.toFixed(1)}%
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default ProgressPage;

