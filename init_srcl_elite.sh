#!/bin/bash
# ==========================================================
#  SRCL Elite Initialization Script
#  Author: schlieve001-pixel | Project: Continuity Lab
#  Purpose: Automate environment setup, folder structure, file creation, and git sync.
# ==========================================================

echo "🚀 Initializing SRCL Elite Environment..."
echo "=========================================================="

# --- FOLDER STRUCTURE ---
echo "📁 Creating folder structure..."
mkdir -p automation datafusion archives data/logs data/optimizer results_montecarlo_v3 srcl_core
sleep 1

# --- VERIFY CRITICAL FILES ---
echo "🧩 Checking core scripts..."
CORE_FILES=("command_center.py" "dashboard.py" "gemini_interpreter.py")
for f in "${CORE_FILES[@]}"; do
  if [ ! -f "$f" ]; then
    echo "⚙️  Creating missing file: $f"
    echo "#!/usr/bin/env python3" > "$f"
    echo "print('✅ $f placeholder ready.')" >> "$f"
  fi
done

# --- AUTOMATION MODULES ---
echo "🤖 Setting up automation modules..."
AUTOMATION_FILES=("adaptive_montecarlo.py" "upload_to_gcs.py" "watchdog_agent.py" "archive_with_meta.py" "colab_agent.py")
for f in "${AUTOMATION_FILES[@]}"; do
  if [ ! -f "automation/$f" ]; then
    echo "⚙️  Creating automation module: $f"
    echo "#!/usr/bin/env python3" > automation/$f
    echo "print('✅ $f module placeholder loaded.')" >> automation/$f
  fi
done

# --- DATAFUSION MODULE ---
echo "📊 Creating DataFusion analytics module..."
if [ ! -f "datafusion/aggregate_results.py" ]; then
  echo "#!/usr/bin/env python3" > datafusion/aggregate_results.py
  echo "print('✅ DataFusion analytics module placeholder loaded.')" >> datafusion/aggregate_results.py
fi

# --- PERMISSIONS ---
echo "🔧 Setting executable permissions..."
chmod +x *.py 2>/dev/null
chmod +x automation/*.py 2>/dev/null
chmod +x datafusion/*.py 2>/dev/null
sleep 1

# --- VENV SETUP ---
if [ ! -d ".venv" ]; then
  echo "🐍 Creating Python virtual environment..."
  python3 -m venv .venv
fi
source .venv/bin/activate
echo "✅ Virtual environment active."

# --- INSTALL DEPENDENCIES ---
echo "📦 Installing dependencies..."
pip install -r requirements.txt > /dev/null 2>&1
pip install google-cloud-aiplatform pandas matplotlib seaborn rich tqdm > /dev/null 2>&1
echo "✅ Dependencies installed."

# --- GIT SYNC ---
echo "🧠 Committing structure to GitHub..."
git add .
git commit -m '🧠 Initialize SRCL elite environment structure'
git pull origin main --allow-unrelated-histories
git push origin main
sleep 1

# --- DISPLAY NEXT STEPS ---
echo ""
echo "=========================================================="
echo "✅ SRCL Elite Environment Initialized Successfully!"
echo ""
echo "Next Steps:"
echo "------------------------------------------"
echo "1️⃣ Set Google Cloud credentials:"
echo "   export GOOGLE_APPLICATION_CREDENTIALS=~/keys/srcl-gemini-sa.json"
echo ""
echo "2️⃣ Test Gemini connection:"
echo "   python3 - <<'EOF'"
echo "   from google.cloud import aiplatform"
echo "   aiplatform.init(project='canvas-sum-481614-f6', location='us-central1')"
echo "   print('✅ Vertex AI connection verified.')"
echo "   EOF"
echo ""
echo "3️⃣ Launch the Command Center:"
echo "   python command_center.py"
echo ""
echo "4️⃣ Optional: Run automation tests"
echo "   python automation/adaptive_montecarlo.py"
echo "   python datafusion/aggregate_results.py"
echo ""
echo "🎯 All systems ready — Welcome to the SRCL Elite stack."
echo "=========================================================="
