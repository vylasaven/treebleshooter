# Contributing to Treebleshooter 🎯

First off, thanks for taking the time to contribute! The fact that you're reading this means you're awesome. 🦆

## Table of Contents
- [How Can I Contribute?](#how-can-i-contribute)
- [Your First Contribution](#your-first-contribution)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Adding Troubleshooting Guides](#adding-troubleshooting-guides)

## How Can I Contribute?

### 🐛 Reporting Bugs
Found something broken? Let us know!
- Check if the bug already exists in [Issues](https://github.com/davidarnold/treebleshooter/issues)
- If not, [create a new issue](https://github.com/davidarnold/treebleshooter/issues/new?template=bug_report.md)
- Include: what you did, what happened, what should have happened
- Bonus points for including the error message!

### 💡 Suggesting Features
Have an idea to make Treebleshooter better?
- Check [existing feature requests](https://github.com/davidarnold/treebleshooter/issues?q=is%3Aissue+label%3Aenhancement)
- [Create a feature request](https://github.com/davidarnold/treebleshooter/issues/new?template=feature_request.md)
- Explain the problem it solves and who it helps

### 🎨 Contributing Troubleshooting Guides
This is the fun part! Add your own whimsical guides:
1. Create a new `.tsg` file in `data/examples/`
2. Follow the existing format (they're just JSON!)
3. Make it funny, helpful, or both
4. Test it works in the app
5. Submit a PR with your guide

### 🔧 Contributing Code
Ready to dive into the code? Awesome!
- Fix bugs (look for `good first issue` labels)
- Add features
- Improve documentation
- Add tests

## Your First Contribution

New to open source? No problem! Here's how to start:

1. **Find a good first issue**
   - Look for issues labeled [`good first issue`](https://github.com/davidarnold/treebleshooter/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22)
   - Or add a fun troubleshooting guide (easiest way to start!)

2. **Comment on the issue**
   - Say you'd like to work on it
   - Ask any questions you have

3. **Make your changes**
   - Fork the repo
   - Create a branch: `git checkout -b my-awesome-feature`
   - Make your changes
   - Test them!

4. **Submit a Pull Request**
   - Push to your fork
   - Open a PR with a clear title and description

## Development Setup

```bash
# 1. Fork and clone the repo
git clone https://github.com/YOUR-USERNAME/treebleshooter.git
cd treebleshooter

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
python main.py

# 5. Run tests
python -m pytest tests/ -v
```

## Pull Request Process

1. **Before submitting:**
   - Run tests: `python -m pytest tests/`
   - Test the app manually
   - Update documentation if needed
   - Add tests for new features

2. **PR Guidelines:**
   - Clear title describing the change
   - Reference any related issues (#123)
   - Include screenshots for UI changes
   - Describe what you changed and why

3. **After submitting:**
   - Watch for review comments
   - Make requested changes
   - Be patient and friendly!

## Style Guidelines

### Python Code Style
```python
# Good class naming
class TroubleshootingGuide:  # PascalCase for classes
    
    def load_guide(self):  # snake_case for methods
        # Clear, helpful comments
        guide_data = self._parse_json()  # Private methods start with _
        return guide_data
```

### Commit Messages
```
✅ Good: "Fix radio buttons not appearing after guide restart"
✅ Good: "Add quantum coffee temperature guide"
❌ Bad: "Fixed stuff"
❌ Bad: "Update guide_executor_view.py"
```

### Documentation
- Write like you're explaining to a friend
- Include examples
- Add humor where appropriate
- Keep technical docs clear and concise

## Adding Troubleshooting Guides

Want to add a funny troubleshooting guide? Here's a template:

```json
{
  "metadata": {
    "title": "Your Funny Problem",
    "description": "When your gadget does that thing",
    "author": "Your Name",
    "version": "1.0.0",
    "created_date": "2024-01-01",
    "last_modified_date": "2024-01-01",
    "tags": ["funny", "gadget"],
    "difficulty_level": "Easy",
    "estimated_time_minutes": 5
  },
  "root_node_id": "start",
  "nodes": {
    "start": {
      "node_id": "start",
      "question": "Is your gadget doing the thing?",
      "description": "Let's figure this out",
      "help_text": "Be honest",
      "parent_node_id": null,
      "answers": [
        {
          "answer_id": "yes",
          "answer_text": "Yes, it's doing the thing",
          "next_node_id": null,
          "is_solution": true,
          "solution_text": "Turn it off and on again. It's always that."
        }
      ]
    }
  }
}
```

## Community Guidelines

### Be Awesome To Each Other
- Be welcoming and inclusive
- Be patient with newcomers
- Be constructive with criticism
- Assume good intentions
- No hate speech, harassment, or trolling

### The Vibe We're Going For
- Helpful but not condescending
- Professional but with personality
- Serious about quality, playful about everything else
- Like rubber duck debugging, but the duck talks back

## Questions?

- Create a [discussion](https://github.com/davidarnold/treebleshooter/discussions)
- Open an issue with the `question` label
- Be patient - this is a side project!

## Recognition

Contributors will be added to our [CONTRIBUTORS.md](CONTRIBUTORS.md) file! 

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

Ready to help people troubleshoot their quantum coffee makers and existential toasters? Let's do this! 🚀