PRODUCTION_DEPLOYMENT.md# Production Deployment Guide

## Docker Setup

### docker-compose.yml
```yaml
version: '3.9'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  backend:
    build: .
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/${DB_NAME}
      FLASK_ENV: production
      GEMINI_API_KEY: ${GEMINI_API_KEY}
      SECRET_KEY: ${SECRET_KEY}
    ports:
      - "5000:5000"
    depends_on:
      - db
volumes:
  postgres_data:
```

## Backend Requirements (requirements.txt)
```
Flask==2.3.0
Flask-SQLAlchemy==3.0.5
Flask-CORS==4.0.0
Flask-JWT-Extended==4.5.2
PyJWT==2.8.0
PyPDF2==3.0.1
Werkzeug==2.3.0
gunicorn==21.2.0
psycopg2-binary==2.9.7
Python-dotenv==1.0.0
google-generativeai==0.3.0
requests==2.31.0
celery==5.3.1
```

## Frontend Dockerfile
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY frontend/package.json .
RUN npm install
COPY frontend/ .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```

## CI/CD Configuration (.github/workflows/deploy.yml)
```yaml
name: Deploy to Production
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker
        run: |
          docker build -t ai-study-assistant:${{ github.sha }} .
          docker push ai-study-assistant:${{ github.sha }}
      - name: Deploy to Render
        run: |
          curl -X POST ${{ secrets.RENDER_DEPLOY_HOOK }} 
      - name: Run Tests
        run: |
          pytest backend/tests/
      - name: Security Scan
        run: |
          pip install bandit
          bandit -r backend/
```

## Environment Variables (.env.production)
```
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@db-host:5432/db-name
GEMINI_API_KEY=your_api_key
SECRET_KEY=your-secret-key-min-32-chars
DB_USER=studyassistant
DB_PASSWORD=secure_password
DB_NAME=ai_study_assistant
```

## Deployment Steps

### Local Docker Testing
```bash
docker-compose up --build
```

### Render Deployment
1. Connect GitHub repository
2. Add environment variables
3. Deploy from main branch

### Vercel Frontend Deployment  
1. Connect frontend folder
2. Set build command: `npm run build`
3. Set start command: `npm run preview`

## Security Checklist
- [ ] Environment variables in Secrets
- [ ] HTTPS enabled
- [ ] CORS configured for production
- [ ] Database backups enabled
- [ ] Rate limiting implemented
- [ ] Input validation on all endpoints
- [ ] SQL injection prevention
- [ ] XSS protection headers
- [ ] CSRF tokens enabled
- [ ] Dependency security audit

## Monitoring & Logging
```python
# Sentry Integration
import sentry_sdk
sentry_sdk.init("your-sentry-dsn")

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('app.log')]
)
```

## Database Migrations (Alembic)
```bash
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
