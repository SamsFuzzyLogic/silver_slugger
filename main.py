import os
import subprocess

# Step 1: Run data generation
print("🔄 Generating fresh data...")
subprocess.run(["python", "generate_data.py"])

# Step 2: Launch Streamlit app
print("🚀 Launching Streamlit dashboard...")
subprocess.run(["streamlit", "run", "app.py"])
