<img width="1456" height="816" alt="Treebleshooter - Rubber Duck Debugging Holographic Decision Tree" src="https://github.com/user-attachments/assets/34511ade-8381-4e4f-9cb6-09faa5938bbe" />

# 🎯 Treebleshooter

> *When your rubber duck needs a flowchart*

[![Tests](https://github.com/davidarnold/treebleshooter/workflows/Tests/badge.svg)](https://github.com/davidarnold/treebleshooter/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

Transform your tech support rage into hilarious troubleshooting guides. Because sometimes the problem really IS quantum coffee temperature.

![Treebleshooter Demo](docs/images/demo.gif)

## 🎬 Watch It Being Built!

Want to see how Treebleshooter came to life? [Watch the creation video](https://your-video-link-here.com) - bugs, breakthroughs, and rubber ducks included!

## ✨ Features

- **🌳 Visual Decision Trees** - Create branching troubleshooting paths with drag-and-drop ease
- **😄 Whimsical Example Guides** - Learn by laughing at our quantum coffee maker problems
- **🎨 Modern Dark Theme** - Easy on the eyes during those 3 AM debugging sessions
- **📦 Product Categorization** - Organize guides by product and problem type
- **💾 JSON-Based Storage** - Human-readable, version-control friendly guide format
- **🧪 Extensively Tested** - 14+ tests ensuring your guides always load correctly
- **🦆 Rubber Duck Approved** - Even includes a guide for when your rubber duck starts offering solutions

## 🚀 Quick Start

### One-Line Install & Run

```bash
curl -sSL https://raw.githubusercontent.com/davidarnold/treebleshooter/main/run_treebleshooter.sh | bash
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/davidarnold/treebleshooter.git
cd treebleshooter

# Run the easy setup script
./run_treebleshooter.sh

# Or set up manually
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 🎮 How to Use

1. **Launch Treebleshooter** - Run `python main.py`
2. **Pick a Product** - Choose from our hilarious examples or create your own
3. **Select a Problem** - What's gone wrong today?
4. **Follow the Guide** - Answer questions to reach a solution
5. **Create Your Own** - Build guides for your actual problems (or fictional ones!)

## 📚 Example Guides Included

- **Smart Toaster 3000** - When your toaster gets too smart for its own good
- **Quantum Coffee Maker** - Coffee that exists in multiple temperature states
- **Procrastination Station Pro** - For when you accidentally become productive
- **Motivational Mirror™** - When encouragement goes too far
- **Rubber Duck Debugger** - When your duck won't stop offering solutions

## 🛠️ For Developers

### Architecture
```
src/
├── models/         # Data structures (Guide, Node, Answer)
├── views/          # UI components (PyQt5)
├── controllers/    # Business logic
└── utils/          # Helpers and constants
```

### Running Tests
```bash
python -m pytest tests/ -v
```

### Creating Custom Guides
Guides are just JSON! Create a `.tsg` file:
```json
{
  "metadata": {
    "title": "My Device Won't Start",
    "description": "Troubleshooting power issues",
    "author": "Your Name"
  },
  "nodes": {
    "root": {
      "question": "Is it plugged in?",
      "answers": [
        {
          "answer_text": "No",
          "is_solution": true,
          "solution_text": "Plug it in. Problem solved!"
        }
      ]
    }
  }
}
```

## 🤝 Contributing

We love contributions! Whether it's:
- 🐛 Bug reports
- 💡 Feature ideas
- 🎨 UI improvements
- 😄 Funny troubleshooting guides
- 📚 Documentation updates

Check out our [Contributing Guide](CONTRIBUTING.md) to get started.

### Good First Issues
- Add a troubleshooting guide for your favorite gadget
- Improve the splash screen messages
- Add more color themes
- Create unit tests for uncovered code

## 📖 Documentation

- [Beginner Developer Guide](BEGINNER_DEVELOPER_GUIDE.md) - What's safe to change
- [Prompting Guide](ALLENS_PROMPTING_GUIDE.md) - How to work with AI assistants
- [Data Structures Guide](DATA_STRUCTURES_GUIDE.md) - Understanding the codebase
- [Contributing](CONTRIBUTING.md) - How to contribute

## 🏆 Why Treebleshooter?

- **It's Actually Useful** - Real companies need troubleshooting guides
- **It's Fun to Build For** - Add your own personality to guides
- **It's Educational** - Great project to learn PyQt5 and MVC architecture
- **It's Extensible** - Export to web, mobile, PDF... sky's the limit!

## 🗺️ Roadmap

- [ ] Web export functionality
- [ ] Collaborative editing
- [ ] AI-powered guide generation
- [ ] Mobile companion app
- [ ] Analytics on guide effectiveness
- [ ] Guide marketplace
- [ ] Integration with ticketing systems

## 📝 License

MIT License - see [LICENSE](LICENSE) file. Basically: do whatever you want with it!

## 🙏 Acknowledgments

- Created for Allen, who needed better troubleshooting tools
- Inspired by every tech support call that could've been a flowchart
- Special thanks to all rubber ducks who've listened to our debugging sessions
- Built with [Claude Code](https://claude.ai/code) assistance

## 🦆 Quote of the Day

> "Have you tried turning it off and on again?" - Every IT Support Ever

> "My toaster just asked me about the meaning of bread" - Actual Treebleshooter User

---


**Made with 💙 and a healthy dose of debugging frustration**

*P.S. - If you use this for actual tech support and it saves you time, please let us know. We're collecting success stories and hilarious failure tales equally.*
