# AI-Powered Resume Screening & Interview Scheduling

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> An intelligent end-to-end AI hiring assistant that automates resume screening, candidate ranking, and interview scheduling for recruiters.

---

## 📋 Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Overview](#solution-overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Azure Deployment](#azure-deployment)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Problem Statement

Recruiters in large organizations face significant challenges:

- **Manual Resume Processing**: Spending hours downloading and parsing 100+ resumes from job portals like Naukri for every role
- **Time-Consuming Screening**: Manually comparing resumes against job descriptions
- **Scheduling Overhead**: Playing email/phone tag with candidates (3-5 back-and-forth messages per candidate)
- **Candidate Dropouts**: Losing good candidates due to slow response times
- **Strategic Task Limitation**: Keeping recruiters away from high-value activities like improving talent quality

### Impact
- Delayed hiring timelines
- Frustrated candidate experience
- Reduced recruiter productivity
- Missed opportunities with top talent

---

## 💡 Solution Overview

An **end-to-end AI hiring assistant** that streamlines the entire recruitment workflow:

1. **Automated Resume Fetching**: Integrates with Naukri portal APIs (Resdex) to automatically retrieve resumes
2. **Intelligent Parsing**: Extracts structured data (skills, experience, education) from resumes
3. **AI-Powered Matching**: Uses embeddings and vector similarity to rank candidates against job descriptions
4. **Transparent Scoring**: Provides explainable AI results showing why candidates were shortlisted
5. **Automated Scheduling**: Handles interview scheduling by matching candidate and interviewer availability
6. **Smart Notifications**: Sends calendar invites, reminders, and updates automatically

### Workflow
```
Upload JD → AI Ranks Candidates → Review Shortlist → Click "Schedule Interview" → System Handles Rest
```

---

## ✨ Key Features

### Resume Processing
- 📄 Automatic resume fetching from job portals
- 🔍 Intelligent parsing (PDF, DOCX formats)
- 📊 Structured data extraction (skills, experience, education, contact info)

### AI-Powered Matching
- 🤖 Semantic matching using sentence transformers
- 📈 Percentage-based candidate ranking
- 💡 Explainable AI (highlights matching skills, keywords, experience)
- 🎯 Customizable matching criteria

### Interview Scheduling
- 📅 Automatic availability collection from candidates
- 🔄 Calendar integration (Google Calendar, Outlook)
- ⚡ Smart slot matching algorithm
- 📧 Automated invite generation with meeting links

### Notifications & Reminders
- ✉️ Email notifications (SMTP)
- 📱 Optional Telegram/WhatsApp bot integration
- ⏰ Automated reminders before interviews
- 🔔 Status update notifications

### Recruiter Dashboard
- 📊 Visual candidate rankings
- 🔍 Detailed candidate profiles
- 📋 Interview scheduling interface
- 📈 Analytics and insights

---

## 🏗 Architecture

```
┌─────────────────┐
│  Job Portal API │ (Naukri Resdex)
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────────────────────────────┐
│                   Backend Services                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  │
│  │   Resume     │  │  AI Matcher  │  │  Scheduler   │  │
│  │   Parser     │→ │  (Embeddings)│→ │  (Calendar)  │  │
│  └──────────────┘  └──────────────┘  └──────────────┘  │
│          ↓                 ↓                  ↓          │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Vector Database (FAISS)                │  │
│  └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
         ↓                                      ↓
┌─────────────────┐                  ┌─────────────────┐
│  FastAPI/Flask  │                  │  Notification   │
│   REST API      │                  │    Service      │
└────────┬────────┘                  └─────────────────┘
         │
         ↓
┌─────────────────┐
│  Streamlit/     │
│  React Frontend │
└─────────────────┘
```

---

## 🛠 Tech Stack

### Backend
- **Web Framework**: FastAPI / Flask
- **Task Queue**: Celery (for async operations)
- **Database**: PostgreSQL / SQLite (candidate data)
- **Vector Database**: FAISS / Weaviate (embeddings)

### AI/ML
- **Resume Parsing**: PyResparser, spaCy, PyMuPDF, pdfminer.six
- **Embeddings**: Sentence-Transformers (MiniLM/mpnet)
- **NLP**: spaCy, NLTK

### Integrations
- **Calendar APIs**: Google Calendar API, Microsoft Graph API
- **Email**: SMTP (email notifications)
- **Messaging**: python-telegram-bot (optional)
- **Scheduling**: APScheduler (reminders)

### Frontend
- **Quick Demo**: Streamlit
- **Production**: React + Material UI (optional)

### Development
- **Language**: Python 3.8+
- **Testing**: pytest, unittest
- **Documentation**: Sphinx
- **Version Control**: Git

---

## 📁 Project Structure

```
AI-Powered-Resume-Screening/
├── README.md                      # This file
├── requirements.txt               # Python dependencies
├── .gitignore                    # Git ignore rules
├── .env.example                  # Environment variables template
│
├── config/                       # Configuration files
│   ├── __init__.py
│   └── settings.py              # App settings and constants
│
├── src/                         # Source code
│   ├── __init__.py
│   │
│   ├── resume_parser/           # Resume parsing module
│   │   ├── __init__.py
│   │   ├── parser.py           # Main parsing logic
│   │   └── extractor.py        # Data extraction utilities
│   │
│   ├── ai_matcher/             # AI matching engine
│   │   ├── __init__.py
│   │   ├── embeddings.py       # Generate embeddings
│   │   ├── matcher.py          # Matching algorithm
│   │   └── ranker.py           # Candidate ranking
│   │
│   ├── scheduler/              # Interview scheduling
│   │   ├── __init__.py
│   │   ├── calendar_integration.py  # Calendar API integration
│   │   ├── availability_collector.py # Collect availability
│   │   └── scheduler.py        # Scheduling logic
│   │
│   ├── notifications/          # Notification services
│   │   ├── __init__.py
│   │   ├── email_notifier.py  # Email notifications
│   │   └── reminder_service.py # Automated reminders
│   │
│   ├── api/                    # REST API
│   │   ├── __init__.py
│   │   ├── main.py            # FastAPI application
│   │   ├── routes/            # API endpoints
│   │   │   ├── __init__.py
│   │   │   ├── resume.py     # Resume endpoints
│   │   │   ├── matching.py   # Matching endpoints
│   │   │   └── scheduling.py # Scheduling endpoints
│   │   └── models/           # Data models
│   │       ├── __init__.py
│   │       ├── candidate.py  # Candidate model
│   │       ├── job.py        # Job description model
│   │       └── interview.py  # Interview model
│   │
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       └── helpers.py         # Helper functions
│
├── frontend/                   # Frontend application
│   ├── streamlit_app.py       # Streamlit main app
│   └── components/            # UI components
│       ├── __init__.py
│       ├── dashboard.py       # Main dashboard
│       ├── candidate_list.py  # Candidate list view
│       └── scheduler_ui.py    # Scheduling interface
│
├── data/                      # Data directory
│   ├── sample_resumes/       # Sample resume files
│   └── sample_jds/           # Sample job descriptions
│
├── tests/                     # Unit and integration tests
│   ├── __init__.py
│   ├── test_parser.py
│   ├── test_matcher.py
│   └── test_scheduler.py
│
├── docs/                      # Documentation
│   ├── architecture.md       # Architecture details
│   ├── api_documentation.md  # API reference
│   └── setup_guide.md        # Detailed setup guide
│
└── scripts/                   # Utility scripts
    ├── setup.sh              # Setup script
    ├── run_dev.sh           # Development server script
    └── azure_setup.sh       # Azure deployment script
```

---

## ⚡ Quick Start

Get started in 5 minutes! See [QUICKSTART.md](QUICKSTART.md) for detailed guide.

```bash
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Run the app
streamlit run frontend/streamlit_app.py

# 3. Test with sample data
# - Upload resumes from data/sample_resumes/
# - Use job descriptions from data/sample_jds/
# - View AI-powered match results!
```

**Access the app:** http://localhost:8501

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git
- (Optional) Virtual environment tool (venv, conda)

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd AI-Powered-Resume-Screening-
```

### Step 2: Create Virtual Environment
```bash
# Using venv
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Step 4: Configure Environment Variables
```bash
cp .env.example .env
# Edit .env file with your configurations
```

### Step 5: Run Setup Script
```bash
chmod +x scripts/setup.sh
./scripts/setup.sh
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Application Settings
APP_NAME=AI Resume Screener
APP_VERSION=1.0.0
DEBUG=True

# API Settings
API_HOST=0.0.0.0
API_PORT=8000

# Database
DATABASE_URL=sqlite:///./resume_screening.db

# Google Calendar API
GOOGLE_CALENDAR_CREDENTIALS_PATH=./credentials/google_calendar.json

# Microsoft Graph API (Outlook)
MICROSOFT_CLIENT_ID=your_client_id
MICROSOFT_CLIENT_SECRET=your_client_secret
MICROSOFT_TENANT_ID=your_tenant_id

# Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password

# AI Model Settings
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
VECTOR_DB_PATH=./data/vector_db

# Naukri API (Resdex)
NAUKRI_API_KEY=your_api_key
NAUKRI_API_SECRET=your_api_secret

# Optional: Telegram Bot
TELEGRAM_BOT_TOKEN=your_bot_token
```

---

## 📖 Usage

### Starting the Backend API

```bash
# Development mode
python src/api/main.py

# Or using uvicorn directly
uvicorn src.api.main:app --reload --host 0.0.0.0 --port 8000
```

### Starting the Frontend

```bash
# Streamlit Dashboard
streamlit run frontend/streamlit_app.py
```

### Basic Workflow

1. **Upload Job Description**
   - Navigate to the dashboard
   - Upload or paste a job description

2. **Fetch/Upload Resumes**
   - Automatically fetch from Naukri API
   - Or manually upload resume files

3. **Review AI Rankings**
   - View ranked candidate list
   - Check match percentages and explanations

4. **Schedule Interviews**
   - Select candidates to interview
   - System collects availability and schedules automatically

5. **Track Progress**
   - Monitor interview statuses
   - View analytics and insights

---

## ☁️ Azure Deployment

Deploy to Azure App Service in minutes! See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md) for complete guide.

### Quick Deploy

```bash
# Run automated setup script
chmod +x scripts/azure_setup.sh
./scripts/azure_setup.sh
```

Or deploy manually:

```bash
# 1. Create Azure resources
az group create --name rg-resume-screener --location eastus
az appservice plan create --name plan-resume-screener --resource-group rg-resume-screener --is-linux --sku B1
az webapp create --resource-group rg-resume-screener --plan plan-resume-screener --name ai-resume-screener --runtime "PYTHON:3.10"

# 2. Configure environment variables
az webapp config appsettings set --resource-group rg-resume-screener --name ai-resume-screener \
  --settings AZURE_OPENAI_ENDPOINT="YOUR_ENDPOINT" AZURE_OPENAI_API_KEY="YOUR_KEY"

# 3. Deploy code
az webapp up --name ai-resume-screener --resource-group rg-resume-screener
```

**Features:**
- ✅ Docker container support
- ✅ Auto-scaling capabilities
- ✅ CI/CD with GitHub Actions
- ✅ Application Insights monitoring
- ✅ HTTPS enabled by default

**Deployment Options:**
1. **Azure App Service** (Recommended) - See [AZURE_DEPLOYMENT.md](AZURE_DEPLOYMENT.md)
2. **Docker Container** - Use provided `Dockerfile`
3. **GitHub Actions** - CI/CD workflow in `.github/workflows/azure-deploy.yml`

---

## 📚 API Documentation

Once the server is running, access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

```
POST   /api/v1/jobs              Create new job posting
POST   /api/v1/resumes/upload    Upload resume files
GET    /api/v1/resumes/fetch     Fetch resumes from portal
POST   /api/v1/match             Match resumes to job
GET    /api/v1/candidates        List ranked candidates
POST   /api/v1/interviews        Schedule interview
GET    /api/v1/interviews/{id}   Get interview details
```

See [docs/api_documentation.md](docs/api_documentation.md) for detailed API reference.

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_matcher.py

# Run with verbose output
pytest -v
```

---

## 👥 Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints where applicable
- Write docstrings for all functions and classes

### Git Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add your feature description"

# Push to remote
git push origin feature/your-feature-name
```

### Commit Message Convention
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 📊 Evaluation Criteria

This system is designed to be evaluated on:

1. **Task Success Rate**: Accuracy of candidate matching to JD
2. **Efficiency Gain**: % reduction in manual recruiter effort
3. **Scheduling Accuracy**: Interviews fixed without manual intervention
4. **Explainability**: Clear reasoning for candidate shortlisting
5. **Candidate Experience**: Seamless and fast scheduling process

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'feat: Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **ITC Infotech** for the problem statement and opportunity
- Open source community for amazing tools and libraries
- Contributors and maintainers of this project

---

## 📞 Contact & Support

For questions, issues, or suggestions:

- Create an issue on GitHub
- Email: [your-email@example.com]
- Documentation: [docs/](docs/)

---

## 🗺️ Roadmap

### Phase 1 (Current)
- [x] Project setup and structure
- [ ] Resume parser implementation
- [ ] AI matching engine
- [ ] Basic scheduling functionality

### Phase 2
- [ ] Advanced calendar integration
- [ ] Multi-language resume support
- [ ] Enhanced explainability dashboard
- [ ] Performance optimization

### Phase 3
- [ ] React frontend
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Enterprise features

---

**©2025 ITC Infotech. All Rights Reserved.**

---

*Built with ❤️ using Python and AI*
