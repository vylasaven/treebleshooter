#!/bin/bash

# ===============================================
#  🌳 TREEBLESHOOTER LAUNCHER 🌳
#  The Easiest Way to Run Your Troubleshooting App
#  Created for Allen by David (and Claude)
# ===============================================

echo ""
echo "🚀 ========================================= 🚀"
echo "   Welcome to Treebleshooter Launcher!"
echo "   Your journey to troubleshooting mastery"
echo "   begins in 3... 2... 1..."
echo "🚀 ========================================= 🚀"
echo ""

# ℹ️ Fun Fact: This script is smarter than 73% of rubber ducks
sleep 1

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Oops! Can't find main.py"
    echo "ℹ️  Make sure you run this script from the treebleshooter folder"
    echo "ℹ️  Try: cd ~/treebleshooter"
    echo "ℹ️  Then: ./run_treebleshooter.sh"
    exit 1
fi

echo "📁 Checking project structure..."
echo "ℹ️  Did you know? Your app has $(find src -name "*.py" | wc -l) Python files!"
sleep 1

# Check if Python 3 is installed
echo ""
echo "🐍 Checking for Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "ℹ️  Python is like coffee for computers - essential!"
    echo "ℹ️  Install it with: brew install python@3.11"
    echo "ℹ️  (If you don't have brew, visit https://brew.sh first)"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo "✅ Found $PYTHON_VERSION"
echo "ℹ️  Fun fact: Python was named after Monty Python, not the snake!"
sleep 1

# Check if virtual environment exists
echo ""
echo "🔮 Looking for virtual environment..."
if [ ! -d "venv" ]; then
    echo "📦 Creating your personal Python bubble (virtual environment)..."
    echo "ℹ️  This is like a sandbox where your app can play safely!"
    echo "ℹ️  It keeps all your app's toys (packages) in one place!"
    python3 -m venv venv
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to create virtual environment"
        echo "ℹ️  This is like trying to blow a bubble with no soap!"
        echo "ℹ️  Try: python3 -m pip install --user virtualenv"
        exit 1
    fi
    echo "✅ Virtual environment created!"
    echo "ℹ️  Your app now has its own private Python playground!"
else
    echo "✅ Virtual environment found!"
    echo "ℹ️  Your Python playground is ready for action!"
fi

# Activate virtual environment
echo ""
echo "🎭 Activating virtual environment..."
echo "ℹ️  This is like putting on your troubleshooting cape!"
source venv/bin/activate

if [ $? -ne 0 ]; then
    echo "❌ Failed to activate virtual environment"
    echo "ℹ️  The cape got tangled! Try running: source venv/bin/activate manually"
    exit 1
fi

echo "✅ Virtual environment activated!"
echo "ℹ️  You're now in the Matrix... I mean, the venv!"
sleep 1

# Check and install requirements
echo ""
echo "📚 Checking dependencies..."
echo "ℹ️  These are like the ingredients for your app recipe!"

# Check if PyQt5 is installed (our main dependency)
if ! python -c "import PyQt5" 2>/dev/null; then
    echo "📥 Installing required packages..."
    echo "ℹ️  This is like downloading superpowers for your app!"
    echo "ℹ️  PyQt5: Makes things pretty (very important!)"
    echo "ℹ️  And other magical ingredients..."
    echo ""
    
    pip install --upgrade pip > /dev/null 2>&1
    pip install -r requirements.txt
    
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install requirements"
        echo "ℹ️  The package delivery drone crashed!"
        echo "ℹ️  Try running: pip install -r requirements.txt"
        echo "ℹ️  If that fails, sacrifice a rubber duck to the Python gods"
        exit 1
    fi
    echo ""
    echo "✅ All packages installed!"
    echo "ℹ️  Your app is now fully armed and operational!"
else
    echo "✅ All dependencies are already installed!"
    echo "ℹ️  Your app's utility belt is fully stocked!"
fi

# Check if example guides exist
echo ""
echo "📖 Checking example guides..."
if [ ! -d "data/examples" ] || [ -z "$(ls -A data/examples 2>/dev/null)" ]; then
    echo "🎨 Creating hilarious example guides..."
    echo "ℹ️  Including classics like 'When Your Toaster Gets Existential'"
    echo "ℹ️  And 'Quantum Coffee Temperature Issues'"
    python create_example_guides.py > /dev/null 2>&1
    echo "✅ Example guides created!"
    echo "ℹ️  8 whimsical troubleshooting scenarios ready!"
else
    GUIDE_COUNT=$(ls data/examples/*.tsg 2>/dev/null | wc -l)
    echo "✅ Found $GUIDE_COUNT example guides!"
    echo "ℹ️  Each one more ridiculous than the last!"
fi

sleep 1

# Final countdown
echo ""
echo "🎬 ========================================= 🎬"
echo "   LAUNCHING TREEBLESHOOTER!"
echo "   ℹ️  Pro tip: The app looks best in dark mode!"
echo "   ℹ️  Another tip: Try the Quantum Coffee guide!"
echo "   ℹ️  Final tip: Ctrl+C quits the app cleanly!"
echo "🎬 ========================================= 🎬"
echo ""

sleep 2

echo "🚀 Initiating launch sequence..."
echo "ℹ️  If the app doesn't start, try turning it off and on again"
echo "ℹ️  (That's IT Crowd humor - your rubber duck will get it)"
echo ""

# Run the application
python main.py

# Check exit status
if [ $? -eq 0 ]; then
    echo ""
    echo "👋 ========================================= 👋"
    echo "   Thanks for using Treebleshooter!"
    echo "   ℹ️  Your troubleshooting skills increased by 42 points!"
    echo "   ℹ️  Come back soon for more decision tree adventures!"
    echo "👋 ========================================= 👋"
else
    echo ""
    echo "💥 ========================================= 💥"
    echo "   Oh no! Something went wrong!"
    echo "   ℹ️  Don't panic! This is troubleshootable!"
    echo "   ℹ️  Check the error message above"
    echo "   ℹ️  Or try running: python main.py"
    echo "   ℹ️  Still stuck? Time to debug the debugger!"
    echo "💥 ========================================= 💥"
fi

# Deactivate virtual environment
deactivate 2>/dev/null

echo ""
echo "🏁 Script complete! You're a troubleshooting champion! 🏆"