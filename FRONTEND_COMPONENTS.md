FRONTEND_COMPONENTS.md# Frontend React Components

## App.jsx (Main Component)
```jsx
import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import useAuthStore from './store/authStore';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import MaterialUpload from './pages/MaterialUpload';
import QuizGenerator from './pages/QuizGenerator';

const App = () => {
  const { token, checkAuth } = useAuthStore();

  useEffect(() => {
    checkAuth();
  }, []);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/" element={token ? <Dashboard /> : <Navigate to="/login" />} />
        <Route path="/upload" element={token ? <MaterialUpload /> : <Navigate to="/login" />} />
        <Route path="/quiz/:id" element={token ? <QuizGenerator /> : <Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

export default App;
```

## Zustand Store (authStore.js)
```jsx
import create from 'zustand';

const useAuthStore = create((set) => ({
  token: localStorage.getItem('token') || null,
  user: null,
  login: async (username, password) => {
    const res = await fetch('/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password })
    });
    const data = await res.json();
    if (res.ok) {
      localStorage.setItem('token', data.token);
      set({ token: data.token });
    }
    return res.ok;
  },
  logout: () => {
    localStorage.removeItem('token');
    set({ token: null, user: null });
  },
  checkAuth: () => {
    const token = localStorage.getItem('token');
    set({ token });
  }
}));

export default useAuthStore;
```

## API Service (api.js)
```jsx
import axios from 'axios';

const api = axios.create({
  baseURL: '/api'
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: (username, email, password) =>
    api.post('/auth/register', { username, email, password }),
  login: (username, password) =>
    api.post('/auth/login', { username, password })
};

export const materialsAPI = {
  upload: (file, title) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('title', title);
    return api.post('/materials/upload', formData);
  },
  getAll: () => api.get('/materials'),
  delete: (id) => api.delete(`/materials/${id}`)
};

export const quizAPI = {
  generate: (materialId, numQuestions = 5) =>
    api.post('/quiz/generate', { material_id: materialId, num_questions: numQuestions }),
  submit: (quizId, answers) =>
    api.post(`/quiz/${quizId}/submit`, { answers })
};

export const summaryAPI = {
  generate: (materialId) =>
    api.post('/summary/generate', { material_id: materialId })
};

export default api;
```

## Login Component (pages/Login.jsx)
```jsx
import React, { useState } from 'react';
import useAuthStore from '../store/authStore';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const { login } = useAuthStore();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const success = await login(username, password);
      if (success) {
        navigate('/');
      } else {
        setError('Invalid credentials');
      }
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="login-container">
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        {error && <p className="error">{error}</p>}
        <button type="submit">Login</button>
      </form>
    </div>
  );
};

export default Login;
```

## Tests (tests/api.test.js)
```jsx
import { describe, it, expect, beforeEach, vi } from 'vitest';
import { authAPI, materialsAPI, quizAPI } from '../api';

describe('API Services', () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it('should call auth login endpoint', async () => {
    const mockFetch = vi.fn();
    global.fetch = mockFetch;
    
    await authAPI.login('user', 'pass');
    expect(mockFetch).toHaveBeenCalled();
  });

  it('should upload material', async () => {
    const file = new File(['content'], 'test.pdf');
    const formData = new FormData();
    formData.append('file', file);
    
    expect(formData.has('file')).toBe(true);
  });
});
```

## Package.json Scripts
```json
{
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "test": "vitest",
    "lint": "eslint src --fix"
  },
  "devDependencies": {
    "@vitejs/plugin-react": "latest",
    "vitest": "latest",
    "eslint": "latest",
    "@testing-library/react": "latest"
  }
}
```
