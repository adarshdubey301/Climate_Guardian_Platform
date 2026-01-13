import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import time
try:
    from groq import Groq
except ImportError:
    Groq = None

from PIL import Image
import os
import random
import auth  # Import authentication module

# Initialize session state variables at the start
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

def main():
    # Now this will work without crashing
    if not st.session_state['logged_in']:
        st.write("Please log in.")
    # ... rest of your code

# ==========================================
# 0. CONFIGURATION & STYLING
# ==========================================
st.set_page_config(page_title="ClimateGuardian AI", page_icon="🌿", layout="wide", initial_sidebar_state="collapsed")

# Configure the Groq API key and instantiate client
_groq_key = st.secrets.get("GROQ_API_KEY", "") if hasattr(st, "secrets") else ""
groq_client = None
if Groq:
    if _groq_key and _groq_key not in ['YOUR_API_KEY_HERE', 'gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE']:
        try:
            groq_client = Groq(api_key=_groq_key)
        except Exception:
            groq_client = None


# --- CUSTOM CSS FOR ECO THEME ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background: linear-gradient(135deg, #f4fdf4 0%, #e8f5e9 100%);
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #e8f5e9;
        border-right: 3px solid #c8e6c9;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #2e7d32;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #4CAF50;
        color: white;
        border-radius: 12px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;
    }
    div.stButton > button:hover {
        background-color: #45a049;
        transform: scale(1.05);
    }
    
    /* Input Fields */
    .stTextInput > div > div > input {
        border-radius: 10px;
        border: 2px solid #4CAF50;
    }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #1b5e20;
        font-size: 2em;
        font-weight: bold;
    }
    
    /* Custom Card */
    .eco-card {
        padding: 25px;
        background-color: white;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 20px;
        border-left: 5px solid #4CAF50;
    }
    
    /* Game Card */
    .game-card {
        padding: 30px;
        background: linear-gradient(135deg, #e8f5e9 0%, #c8e6c9 100%);
        border-radius: 20px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        margin-bottom: 25px;
        border: 3px solid #4CAF50;
        text-align: center;
    }
    
    /* Progress Bar Custom */
    .progress-container {
        background-color: #e0e0e0;
        border-radius: 20px;
        padding: 3px;
        margin: 10px 0;
    }
    
    .progress-bar {
        background: linear-gradient(90deg, #4CAF50 0%, #8BC34A 100%);
        height: 25px;
        border-radius: 20px;
        text-align: center;
        color: white;
        font-weight: bold;
        line-height: 25px;
    }
    
    /* Chat Messages */
    .chat-message {
        padding: 10px 15px;
        border-radius: 10px;
        margin: 10px 0;
    }
    
    .user-message {
        background-color: #4CAF50;
        color: white;
        margin-left: 20%;
    }
    
    .assistant-message {
        background-color: #f0f0f0;
        color: #333;
        margin-right: 20%;
    }
    </style>
    """, unsafe_allow_html=True)

# ==========================================
# 1. SESSION STATE SETUP
# ==========================================
if 'student_data' not in st.session_state:
    st.session_state['student_data'] = pd.DataFrame(columns=['Student_ID', 'Action', 'Points', 'Date'])

if 'messages' not in st.session_state:
    st.session_state['messages'] = [{"role": "assistant", "content": "🌿 Hi! I'm EcoBot. I can generate quizzes, give tips, or help you save the planet!"}]

if 'quiz_data' not in st.session_state:
    st.session_state['quiz_data'] = []

# Game-specific session states
if 'carbon_footprint' not in st.session_state:
    st.session_state['carbon_footprint'] = 100
    
if 'eco_score' not in st.session_state:
    st.session_state['eco_score'] = 0

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================

def get_groq_response(prompt, model="llama-3.3-70b-versatile"):
    """Get response from Groq API."""
    if not groq_client:
        raise RuntimeError("Groq client not initialized.")
    
    completion = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=model,
        temperature=0.7,
        max_tokens=1024,
    )
    return completion.choices[0].message.content


def test_groq_connection(timeout=10):
    """Simple diagnostic call to verify Groq connectivity and API key validity.
    Returns (success: bool, message: str)"""
    api_key = st.secrets.get('GROQ_API_KEY') if hasattr(st, 'secrets') else None
    # Check against known placeholders
    if not api_key or api_key in (None, '', 'YOUR_API_KEY_HERE', 'gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE'):
        return False, 'Groq API key not configured. Put your key in .streamlit/secrets.toml.'

    try:
        test_prompt = "Say 'hello' in one short sentence."
        if not groq_client:
             return False, "Groq client failed to initialize."
             
        response = groq_client.chat.completions.create(
            messages=[{"role": "user", "content": test_prompt}],
            model="llama-3.3-70b-versatile",
        )
        text = response.choices[0].message.content

        if text and text.strip():
            return True, text.strip()
        return False, 'Groq returned an empty response.'

    except Exception as e:
        return False, str(e)


def parse_groq_error(msg):
    """Return a short actionable suggestion based on common Groq error messages."""
    if not msg:
        return "No error message available. Try running 'Test Groq Connection' to get details."
    lm = msg.lower()
    if any(k in lm for k in ['api key not valid', 'api_key_invalid', 'invalid api key', 'invalid key', '401', '403', 'unauthorized']):
        return "Invalid or unauthorized API key. Check your key in `.streamlit/secrets.toml`."
    if 'missing key' in lm or 'missing api' in lm:
        return "API key missing — add `GROQ_API_KEY` to `.streamlit/secrets.toml`."
    if 'quota' in lm or 'rate' in lm or '429' in lm:
        return "Rate limit exceeded — wait a moment before trying again."
    return "No specific recommendation could be inferred. Copy the raw error (debug) and paste it here or share it with me for help."

def _load_local_question():
    """Load a random question from local JSON bank and convert to AI-style output"""
    import json
    p = os.path.join('assets', 'questions_sustainability.json')
    try:
        with open(p, 'r', encoding='utf-8') as f:
            qbank = json.load(f)
        if not qbank:
            return None
        sel = random.choice(qbank)
        letters = ['A', 'B', 'C', 'D']
        ans_letter = letters[sel['ans']] if 'ans' in sel and isinstance(sel['ans'], int) else 'A'
        return {
            'q': sel.get('q', 'No question'),
            'options': sel.get('options', []),
            'ans': ans_letter,
            'exp': sel.get('exp', '')
        }
    except Exception as ex:
        # local fallback failed
        return None


def generate_ai_quiz_question():
    """Generates a dynamic quiz question using Groq."""
    api_key = st.secrets.get('GROQ_API_KEY') if hasattr(st, 'secrets') else None

    # If no API key configured, use local bank and set transient notice
    if not api_key or api_key in (None, '', 'YOUR_API_KEY_HERE', 'gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE'):
        q = _load_local_question()
        if q:
            st.session_state['fallback_notice'] = 'Groq AI unavailable — using local question bank.'
            st.session_state['fallback_notice_time'] = time.time()
            return q
        else:
            st.error('AI generation unavailable and local question bank could not be loaded.')
            return None

    prompt = (
        "Generate 1 multiple choice question about environmental sustainability, recycling, or climate change.\n"
        "Strictly follow this format using the pipe symbol (|) as a separator:\n"
        "Question Text | Option A | Option B | Option C | Option D | Correct Option (A/B/C/D) | Short Explanation"
    )

    try:
        text = get_groq_response(prompt, model="llama-3.3-70b-versatile")

        if text:
            parts = text.split('|')
            if len(parts) >= 6:
                return {
                    "q": parts[0].strip(),
                    "options": [parts[1].strip(), parts[2].strip(), parts[3].strip(), parts[4].strip()],
                    "ans": parts[5].strip().upper(),
                    "exp": parts[6].strip() if len(parts) > 6 else "Great job saving the planet!"
                }

        # Unexpected or empty output - fall back to local and show brief notice
        local_q = _load_local_question()
        if local_q:
            st.session_state['fallback_notice'] = 'AI returned unexpected format — using local question bank.'
            st.session_state['fallback_notice_time'] = time.time()
            return local_q
        return None

    except Exception as e:
        msg = str(e)
        # Common invalid-key detection
        if 'API key not valid' in msg or 'API_KEY_INVALID' in msg or 'Missing key' in msg or 'invalid' in msg.lower():
            st.session_state['fallback_notice'] = 'AI generation failed: invalid/missing Groq key — using local questions.'
            st.session_state['fallback_notice_time'] = time.time()
            local_q = _load_local_question()
            if local_q:
                return local_q
        st.error(f'Error generating quiz: {msg}')
        local_q = _load_local_question()
        if local_q:
            st.session_state['fallback_notice'] = 'AI generation error — using local question bank.'
            st.session_state['fallback_notice_time'] = time.time()
            return local_q
        return None

def log_action(action, points):
    """Log student action to database and persist eco score for logged-in user"""
    student_id = st.session_state.get('username', 'Student_User')
    new_data = pd.DataFrame({
        'Student_ID': [student_id], 
        'Action': [action],
        'Points': [points],
        'Date': [datetime.date.today()]
    })
    st.session_state['student_data'] = pd.concat([st.session_state['student_data'], new_data], ignore_index=True)
    st.session_state['eco_score'] += points

    # Persist to user database if logged in
    if st.session_state.get('username'):
        try:
            auth.update_user_score(st.session_state['username'], int(st.session_state['eco_score']))
            st.session_state['user_info'] = auth.get_user_info(st.session_state['username'])
        except Exception as e:
            st.warning(f"Could not persist eco score: {e}")

# ==========================================
# 3. AI CHAT INTERFACE
# ==========================================

def chat_interface():
    st.markdown('<div class="eco-card"><h3>🤖 EcoBot Mentor</h3><p>Ask me anything about nature and sustainability!</p></div>', unsafe_allow_html=True)
    
    # --- Groq Diagnostics ---
    with st.expander("🔧 Groq Diagnostics", expanded=False):
        api_key = st.secrets.get('GROQ_API_KEY') if hasattr(st, 'secrets') else None
        key_ok = bool(api_key and api_key not in (None, '', 'YOUR_API_KEY_HERE', 'gsk_YOUR_ACTUAL_GROQ_API_KEY_HERE'))
        st.write(f"**API key configured:** {'Yes' if key_ok else 'No'}")
        if st.button("Test Groq Connection", key="test_groq"):
            with st.spinner("Testing Groq connection..."):
                ok, msg = test_groq_connection()
                if ok:
                    st.success(f"Connection OK — sample reply: {msg}")
                else:
                    st.error(f"Connection failed: {msg}")
                    st.info("If the key is missing or invalid, add it to `.streamlit/secrets.toml`.")

        # Retry last failed prompt (if any) and debug controls
        if st.session_state.get('last_prompt'):
            st.write(f"**Last prompt:** {st.session_state['last_prompt']}")
            if st.button("Retry last prompt", key="retry_prompt"):
                with st.spinner("Retrying last prompt..."):
                    try:
                        ai_prompt = f"You are EcoBot, a fun sustainability expert for students. Keep it short (2-3 sentences) and encouraging. Answer: {st.session_state['last_prompt']}"
                        reply = get_groq_response(ai_prompt)
                        if reply:
                            st.session_state['messages'].append({"role": "assistant", "content": reply})
                            st.success("Retry successful — response added to chat.")
                        else:
                            st.error("Retry returned an empty response.")
                    except Exception as e:
                        st.session_state['last_groq_error'] = str(e)
                        st.error(f"Retry failed: {st.session_state['last_groq_error']}")

        if st.session_state.get('last_groq_error'):
            if st.checkbox("Show raw error (debug)", key="show_raw_err"):
                st.code(st.session_state['last_groq_error'])
            st.write("**Suggested action:**")
            st.info(parse_groq_error(st.session_state['last_groq_error']))

    # Display chat messages
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.markdown(f'<div class="chat-message user-message">{msg["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message assistant-message">🌿 {msg["content"]}</div>', unsafe_allow_html=True)

    # Chat input
    if prompt := st.chat_input("How can I recycle glass?"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("EcoBot is thinking... 🌱"):
            try:
                ai_prompt = f"You are EcoBot, a fun sustainability expert for students. Keep it short (2-3 sentences) and encouraging. Answer: {prompt}"
                reply = get_groq_response(ai_prompt)
            except Exception as e:
                # Store the raw error and last prompt for diagnostics and show a friendly message to the user
                st.session_state['last_groq_error'] = str(e)
                st.session_state['last_prompt'] = prompt
                st.session_state['last_error_time'] = time.time()
                reply = "I'm having trouble connecting to the nature network. Try the 'Test Groq Connection' in the diagnostics or check your API key. 🌍"
                # Also display a brief, non-sensitive notice in the UI for quick help
                st.error(f"Groq error: {st.session_state.get('last_groq_error', 'Unknown error')} (see diagnostics)")
        
        st.session_state.messages.append({"role": "assistant", "content": reply})
        st.rerun()

# ==========================================
# 4. AI QUIZ GAME
# ==========================================

def quiz_interface():
    st.markdown('<div class="eco-card"><h3>🎮 AI Eco-Challenge</h3><p>Infinite questions generated by AI (local fallback used when API is not configured).</p></div>', unsafe_allow_html=True)
    
    # Fallback notices from AI generation are now suppressed to avoid showing technical messages in the UI.
    # If you want to inspect fallback events for debugging, enable logging to console or a debug panel.
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Generate multiple questions (default 4) and display them all
        if not st.session_state['quiz_data']:
            if st.button("🌱 Generate 4 New Questions", key="gen_quiz"):
                with st.spinner("Growing new questions..."):
                    qs = []
                    for _ in range(4):
                        q_data = generate_ai_quiz_question()
                        if q_data:
                            qs.append(q_data)
                        else:
                            break
                    if qs:
                        st.session_state['quiz_data'] = qs
                        st.rerun()
                    else:
                        st.error("AI couldn't generate questions. Try again.")
        
        if st.session_state['quiz_data']:
            questions = st.session_state['quiz_data']
            # Display all generated questions with independent answer controls
            for idx, q in enumerate(list(questions)):
                st.markdown("---")
                st.subheader(f"Q {idx+1}: {q['q']}")
                opts = q['options']
                choice = st.radio("Select an answer:", opts, key=f"quiz_choice_{idx}")
                choice_index = opts.index(choice)
                choice_letter = ["A", "B", "C", "D"][choice_index]
                if st.button("Submit Answer", key=f"submit_quiz_{idx}"):
                    if choice_letter == q['ans']:
                        st.balloons()
                        st.success(f"✅ Correct! 🎉 {q['exp']}")
                        log_action("AI Quiz Win", 15)
                        time.sleep(1)
                        # remove answered question
                        st.session_state['quiz_data'].pop(idx)
                        st.rerun()
                    else:
                        st.error(f"❌ Oops! The correct answer was Option {q['ans']}.")
                        st.warning(q['exp'])
                        time.sleep(2)
                        st.session_state['quiz_data'].pop(idx)
                        st.rerun()

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/4148/4148323.png", width=150)
        st.metric("🌱 Eco-Score", st.session_state['eco_score'])

# ==========================================
# 5. MISSION TRACKER
# ==========================================

def mission_tracker():
    st.markdown('<div class="eco-card"><h3>📝 Daily Green Missions</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        action = st.selectbox("Select Mission Completed:", 
                              ["Recycled Plastic", "Planted a Tree", "Walked/Biked to School", 
                               "Saved Electricity", "Used Reusable Bag", "Composted Food"],
                              key="mission_select")
    
    with col2:
        points_map = {
            "Recycled Plastic": 5, 
            "Planted a Tree": 50, 
            "Walked/Biked to School": 20, 
            "Saved Electricity": 10, 
            "Used Reusable Bag": 5, 
            "Composted Food": 15
        }
        st.metric(label="Points Value", value=points_map[action])
    
    if st.button("✅ Log Mission", key="log_mission"):
        log_action(action, points_map[action])
        st.success(f"Mission '{action}' logged! +{points_map[action]} points")
        time.sleep(1)
        st.rerun()
    
    # Mission History
    st.markdown("### 📋 Mission History")
    df = st.session_state['student_data']
    if df.empty:
        st.info("No missions logged yet.")
    else:
        recent = df.tail(5).sort_index(ascending=False)
        st.dataframe(recent[['Action', 'Points', 'Date']], use_container_width=True)

# ==========================================
# 6. SUSTAINABILITY PREDICTOR
# ==========================================

def sustainability_predictor():
    st.markdown('<div class="eco-card"><h3>🔮 Predict Your Sustainability Impact</h3></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("#### 🌍 Carbon Footprint Tracker")
        
        transport = st.selectbox("🚗 Transportation:", 
                                ["Walk/Bike (-5 CO₂)", "Public Transport (-2 CO₂)", 
                                 "Electric Car (0 CO₂)", "Gasoline Car (+10 CO₂)"],
                                key="transport")
        
        diet = st.selectbox("🍽️ Diet:", 
                           ["Plant-Based (-3 CO₂)", "Local Produce (-2 CO₂)", 
                            "Mixed Diet (+2 CO₂)", "Imported Meat (+8 CO₂)"],
                           key="diet")
        
        energy = st.selectbox("💡 Energy:", 
                             ["Solar Power (-5 CO₂)", "Energy Saver (-3 CO₂)", 
                              "Normal Usage (+1 CO₂)", "High Consumption (+7 CO₂)"],
                             key="energy")
        
        if st.button("📊 Calculate Impact", key="calc_impact"):
            # Extract values
            transport_val = int(transport.split('(')[1].split()[0].replace('+', ''))
            diet_val = int(diet.split('(')[1].split()[0].replace('+', ''))
            energy_val = int(energy.split('(')[1].split()[0].replace('+', ''))
            
            change = transport_val + diet_val + energy_val
            st.session_state['carbon_footprint'] += change
            st.session_state['carbon_footprint'] = max(0, min(200, st.session_state['carbon_footprint']))
            
            if change < 0:
                st.success(f"🎉 Amazing! You reduced carbon by {abs(change)} units!")
                log_action("Carbon Reduction", abs(change) * 2)
                st.balloons()
            else:
                st.warning(f"⚠️ Your choices increased carbon by {change} units.")
            
            time.sleep(1)
            st.rerun()
    
    with col2:
        carbon = st.session_state['carbon_footprint']
        st.metric("🌡️ Your Carbon Level", f"{carbon} CO₂")
        
        # Status
        if carbon <= 50:
            status = "🌟 Eco Hero!"
            color = "#4CAF50"
        elif carbon <= 100:
            status = "👍 Good Job!"
            color = "#FFC107"
        else:
            status = "🔥 Need Improvement"
            color = "#F44336"
        
        st.markdown(f"**Status:** {status}")
        
        # Progress bar
        percentage = min(100, (carbon / 200) * 100)
        progress_html = f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {percentage}%; background-color: {color};">
                {int(percentage)}%
            </div>
        </div>
        """
        st.markdown(progress_html, unsafe_allow_html=True)
        
        if st.button("🔄 Reset", key="reset_carbon"):
            st.session_state['carbon_footprint'] = 100
            st.rerun()

# ==========================================
# 7. GAMES HUB (PYGAME EMBEDDED)
# ==========================================

def games_hub():
    st.markdown('<div class="eco-card"><h2>🎯 Interactive Sustainability Games</h2><p>Play, Learn, and Save the Planet!</p></div>', unsafe_allow_html=True)
    
    # Three games in grid layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="game-card">
            <h3>🏃 Eco-Runner</h3>
            <img src="https://cdn-icons-png.flaticon.com/512/3588/3588435.png" width="120">
            <p style="margin: 15px 0;">Control a person collecting leaves while avoiding waste! Get your carbon score to zero!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🎮 **How to Play:**\n- Use ↑↓ arrow keys to move\n- Collect green leaves (-10 CO₂)\n- Avoid red waste (+20 CO₂)\n- Goal: Reach 0 carbon!")
        
        if st.button("🎮 Launch Eco-Runner", key="launch_eco_runner"):
            st.success("✅ Game launching! Check the pygame window that opened.")
            st.balloons()
            try:
                import games.eco_runner as eco_runner
                eco_runner.run_game()
                # After game ends, add points (persisted inside log_action)
                log_action("Eco-Runner Victory", 50)
                st.success("🎉 Game completed! +50 points added!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error launching game: {str(e)}")
    
    with col2:
        st.markdown("""
        <div class="game-card">
            <h3>⚡ Renewable Energy Puzzle</h3>
            <img src="https://cdn-icons-png.flaticon.com/512/3176/3176215.png" width="120">
            <p style="margin: 15px 0;">Match renewable energy sources to the right locations and achieve net-zero emissions!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🎮 **How to Play:**\n- Click energy button (Solar/Wind/Hydro)\n- Click matching colored tiles\n- Correct = -50 emissions\n- Wrong = +30 emissions\n- Goal: Reach net-zero!")
        
        if st.button("🎮 Launch Renewable Energy Puzzle", key="launch_renewable"):
            st.success("✅ Game launching! Check the pygame window that opened.")
            st.balloons()
            try:
                import games.renewable_energy as renewable_energy
                renewable_energy.run_game()
                # After game ends, add points (persisted inside log_action)
                log_action("Renewable Energy Victory", 50)
                st.success("🎉 Game completed! +50 points added!")
                time.sleep(2)
                st.rerun()
            except Exception as e:
                st.error(f"Error launching game: {str(e)}")
    
    with col3:
        st.markdown("""
        <div class="game-card">
            <h3>♻️ Smart Waste Segregation</h3>
            <img src="https://cdn-icons-png.flaticon.com/512/3524/3524388.png" width="120">
            <p style="margin: 15px 0;">Use hand gestures to sort waste into correct bins! AI-powered recycling game!</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("🎮 **How to Play:**\n- Allow camera access\n- Use hand pinch to grab items\n- Sort into correct colored bins\n- Goal: High score before 5 misses!")
        
        if st.button("🎮 Launch Waste Segregation", key="launch_waste_seg"):
            # Import and run the game inline
            import games.waste_segregation as waste_segregation
            waste_segregation.run_game()

    # --- New: Fire Rescue 3D (Ursina) ---
    st.markdown("""
    <div class="game-card">
        <h3>🔥 Fire Rescue 3D</h3>
        <img src="https://cdn-icons-png.flaticon.com/512/482/482631.png" width="120">
        <p style="margin: 15px 0;">First-person mission: Protect the Sacred Tree from falling fireballs! Use mouse to shoot water.</p>
    </div>
    """, unsafe_allow_html=True)

    st.info("🎮 **How to Play:**\n- WASD to move | Mouse to aim | Click to shoot water\n- Protect the Sacred Tree — if a fireball hits leaves, the mission ends!")

    if st.button("🎮 Launch Fire Rescue", key="launch_fire_rescue"):
        st.success("✅ Game launching! Check the Ursina window that opened.")
        st.balloons()
        try:
            import games.fire_rescue as fire_rescue
            fire_rescue.run_game()
            # After game ends, award points (persisted in log_action)
            log_action("Fire Rescue Victory", 50)
            st.success("🎉 Mission complete! +50 points added!")
            time.sleep(2)
            st.rerun()
        except Exception as e:
            st.error(f"Error launching game: {str(e)}")

# ==========================================
# 8. ADMIN DASHBOARD
# ==========================================

def admin_dashboard():
    st.markdown('<div class="eco-card"><h3>🏫 School Sustainability Dashboard</h3></div>', unsafe_allow_html=True)
    
    df = st.session_state['student_data']
    
    if df.empty:
        st.info("📊 No data yet. Start logging missions and playing games!")
        return

    # Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("🌱 Total Eco-Points", df['Points'].sum())
    col2.metric("📊 Total Actions", len(df))
    col3.metric("🌳 Trees Planted", len(df[df['Action'] == "Planted a Tree"]))
    
    st.divider()
    
    # Charts
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        fig_pie = px.pie(df, names='Action', values='Points', 
                        title="Impact Distribution", 
                        color_discrete_sequence=px.colors.sequential.Greens_r)
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with chart_col2:
        action_summary = df.groupby('Action')['Points'].sum().reset_index()
        fig_bar = px.bar(action_summary, x='Action', y='Points', 
                        title="Top Activities",
                        color='Points',
                        color_continuous_scale='Greens')
        st.plotly_chart(fig_bar, use_container_width=True)
    
    # Activity Log
    st.markdown("### 📈 Activity Log")
    st.dataframe(df.sort_index(ascending=False), use_container_width=True)

# ==========================================
# 9. MAIN LAYOUT
# ==========================================

def main():
    # Check if user is logged in
    if not st.session_state['logged_in']:
        # Show login or signup page
        if st.session_state.get('show_signup', False):
            auth.signup_page()
        else:
            auth.login_page()
        return
    
    # User is logged in - show main app
    # Sidebar
    with st.sidebar:
        st.title("🌍 ClimateGuardian AI")
        
        try:
            st.image("https://cdn-icons-png.flaticon.com/512/3773/3773698.png", width=150)
        except:
            pass
        
        st.markdown("**Save Earth, Save Future** 🌿")
        
        # User Profile Section
        st.markdown("---")
        st.markdown(f"### 👤 Welcome, {st.session_state['username']}!")
        
        user_info = st.session_state.get('user_info', {})
        if user_info:
            st.metric("🌱 Total Eco-Score", user_info.get('eco_score', 0))
        
        st.markdown("---")
        
        menu = st.radio("📍 Navigate", ["🎓 Student Hub", "📊 Admin Dashboard"])
        
        st.divider()
        st.info("💡 **Tip:** Complete missions daily to earn Eco-Points!")
        
        # Logout button
        if st.button("🚪 Logout", key="logout_btn", use_container_width=True):
            # Update user score before logout
            if st.session_state['username']:
                auth.update_user_score(st.session_state['username'], st.session_state['eco_score'])
            auth.logout()
        
        st.caption("Developed by Environment Cleaner")

    # Header
    st.title(f"🌿 Welcome to ClimateGuardian AI, {st.session_state['username']}!")
    st.markdown("*Your AI-powered companion for a greener planet*")
    st.divider()

    # Main Content
    if menu == "🎓 Student Hub":
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🤖 AI Chat", 
            "🎮 AI Quiz", 
            "✅ Missions", 
            "🔮 Predict Sustainability",
            "🎯 Games Hub"
        ])
        
        with tab1:
            chat_interface()
        with tab2:
            quiz_interface()
        with tab3:
            mission_tracker()
        with tab4:
            sustainability_predictor()
        with tab5:
            games_hub()
            
    elif menu == "📊 Admin Dashboard":
        admin_dashboard()

if __name__ == "__main__":
    main()
