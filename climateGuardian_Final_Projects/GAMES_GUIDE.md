# 🎮 ClimateGuardian AI - Games Guide

## 🌟 Complete Games Overview

---

## 🏃 Game 1: Eco-Runner

### 📖 Story
You are an environmental hero collecting fallen leaves to reduce carbon emissions while avoiding garbage and waste!

### 🎯 Objective
Reduce your carbon score from 100 to 0 by collecting leaves and avoiding waste.

### 🎮 Controls
- **↑ (Up Arrow)** - Move person up
- **↓ (Down Arrow)** - Move person down

### 📊 Scoring
- 🍃 **Collect Leaf:** -10 CO₂ (Reduces carbon)
- 🗑️ **Hit Garbage:** +20 CO₂ (Increases carbon)
- 🏆 **Win Condition:** Carbon score = 0

### 💡 Strategy Tips
1. Focus on collecting leaves first
2. Avoid all garbage items
3. Use the full vertical space to dodge
4. Keep an eye on your carbon score
5. Don't rush - precision is key!

### 🎨 Visual Elements
- **Sky:** Light blue gradient background
- **Ground:** Green grass
- **Player:** Animated person with head, body, arms, legs
- **Collectibles:** Green leaves with veins
- **Obstacles:** Gray garbage cans with red waste

### ⏱️ Gameplay Tips
- Items spawn randomly from the right
- Move strategically to maximize collection
- One mistake won't end the game - keep playing!
- The game ends when you reach 0 carbon (WIN!)

---

## ⚡ Game 2: Renewable Energy Puzzle

### 📖 Story
Place renewable energy sources on the correct tiles to reduce global emissions and achieve net-zero!

### 🎯 Objective
Reduce emissions from 500 tons to 0 by correctly placing energy sources on the colored grid.

### 🎮 Controls
- **Mouse Click** - Select energy source button
- **Mouse Click** - Click on grid tile to place

### 🌈 Energy Source Matching
| Energy Type | Color | Tile Color | Symbol |
|-------------|-------|------------|--------|
| **Solar** | Yellow | Yellow | ☀️ |
| **Wind** | Blue | Blue | 💨 |
| **Hydro** | Cyan | Light Blue | 💧 |

### 📊 Scoring
- ✅ **Correct Match:** -50 tons CO₂
- ❌ **Wrong Match:** +30 tons CO₂
- 🏆 **Win Condition:** Emissions = 0

### 💡 Strategy Tips
1. **Look carefully** at the tile colors before clicking
2. **Remember the pattern:**
   - ☀️ Solar = Yellow tiles
   - 💨 Wind = Blue tiles
   - 💧 Hydro = Cyan tiles
3. **Plan ahead** - minimize wrong placements
4. **Visual feedback** - selected button has white border
5. **Take your time** - accuracy over speed

### 🎨 Visual Features
- Gradient sky background
- Large 5x5 grid
- Three energy selection buttons at top
- Real-time emissions counter
- Color-coded progress bar
- Particle effects on placement

### 🎯 Winning Strategy
- Start with one energy type at a time
- Clear all yellow tiles first (Solar)
- Then blue tiles (Wind)
- Finally cyan tiles (Hydro)
- Avoid random clicking!

---

## ♻️ Game 3: Smart Waste Segregation

### 📖 Story
Falling waste items need to be sorted into the correct recycling bins. Can you save the planet by sorting correctly?

### 🎯 Objective
Sort falling waste items into matching colored bins without missing 5 items.

### 🎮 Controls
- **Hand Gesture** - Show hand to camera
- **Pinch** - Touch index finger + thumb to grab items
- **Drag** - Move hand while pinching to drag item
- **Release** - Open fingers to drop into bin

### 🌈 Bin Color Guide
| Bin Color | Waste Type | Examples |
|-----------|------------|----------|
| 🔵 **Blue** | Plastic | Bottle, Bag, Cup |
| 🟡 **Yellow** | Paper | Newspaper, Cardboard, Magazine |
| 🔴 **Red** | Metal | Can, Foil, Tin |
| 🟢 **Green** | Organic | Apple, Banana, Leaves |

### 📊 Scoring
- ✅ **Correct Bin:** +10 points
- ❌ **Wrong Bin:** -5 points
- 💔 **Missed Item:** Counts toward game over (5 max)
- 🏆 **Win Condition:** High score before 5 misses

### 💡 Strategy Tips
1. **Read the label** - Each item shows its type
2. **Color association:**
   - Plastic = Blue (like water bottles)
   - Paper = Yellow (like notepad)
   - Metal = Red (like cans)
   - Organic = Green (like plants)
3. **Prioritize accuracy** over speed
4. **Grab items early** - don't wait until last second
5. **Drop precisely** - make sure you're over the correct bin

### 🎨 Visual Features
- Four colored bins at bottom
- Falling waste items with labels
- Real-time score display
- Missed counter (X/5)
- Color-coded waste items
- Hand tracking skeleton overlay
- Pinch detection indicator

### ⏱️ Gameplay Mechanics
- Items spawn every ~2 seconds
- Items fall at constant speed
- Hand tracking uses AI (MediaPipe)
- Game levels up every 50 points
- Faster spawn rate at higher levels
- Game over after 5 misses

### 🎓 Educational Value
Learn the **4 Rs of Waste Management:**
1. **Reduce** - Use less
2. **Reuse** - Use again
3. **Recycle** - Process for new use
4. **Recover** - Extract energy/materials

---

## 🏆 Points & Rewards

### Points Earned Per Game:
| Game | Base Points | Bonus |
|------|-------------|-------|
| Eco-Runner | 50 | For reaching 0 carbon |
| Renewable Energy | 50 | For net-zero achievement |
| Waste Segregation | 75 | For high-score completion |

### Logged Actions:
- **Eco-Runner Victory** - 50 points
- **Renewable Energy Victory** - 50 points  
- **Waste Segregation Champion** - 75 points

### Total Possible: **175 points** per full game session!

---

## 🎯 Achievement Guide

### Eco-Runner Achievements:
- 🥉 **Leaf Collector** - Collect 10 leaves
- 🥈 **Carbon Reducer** - Get below 50 CO₂
- 🥇 **Eco Hero** - Win the game (0 CO₂)

### Renewable Energy Achievements:
- 🥉 **First Placement** - Place 5 correct tiles
- 🥈 **Half Clean** - Reduce emissions to 250
- 🥇 **Net-Zero Hero** - Achieve 0 emissions

### Waste Segregation Achievements:
- 🥉 **Beginner Sorter** - 50 points
- 🥈 **Recycling Pro** - 100 points
- 🥇 **Waste Master** - 150+ points

---

## 🐛 Troubleshooting

### Game Won't Launch?
1. Check pygame is installed: `pip install pygame`
2. Ensure you're in the correct directory
3. Try restarting Streamlit app

### Controls Not Working?
1. **Eco-Runner:** Click on the game window first
2. **Energy Puzzle:** Make sure mouse is over canvas
3. **Waste Segregation:** Check camera permissions

### Camera Not Working (Waste Segregation)?
1. Allow camera access when prompted
2. Close other apps using camera
3. Check camera drivers are updated
4. Try different camera (if available)

### Hand Not Detected?
1. Ensure good lighting
2. Keep hand fully visible in frame
3. Position hand at arm's length from camera
4. Try different hand positions
5. Clean camera lens

### Slow Performance?
1. Close other applications
2. Ensure good system resources
3. Reduce screen resolution if needed

---

## 📚 Learning Outcomes

After playing these games, students will understand:

### Environmental Concepts:
- ✅ Carbon footprint and emissions
- ✅ Renewable energy sources
- ✅ Proper waste segregation
- ✅ Recycling categories

### Skills Developed:
- 🎯 Hand-eye coordination
- 🧠 Pattern recognition
- ⚡ Quick decision making
- 🎨 Color association
- 📊 Resource management

---

## 🌟 Pro Tips for Maximum Points

### General Strategy:
1. **Play all three games** for maximum points (175 total)
2. **Practice makes perfect** - replay to improve
3. **Focus on accuracy** rather than speed
4. **Learn the patterns** in each game
5. **Stay calm** - rushing causes mistakes

### Time Management:
- Eco-Runner: ~2-3 minutes per game
- Energy Puzzle: ~3-5 minutes per game
- Waste Segregation: ~2-4 minutes per game
- **Total session:** 10-15 minutes for all games

---

## 🎊 Fun Facts

### Did You Know?
- 🍃 **One tree** absorbs about 48 lbs of CO₂ per year
- ⚡ **Solar panels** can last 25-30 years
- ♻️ **Recycling one aluminum can** saves enough energy to run a TV for 3 hours
- 🌍 **Proper waste sorting** can reduce landfill waste by 75%

---

## 📞 Support

Having issues? Check:
1. **INSTALLATION_GUIDE.md** - Setup instructions
2. **README.md** - General documentation
3. **UPDATE_SUMMARY.md** - Latest changes

---

**🌍 Happy Gaming! Save the Planet, One Game at a Time! ♻️**

---

*Last Updated: 2024*  
*Version: 2.0*  
*Compatibility: Python 3.8+, Pygame 2.5.2+, OpenCV 4.9+, MediaPipe 0.10+*
