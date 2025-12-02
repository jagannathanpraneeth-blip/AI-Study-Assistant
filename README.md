# 🎓 AI-Powered Study Assistant

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://react.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An AI-powered study companion that helps students learn effectively through intelligent material analysis, AI-generated quiz questions, automated study notes, and progress tracking. Built with React, Flask, and Google Gemini API.

## ✨ Features

- 📚 **Material Upload & Analysis**: Upload PDFs, text files to analyze course materials
- 🤖 **AI-Generated Quizzes**: Automatically create quiz questions from study materials
- 📝 **Smart Notes**: Generate organized study notes with key concepts and summaries
- 📊 **Progress Tracking**: Monitor your learning progress and performance analytics
- 💬 **Natural Language Processing**: Understand complex topics with AI explanations
- 🎯 **Spaced Repetition**: Intelligent review scheduling based on your performance

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask 3.0
- **Database**: PostgreSQL / SQLite (dev)
- **ORM**: SQLAlchemy
- **API**: RESTful with CORS support
- **AI**: Google Gemini API
- **File Processing**: PyPDF2, python-docx

### Frontend
- **Framework**: React 18
- **Language**: TypeScript
- **Build Tool**: Vite
- **HTTP Client**: Axios
- **State Management**: Zustand / Context API
- **Styling**: CSS3 / TailwindCSS (optional)

## 📋 Project Structure

```
AI-Study-Assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # Flask app factory
│   │   ├── routes/              # API endpoints
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic (Gemini, PDF parsing)
│   │   └── utils/               # Utilities & validators
│   ├── requirements.txt         # Python dependencies
│   ├── run.py                   # Entry point
│   └── README.md
├── frontend/
│   ├── src/
│   │   ├── components/          # React components
│   │   ├── pages/               # Page components
│   │   ├── services/            # API client
│   │   └── App.tsx
│   ├── package.json
│   ├── vite.config.ts
│   └── README.md
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- npm or yarn
- Git

### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file
cat > .env << EOF
FLASK_ENV=development
DATABASE_URL=sqlite:///study_assistant.db
GEMINI_API_KEY=your_gemini_api_key_here
SECRET_KEY=dev-secret-key-change-in-production
FLASK_APP=run.py
EOF

# Run the app
python run.py
```

Backend runs at: `http://localhost:5000`

### Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Create .env.local file
cat > .env.local << EOF
VITE_API_URL=http://localhost:5000
VITE_GEMINI_API_KEY=your_gemini_api_key_here
EOF

# Run development server
npm run dev
```

Frontend runs at: `http://localhost:3000`

## 📚 API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Authentication
- `POST /api/auth/signup` - Register new user
- `POST /api/auth/login` - User login

### Materials
- `POST /api/materials/upload` - Upload study material
- `GET /api/materials/list` - List user's materials
- `GET /api/materials/<id>` - Get material details

### Quizzes
- `POST /api/quizzes/generate` - Generate quiz from material
- `POST /api/quizzes/submit` - Submit quiz answers
- `GET /api/quizzes/history` - Get quiz history

### Progress
- `GET /api/progress/stats` - Get progress statistics
- `GET /api/progress/analytics` - Get detailed analytics

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```
FLASK_ENV=development              # development or production
DATABASE_URL=sqlite:///study.db    # Database connection URL
GEMINI_API_KEY=xxx                 # Get from Google AI Studio
SECRET_KEY=your-secret-key         # Flask secret key
MAX_FILE_SIZE=50                   # Max upload size in MB
```

**Frontend (.env.local)**
```
VITE_API_URL=http://localhost:5000
VITE_GEMINI_API_KEY=xxx
```

## 🎓 How It Works

1. **Upload Material**: Students upload PDFs or text files containing course material
2. **Text Extraction**: Backend extracts text from uploaded files
3. **AI Analysis**: Google Gemini API analyzes the material
4. **Content Generation**: System generates:
   - Comprehensive study summaries
   - Multiple choice quiz questions
   - Organized study notes
5. **Interactive Learning**: Students take quizzes and track progress
6. **Analytics**: Dashboard shows performance metrics and learning insights

## 📖 Learning Outcomes

This project helps you develop:
- ✅ Full-stack web development (React + Flask)
- ✅ AI/ML integration (Google Gemini API)
- ✅ Database design (SQLAlchemy ORM)
- ✅ RESTful API design
- ✅ TypeScript for type safety
- ✅ File handling and text processing
- ✅ Authentication & authorization
- ✅ Deployment practices

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🙋 Support

For questions or issues, please open an GitHub issue or contact the maintainer.

---

**Made for students **
