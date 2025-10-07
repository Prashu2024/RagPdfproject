# RAG Learning Assistant Frontend

A modern React-based frontend for the RAG Learning Assistant, built with Vite and styled with Tailwind CSS. This application provides an intuitive interface for students to interact with their coursebooks through AI-powered features.

## 🚀 Features

- **📚 PDF Management**: Upload and manage multiple PDF coursebooks
- **📖 PDF Viewer**: View PDFs with zoom, page navigation, and search
- **🧠 Quiz Generator**: Generate and take quizzes from uploaded PDFs
- **💬 RAG Chat**: Ask questions and get AI-powered answers with citations
- **📊 Progress Tracking**: Monitor learning progress and analytics
- **📱 Responsive Design**: Works seamlessly on desktop and mobile

## 🛠️ Tech Stack

- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: Tailwind CSS
- **PDF Viewer**: react-pdf
- **HTTP Client**: Axios
- **Routing**: React Router DOM
- **Icons**: Lucide React

## 🚀 Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Open your browser:**
   Navigate to `http://localhost:5173`

### Build for Production

```bash
npm run build
```

The built files will be in the `dist/` directory.

## 📁 Project Structure

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── components/         # Reusable UI components
│   │   └── Sidebar.jsx    # Main navigation sidebar
│   ├── pages/             # Page components
│   │   ├── Dashboard.jsx  # Dashboard overview
│   │   ├── PDFViewer.jsx  # PDF viewing interface
│   │   ├── QuizPage.jsx   # Quiz generation and taking
│   │   ├── ChatPage.jsx   # RAG chat interface
│   │   └── ProgressPage.jsx # Progress tracking
│   ├── services/          # API integration
│   │   └── api.js         # Axios API client
│   ├── App.jsx            # Main application component
│   ├── main.jsx           # Application entry point
│   └── index.css          # Global styles
├── package.json           # Dependencies and scripts
├── tailwind.config.js     # Tailwind CSS configuration
├── vite.config.js         # Vite configuration
└── README.md             # This file
```

## 🎨 UI Components

### Sidebar
- PDF upload functionality
- PDF selection (individual or all PDFs)
- Navigation menu
- Progress indicators

### Dashboard
- Overview of uploaded PDFs
- Quick stats and analytics
- Recent activity

### PDF Viewer
- PDF display with react-pdf
- Zoom controls
- Page navigation
- Download functionality

### Quiz Page
- Quiz configuration (type, number of questions)
- Quiz generation from specific PDF or all PDFs
- Interactive quiz taking
- Results and explanations

### Chat Page
- RAG-based Q&A interface
- Question input with PDF context
- Answer display with citations
- Similar topics discovery

### Progress Page
- Learning analytics dashboard
- Quiz performance tracking
- Study patterns and insights

## 🔧 Configuration

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=RAG Learning Assistant
```

### API Integration

The frontend communicates with the backend through the API service located in `src/services/api.js`. All API calls are centralized and include:

- PDF management endpoints
- Quiz generation and submission
- RAG chat functionality
- Progress tracking

## 🎨 Styling

The application uses Tailwind CSS for styling with a custom design system:

- **Primary Colors**: Blue theme for main actions
- **Secondary Colors**: Gray theme for secondary elements
- **Typography**: Clean, readable fonts
- **Spacing**: Consistent spacing system
- **Responsive**: Mobile-first responsive design

### Custom CSS Classes

```css
.btn-primary     /* Primary button styling */
.btn-secondary   /* Secondary button styling */
.card           /* Card container styling */
```

## 🧪 Development

### Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint

### Code Structure

- **Components**: Reusable UI components in `src/components/`
- **Pages**: Main page components in `src/pages/`
- **Services**: API integration in `src/services/`
- **Styles**: Global styles in `src/index.css`

### Adding New Features

1. Create components in `src/components/`
2. Add pages in `src/pages/`
3. Update routing in `src/App.jsx`
4. Add API calls in `src/services/api.js`
5. Style with Tailwind CSS classes

## 🐛 Troubleshooting

### Common Issues

1. **Build Errors**
   - Clear node_modules and reinstall
   - Check Node.js version compatibility
   - Verify all dependencies are installed

2. **API Connection Issues**
   - Ensure backend server is running
   - Check API base URL configuration
   - Verify CORS settings

3. **PDF Viewer Issues**
   - Check if PDF files are accessible
   - Verify react-pdf dependencies
   - Check browser console for errors

4. **Styling Issues**
   - Ensure Tailwind CSS is properly configured
   - Check for conflicting CSS
   - Verify PostCSS configuration

### Debug Mode

Enable debug mode for detailed error messages:
```bash
VITE_DEBUG=true npm run dev
```

## 📦 Deployment

### Build for Production

```bash
npm run build
```

### Deploy to Static Hosting

1. Build the application
2. Upload the `dist/` directory to your hosting provider
3. Configure API endpoints for production
4. Set up proper CORS headers

### Environment Configuration

Update environment variables for production:
```env
VITE_API_BASE_URL=https://your-api-domain.com/api
VITE_APP_NAME=RAG Learning Assistant
```

## 🤝 Contributing

1. Follow React best practices
2. Use functional components with hooks
3. Implement responsive design
4. Write clean, readable code
5. Add comments for complex logic

## 📄 License

This project is part of the RAG Learning Assistant and follows the same MIT License.

---

**Built with React, Vite, and Tailwind CSS**