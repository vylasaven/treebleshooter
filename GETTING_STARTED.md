# Getting Started with Treebleshooter

Welcome Allen! This guide will walk you through everything you need to get started with your Treebleshooter project.

## Prerequisites Setup

### 1. Setting Up Git and GitHub

#### Create a GitHub Account
1. Go to [github.com](https://github.com)
2. Click "Sign up" and create your account
3. Verify your email address

#### Install Git on Your Mac
1. Open Terminal (find it in Applications > Utilities)
2. Install Homebrew if you don't have it:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
3. Install Git:
   ```bash
   brew install git
   ```

#### Configure Git
Run these commands in Terminal (replace with your info):
```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

#### Set up SSH Key for GitHub
1. Generate an SSH key:
   ```bash
   ssh-keygen -t ed25519 -C "your.email@example.com"
   ```
   (Just press Enter for all prompts to use defaults)

2. Copy your public key:
   ```bash
   pbcopy < ~/.ssh/id_ed25519.pub
   ```

3. Add to GitHub:
   - Go to GitHub.com > Settings > SSH and GPG keys
   - Click "New SSH key"
   - Paste the key and save

### 2. Install Claude Code

1. **Purchase Claude Code Subscription** ($20/month - worth it!)
   - Go to [claude.ai](https://claude.ai)
   - Sign up and subscribe to Claude Code

2. **Install Claude Code CLI**
   ```bash
   brew install anthropic/tap/claude-code
   ```

3. **Authenticate Claude Code**
   ```bash
   claude-code auth
   ```
   Follow the prompts to log in with your Claude account

### 3. Install Python and PyQt5

1. **Install Python 3.11+**
   ```bash
   brew install python@3.11
   ```

2. **Verify Python installation**
   ```bash
   python3 --version
   ```

## Setting Up the Project

### 1. Clone This Repository

If David has pushed this to GitHub:
```bash
git clone git@github.com:USERNAME/treebleshooter.git
cd treebleshooter
```

Or if working locally:
```bash
cd ~/treebleshooter
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it (you'll do this every time you work on the project)
source venv/bin/activate

# Your terminal prompt should now show (venv) at the beginning
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

## Understanding the Project Structure

```
treebleshooter/
├── main.py                 # Application entry point
├── src/
│   ├── models/            # Data models (tree structures)
│   ├── views/             # UI components
│   ├── controllers/       # Business logic
│   └── utils/             # Helper functions
├── data/                   # Saved troubleshooting guides
├── resources/             # Images, icons, styles
└── tests/                 # Unit tests
```

## Key Concepts

### What is a Troubleshooting Tree?
Think of it like a "Choose Your Own Adventure" book:
- Each node is a question or diagnostic step
- Each answer leads to a different path
- Paths eventually lead to solutions or further diagnostics

### Example Tree Structure:
```
"Computer won't start"
├── "Is it plugged in?"
│   ├── Yes → "Check power button"
│   └── No → "Plug it in and try again"
└── "Any lights showing?"
    ├── Yes → "Check monitor connection"
    └── No → "Test power outlet"
```

## Making Changes

### Basic Git Workflow

1. **Make your changes** in the code

2. **Check what changed**:
   ```bash
   git status
   ```

3. **Add changes**:
   ```bash
   git add .
   ```

4. **Commit changes**:
   ```bash
   git commit -m "Describe what you changed"
   ```

5. **Push to GitHub**:
   ```bash
   git push
   ```

### Using Claude Code for Help

When you're stuck or want to add features:
```bash
# In the project directory
claude-code

# Then ask questions like:
# "How do I add a new button to the main window?"
# "Help me create a new troubleshooting node type"
# "Debug this error: [paste error]"
```

## Troubleshooting Common Issues

### Virtual Environment Not Activating
- Make sure you're in the project directory
- Run: `source venv/bin/activate`
- On Windows, use: `venv\Scripts\activate`

### PyQt5 Import Errors
- Ensure virtual environment is activated
- Reinstall: `pip install --upgrade PyQt5`

### Application Won't Start
- Check Python version: `python --version` (should be 3.11+)
- Check all dependencies: `pip list`
- Look for error messages in terminal

## Next Steps

1. **Run the application** and explore the interface
2. **Create your first troubleshooting guide** using the wizard
3. **Save and load** guides to understand the data format
4. **Customize** the appearance in `resources/styles.qss`
5. **Add your own features** - the code is well-commented!

## Getting Help

- **Claude Code**: Your AI pair programmer (`claude-code` in terminal)
- **Project Documentation**: Check the `docs/` folder
- **Python/PyQt5 Docs**: 
  - [PyQt5 Documentation](https://www.riverbankcomputing.com/static/Docs/PyQt5/)
  - [Python Official Docs](https://docs.python.org/3/)

## Tips for Success

1. **Commit often** - Save your progress frequently with git
2. **Test as you go** - Run the app after each change
3. **Read error messages** - They usually tell you exactly what's wrong
4. **Use Claude Code** - It's like having an expert sitting next to you
5. **Have fun!** - This is your project to shape however you want

---

Remember: Every expert was once a beginner. Take it one step at a time, and don't hesitate to experiment!