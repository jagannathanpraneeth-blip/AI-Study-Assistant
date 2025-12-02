# 🚀 AI-Study-Assistant - Quick Start Guide

Follow these steps to get the AI-Study-Assistant up and running on your local machine.

## 📋 Prerequisites

- Python 3.8 or higher
- Node.js 16+ and npm
- Git
- A text editor (VS Code recommended)
- Google Gemini API key (get it from https://aistudio.google.com)

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/jagannathanpraneeth-blip/AI-Study-Assistant.git
cd AI-Study-Assistant
```

## 2️⃣ Backend Setup (Python/Flask)

### Step 1: Navigate to Backend
```bash
cd backend
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Create .env File
```bash
# Copy the example file
cp ../.env.example .env

# Edit .env and add your Gemini API key
# Open .env with your text editor and replace:
# GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Run Backend
```bash
python run.py
```

✅ Backend will start at `http://localhost:5000`

## 3️⃣ Frontend Setup (React/TypeScript)

### Step 1: Open New Terminal and Navigate to Frontend
```bash
cd frontend
```

### Step 2: Install Dependencies
```bash
npm install
```

### Step 3: Create .env.local File
```bash
# Create a new file named .env.local in the frontend directory
# Add these variables:
VITE_API_URL=http://localhost:5000
VITE_GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 4: Run Frontend
```bash
npm run dev
```

✅ Frontend will start at `http://localhost:3000`

## 📚 Project Structure Setup

The repository has been initialized with:

```
AI-Study-Assistant/
├── backend/
│   ├── app/
│   │   └── __init__.py          # Flask app factory (initialized)
│   ├── requirements.txt           # Python dependencies (ready)
│   └── run.py                     # Entry point (TO CREATE)
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json               # (TO CREATE)
│   └── vite.config.ts             # (TO CREATE)
├── .env.example                   # Environment variables template
├── README.md                      # Full documentation
└── LICENSE                        # MIT License
```

## ⚙️ Configuration Files to Create

Before running, you need to create these additional files. See the [README.md](README.md) for complete code samples.

### Backend Files to Add:
- `backend/run.py` - Flask app entry point
- `backend/app/routes/` - API endpoints (auth, materials, quizzes, progress)
- `backend/app/services/` - Business logic (Gemini API, PDF parsing)
- `backend/app/models/` - Database models

### Frontend Files to Add:
- `frontend/package.json` - Dependencies
- `frontend/tsconfig.json` - TypeScript config
- `frontend/vite.config.ts` - Vite config
- `frontend/src/App.tsx` - Main React component
- `frontend/src/components/` - React components

## 🔑 Getting Your Gemini API Key

1. Go to https://aistudio.google.com
2. Click "Get API Key"
3. Create a new API key or use existing one
4. Copy the key
5. Paste it in both `.env` files:
   - `backend/.env` → `GEMINI_API_KEY=xxx`
   - `frontend/.env.local` → `VITE_GEMINI_API_KEY=xxx`

## 📝 .env File Template

Backend `.env`:
```
FLASK_ENV=development
DATABASE_URL=sqlite:///study_assistant.db
GEMINI_API_KEY=your_key_here
SECRET_KEY=dev-secret-key
FLASK_APP=run.py
```

Frontend `.env.local`:
```
VITE_API_URL=http://localhost:5000
VITE_GEMINI_API_KEY=your_key_here
```

## 🧪 Test the Setup

### Backend Health Check
```bash
curl http://localhost:5000/api/health
```
Should return: `{"status": "healthy"}`

### Frontend
Open http://localhost:3000 in your browser

## 📖 Next Steps

1. **Complete File Implementation**: Add the remaining backend and frontend files from the README
2. **Database Setup**: Run database migrations
3. **Test APIs**: Use Postman or curl to test endpoints
4. **Build Features**: Start implementing features
5. **Deploy**: Deploy to Vercel (frontend) and Render (backend)

## 🐛 Troubleshooting

### Python Module Not Found
```bash
# Make sure venv is activated and requirements are installed
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Flask runs on 5000, change in run.py if needed
# React runs on 3000, Vite will use next available if in use
```

### CORS Error
- Make sure backend is running
- Check frontend is using correct API_URL

### API Key Issues
- Verify key is correctly copied in both .env files
- Check key is valid at https://aistudio.google.com

## 📞 Support

For detailed documentation, see [README.md](README.md)

For issues, create a GitHub issue in the repository.

---

**Happy Coding! 🚀**
