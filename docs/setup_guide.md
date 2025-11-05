# Detailed Setup Guide

This guide provides comprehensive instructions for setting up the AI-Powered Resume Screening & Interview Scheduling system.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [System Requirements](#system-requirements)
3. [Installation Steps](#installation-steps)
4. [Configuration](#configuration)
5. [Database Setup](#database-setup)
6. [External Service Integration](#external-service-integration)
7. [Running the Application](#running-the-application)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software

1. **Python 3.8 or higher**
   ```bash
   python --version
   # Should output: Python 3.8.x or higher
   ```

2. **pip (Python package manager)**
   ```bash
   pip --version
   ```

3. **Git**
   ```bash
   git --version
   ```

4. **Virtual Environment Tool** (recommended)
   - venv (comes with Python)
   - or conda

### Optional but Recommended

- **Docker** (for containerized deployment)
- **PostgreSQL** (for production database)
- **Redis** (for Celery task queue)

---

## System Requirements

### Minimum Requirements

- **OS**: Linux, macOS, or Windows 10+
- **RAM**: 4 GB
- **Disk Space**: 5 GB free space
- **CPU**: Dual-core processor

### Recommended Requirements

- **OS**: Ubuntu 20.04+ or macOS 12+
- **RAM**: 8 GB or more
- **Disk Space**: 10 GB free space
- **CPU**: Quad-core processor
- **GPU**: (Optional) For faster embedding generation

---

## Installation Steps

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd AI-Powered-Resume-Screening-
```

### Step 2: Create Virtual Environment

#### Using venv (Python's built-in)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### Using conda

```bash
# Create conda environment
conda create -n resume-screener python=3.10

# Activate conda environment
conda activate resume-screener
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install required packages
pip install -r requirements.txt
```

This will install all necessary packages including:
- FastAPI
- Streamlit
- Sentence Transformers
- spaCy
- and many more...

### Step 4: Download spaCy Language Model

```bash
# Download English language model
python -m spacy download en_core_web_sm

# For better accuracy (larger model):
# python -m spacy download en_core_web_md
```

### Step 5: Create Required Directories

```bash
# Create directories for data storage
mkdir -p data/resumes data/vector_db logs credentials
```

---

## Configuration

### Step 1: Copy Environment Template

```bash
cp .env.example .env
```

### Step 2: Edit Environment Variables

Open `.env` file and configure:

#### Basic Settings

```env
APP_NAME=AI Resume Screener
DEBUG=True
SECRET_KEY=your-random-secret-key-here
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Database Configuration

For development (SQLite - default):
```env
DATABASE_URL=sqlite:///./resume_screening.db
```

For production (PostgreSQL):
```env
DATABASE_URL=postgresql://user:password@localhost:5432/resume_screening
```

#### Email Configuration

For Gmail:
```env
SMTP_ENABLED=True
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
EMAIL_FROM=your_email@gmail.com
```

**Note**: For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833).

---

## Database Setup

### SQLite (Development)

No setup required. Database file will be created automatically on first run.

### PostgreSQL (Production)

#### 1. Install PostgreSQL

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### 2. Create Database

```bash
# Login to PostgreSQL
sudo -u postgres psql

# Create database and user
CREATE DATABASE resume_screening;
CREATE USER screener WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE resume_screening TO screener;

# Exit
\q
```

#### 3. Run Migrations

```bash
# TODO: Add migration commands when implemented
# alembic upgrade head
```

---

## External Service Integration

### Google Calendar Integration

#### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google Calendar API

#### 2. Create Credentials

1. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client ID"
2. Select "Desktop App"
3. Download credentials JSON
4. Save as `credentials/google_calendar.json`

#### 3. Update .env

```env
GOOGLE_CALENDAR_ENABLED=True
GOOGLE_CALENDAR_CREDENTIALS_PATH=./credentials/google_calendar.json
```

### Microsoft Outlook Integration

#### 1. Register Application

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" → "App registrations"
3. Create new registration

#### 2. Configure API Permissions

Add permissions:
- `Calendars.ReadWrite`
- `User.Read`

#### 3. Update .env

```env
MICROSOFT_CALENDAR_ENABLED=True
MICROSOFT_CLIENT_ID=your_client_id
MICROSOFT_CLIENT_SECRET=your_client_secret
MICROSOFT_TENANT_ID=your_tenant_id
```

### Naukri API Integration

Contact Naukri for API access and credentials.

```env
NAUKRI_API_ENABLED=True
NAUKRI_API_KEY=your_api_key
NAUKRI_API_SECRET=your_api_secret
```

---

## Running the Application

### Backend API

#### Development Mode

```bash
# Navigate to src/api directory
cd src/api

# Run with uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Or use the provided script:
```bash
chmod +x scripts/run_dev.sh
./scripts/run_dev.sh
```

Access API documentation:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

#### Production Mode

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Frontend (Streamlit)

In a new terminal:

```bash
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Run Streamlit app
streamlit run frontend/streamlit_app.py
```

Access dashboard: http://localhost:8501

### Background Workers (Celery)

If using Celery for task queue:

```bash
# Start Redis
redis-server

# Start Celery worker
celery -A src.tasks worker --loglevel=info
```

---

## Verification

### 1. Test API

```bash
curl http://localhost:8000/health
# Should return: {"status": "healthy"}
```

### 2. Test Streamlit

Open http://localhost:8501 in browser

### 3. Test Resume Parsing

```bash
# Upload a test resume via Streamlit UI
# or
curl -X POST "http://localhost:8000/api/v1/resumes/upload" \
  -F "file=@path/to/resume.pdf"
```

---

## Troubleshooting

### Common Issues

#### 1. Port Already in Use

```bash
# Find process using port 8000
lsof -i :8000  # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill process
kill -9 <PID>  # macOS/Linux
taskkill /PID <PID> /F  # Windows
```

#### 2. Module Not Found Errors

```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

#### 3. spaCy Model Not Found

```bash
python -m spacy download en_core_web_sm
```

#### 4. Database Connection Error

Check:
- PostgreSQL is running: `sudo service postgresql status`
- Credentials in `.env` are correct
- Database exists: `psql -l`

#### 5. SMTP Authentication Error

For Gmail:
- Enable 2-factor authentication
- Generate App Password
- Use App Password in `.env`, not your regular password

### Logs

Check logs for errors:
```bash
# Application logs
tail -f logs/app.log

# Streamlit logs
# Check terminal where streamlit is running
```

---

## Docker Deployment (Optional)

### Create Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m spacy download en_core_web_sm

COPY . .

EXPOSE 8000

CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build image
docker build -t resume-screener .

# Run container
docker run -p 8000:8000 --env-file .env resume-screener
```

---

## Next Steps

After successful setup:

1. Upload sample resumes
2. Create job descriptions
3. Test matching functionality
4. Configure calendar integration
5. Test interview scheduling
6. Review analytics

---

## Getting Help

- Check logs in `logs/app.log`
- Review documentation in `docs/`
- Create an issue on GitHub
- Contact support team

---

## Security Checklist

Before production deployment:

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Use strong database password
- [ ] Enable HTTPS
- [ ] Configure firewall rules
- [ ] Set up rate limiting
- [ ] Enable authentication
- [ ] Review CORS settings
- [ ] Encrypt sensitive data
- [ ] Regular security updates
- [ ] Backup strategy in place
