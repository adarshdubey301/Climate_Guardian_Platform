import subprocess
import sys
import os

def run_game():
    """Run the Fire Rescue Ursina game as a separate process."""
    script = os.path.join(os.path.dirname(__file__), 'fire_rescue_game.py')
    try:
        subprocess.run([sys.executable, script], check=True)
    except Exception as e:
        # Re-raise so caller can display an error message
        raise
