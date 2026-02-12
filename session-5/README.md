# Session 5: Evaluating a LinkedIn Post Writer

Links:
- [Example 1: Generate Posts](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-5/1-generate_posts.py)
- [Example 2: Annotation App](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-5/2-annotation_app.py)
- [Example 3: Run Evals](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-5/3-run_evals.py)

## How to run the examples

### uv

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-5
    uv sync
    ```
3. Set up environment
    ```
    cp .env.example .env
    # Add your OpenAI API key to .env
    ```
4. Run the examples
    ```
    # Step 1: Generate posts
    uv run 1-generate_posts.py

    # Step 2: Annotate posts
    uv run streamlit run 2-annotation_app.py

    # Step 3: Run evaluations
    uv run 3-run_evals.py
    ```

### Python/pip

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-5
    python -m venv s5-env
    ```
3. Activate venv
    ```
    # mac/linux
    source s5-env/bin/activate
    
    # windows
    .\s5-env\Scripts\activate.bat
    ```
4. Install dependencies
    ```
    pip install -e .
    ```
5. Set up environment
    ```
    cp .env.example .env
    # Add your OpenAI API key to .env
    ```
6. Run the examples
    ```
    # Step 1: Generate posts
    python 1-generate_posts.py

    # Step 2: Annotate posts
    streamlit run 2-annotation_app.py

    # Step 3: Run evaluations
    python 3-run_evals.py
    ```

## Workflow

### Step 0: Prepare Input Data

Add post ideas to `data/_inputs/30-post-ideas.csv` (CSV with header "Post Idea", one idea per row).

### Step 1: Generate Posts (`1-generate_posts.py`)

Reads ideas from the input CSV, generates LinkedIn posts via OpenAI (`gpt-5`) using the prompt template at `prompts/prompt-v3.md`, and saves results to `data/YYYY-MM-DD_prompt-vN/request_response.csv`. The prompt is configurable via the `prompt_path` variable.

### Step 2: Annotate Results (`2-annotation_app.py`)

Streamlit app for reviewing generated posts. Select a CSV, navigate through posts, add free-text notes and custom binary labels (e.g., "Good", "Too generic"). Annotations auto-save and can be exported as CSV.

### Step 3: Run Evaluations (`3-run_evals.py`)

Runs code-based quality checks (defined in `evals.py`) against each post and saves results to `request_response-evals.csv`. Set the `data_path` variable to the CSV you want to evaluate.

**Built-in evals:**

| Eval | What it checks |
|------|---------------|
| `check_no_banned_phrases` | Clichés like "no fluff", "no hacks" |
| `check_no_tricolons` | Tricolon patterns (comma, period, or newline-separated) |
| `check_em_dash_count` | More than one em dash (—) per post |

## Prompt Versioning

Prompts are versioned in the `prompts/` directory. Each version builds on the previous:

- **v1** — Base prompt with format instructions (hook/body/CTA structure) and two example posts
- **v2** — Adds guidelines: one-sentence paragraphs, conversational tone, em dash limit (max 1 per post)
- **v3** — Adds stricter rules: no invented details, CTA limited to questions or links, listicle items capped at 3-5, numbered listicles required, ban on tricolons and marketing clichés

The active prompt is set via the `prompt_path` variable in `1-generate_posts.py` (currently `prompts/prompt-v3`).
