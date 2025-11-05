# 🧪 Local Testing Guide - Run the App on Your Machine

Test the beautiful UI and full functionality on your local machine in **3 minutes**!

---

## 🚀 Super Quick Start (Automated)

### **For Linux/Mac:**

```bash
# 1. Setup (run once)
chmod +x setup.sh run.sh
./setup.sh

# 2. Run the app
./run.sh

# 3. Open browser to: http://localhost:8501
```

### **For Windows:**

```cmd
# 1. Setup (run once)
setup.bat

# 2. Run the app
run.bat

# 3. Open browser to: http://localhost:8501
```

**That's it!** 🎉

---

## 📋 Manual Setup (Alternative)

If you prefer manual control:

### Step 1: Install Python 3.8+

Check if you have Python:
```bash
python3 --version  # Should show 3.8 or higher
```

If not installed, download from: https://www.python.org/downloads/

---

### Step 2: Create Virtual Environment

```bash
# Create venv
python3 -m venv venv

# Activate it
# Linux/Mac:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

---

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install packages (2-3 minutes)
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm
```

---

### Step 4: Create .env File

Create a file named `.env` in the root directory:

```bash
# Azure OpenAI Configuration
AZURE_OPENAI_ENDPOINT=https://itcmentor.openai.azure.com/
AZURE_OPENAI_API_KEY=4FuAkN0MCCjWTv2zGuwvOw622IjmsnwWbh0SCo7U2xuNhP3rY3AoJQQJ99BlACYeBjFXj3w3AAABACOGrcAG
AZURE_EMBEDDING_DEPLOYMENT=text-embedding-3-large
AZURE_GPT_DEPLOYMENT=gpt-4o-mini
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_EMBEDDING_DIMENSION=3072

# App Configuration
AI_PROVIDER=azure
AZURE_OPENAI_ENABLED=True
USE_SAMPLE_DATA=True
LOG_LEVEL=INFO
```

---

### Step 5: Run the App

```bash
streamlit run frontend/streamlit_app.py
```

**Opens automatically in your browser at: http://localhost:8501**

---

## 🎨 What You'll See:

### **Landing Page:**
- 🎯 Purple gradient background
- 📊 Modern white content card
- 🏢 ITC Infotech branding
- 📈 Dashboard metrics (all 0 initially)
- 🎨 Beautiful animations

### **Navigation:**
- 📊 Dashboard
- 📤 Upload Resumes
- 🎯 Match Candidates
- 🏆 Top Candidates
- 📅 Schedule Interviews (coming soon)
- 📈 Analytics (coming soon)

---

## 🧪 Test the Full Flow:

### **Test 1: Upload Sample Resume**

1. Click **"📤 Upload Resumes"** in sidebar
2. Click **"Browse files"**
3. Select a file from: `data/sample_resumes/rajesh_kumar_python.txt`
4. Click **"🔍 Parse Resumes"**
5. ✅ See success message!

### **Test 2: AI Matching**

1. Click **"🎯 Match Candidates"** in sidebar
2. Open `data/sample_jds/senior_python_developer.txt`
3. Copy the entire job description
4. Paste into the text area
5. (Optional) Add skills: `Python, FastAPI, AWS, Docker`
6. Click **"🚀 Start AI Matching"**
7. Wait 10-20 seconds for AI processing
8. ✅ See match results with scores!

### **Test 3: View Top Candidates**

1. Click **"🏆 Top Candidates"** in sidebar
2. See ranked candidates with:
   - Match scores (color-coded)
   - AI explanations
   - Matching skills (blue pills)
   - Missing skills
   - Experience details
3. Expand any candidate to see full details

---

## 🎯 Expected Results:

### **Rajesh Kumar (Python Developer)**
- **Match Score**: ~85-92%
- **Skills Match**: Python, FastAPI, AWS, Docker, PostgreSQL
- **Experience**: 7 years
- **Explanation**: Strong match - all key skills present

### **Priya Sharma (Data Scientist)**
- **Match Score**: ~65-75%
- **Skills Match**: Python, TensorFlow, AWS
- **Missing**: FastAPI, Docker
- **Explanation**: Good technical skills, some missing requirements

### **Amit Patel (Full Stack)**
- **Match Score**: ~55-65%
- **Skills Match**: Python, JavaScript, Docker
- **Missing**: FastAPI, AWS experience
- **Explanation**: Moderate match - some relevant skills

---

## 🎨 UI Features to Test:

### **Hover Effects:**
- ✅ Metric cards lift up on hover
- ✅ Buttons get elevated shadow
- ✅ Candidate cards slide right
- ✅ Skill tags bounce up

### **Animations:**
- ✅ Smooth transitions everywhere
- ✅ Gradient text for headers
- ✅ Progress bar during parsing
- ✅ Balloons on successful match!

### **Color Coding:**
- 🟢 **Excellent** (80-100%): Green gradient
- 🔵 **Good** (60-79%): Blue gradient
- 🟠 **Moderate** (40-59%): Orange gradient
- 🔴 **Weak** (0-39%): Red gradient

---

## 🐛 Troubleshooting:

### **Error: "Module not found"**

**Solution:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

---

### **Error: "Can't find model 'en_core_web_sm'"**

**Solution:**
```bash
python -m spacy download en_core_web_sm
```

---

### **Error: "Azure OpenAI API error"**

**Possible causes:**
1. Missing `.env` file
2. Wrong API key
3. API quota exceeded

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify contents
cat .env | grep AZURE_OPENAI_API_KEY

# Test API key
python -c "from config.settings import settings; print(settings.AZURE_OPENAI_API_KEY[:20])"
```

---

### **Port 8501 already in use**

**Solution:**
```bash
# Kill existing Streamlit process
pkill -f streamlit

# Or use different port
streamlit run frontend/streamlit_app.py --server.port 8502
```

---

### **App looks plain (no styling)**

**Cause:** Browser cache

**Solution:**
1. Hard refresh: `Ctrl+Shift+R` (Windows) or `Cmd+Shift+R` (Mac)
2. Clear browser cache
3. Try incognito/private window

---

## 🔧 Development Mode:

### **Enable Debug Mode:**

Add to `.env`:
```bash
DEBUG=True
LOG_LEVEL=DEBUG
```

### **Watch for Changes:**

Streamlit auto-reloads when you save files!

---

## 📊 Performance Tips:

### **First Run is Slow:**
- spaCy model loads (~100MB)
- Azure OpenAI API first call
- Subsequent runs are faster!

### **Matching Takes Time:**
- Generating embeddings: ~2-3 seconds per resume
- GPT explanations: ~3-5 seconds per candidate
- **10 resumes**: ~30-60 seconds total

---

## 🎯 Test Sample Data:

All sample data is in `data/` directory:

### **Sample Resumes:**
1. `rajesh_kumar_python.txt` - Strong Python match
2. `priya_sharma_datascience.txt` - Data Science profile
3. `amit_patel_fullstack.txt` - Full stack developer
4. `sarah_jones_devops.txt` - DevOps engineer
5. `john_doe_java.txt` - Java developer

### **Sample Job Descriptions:**
1. `senior_python_developer.txt` - Backend Python role
2. `data_scientist.txt` - ML/AI role
3. `devops_engineer.txt` - Infrastructure role

### **Expected Matches:**

| Resume | For Python JD | For Data Science JD | For DevOps JD |
|--------|---------------|---------------------|---------------|
| Rajesh | 85-92% | 60-70% | 50-60% |
| Priya | 65-75% | 90-95% | 45-55% |
| Amit | 55-65% | 50-60% | 60-70% |
| Sarah | 50-60% | 40-50% | 85-92% |
| John | 40-50% | 35-45% | 55-65% |

---

## 🚀 Next Steps:

### **After Local Testing:**

1. ✅ **Works well?** → Deploy to Streamlit Cloud (free!)
2. 📖 **Read:** `STREAMLIT_CLOUD_DEPLOY.md`
3. 🌐 **Deploy:** https://share.streamlit.io/
4. 🎉 **Share:** Your live URL with team!

---

## 💡 Pro Tips:

1. **Use sample data** for quick testing
2. **Try different JDs** to see varied matches
3. **Check AI explanations** - they're detailed!
4. **Hover over elements** to see animations
5. **Upload real resumes** to test parsing

---

## 📸 Screenshots:

### **Expected UI:**
- Purple gradient background
- Clean white content cards
- Dark sidebar with ITC branding
- Colorful metric cards
- Smooth animations
- Modern typography

---

## ⚡ Quick Commands Reference:

```bash
# Setup (run once)
./setup.sh          # Linux/Mac
setup.bat           # Windows

# Run app
./run.sh            # Linux/Mac
run.bat             # Windows

# Manual run
source venv/bin/activate && streamlit run frontend/streamlit_app.py

# Stop app
Ctrl+C

# Check logs
tail -f logs/app.log
```

---

## 🎊 Success Checklist:

- [ ] Python 3.8+ installed
- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] spaCy model downloaded
- [ ] .env file configured
- [ ] App runs without errors
- [ ] Browser opens to http://localhost:8501
- [ ] Beautiful purple gradient UI visible
- [ ] Can upload resumes
- [ ] Can perform AI matching
- [ ] See match scores and explanations
- [ ] All animations work

---

**🎉 Enjoy testing your beautiful AI Resume Screener!**

For deployment to the cloud (FREE), see: `STREAMLIT_CLOUD_DEPLOY.md`
