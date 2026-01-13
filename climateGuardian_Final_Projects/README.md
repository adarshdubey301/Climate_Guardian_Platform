# 🌍 ClimateGuardian AI

An interactive AI-powered sustainability education platform built with Streamlit and Pygame.

## 🌟 Features

### 🔐 Authentication System
- **User Registration**: Create your personal account with username, email, and password
- **Secure Login**: SHA-256 encrypted password protection
- **User Profiles**: Track your personal eco-score and progress
- **Session Management**: Secure user sessions throughout the application

### Student Hub
- **🤖 AI Chat**: Interactive chatbot powered by Google Gemini AI for sustainability questions
- **🎮 AI Quiz**: Dynamic quiz generator with unlimited eco-friendly questions
- **✅ Missions**: Daily green mission tracker to log eco-friendly activities
- **🔮 Predict Sustainability**: Carbon footprint calculator with real-time feedback
- **🎯 Games Hub**: Two playable Pygame games integrated into the platform

### Games
1. **🏃 Eco-Runner**: Control a person collecting green leaves while avoiding red waste items (Enhanced with custom graphics!)
2. **⚡ Renewable Energy Puzzle**: Match renewable energy sources to correct locations to achieve net-zero
3. **♻️ Smart Waste Segregation**: AI-powered hand gesture game - use camera to sort waste into bins!

### Admin Dashboard
- **📊 Analytics**: Visual charts showing impact distribution and top activities
- **📈 Activity Log**: Complete history of all logged missions and activities
- **🌳 Metrics**: Total eco-points, actions, and trees planted

## 📁 Project Structure

```
climateguardian-ai/
│
├── app.py                      # Main Streamlit application
├── auth.py                     # Authentication module (login/signup)
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── users_database.csv          # User database (auto-created)
│
├── .streamlit/
│   └── secrets.toml           # API keys (create this file)
│
└── games/
    ├── __init__.py            # Package initializer
    ├── eco_runner.py          # Eco-Runner game
    └── renewable_energy.py    # Renewable Energy Puzzle game
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Clone the repository
```bash
git clone <your-repo-url>
cd climateguardian-ai
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Set up API Key
1. Get a Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create `.streamlit/secrets.toml` file
3. Add your API key:
```toml
GEMINI_API_KEY = "your-actual-api-key-here"
```

### Step 4: Run the application
```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## 🔐 First Time Setup

### Create Your Account
1. When you first run the app, you'll see the **Login Page**
2. Click **"📝 Sign Up"** button
3. Fill in your details:
   - Full Name
   - Email Address
   - Username (unique)
   - Password (minimum 6 characters)
   - Confirm Password
4. Check the "I agree to help save the planet! 🌍" checkbox
5. Click **"🌟 Create Account"**
6. You'll be redirected to login with your new credentials

### Login
1. Enter your **Username** and **Password**
2. Click **"🚀 Login"**
3. Start your eco-journey!

### Features After Login
- Your username displayed in the sidebar
- Personal eco-score tracking
- All activities saved to your profile
- Logout button to securely end your session

## 🎮 How to Play Games

### Eco-Runner
1. Navigate to **Games Hub** tab
2. Click **"🎮 Launch Eco-Runner"**
3. A Pygame window will open
4. Use **↑** and **↓** arrow keys to move
5. Collect **green items** (reduce carbon by 10)
6. Avoid **red obstacles** (increase carbon by 20)
7. Goal: Get carbon score to 0!

### Renewable Energy Puzzle
1. Navigate to **Games Hub** tab
2. Click **"🎮 Launch Renewable Energy Puzzle"**
3. A Pygame window will open
4. Click an energy button (Solar/Wind/Hydro)
5. Click matching colored tiles on the grid
6. Correct matches reduce emissions by 50 tons
7. Wrong matches increase emissions by 30 tons
8. Goal: Reach net-zero emissions!

## 💡 Features Explained

### AI Chat (Gemini-powered)
- Ask questions about recycling, climate change, sustainability
- Get instant, encouraging responses
- All responses are tailored for students

### AI Quiz Generator
- Generates unlimited unique questions using AI
- Topics: Environment, recycling, renewable energy, climate
- Earn 15 points for each correct answer
- Get explanations for every answer

### Mission Tracker
- Log daily eco-friendly activities
- Earn points based on impact:
  - Recycled Plastic: 5 points
  - Planted a Tree: 50 points
  - Walked/Biked to School: 20 points
  - Saved Electricity: 10 points
  - Used Reusable Bag: 5 points
  - Composted Food: 15 points

### Carbon Footprint Calculator
- Make daily choices (transportation, diet, energy)
- See real-time impact on carbon level
- Visual feedback with color-coded status
- Earn bonus points for carbon reduction

### Admin Dashboard
- View comprehensive analytics
- Track school-wide sustainability efforts
- Export data for reports
- Visualize impact with interactive charts

## 🎨 Customization

### Changing Colors
Edit the CSS in `app.py` under the `st.markdown()` section with custom styles.

### Adding New Missions
Modify the `points_map` dictionary in the `mission_tracker()` function:
```python
points_map = {
    "Your New Mission": 25,
    # ... existing missions
}
```

### Adding More Quiz Questions
The AI generates questions automatically, but you can modify the prompt in `generate_ai_quiz_question()` to focus on specific topics.

## 🔧 Troubleshooting

### Games not launching
- Ensure Pygame is installed: `pip install pygame`
- Check that the `games/` folder exists with both game files
- Try running games directly: `python games/eco_runner.py`

### API errors
- Verify your API key in `.streamlit/secrets.toml`
- Check internet connection
- Ensure you haven't exceeded API quota

### Import errors
- Reinstall dependencies: `pip install -r requirements.txt`
- Use virtual environment (recommended):
  ```bash
  python -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  pip install -r requirements.txt
  ```

## 📊 Data Storage

- All data is stored in Streamlit session state
- Data persists during the session
- To save permanently, export from Admin Dashboard
- For production, integrate with a database (SQLite, PostgreSQL, etc.)

## 🌱 Future Enhancements

- [ ] User authentication and profiles
- [ ] Leaderboard system
- [ ] More interactive games
- [ ] Mobile app version
- [ ] Social sharing features
- [ ] Rewards and badges system
- [ ] Integration with real carbon offset APIs

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Credits

- **Developed by**: Environment Cleaner Team
- **AI powered by**: Google Gemini
- **Framework**: Streamlit
- **Games**: Pygame
- **Icons**: Flaticon

## 📞 Support

For questions or issues:
- Open an issue on GitHub
- Contact: your-email@example.com

---

**Made with 💚 for a greener planet 🌍**
