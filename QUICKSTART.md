# 🚀 Quick Start Guide

Get the AI Resume Screening system running in 5 minutes!

---

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

---

## ⚡ Quick Setup (3 Steps)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd AI-Powered-Resume-Screening-

# Install Python packages
pip install -r requirements.txt

# Download spaCy language model
python -m spacy download en_core_web_sm
```

### Step 2: Configure Environment

The `.env` file is already configured with Azure OpenAI credentials and sample data settings. No changes needed!

✅ Azure OpenAI is ready
✅ Sample data is enabled
✅ All settings configured

### Step 3: Run the App

```bash
# Start Streamlit dashboard
streamlit run frontend/streamlit_app.py
```

The app will open in your browser at: **http://localhost:8501**

---

## 🎯 Test with Sample Data

### Option A: Use Sample Resume Text Files

1. Open `data/sample_resumes/` folder
2. Copy content from any `.txt` file (e.g., `rajesh_kumar_python.txt`)
3. Create a new `.txt` file on your desktop
4. Paste the content and save
5. Upload this file in the Streamlit app

### Option B: Quick Test Flow

1. **Go to "Upload Resumes" tab**
   - Copy text from `data/sample_resumes/rajesh_kumar_python.txt`
   - Save as a new `.txt` file
   - Upload the file
   - Click "Parse Resumes"

2. **Go to "Match Candidates" tab**
   - Copy text from `data/sample_jds/senior_python_developer.txt`
   - Paste into the Job Description field
   - Add required skills: `Python, FastAPI, Docker, AWS`
   - Click "Start Matching"

3. **Go to "Top Candidates" tab**
   - See AI-powered match results!
   - View match scores, explanations, and skill analysis

---

## 📊 Sample Data Available

### Job Descriptions (`data/sample_jds/`)
- `senior_python_developer.txt` - Python role (5-8 years)
- `data_scientist.txt` - ML/AI role (3-6 years)
- `fullstack_developer.txt` - React + Node.js role (3-5 years)

### Resumes (`data/sample_resumes/`)
- `rajesh_kumar_python.txt` - Senior Python Dev (Excellent match for Python JD)
- `priya_sharma_datascience.txt` - Data Scientist (Perfect for DS JD)
- `amit_patel_fullstack.txt` - Full Stack Dev (Great for Full Stack JD)
- `sneha_reddy_junior.txt` - Junior Developer (Moderate match)
- `vikram_singh_devops.txt` - DevOps Engineer (Partial match)

---

## 🎨 What You'll See

### Beautiful UI Features:
- 🌈 **Gradient backgrounds** and modern design
- 📊 **Animated metric cards** showing statistics
- 🎯 **Color-coded match scores**:
  - 🟢 Green (80%+): Excellent match
  - 🔵 Blue (60-80%): Good match
  - 🟠 Orange (40-60%): Moderate match
  - 🔴 Red (<40%): Weak match
- 💡 **AI-powered explanations** for each candidate
- 🏷️ **Skill tags** showing matching/missing skills
- 📈 **Real-time progress** indicators

---

## 🔍 Features to Try

### 1. Dashboard
- View total resumes, shortlisted candidates, and statistics
- Quick actions for common tasks

### 2. Upload Resumes
- Drag-and-drop file upload
- Support for PDF, DOCX, DOC formats
- Real-time parsing progress

### 3. Match Candidates
- Enter job description
- Specify required skills (optional)
- AI analyzes and ranks candidates

### 4. Top Candidates
- View ranked list with detailed scores
- See AI explanations for each match
- Analyze matching and missing skills
- Adjust minimum score threshold

---

## 💡 Pro Tips

1. **Match Score Threshold**: Use the sidebar slider to filter candidates
   - 0.8+ for highly qualified candidates
   - 0.6+ for good matches
   - 0.5+ for all reasonable matches

2. **Required Skills**: Add them for better matching
   - Example: `Python, FastAPI, Docker, AWS, PostgreSQL`
   - Helps prioritize candidates with must-have skills

3. **Multiple Resumes**: Upload 3-5 resumes for best comparison

4. **Different JDs**: Try matching same resumes against different job descriptions

---

## 🐛 Troubleshooting

### Issue: Package installation errors
```bash
# Upgrade pip first
pip install --upgrade pip

# Then install requirements
pip install -r requirements.txt
```

### Issue: spaCy model not found
```bash
# Download the model explicitly
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; spacy.load('en_core_web_sm')"
```

### Issue: Port 8501 already in use
```bash
# Use a different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

### Issue: Azure OpenAI errors
- Check that `.env` file exists
- Verify API key is correct in `.env`
- Ensure you have internet connection

---

## 📱 Expected Results

When you match **Rajesh Kumar** (Python developer) to **Senior Python Developer** JD:

- ✅ Match Score: **85-95%**
- ✅ Explanation: "Excellent match - 7 years Python experience, FastAPI, AWS, Docker"
- ✅ Matching Skills: Python, FastAPI, Django, PostgreSQL, Docker, AWS, Redis
- ✅ Missing Skills: Kubernetes (if specified in JD)

---

## 🎓 Learning Path

1. **First Run**: Test with provided sample data
2. **Experiment**: Try different JD and resume combinations
3. **Create Data**: Add your own sample resumes
4. **Customize**: Adjust match score thresholds
5. **Advanced**: Explore the code and add features

---

## 📚 Next Steps

After testing with sample data:

1. **Real Data**: Use actual resumes (with permission!)
2. **API Integration**: Set up FastAPI endpoints (coming soon)
3. **Scheduling**: Implement interview scheduling (Phase 2)
4. **Deployment**: Deploy to Azure (coming soon)

---

## 🆘 Need Help?

- **Sample Data Issues**: Check `data/README.md`
- **General Setup**: Check main `README.md`
- **Technical Docs**: Check `docs/` folder
- **API Docs**: Visit http://localhost:8000/docs (when API is running)

---

## ✅ Checklist

- [ ] Python 3.8+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] spaCy model downloaded
- [ ] Streamlit app running
- [ ] Tested with sample resume
- [ ] Tested with sample JD
- [ ] Viewed match results

---

**Congratulations! You're ready to use the AI Resume Screener! 🎉**

For detailed information, see the main [README.md](README.md)

---

©2025 ITC Infotech | Powered by Azure OpenAI
