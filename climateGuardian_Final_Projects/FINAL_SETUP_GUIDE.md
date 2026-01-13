# 🌍 ClimateGuardian AI - Final Setup Guide

## ✅ **Complete Project Structure**

```
climateguardian-ai/
│
├── app.py                          # Main Streamlit application ✅
├── auth.py                         # Login/Signup system ✅
├── requirements.txt                # All dependencies ✅
├── README.md                       # Documentation ✅
├── .gitignore                      # Git ignore file ✅
│
├── .streamlit/
│   └── secrets.toml               # API key configuration ✅
│
├── games/
│   ├── __init__.py                # Package initializer ✅
│   ├── eco_runner.py              # 🏃 Game 1: Eco-Runner ✅
│   ├── renewable_energy.py        # ⚡ Game 2: Energy Puzzle ✅
│   └── waste_segregation.py       # ♻️ Game 3: Waste Segregation ✅
│
└── users_database.csv              # Auto-generated on first run
```

---

## 🚀 **Installation Steps**

### **Step 1: Install Python**
- Download Python 3.8+ from https://www.python.org/downloads/
- During installation, **CHECK** "Add Python to PATH"

### **Step 2: Install All Dependencies**

Open terminal/command prompt in your project folder and run:

```bash
pip install -r requirements.txt
```

This installs:
- ✅ `streamlit` - Web framework
- ✅ `pandas` - Data handling
- ✅ `plotly` - Charts
- ✅ `google-generativeai` - AI chatbot
- ✅ `Pillow` - Image handling
- ✅ `pygame` - Games 1 & 2
- ✅ `opencv-python` - Camera for Game 3
- ✅ `mediapipe` - Hand tracking for Game 3
- ✅ `numpy` - Math operations

### **Step 3: Configure API Key**

Edit `.streamlit/secrets.toml` and add your Gemini API key:

```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

Get free key: https://makersuite.google.com/app/apikey

### **Step 4: Run the Application**

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎮 **Three Games Overview**

### **Game 1: 🏃 Eco-Runner**
- **Type:** Pygame window
- **Controls:** Arrow keys (↑↓)
- **Graphics:** Person collecting leaves, avoiding garbage
- **Goal:** Reduce carbon to 0
- **Points:** 50 when you win
- **How to launch:** Click "🎮 Launch Eco-Runner" in Games Hub

### **Game 2: ⚡ Renewable Energy Puzzle**
- **Type:** Pygame window
- **Controls:** Mouse click
- **Mechanics:** Match energy sources to colored tiles
- **Goal:** Reduce emissions to 0
- **Points:** 50 when you win
- **How to launch:** Click "🎮 Launch Renewable Energy Puzzle" in Games Hub

### **Game 3: ♻️ Smart Waste Segregation (NEW!)**
- **Type:** OpenCV window with camera
- **Controls:** Hand gestures (pinch to grab)
- **Mechanics:** Sort falling trash into colored bins
- **Goal:** High score before 5 misses
- **Points:** 75 + your final score
- **How to launch:** Click "🎮 Launch Waste Segregation" in Games Hub

---

## 🎯 **How to Play Each Game**

### **🏃 Eco-Runner**

1. Click "🎮 Launch Eco-Runner"
2. Pygame window opens
3. **Controls:**
   - ↑ (Up Arrow) - Move up
   - ↓ (Down Arrow) - Move down
4. **Gameplay:**
   - Collect green leaves (🍃) = -10 CO₂
   - Avoid red garbage (🗑️) = +20 CO₂
5. **Win:** Reach 0 carbon score
6. **Rewards:** +50 eco-points automatically added

---

### **⚡ Renewable Energy Puzzle**

1. Click "🎮 Launch Renewable Energy Puzzle"
2. Pygame window opens
3. **Controls:**
   - Mouse click energy button (☀️ Solar, 💨 Wind, 💧 Hydro)
   - Mouse click on grid tile
4. **Gameplay:**
   - Yellow tiles = Solar ☀️
   - Blue tiles = Wind 💨
   - Cyan tiles = Hydro 💧
   - Correct = -50 emissions
   - Wrong = +30 emissions
5. **Win:** Reach net-zero (0 emissions)
6. **Rewards:** +50 eco-points automatically added

---

### **♻️ Smart Waste Segregation (NEW!)**

1. Click "🎮 Launch Waste Segregation"
2. OpenCV window opens with camera
3. **Setup:**
   - Allow camera access
   - Make sure you have good lighting
   - Position yourself so camera can see your hand
4. **Controls:**
   - Show hand to camera
   - **PINCH** (touch index finger + thumb together) to grab items
   - **DRAG** hand while pinching to move item
   - **RELEASE** pinch to drop into bin
   - Press **SPACE** to start game
   - Press **P** to pause
   - Press **Q** to quit
5. **Gameplay:**
   - Falling items appear from top
   - Grab with pinch gesture
   - Drag to matching colored bin:
     - 🔵 **Blue** = Plastic
     - 🟡 **Yellow** = Paper
     - 🔴 **Red** = Metal
     - 🟢 **Green** = Organic
   - Correct bin = +10 score
   - Wrong bin = -5 score
   - Missed items count toward game over (5 max)
6. **Win:** Get high score before missing 5 items
7. **Rewards:** +75 eco-points + your final score

---

## 🏆 **Complete Points System**

| Activity | Points | Category |
|----------|--------|----------|
| **AI Quiz** (correct answer) | 15 | Learning |
| **Planted a Tree** (mission) | 50 | Mission |
| **Recycled Plastic** (mission) | 5 | Mission |
| **Walked to School** (mission) | 20 | Mission |
| **Saved Electricity** (mission) | 10 | Mission |
| **Used Reusable Bag** (mission) | 5 | Mission |
| **Composted Food** (mission) | 15 | Mission |
| **Carbon Reduction** (calculator) | Variable | Predictor |
| **Eco-Runner Victory** | 50 | Game |
| **Energy Puzzle Victory** | 50 | Game |
| **Waste Segregation** | 75 + score | Game |

**Maximum Points Per Session: 250+**

---

## 🎓 **Complete Feature List**

### **🔐 Authentication**
- ✅ User registration with email
- ✅ Secure login (SHA-256 encryption)
- ✅ Personal user profiles
- ✅ Score tracking per user

### **🤖 AI Features**
- ✅ AI chatbot (Gemini-powered)
- ✅ Dynamic quiz generator
- ✅ Real-time responses

### **📊 Tracking Features**
- ✅ Mission logger with date stamps
- ✅ Carbon footprint calculator
- ✅ Admin dashboard with charts
- ✅ Activity history

### **🎮 Games (3 Total)**
- ✅ Eco-Runner (Pygame)
- ✅ Renewable Energy Puzzle (Pygame)
- ✅ Waste Segregation (OpenCV + MediaPipe)

---

## 🐛 **Troubleshooting**

### **Game 3 (Waste Segregation) Specific Issues:**

**Camera not opening:**
- Check if another app is using the camera
- Close Zoom, Skype, or other video apps
- Try restarting your computer
- Check camera permissions in system settings

**Hand not detected:**
- Ensure good lighting (face a window or lamp)
- Keep hand fully visible in frame
- Position hand at arm's length from camera
- Try different hand positions
- Make sure camera lens is clean

**Pinch not working:**
- Touch index finger tip to thumb tip firmly
- Hold for 1 second
- Make sure both fingers are visible
- Try different lighting

**Game lagging:**
- Close other applications
- Ensure your computer meets requirements:
  - CPU: 2.0 GHz or faster
  - RAM: 4 GB minimum
  - Camera: 480p or better

---

## 🎯 **Quick Troubleshooting Commands**

### **Test if camera works:**
```python
import cv2
cap = cv2.VideoCapture(0)
ret, frame = cap.read()
cap.release()
print("Camera OK!" if ret else "Camera not found")
```

### **Test if all packages installed:**
```bash
pip list | grep -E "streamlit|pygame|opencv|mediapipe|pandas|plotly"
```

### **Reinstall all dependencies:**
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## ✅ **Pre-Launch Checklist**

Before playing, make sure:

- [ ] Python 3.8+ installed
- [ ] All packages installed (`pip install -r requirements.txt`)
- [ ] API key configured in `.streamlit/secrets.toml`
- [ ] Camera is connected and working (for Game 3)
- [ ] Good lighting in room (for Game 3)
- [ ] No other apps using camera (for Game 3)
- [ ] Streamlit app running (`streamlit run app.py`)
- [ ] User account created and logged in

---

## 🎮 **Gameplay Tips**

### **Eco-Runner:**
- Stay in the middle of the screen
- React quickly to obstacles
- Collect all leaves you can
- One mistake won't end the game

### **Energy Puzzle:**
- Look at tile colors carefully before clicking
- Remember: Yellow=Solar, Blue=Wind, Cyan=Hydro
- Take your time - accuracy over speed
- Plan ahead to minimize wrong placements

### **Waste Segregation:**
- **Lighting is key** - make sure room is well-lit
- Practice the pinch gesture before starting
- Grab items early - don't wait until last second
- Match colors: Blue=Plastic, Yellow=Paper, Red=Metal, Green=Organic
- Focus on accuracy - wrong bins reduce score
- Watch the missed counter - game ends at 5 misses

---

## 📞 **Support**

### **Common Issues:**

1. **"Module not found" error**
   - Solution: `pip install [module_name]`

2. **"Camera not detected" (Game 3)**
   - Solution: Check camera connection, restart app

3. **"API key error" (Chat/Quiz)**
   - Solution: Check `.streamlit/secrets.toml` has valid key

4. **Games not launching**
   - Solution: Make sure `games/` folder exists with all files

5. **Hand tracking not working (Game 3)**
   - Solution: Improve lighting, clean camera lens, position hand properly

---

## 🌟 **Success Indicators**

You'll know everything is working when:

✅ App loads without errors  
✅ You can create account and login  
✅ AI Chat responds to messages  
✅ Quiz generates questions  
✅ Missions can be logged  
✅ Carbon calculator updates display  
✅ Eco-Runner opens in Pygame window  
✅ Energy Puzzle opens in Pygame window  
✅ Waste Segregation opens with camera feed  
✅ Points are added when games complete  
✅ Admin Dashboard shows your stats  

---

## 🎊 **You're Ready!**

Your complete ClimateGuardian AI platform with:
- ✅ User authentication
- ✅ AI-powered chat and quiz
- ✅ Mission tracking
- ✅ Carbon calculator
- ✅ **3 fully playable games**
- ✅ Admin dashboard

**Happy Gaming! Let's save the planet! 🌍♻️🎮**

---

**Last Updated:** 2024  
**Version:** 3.0 (Complete with all 3 games)  
**Status:** ✅ Production Ready
