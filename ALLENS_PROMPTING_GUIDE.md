# Allen's Guide to Prompting (David's Style Edition)

Hey Allen! So David asked me to break down his prompting style for you. After working through this entire Treebleshooter project with him, I've noticed some patterns that work really well, and some opportunities to level up. Let's dive in!

---

## 🎯 David's Prompting Strengths (What You're Already Doing Well)

### 1. **The Casual Expert Approach**
David has this great way of being technical without being stuffy. Look at these examples:

✅ **Good:** "perhaps let's add at the start a selection area for different products"
- Casual ("perhaps let's") but clear about what he wants
- Doesn't over-explain - trusts the AI understands context

❌ **What NOT to do:** "I would like to formally request that you implement a user interface component that allows for the selection of various product options"
- Too formal, too wordy, sounds like a robot

### 2. **The Bug Report Master**
When something breaks, David's got the reporting down:

✅ **David's Style:**
```
"I am getting this error when I try to run the application"
[includes actual error message]
```

This is PERFECT because:
- States the problem clearly
- Provides the actual error
- Doesn't try to guess the solution

### 3. **The Multi-Tasker**
David often combines related requests efficiently:

✅ **Example:** "two things. 1.) please make the application quit when hitting ctrl-c. 2.) make the troubleshooting guides that are only 1 step much longer"

This works because:
- Numbered lists = clear structure
- Related tasks = efficient session
- Specific requirements (ctrl-c, at least 4 deep)

### 4. **The Goldilocks Principle**
Not too vague, not too controlling, just right:

✅ **Good:** "let's change the color to look more modern, sleek, and technological"
- Gives creative direction without micromanaging
- Uses descriptive adjectives for guidance
- Leaves room for interpretation

---

## 🔄 Opportunities for Improvement

### 1. **The Context Sandwich**
Sometimes David jumps straight to the request without setup. Adding a tiny bit of context helps:

**Current Style:**
"the troubleshooting guides aren't loading"

**Enhanced Style:**
"the troubleshooting guides aren't loading when I click on them in the UI"

**Why it helps:** That extra breadcrumb helps the AI zero in on the specific area faster.

### 2. **The Success Criteria**
David's good at saying what he wants, but could be clearer about how to know it's done:

**Current Style:**
"make it so that it is very clearly labeled and easy to extend and maintain"

**Enhanced Style:**
"make it so that it is very clearly labeled and easy to extend and maintain - I want Allen to be able to add new guides without reading any documentation"

**Why it helps:** Concrete success criteria = better results.

### 3. **The Priority Flag**
When asking for multiple things, indicating priority helps:

**Current Style:**
"put some whimsical svg graphics scattered amongst the creation guide. kind of random objects or comics. do this at the very end."

**Enhanced Style:**
"put some whimsical svg graphics scattered amongst the creation guide. kind of random objects or comics. do this at the very end. [LOW PRIORITY - skip if complex]"

**Why it helps:** Helps the AI manage time and complexity.

---

## 🚀 David's Prompting Patterns to Copy

### Pattern 1: The Friendly Commander
```
"perhaps let's [action]"
"please [specific request]"
"everything looks pretty good. let's [improvement]"
```
**Why it works:** Polite but direct. Gets things done without being demanding.

### Pattern 2: The Problem + Evidence
```
"I can walk through a guide once, but then for some reason [specific issue]"
```
**Why it works:** Describes what works, what doesn't, and provides clues ("for some reason") that invite investigation.

### Pattern 3: The Thoughtful Feature Request
```
"please put the install steps into a run script for my friend so he can run it without having to mess with the venv stuff"
```
**Why it works:** 
- Explains WHO needs it (friend)
- Explains WHY (avoid venv complexity)
- Clear WHAT (run script)

---

## 💡 Prompting Techniques to Try

### 1. **The Sandwich Technique**
```
Context → Request → Constraints/Preferences

"I'm working on making this app user-friendly for beginners →
please add tooltips to all the main buttons →
keep the text casual and helpful, not technical"
```

### 2. **The Example-Driven Prompt**
```
"Change the error messages to be more friendly
Current: 'Error: Invalid node reference'
Desired style: 'Oops! Can't find that troubleshooting step'"
```

### 3. **The Progressive Refinement**
Instead of one big request, break it down:
```
First: "Let's create a basic settings page"
Then: "Now add theme selection to the settings"
Finally: "Make the theme change instant without restart"
```

---

## 🎮 Your Prompting Cheat Sheet

### For Bug Reports:
```
"[What you were doing] when [what went wrong]. 
Here's the error: [paste error]
Expected: [what should happen]"
```

### For Feature Requests:
```
"Let's add [feature] to help [who] do [what].
For example: [specific example]
Important: [any constraints]"
```

### For Improvements:
```
"[Current thing] works, but could be better.
Specifically: [what's not ideal]
Perhaps: [suggested improvement]"
```

### For Creative Tasks:
```
"Make it [adjective] and [adjective].
Think [reference/inspiration].
Avoid [what you don't want]."
```

---

## 🏆 David's Secret Sauce

What makes David's prompting style particularly effective:

1. **Trusts the AI's competence** - Doesn't over-explain obvious things
2. **Maintains conversational flow** - Feels like pair programming, not commanding
3. **Provides feedback loops** - "everything looks pretty good" before asking for changes
4. **Thinks about the end user** - "for my friend Allen" shows empathy
5. **Embraces whimsy** - Not afraid to ask for fun stuff

---

## 🎯 Action Items for Allen

1. **Start with David's casual style** - It's friendly and effective
2. **Add more "because" statements** - Explain why you want something
3. **Use examples liberally** - Show don't just tell
4. **Break complex requests into steps** - Easier to debug if something goes wrong
5. **Don't be afraid to be specific** - "at least 4 deep" is better than "longer"

---

## 🎬 Putting It All Together

Here's how to craft a David-style prompt for your next request:

```
"Hey, I noticed [observation]. 
Let's [action] to make it [desired outcome].
Maybe something like [example or inspiration].
Important: [any critical requirements].
Feel free to [creative freedom area] but make sure [constraint]."
```

### Real Example:
"Hey, I noticed the settings page is pretty bare.
Let's add some user preferences to make it more useful.
Maybe something like theme selection, auto-save toggles, and debug mode.
Important: keep all settings in one JSON file for simplicity.
Feel free to add other useful settings but make sure they actually work."

---

## 🦆 Final Wisdom

David's prompting style works because it treats the AI like a competent collaborator, not a servant or a magic genie. It's the programming equivalent of "Hey buddy, let's build something cool" versus "Computer, execute subroutine alpha."

Keep being conversational, specific when it matters, vague when creativity helps, and always remember: the best prompt is the one that gets you what you want with minimal back-and-forth.

Happy prompting, Allen! And remember - David's style got us this far, but feel free to add your own flavor. Maybe you're more emoji-heavy, or prefer bullet points, or like to include dad jokes. Find what works for you!

---

*P.S. - David, your prompting style is honestly refreshing. The casual expertise vibe makes the whole interaction feel like pair programming with a friend rather than instructing a machine. The main enhancement would be adding just a touch more context on the "why" behind requests - it helps the AI make better decisions when there are trade-offs. Keep being wonderfully whimsical!* 🦆