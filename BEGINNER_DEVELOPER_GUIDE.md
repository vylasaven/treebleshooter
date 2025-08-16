# 🎯 Treebleshooter Beginner Developer Guide

Hey Allen! This guide will help you customize Treebleshooter without breaking anything. I've organized it from **SAFE** to **DANGER ZONE** so you know exactly what you can touch.

---

## 🟢 TOTALLY SAFE TO CHANGE (Go Wild!)

### 1. **All Text Content & Labels**
These are just strings - change them to whatever you want!

#### Application Title & Branding
**File:** `src/utils/constants.py`
```python
APP_NAME = "Treebleshooter"  # Change to "Allen's Debug Helper" or whatever!
APP_VERSION = "1.0.0"         # Update when you make changes
APP_AUTHOR = "Allen"          # That's you!
APP_DESCRIPTION = "Professional Troubleshooting Guide Creator"  # Make it fun!
```

#### Window Titles & Group Labels
**File:** `src/views/main_window.py` (lines 73-90)
- Change `"Select Product"` to `"Pick Your Troubled Device"`
- Change `"Problem Category"` to `"What's Wrong?"`
- Change any button text like `"Execute Guide"` to `"Let's Fix This!"`

#### Guide Executor Messages
**File:** `src/views/guide_executor_view.py`
- Line 53: `"No Guide Loaded"` → `"Pick a guide to get started!"`
- Line 83: `"Current Step"` → `"What's happening?"`
- Line 87: `"Ready to start troubleshooting"` → `"Let's solve this problem!"`
- Line 103: `"Select Your Answer"` → `"What describes your situation?"`

### 2. **Colors & Visual Style**
**File:** `src/styles/dark_theme.qss`

You can change ANY color in here! Some fun ones to try:
```css
/* Main background - currently dark gray */
QMainWindow {
    background-color: #1a1a2e;  /* Try #2d132c for purple or #0f3057 for blue */
}

/* The cyan accent color used throughout */
#primary-button {
    background-color: #00d4ff;  /* Try #ff6b6b for red or #4ecdc4 for teal */
}

/* Success/solution color */
#solution-group {
    border: 2px solid #00ff00;  /* Try #ffd700 for gold */
}
```

**Safe color changes:**
- Any hex color code (#rrggbb)
- Border widths (1px, 2px, 3px, etc.)
- Font sizes (but keep them reasonable: 10pt - 24pt)
- Padding and margins

### 3. **Example Troubleshooting Guides**
**Directory:** `data/examples/`

All `.tsg` files are just JSON! You can:
- Edit the funny text in any guide
- Change questions and answers
- Modify solution text
- Add more humor

**Example:** Open `data/examples/toast-too-dark.tsg` and change:
```json
"question": "Is your toast coming out darker than the depths of space?"
```
To:
```json
"question": "Is your toast basically charcoal at this point?"
```

### 4. **Product Catalog**
**File:** `data/product_catalog.json`

Add your own products! Copy this template:
```json
"your-product-id": {
    "product_id": "your-product-id",
    "product_name": "Allen's Amazing Gadget",
    "description": "Does things and stuff",
    "manufacturer": "Allen Industries",
    "version": "1.0.0",
    "problem_categories": {
        "not-working": {
            "category_id": "not-working",
            "category_name": "It's Broken",
            "description": "When it just won't work",
            "guide_ids": []
        }
    }
}
```

---

## 🟡 SAFE WITH CAUTION (Test After Changing)

### 1. **Window Sizes**
**File:** `src/utils/constants.py`
```python
WINDOW_MIN_WIDTH = 900   # Don't go below 600
WINDOW_MIN_HEIGHT = 700  # Don't go below 400
```

### 2. **File Extensions**
**File:** `src/utils/constants.py`
```python
GUIDE_FILE_EXTENSION = ".tsg"  # Keep this unless you update ALL file saves/loads
```

### 3. **Logging Messages**
**Files:** Any `.py` file with `logger.info()` or `logger.debug()`

You can change the text in logging messages:
```python
logger.info("Guide loaded successfully")  # Change to "Guide is ready to rock!"
```

### 4. **Splash Screen Messages**
**File:** `main.py` (lines 20-35)

Change the loading messages, but keep the structure:
```python
splash.showMessage("Initializing quantum troubleshooting matrix...", 
                  Qt.AlignBottom | Qt.AlignCenter, Qt.white)
```

---

## 🔴 DANGER ZONE (Don't Touch Unless You Know What You're Doing!)

### ❌ **DO NOT CHANGE These Things:**

1. **Function/Method Names**
   ```python
   def load_guide(self, guide):  # DON'T rename to 'load_the_guide'
   ```

2. **Class Names**
   ```python
   class GuideExecutorView(QWidget):  # DON'T rename classes
   ```

3. **Signal Names**
   ```python
   guide_completed = pyqtSignal(str)  # DON'T rename signals
   ```

4. **Dictionary Keys in Data Structures**
   ```python
   "node_id": "xyz"  # DON'T change to "node_identifier"
   "metadata": {...}  # DON'T change to "meta_data"
   ```

5. **Import Statements**
   ```python
   from PyQt5.QtWidgets import QWidget  # DON'T modify imports
   ```

6. **File Structure**
   ```
   src/
   ├── models/        # DON'T rename directories
   ├── views/         # DON'T move files between folders
   ├── controllers/   # DON'T change the structure
   ```

---

## 🎨 Quick Customization Ideas for Allen

### Make It Yours - Easy Mode:

1. **Change the Splash Screen** (`main.py`):
   - Add your own silly loading messages
   - Current: "Initializing quantum flux capacitors..."
   - Try: "Waking up the debugging ducks..." or "Charging the problem-solver..."

2. **Customize Button Text** (`src/views/main_window.py`):
   - "Create New Guide" → "Build a Troubleshooter"
   - "Execute Guide" → "Run It!"
   - "Edit Guide" → "Tweak It"

3. **Theme Colors** (`src/styles/dark_theme.qss`):
   - Make a "hacker green" theme: Change #00d4ff to #00ff00
   - Make a "sunset" theme: Use #ff6b6b, #feca57, #48dbfb
   - Make it "corporate boring": Use #4a4a4a, #6a6a6a, #8a8a8a

4. **Window Title** (`src/views/main_window.py` line 72):
   ```python
   self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
   # Change to:
   self.setWindowTitle(f"Allen's {APP_NAME} - Now With Extra Debugging!")
   ```

5. **Fun Easter Eggs** - Add these anywhere:
   - In solution text: "Solution: Have you tried turning it off and on again? (Classic!)"
   - In help text: "If all else fails, blame quantum mechanics"
   - In error messages: "Oops! The troubleshooter needs troubleshooting"

---

## 📝 How to Test Your Changes

1. **After changing text/labels:**
   ```bash
   python main.py
   ```
   - Click around and make sure your new text appears

2. **After changing colors:**
   ```bash
   python main.py
   ```
   - Check that text is still readable
   - Make sure buttons still look clickable

3. **After changing guides:**
   ```bash
   python test_gui_walkthrough.py
   ```
   - This ensures guides still load and work

4. **After ANY changes in the DANGER ZONE:**
   ```bash
   python -m pytest tests/ -v
   ```
   - ALL tests must pass!

---

## 🚀 Your First Customization Challenge

Try this sequence to get comfortable:

1. **Change the app name** in `src/utils/constants.py` to "Allen's Debug Buddy"
2. **Change the main color** in `dark_theme.qss` from cyan (#00d4ff) to green (#00ff00)
3. **Edit a funny message** in `data/examples/toast-too-dark.tsg`
4. **Run the app** and see your changes!

---

## 💡 Pro Tips

- **Use Find & Replace carefully** - If you change a color, use your editor's "Find All" to change it everywhere
- **Keep backups** - Before big changes, copy the file and name it `.backup`
- **One change at a time** - Easier to find what broke if something goes wrong
- **Read the comments** - I've added helpful comments throughout the code
- **The tests are your friend** - If tests pass, the app probably still works!

---

## 🆘 If You Break Something

1. **Check the terminal/console** for error messages
2. **Git is your friend**: `git diff` shows what you changed
3. **Revert a file**: `git checkout -- path/to/file.py`
4. **Nuclear option**: `git reset --hard` (undoes ALL changes)

---

## 🎉 Have Fun!

Remember: The worst thing that happens is you break something and have to revert. That's how we all learned! Make it yours, make it weird, make it wonderful.

Happy customizing!
- Your Helpful Debug Duck 🦆