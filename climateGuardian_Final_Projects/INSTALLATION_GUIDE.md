# 🌍 ClimateGuardian AI - Complete Installation Guide

## 📋 Prerequisites

Before you begin, make sure you have the following installed on your system:

1. **Python 3.8 or higher** - [Download Python](https://www.python.org/downloads/)
2. **pip** (Python package installer - comes with Python)
3. **Git** (optional) - [Download Git](https://git-scm.com/downloads)

---

## 🚀 Step-by-Step Installation

### Step 1: Download/Clone the Project

**Option A: If you have Git installed**
```bash
git clone <your-repository-url>
cd climateguardian-ai
```

**Option B: Manual Download**
1. Download the project as a ZIP file
2. Extract it to a folder
3. Open Terminal/Command Prompt in that folder

---

### Step 2: Create a Virtual Environment (Recommended)

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` appear in your terminal prompt.

---

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web framework)
- pandas (data handling)
- plotly (charts)
- google-generativeai (AI chatbot)
- Pillow (image handling)
- pygame (games)

**If you encounter any errors:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

---

### Step 4: Get Your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Click **"Create API Key"**
3. Copy your API key (it looks like: `AIzaSyD...`)

---

### Step 5: Configure the API Key

**Method 1: Using secrets.toml (Recommended)**

1. Navigate to `.streamlit` folder
2. Open `secrets.toml` file
3. Replace `"your-gemini-api-key-here"` with your actual API key:

```toml
GEMINI_API_KEY = "AIzaSyD_your_actual_key_here"
```

**Method 2: Direct in app.py (Quick Test)**

Open `app.py` and find this line (around line 12):
```python
genai.configure(api_key=st.secrets.get("GEMINI_API_KEY", "YOUR_API_KEY_HERE"))
```

Replace with:
```python
genai.configure(api_key="AIzaSyD_your_actual_key_here")
```

⚠️ **Security Note:** Method 2 is only for testing. Don't share this file if you use Method 2!

---

### Step 6: Verify Installation

Check if all packages are installed:
```bash
pip list
```

You should see:
- streamlit
- pandas
- plotly
- google-generativeai
- Pillow
- pygame

---

### Step 7: Run the Application

```bash
streamlit run app.py
```

**What should happen:**
1. Terminal will show: `You can now view your Streamlit app in your browser.`
2. Your default browser will automatically open
3. You'll see the app at: `http://localhost:8501`

---

## 🔐 First Time Setup - Create Your Account

### Step 1: Sign Up
1. When the app opens, you'll see the **Login Page**
2. Click the **"📝 Sign Up"** button
3. Fill in the registration form:
   - **Full Name**: Your name
   - **Email**: Your email address
   - **Username**: Choose a unique username (no spaces)
   - **Password**: At least 6 characters
   - **Confirm Password**: Same as password
4. Check the **"I agree to help save the planet! 🌍"** checkbox
5. Click **"🌟 Create Account"**

### Step 2: Login
1. After successful registration, you'll be redirected to the login page
2. Enter your **username** and **password**
3. Click **"🚀 Login"**
4. You're in! Start your eco-journey! 🌱

---

## 🎮 How to Use the Application

### 1. **AI Chat** 🤖
- Ask questions about sustainability, recycling, climate change
- Example: "How can I reduce plastic waste?"
- Get instant AI-powered answers

### 2. **AI Quiz** 🎮
- Click "🌱 Generate New Question"
- Answer multiple-choice questions
- Earn 15 points for each correct answer

### 3. **Missions** ✅
- Select a completed eco-friendly action
- Click "✅ Log Mission"
- Earn points based on activity:
  - Planted a Tree: 50 points
  - Walked/Biked to School: 20 points
  - Recycled Plastic: 5 points
  - And more!

### 4. **Predict Sustainability** 🔮
- Choose your daily habits (transportation, diet, energy)
- Click "📊 Calculate Impact"
- See your carbon footprint change in real-time
- Goal: Get your carbon level as low as possible!

### 5. **Games Hub** 🎯

#### **Eco-Runner Game** 🏃
1. Click "🎮 Launch Eco-Runner"
2. A new window will open
3. **Controls:**
   - ↑ (Up Arrow): Move up
   - ↓ (Down Arrow): Move down
4. **Objective:**
   - Collect green circles (reduce carbon by 10)
   - Avoid red squares (increase carbon by 20)
   - Reach 0 carbon to win!
5. Win = +50 points automatically added!

#### **Renewable Energy Puzzle** ⚡
1. Click "🎮 Launch Renewable Energy Puzzle"
2. A new window will open
3. **How to Play:**
   - Click an energy source button (☀️ Solar, 💨 Wind, 💧 Hydro)
   - Click matching colored tiles on the grid
   - Yellow = Solar, Blue = Wind, Cyan = Hydro
4. **Scoring:**
   - Correct match: -50 emissions
   - Wrong match: +30 emissions
5. Reach net-zero emissions to win!
6. Win = Points based on performance!

### 6. **Admin Dashboard** 📊
- View total eco-points
- See all your logged activities
- Track trees planted
- View interactive charts

---

## 🐛 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'streamlit'"
**Solution:**
```bash
pip install streamlit
```

### Problem: Games don't launch
**Solution:**
```bash
pip install pygame
```

### Problem: "API key error" or AI features not working
**Solution:**
1. Check if you added your API key correctly in `.streamlit/secrets.toml`
2. Make sure the key doesn't have extra quotes or spaces
3. Verify the key is valid at [Google AI Studio](https://makersuite.google.com/app/apikey)

### Problem: "Port 8501 is already in use"
**Solution:**
```bash
streamlit run app.py --server.port 8502
```

### Problem: Virtual environment not activating
**Windows:**
```bash
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

**macOS/Linux:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Problem: Pygame window doesn't show
**Solution:**
- Make sure you're not running the app in a remote server
- Games require a display/monitor to work
- Try running on your local computer

---

## 📂 Project File Structure

```
climateguardian-ai/
│
├── app.py                      # Main application
├── auth.py                     # Login/Signup system
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
├── INSTALLATION_GUIDE.md       # This file!
├── .gitignore                 # Git ignore rules
│
├── .streamlit/
│   └── secrets.toml           # API key (don't share!)
│
├── games/
│   ├── __init__.py
│   ├── eco_runner.py          # Eco-Runner game
│   └── renewable_energy.py    # Energy puzzle game
│
└── users_database.csv          # User accounts (auto-created)
```

---

## 🔒 Security Best Practices

1. **Never share your API key** publicly
2. **Don't commit secrets.toml** to GitHub (it's in .gitignore)
3. **Use strong passwords** when creating accounts
4. **Keep your virtual environment** separate from the project

---

## 🆘 Getting Help

### Check Logs
When you run the app, the terminal shows useful error messages. Read them carefully!

### Test Components Individually

**Test if Python works:**
```bash
python --version
```

**Test if Streamlit works:**
```bash
streamlit hello
```

**Test if Pygame works:**
```bash
python games/eco_runner.py
```

**Test if API key works (google-genai):**
```python
from google import genai
client = genai.Client(api_key="your-key-here")
# generate a simple content with the model
response = client.models.generate_content(model='gemini-pro', contents='Hello')
print(response.text)
```

**Legacy (google.generativeai) — kept for reference:**
```python
import google.generativeai as genai
genai.configure(api_key="your-key-here")
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content("Hello")
print(response.text)
```
---

## 🎉 Success Checklist

- [ ] Python 3.8+ installed
- [ ] Virtual environment created and activated
- [ ] All packages installed (requirements.txt)
- [ ] Gemini API key obtained
- [ ] API key added to secrets.toml
- [ ] App runs without errors (`streamlit run app.py`)
- [ ] Can create an account and login
- [ ] AI Chat responds to questions
- [ ] Quiz generates questions
- [ ] Missions can be logged
- [ ] Carbon calculator works
- [ ] Eco-Runner game launches and plays
- [ ] Renewable Energy game launches and plays
- [ ] Admin Dashboard shows data

---

## 📧 Support

If you encounter issues:
1. Check this installation guide again
2. Read error messages carefully
3. Check the README.md file
4. Verify all files are present in the correct structure

---

## 🌟 Tips for Best Experience

1. **Use a modern browser** (Chrome, Firefox, Edge)
2. **Keep the terminal open** while using the app
3. **Don't close the Pygame windows** abruptly - complete the games
4. **Log missions daily** to track your progress
5. **Challenge yourself** to reduce your carbon footprint!

---

**Made with 💚 for a greener planet 🌍**

**Happy Eco-Gaming! 🌱♻️**
