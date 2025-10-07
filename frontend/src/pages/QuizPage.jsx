import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle, XCircle, Award, Clock } from 'lucide-react';
import { quizAPI } from '../services/api';

const QuizPage = ({ selectedPDF, pdfs }) => {
  const [quizType, setQuizType] = useState('MCQ');
  const [numQuestions, setNumQuestions] = useState(5);
  const [quiz, setQuiz] = useState(null);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [generating, setGenerating] = useState(false);

  const generateQuiz = async () => {
    try {
      setGenerating(true);
      setQuiz(null);
      setAnswers({});
      setResult(null);

      const response = await quizAPI.generateQuiz(selectedPDF, quizType, numQuestions);
      if (response.success) {
        setQuiz(response.data);
      }
    } catch (error) {
      console.error('Error generating quiz:', error);
      alert('Failed to generate quiz. Please try again.');
    } finally {
      setGenerating(false);
    }
  };

  const handleAnswerChange = (questionIndex, answer) => {
    setAnswers({
      ...answers,
      [questionIndex]: answer
    });
  };

  const submitQuiz = async () => {
    if (!quiz) return;

    // Check if all questions are answered
    const unansweredQuestions = quiz.questions.length - Object.keys(answers).length;
    if (unansweredQuestions > 0) {
      const confirmSubmit = window.confirm(
        `You have ${unansweredQuestions} unanswered question(s). Submit anyway?`
      );
      if (!confirmSubmit) return;
    }

    const answersArray = quiz.questions.map((_, index) => ({
      question_id: index + 1, // Backend expects 1-based question IDs
      answer: answers[index] || ''
    }));

    try {
      setLoading(true);
      console.log('Submitting quiz:', quiz.quiz_id, answersArray);
      const response = await quizAPI.submitQuiz(quiz.quiz_id, answersArray);
      console.log('Quiz response:', response);
      if (response.success) {
        setResult(response.data);
      } else {
        alert('Failed to submit quiz: ' + (response.message || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error submitting quiz:', error);
      alert('Failed to submit quiz: ' + (error.response?.data?.detail || error.message));
    } finally {
      setLoading(false);
    }
  };

  const resetQuiz = () => {
    setQuiz(null);
    setAnswers({});
    setResult(null);
  };

  if (!selectedPDF && pdfs.length === 0) {
    return (
      <div className="p-8 max-w-4xl mx-auto">
        <div className="card text-center py-12">
          <Award className="w-16 h-16 text-gray-300 mx-auto mb-4" />
          <h2 className="text-2xl font-semibold mb-2">No PDFs Available</h2>
          <p className="text-gray-600">
            Please upload some PDFs first to generate quizzes
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Quiz Generator</h1>
      <p className="text-gray-600 mb-8">
        {selectedPDF 
          ? `Test your knowledge from ${pdfs.find(p => p.id === selectedPDF)?.filename || 'selected PDF'}`
          : 'Test your knowledge from all uploaded PDFs'
        }
      </p>

      {/* Quiz Configuration */}
      {!quiz && !result && (
        <div className="card mb-8">
          <h2 className="text-xl font-semibold mb-4">Configure Your Quiz</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
            <div>
              <label className="block text-sm font-medium mb-2">Quiz Type</label>
              <select
                value={quizType}
                onChange={(e) => setQuizType(e.target.value)}
                className="input-field"
              >
                <option value="MCQ">Multiple Choice Questions (MCQ)</option>
                <option value="SAQ">Short Answer Questions (SAQ)</option>
                <option value="LAQ">Long Answer Questions (LAQ)</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium mb-2">Number of Questions</label>
              <select
                value={numQuestions}
                onChange={(e) => setNumQuestions(parseInt(e.target.value))}
                className="input-field"
              >
                {[3, 5, 10, 15, 20].map(num => (
                  <option key={num} value={num}>{num} questions</option>
                ))}
              </select>
            </div>
          </div>

          <button
            onClick={generateQuiz}
            disabled={generating}
            className="btn-primary w-full md:w-auto flex items-center justify-center gap-2"
          >
            {generating ? (
              <>
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                Generating Quiz...
              </>
            ) : (
              <>
                <Award className="w-4 h-4" />
                Generate Quiz
              </>
            )}
          </button>
        </div>
      )}

      {/* Quiz Display */}
      {quiz && !result && (
        <div>
          <div className="card mb-6">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h2 className="text-xl font-semibold">{quizType} Quiz</h2>
                <p className="text-gray-600">{quiz.total_questions} questions</p>
              </div>
              <button
                onClick={resetQuiz}
                className="btn-secondary flex items-center gap-2"
              >
                <RefreshCw className="w-4 h-4" />
                New Quiz
              </button>
            </div>
          </div>

          <div className="space-y-6">
            {quiz.questions.map((question, index) => (
              <div key={index} className="card">
                <div className="flex items-start gap-4">
                  <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center font-semibold text-primary-700">
                    {index + 1}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium mb-4">{question.question}</h3>
                    
                    {question.type === 'MCQ' && question.options ? (
                      <div className="space-y-2">
                        {question.options.map((option, optionIndex) => (
                          <label
                            key={optionIndex}
                            className="flex items-center gap-3 p-3 border rounded-lg cursor-pointer hover:bg-gray-50 transition-colors"
                          >
                            <input
                              type="radio"
                              name={`question-${index}`}
                              value={option}
                              checked={answers[index] === option}
                              onChange={(e) => handleAnswerChange(index, e.target.value)}
                              className="w-4 h-4 text-primary-600"
                            />
                            <span>{option}</span>
                          </label>
                        ))}
                      </div>
                    ) : (
                      <textarea
                        value={answers[index] || ''}
                        onChange={(e) => handleAnswerChange(index, e.target.value)}
                        placeholder="Type your answer here..."
                        className="input-field min-h-[100px]"
                      />
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="card mt-6 flex items-center justify-between">
            <p className="text-gray-600">
              Answered: {Object.keys(answers).length} / {quiz.total_questions}
            </p>
            <button
              onClick={submitQuiz}
              disabled={loading}
              className="btn-primary flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                  Submitting...
                </>
              ) : (
                <>
                  <CheckCircle className="w-4 h-4" />
                  Submit Quiz
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Results Display */}
      {result && (
        <div>
          <div className="card mb-6 text-center py-8">
            <div className={`w-24 h-24 rounded-full mx-auto mb-4 flex items-center justify-center ${
              result.score >= 80 ? 'bg-green-100' : result.score >= 60 ? 'bg-yellow-100' : 'bg-red-100'
            }`}>
              <span className={`text-4xl font-bold ${
                result.score >= 80 ? 'text-green-600' : result.score >= 60 ? 'text-yellow-600' : 'text-red-600'
              }`}>
                {result.score}%
              </span>
            </div>
            <h2 className="text-2xl font-semibold mb-2">
              {result.score >= 80 ? 'Excellent!' : result.score >= 60 ? 'Good Job!' : 'Keep Practicing!'}
            </h2>
            <p className="text-gray-600">
              You got {result.correct_answers} out of {result.total_questions} questions correct
            </p>
          </div>

          <div className="space-y-6">
            {result.answers && result.answers.map((answer, index) => (
              <div key={index} className="card">
                <div className="flex items-start gap-4">
                  <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    answer.is_correct ? 'bg-green-100' : 'bg-red-100'
                  }`}>
                    {answer.is_correct ? (
                      <CheckCircle className="w-5 h-5 text-green-600" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-600" />
                    )}
                  </div>
                  <div className="flex-1">
                    <h3 className="font-medium mb-2">{answer.question}</h3>
                    
                    <div className="space-y-2 mb-4">
                      <p className="text-sm">
                        <span className="font-medium">Your answer:</span>{' '}
                        <span className={answer.is_correct ? 'text-green-600' : 'text-red-600'}>
                          {answer.user_answer}
                        </span>
                      </p>
                      {!answer.is_correct && (
                        <p className="text-sm">
                          <span className="font-medium">Correct answer:</span>{' '}
                          <span className="text-green-600">{answer.correct_answer}</span>
                        </p>
                      )}
                    </div>
                    
                    <div className="bg-blue-50 border-l-4 border-blue-400 p-4 rounded">
                      <p className="text-sm font-medium text-blue-900 mb-1">Explanation:</p>
                      <p className="text-sm text-blue-800">{answer.explanation}</p>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="card mt-6 flex items-center justify-center gap-4">
            <button
              onClick={resetQuiz}
              className="btn-primary flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Generate New Quiz
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default QuizPage;

