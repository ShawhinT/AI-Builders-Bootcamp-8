# Python Tutor

A Claude Code output-style that turns Claude into a Python tutor for complete beginners. Instead of implementing code for you, it teaches concepts through plain English explanations, hands-on notebooks, and guided exploration.

## Key Features

**Six core teaching behaviors:**
- **Explain Code** - One-sentence summaries, key steps, and core concepts from your files
- **Explain Concepts** - Plain English definitions with real-world analogies and minimal examples
- **Translate Errors** - Error messages in plain English with investigation guidance
- **Guide Modifications** - Describe what to change and where, conceptually (no implementation)
- **Explain Project Flow** - Map how your files connect and trace execution paths
- **Check Code Quality** - Flag AI-generated code quirks and overcomplicated patterns

**Creates learning artifacts:**
- **Notebooks** (`tutor/notebooks/`) - Hands-on practice with progressive complexity
- **Cheatsheets** (`tutor/reference/`) - Quick references using concepts from your actual code

## Setup Instructions

**User-level:**

To use the tutor across any project:

1. Copy `.claude/output-styles/python-tutor.md` to your `~/.claude/output-styles` directory
2. In any Claude Code session, run: `/output-style python-tutor`

Note: You must activate it manually each time you start Claude Code. User-level settings are overridden by project-level settings if both exist.

**Project-level:**

This repo uses project-level configuration. To use it in your own projects:

1. Copy `.claude/output-styles/python-tutor.md` to your project directory
2. Create `.claude/settings.local.json` in your project:
   ```json
   {
     "outputStyle": "python-tutor"
   }
   ```
3. Start Claude Code in that directory (tutor style activates automatically).

## Usage Examples

**Running this example repo:**

```bash
# Clone and navigate to this directory
git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
cd AI-Builders-Bootcamp-8/python-tutor

# Install dependencies (choose one)
uv sync
# or
pip install jupyterlab ipykernel

# Start Claude Code
claude
```

**Interaction examples:**

```
You: "explain example.ipynb"
Claude: [Provides one-sentence summary of the job scraper,
         lists key steps, highlights 3 core concepts like
         BeautifulSoup, data extraction patterns, and DataFrame usage]
```

```
You: "what is a list comprehension?"
Claude: [Plain English definition with real-world analogy,
         minimal runnable example, explanation of why it exists,
         shows where it appears in your code, offers practice notebook]
```

```
You: [Pastes AttributeError traceback]
Claude: [Translates to "You tried to access an attribute that doesn't exist",
         points to the specific line, explains likely cause,
         suggests how to investigate]
```

```
You: "how do I add email extraction to the job scraper?"
Claude: [Describes which file and lines to modify (example.ipynb:45-60),
         explains the conceptual approach (add new find() call in
         extract_job_data function, handle missing emails),
         notes ripple effects and common mistakes,
         does NOT write the implementation code]
```
