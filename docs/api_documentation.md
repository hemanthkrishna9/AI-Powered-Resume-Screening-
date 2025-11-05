# API Documentation

## Base URL

```
http://localhost:8000/api/v1
```

## Authentication

All API endpoints (except health check) require authentication using JWT tokens.

```http
Authorization: Bearer <token>
```

## Endpoints

### Health Check

#### GET /health

Check API health status.

**Response**
```json
{
  "status": "healthy"
}
```

---

## Resume Management

### Upload Resume

#### POST /resumes/upload

Upload one or more resume files.

**Request**
- Content-Type: `multipart/form-data`
- Body:
  - `files`: Resume files (PDF, DOCX)
  - `job_id`: (optional) Associated job ID

**Response**
```json
{
  "success": true,
  "uploaded_count": 3,
  "resumes": [
    {
      "id": "uuid-1",
      "filename": "john_doe_resume.pdf",
      "status": "uploaded",
      "parsed": false
    }
  ]
}
```

### Parse Resume

#### POST /resumes/{resume_id}/parse

Parse uploaded resume and extract data.

**Response**
```json
{
  "id": "uuid-1",
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "skills": ["Python", "FastAPI", "Machine Learning"],
  "experience": [
    {
      "company": "Tech Corp",
      "role": "Software Engineer",
      "start_date": "2020-01",
      "end_date": "2023-12",
      "duration_years": 3.9
    }
  ],
  "education": [
    {
      "degree": "B.Tech Computer Science",
      "institution": "XYZ University",
      "year": 2019
    }
  ]
}
```

### List Resumes

#### GET /resumes

Get list of all resumes with optional filters.

**Query Parameters**
- `job_id`: Filter by job ID
- `parsed`: Filter by parse status (true/false)
- `limit`: Number of results (default: 50)
- `offset`: Pagination offset (default: 0)

**Response**
```json
{
  "total": 100,
  "limit": 50,
  "offset": 0,
  "resumes": [...]
}
```

### Get Resume Details

#### GET /resumes/{resume_id}

Get detailed information about a specific resume.

**Response**
```json
{
  "id": "uuid-1",
  "filename": "john_doe_resume.pdf",
  "uploaded_at": "2025-11-05T10:30:00Z",
  "parsed_data": {...},
  "match_scores": [...]
}
```

---

## Job Management

### Create Job

#### POST /jobs

Create a new job posting.

**Request Body**
```json
{
  "title": "Senior Python Developer",
  "description": "We are looking for an experienced Python developer...",
  "required_skills": ["Python", "FastAPI", "PostgreSQL"],
  "experience_required": 5,
  "location": "Remote"
}
```

**Response**
```json
{
  "id": "uuid-job-1",
  "title": "Senior Python Developer",
  "created_at": "2025-11-05T10:30:00Z",
  "embedding_generated": true
}
```

### List Jobs

#### GET /jobs

Get list of all job postings.

**Response**
```json
{
  "jobs": [
    {
      "id": "uuid-job-1",
      "title": "Senior Python Developer",
      "created_at": "2025-11-05T10:30:00Z",
      "candidate_count": 45
    }
  ]
}
```

---

## Candidate Matching

### Match Candidates

#### POST /match

Match resumes against a job description.

**Request Body**
```json
{
  "job_id": "uuid-job-1",
  "resume_ids": ["uuid-1", "uuid-2", "uuid-3"],
  "min_score": 0.6,
  "top_n": 10
}
```

**Response**
```json
{
  "job_id": "uuid-job-1",
  "total_candidates": 45,
  "matched_candidates": [
    {
      "candidate_id": "uuid-1",
      "name": "John Doe",
      "email": "john@example.com",
      "match_score": 0.87,
      "matching_skills": ["Python", "FastAPI", "PostgreSQL"],
      "missing_skills": ["Docker"],
      "experience_match": 0.9,
      "education_match": 0.85,
      "explanation": "Strong match: 8+ years Python experience, expert in FastAPI..."
    }
  ],
  "generated_at": "2025-11-05T10:30:00Z"
}
```

### Get Match Results

#### GET /match/{job_id}

Get cached match results for a job.

**Response**
```json
{
  "job_id": "uuid-job-1",
  "matched_candidates": [...],
  "generated_at": "2025-11-05T10:30:00Z"
}
```

---

## Interview Scheduling

### Get Availability

#### POST /scheduling/availability

Collect availability from candidate or interviewer.

**Request Body**
```json
{
  "user_id": "uuid-1",
  "user_type": "candidate",
  "available_slots": [
    {
      "start_time": "2025-11-10T10:00:00Z",
      "end_time": "2025-11-10T12:00:00Z"
    },
    {
      "start_time": "2025-11-11T14:00:00Z",
      "end_time": "2025-11-11T17:00:00Z"
    }
  ]
}
```

**Response**
```json
{
  "success": true,
  "user_id": "uuid-1",
  "slots_recorded": 2
}
```

### Find Available Slots

#### POST /scheduling/find-slots

Find available time slots for interview.

**Request Body**
```json
{
  "candidate_id": "uuid-1",
  "interviewer_id": "uuid-int-1",
  "start_date": "2025-11-10",
  "end_date": "2025-11-15",
  "duration_minutes": 60
}
```

**Response**
```json
{
  "available_slots": [
    {
      "start_time": "2025-11-10T10:00:00Z",
      "end_time": "2025-11-10T11:00:00Z",
      "score": 1.0
    }
  ]
}
```

### Schedule Interview

#### POST /scheduling/interviews

Schedule an interview.

**Request Body**
```json
{
  "candidate_id": "uuid-1",
  "interviewer_id": "uuid-int-1",
  "job_id": "uuid-job-1",
  "slot": {
    "start_time": "2025-11-10T10:00:00Z",
    "end_time": "2025-11-10T11:00:00Z"
  },
  "send_notifications": true
}
```

**Response**
```json
{
  "interview_id": "uuid-interview-1",
  "candidate_id": "uuid-1",
  "interviewer_id": "uuid-int-1",
  "scheduled_time": "2025-11-10T10:00:00Z",
  "duration_minutes": 60,
  "meeting_link": "https://meet.google.com/abc-defg-hij",
  "calendar_event_id": "google-event-123",
  "status": "scheduled",
  "notifications_sent": true
}
```

### List Interviews

#### GET /scheduling/interviews

Get list of scheduled interviews.

**Query Parameters**
- `candidate_id`: Filter by candidate
- `interviewer_id`: Filter by interviewer
- `status`: Filter by status (scheduled, completed, cancelled)
- `from_date`: Start date
- `to_date`: End date

**Response**
```json
{
  "interviews": [
    {
      "interview_id": "uuid-interview-1",
      "candidate_name": "John Doe",
      "interviewer_name": "Jane Smith",
      "job_title": "Senior Python Developer",
      "scheduled_time": "2025-11-10T10:00:00Z",
      "status": "scheduled"
    }
  ]
}
```

### Update Interview

#### PUT /scheduling/interviews/{interview_id}

Update or reschedule an interview.

**Request Body**
```json
{
  "new_slot": {
    "start_time": "2025-11-11T14:00:00Z",
    "end_time": "2025-11-11T15:00:00Z"
  },
  "send_notifications": true
}
```

### Cancel Interview

#### DELETE /scheduling/interviews/{interview_id}

Cancel a scheduled interview.

**Response**
```json
{
  "success": true,
  "interview_id": "uuid-interview-1",
  "status": "cancelled",
  "notifications_sent": true
}
```

---

## Notifications

### Send Notification

#### POST /notifications/send

Send a notification manually.

**Request Body**
```json
{
  "type": "email",
  "recipient": "john@example.com",
  "template": "interview_invite",
  "data": {
    "candidate_name": "John Doe",
    "interview_time": "2025-11-10T10:00:00Z"
  }
}
```

---

## Error Responses

All endpoints return consistent error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": {
      "field": "email",
      "issue": "Invalid email format"
    }
  }
}
```

### Error Codes

| Code | Description |
|------|-------------|
| `VALIDATION_ERROR` | Invalid input data |
| `NOT_FOUND` | Resource not found |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `INTERNAL_ERROR` | Server error |
| `RATE_LIMIT_EXCEEDED` | Too many requests |

---

## Rate Limiting

- Default: 60 requests per minute per IP
- Authenticated: 120 requests per minute per user

Headers:
```
X-RateLimit-Limit: 60
X-RateLimit-Remaining: 45
X-RateLimit-Reset: 1699200000
```

---

## Interactive Documentation

When the API server is running, access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
