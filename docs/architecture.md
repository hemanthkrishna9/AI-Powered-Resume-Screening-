# Architecture Documentation

## System Architecture

### Overview

The AI-Powered Resume Screening & Interview Scheduling system follows a modular, layered architecture designed for scalability, maintainability, and extensibility.

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                        Presentation Layer                        │
│  ┌──────────────────┐           ┌──────────────────────────┐   │
│  │  Streamlit UI    │           │    REST API Clients      │   │
│  │  (Dashboard)     │           │  (Mobile/Web Apps)       │   │
│  └──────────────────┘           └──────────────────────────┘   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                         API Layer                                │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              FastAPI REST API                             │  │
│  │  ┌──────────┐  ┌──────────┐  ┌────────────────────┐     │  │
│  │  │ Resume   │  │ Matching │  │    Scheduling      │     │  │
│  │  │ Routes   │  │  Routes  │  │     Routes         │     │  │
│  │  └──────────┘  └──────────┘  └────────────────────┘     │  │
│  └──────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                      Business Logic Layer                        │
│  ┌───────────────┐  ┌───────────────┐  ┌──────────────────┐   │
│  │ Resume Parser │  │  AI Matcher   │  │    Scheduler     │   │
│  │               │  │               │  │                  │   │
│  │ - PDF Parse   │  │ - Embeddings  │  │ - Slot Finding   │   │
│  │ - DOCX Parse  │  │ - Similarity  │  │ - Calendar Sync  │   │
│  │ - Extraction  │  │ - Ranking     │  │ - Availability   │   │
│  └───────────────┘  └───────────────┘  └──────────────────┘   │
│                                                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │              Notification Service                         │ │
│  │  - Email Notifier  - Reminder Service                     │ │
│  └───────────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                       Data Layer                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │  Relational  │  │  Vector DB   │  │  File Storage        │  │
│  │  Database    │  │  (FAISS)     │  │  (Local/S3)          │  │
│  │ (PostgreSQL) │  │              │  │                      │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                            │
┌───────────────────────────▼─────────────────────────────────────┐
│                    External Services                             │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐  │
│  │ Google       │  │  Microsoft   │  │  Job Portal APIs     │  │
│  │ Calendar API │  │  Graph API   │  │  (Naukri Resdex)     │  │
│  └──────────────┘  └──────────────┘  └──────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

## Component Descriptions

### 1. Resume Parser Module

**Purpose**: Extract structured data from resume files

**Components**:
- `ResumeParser`: Main parsing engine
- `DataExtractor`: NLP-based data extraction

**Technologies**:
- PyMuPDF (PDF parsing)
- python-docx (DOCX parsing)
- spaCy (NLP processing)

**Data Flow**:
1. Accept resume file (PDF/DOCX)
2. Extract raw text
3. Parse structured fields (skills, experience, education)
4. Store in database

### 2. AI Matcher Module

**Purpose**: Match and rank candidates against job descriptions

**Components**:
- `EmbeddingGenerator`: Generate semantic embeddings
- `ResumeMatcher`: Calculate similarity scores
- `CandidateRanker`: Rank and filter candidates

**Technologies**:
- Sentence Transformers (embeddings)
- FAISS (vector similarity search)
- NumPy/Scikit-learn (computations)

**Algorithm**:
```python
1. Generate JD embedding
2. Generate resume embeddings (batch)
3. Compute cosine similarity
4. Rank by similarity score
5. Apply filters (min score, required skills)
6. Return top N candidates with explanations
```

### 3. Scheduler Module

**Purpose**: Automate interview scheduling

**Components**:
- `InterviewScheduler`: Core scheduling logic
- `CalendarIntegration`: Calendar API integration
- `AvailabilityCollector`: Collect availability data

**Technologies**:
- Google Calendar API
- Microsoft Graph API
- APScheduler

**Workflow**:
1. Collect candidate availability
2. Fetch interviewer calendar
3. Find matching time slots
4. Create calendar event
5. Send notifications

### 4. Notification Service

**Purpose**: Send automated notifications

**Components**:
- `EmailNotifier`: Email sending
- `ReminderService`: Scheduled reminders

**Technologies**:
- SMTP (email)
- APScheduler (background tasks)

**Types**:
- Interview invitations
- Confirmations
- Reminders (24h, 2h before)
- Status updates

## Data Models

### Candidate
```python
{
    "id": "uuid",
    "name": "string",
    "email": "string",
    "phone": "string",
    "skills": ["string"],
    "experience": [
        {
            "company": "string",
            "role": "string",
            "duration": "string"
        }
    ],
    "education": [
        {
            "degree": "string",
            "institution": "string",
            "year": "int"
        }
    ],
    "resume_path": "string",
    "created_at": "datetime"
}
```

### Job Description
```python
{
    "id": "uuid",
    "title": "string",
    "description": "string",
    "required_skills": ["string"],
    "experience_required": "int",
    "embedding": "array",
    "created_at": "datetime"
}
```

### Interview
```python
{
    "id": "uuid",
    "candidate_id": "uuid",
    "interviewer_id": "uuid",
    "job_id": "uuid",
    "scheduled_time": "datetime",
    "duration": "int",
    "meeting_link": "string",
    "status": "enum",
    "created_at": "datetime"
}
```

## Security Considerations

1. **Authentication**: JWT-based API authentication
2. **Authorization**: Role-based access control (RBAC)
3. **Data Privacy**: Encryption at rest and in transit
4. **API Rate Limiting**: Prevent abuse
5. **Input Validation**: Sanitize all inputs
6. **Secure File Upload**: Validate file types and sizes

## Scalability

### Horizontal Scaling
- Stateless API design
- Load balancer ready
- Distributed task queue (Celery)

### Performance Optimization
- Batch processing for embeddings
- Caching (Redis)
- Database indexing
- Async operations

## Deployment Architecture

```
┌──────────────┐
│ Load Balancer│
└──────┬───────┘
       │
   ┌───┴────┬──────────┐
   │        │          │
┌──▼──┐ ┌──▼──┐  ┌───▼───┐
│API  │ │API  │  │ API   │
│Node1│ │Node2│  │ Node3 │
└──┬──┘ └──┬──┘  └───┬───┘
   │       │         │
   └───────┼─────────┘
           │
    ┌──────▼──────┐
    │  Database   │
    │  (Primary)  │
    └──────┬──────┘
           │
    ┌──────▼──────┐
    │  Database   │
    │  (Replica)  │
    └─────────────┘
```

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit / React |
| API | FastAPI |
| Task Queue | Celery + Redis |
| Database | PostgreSQL |
| Vector DB | FAISS |
| AI/ML | Sentence Transformers, spaCy |
| Calendar | Google Calendar, MS Graph |
| Email | SMTP |
| Deployment | Docker, Kubernetes |

## Future Enhancements

1. **Multi-language support**: Support resumes in multiple languages
2. **Video interviews**: Integration with Zoom/Teams
3. **Advanced analytics**: ML-based hiring insights
4. **Mobile app**: Native mobile applications
5. **Chatbot integration**: WhatsApp/Telegram for candidate interaction
