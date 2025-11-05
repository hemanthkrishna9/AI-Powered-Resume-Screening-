# Sample Data for Testing

This directory contains synthetic data for testing the AI Resume Screening system without external APIs.

## 📁 Directory Structure

```
data/
├── sample_jds/          # Sample job descriptions
├── sample_resumes/      # Sample candidate resumes (text format)
├── resumes/             # Uploaded resumes (auto-created)
└── vector_db/           # FAISS vector database (auto-created)
```

## 📋 Sample Job Descriptions

Located in `sample_jds/`:

1. **senior_python_developer.txt** - Senior Python role (5-8 years)
2. **data_scientist.txt** - Data Science/ML role (3-6 years)
3. **fullstack_developer.txt** - Full Stack (React + Node.js) role (3-5 years)

## 👥 Sample Resumes

Located in `sample_resumes/`:

### High Match Candidates:
1. **rajesh_kumar_python.txt** - Senior Python Developer (7 years)
   - Perfect match for Senior Python Developer JD
   - Skills: Python, FastAPI, Django, AWS, Docker, ML

2. **priya_sharma_datascience.txt** - Data Scientist (5 years)
   - Excellent match for Data Scientist JD
   - Skills: Python, TensorFlow, PyTorch, NLP, ML, AWS

3. **amit_patel_fullstack.txt** - Full Stack Developer (4 years)
   - Great match for Full Stack JD
   - Skills: React, Node.js, MongoDB, AWS, TypeScript

### Moderate Match Candidates:
4. **sneha_reddy_junior.txt** - Junior Developer (1.5 years)
   - Partial match for Python roles
   - Skills: Python, Flask, MySQL

5. **vikram_singh_devops.txt** - DevOps Engineer (6 years)
   - Moderate match for backend roles
   - Skills: Java, Kubernetes, Docker, AWS

## 🧪 How to Test

### Option 1: Using Streamlit UI

1. **Start the app:**
   ```bash
   streamlit run frontend/streamlit_app.py
   ```

2. **Upload resumes:**
   - Go to "Upload Resumes" tab
   - Copy contents from `sample_resumes/*.txt` into new `.txt` files
   - Upload those files (or convert to PDF first)

3. **Match candidates:**
   - Go to "Match Candidates" tab
   - Copy content from any `sample_jds/*.txt` file
   - Paste into Job Description field
   - Click "Start Matching"

4. **View results:**
   - Go to "Top Candidates" tab
   - See AI-powered rankings and explanations

### Option 2: Programmatic Testing

```python
from pathlib import Path
from src.resume_parser.parser import ResumeParser
from src.resume_parser.extractor import DataExtractor
from src.ai_matcher.matcher import ResumeMatcher

# Parse resume
parser = ResumeParser()
extractor = DataExtractor()

resume_path = Path("data/sample_resumes/rajesh_kumar_python.txt")
parsed = parser.parse(resume_path)
resume_data = extractor.extract_all(parsed['raw_text'])

# Load JD
jd_path = Path("data/sample_jds/senior_python_developer.txt")
job_description = jd_path.read_text()

# Match
matcher = ResumeMatcher()
result = matcher.match_resume_to_jd(resume_data, job_description)

print(f"Match Score: {result['match_score']}")
print(f"Explanation: {result['explanation']}")
```

## 📊 Expected Match Results

When matching resumes to the **Senior Python Developer** JD:

| Candidate | Expected Score | Reason |
|-----------|---------------|--------|
| Rajesh Kumar | 85-95% | Perfect match - Senior Python, FastAPI, AWS, 7 years |
| Priya Sharma | 70-80% | Good skills overlap - Python, ML, Cloud |
| Amit Patel | 50-65% | Moderate - Node.js not Python, but full stack |
| Sneha Reddy | 35-50% | Junior with Python but limited experience |
| Vikram Singh | 45-60% | DevOps focus, some Python, good experience |

## 🔄 Generating More Data

To create more synthetic candidates, you can:

1. **Manually create** new `.txt` files following the format
2. **Use AI tools** like ChatGPT to generate realistic resumes
3. **Modify existing** resumes by changing names, skills, experience

## 📝 Resume Format

Each resume should include:

```
NAME
Title/Role

Contact Information:
- Email
- Phone
- LinkedIn
- GitHub
- Location

PROFESSIONAL SUMMARY
Brief overview of experience and skills

TECHNICAL SKILLS
List of technologies, tools, and skills

PROFESSIONAL EXPERIENCE
Company | Location | Dates
- Responsibilities and achievements
- Technologies used

EDUCATION
Degree | University | Year | GPA

CERTIFICATIONS (optional)
List of certifications

PROJECTS (optional)
Project descriptions

ACHIEVEMENTS (optional)
Notable accomplishments

LANGUAGES (optional)
Language proficiencies
```

## 🚫 No External APIs Required

This sample data allows you to:
- ✅ Test the complete resume screening workflow
- ✅ Demo the system without Naukri API access
- ✅ Develop and validate features offline
- ✅ Run automated tests

## 💡 Tips

1. **Variety**: Create resumes with different experience levels
2. **Realism**: Use realistic job titles, companies, and technologies
3. **Skills**: Vary skill sets to test matching accuracy
4. **Format**: Keep consistent formatting for better parsing
5. **Convert to PDF**: You can convert `.txt` files to PDF for more realistic testing

## 🔧 Troubleshooting

**Issue**: Resumes not parsing correctly
- **Solution**: Check file format, ensure UTF-8 encoding

**Issue**: Low match scores for expected candidates
- **Solution**: Check skill keywords match between resume and JD

**Issue**: AI explanations not generated
- **Solution**: Verify Azure OpenAI credentials in `.env` file

---

For questions or issues, refer to the main project README.md
