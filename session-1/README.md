# Session 1: Software 1.0, Coding with AI

Links:
- [Example: Scraping AI Job Board with Python](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-1/example-scrape_job_board.ipynb)
- [Live Coding Examples](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-1/live-coding-example)
- [ChatGPT](https://chatgpt.com/share/696a817e-9c10-8010-986d-5d5bb66d0d85) and [Claude Code](https://claude.ai/share/0351db1d-7b70-45f8-b1d9-ed5a0619a313) chats

## How to run the examples

### uv

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to this folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-1
    uv sync
    ```
3. Launch Jupyter Lab
    ```
    uv run jupyter lab
    ```

### Standard Python

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to this folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-1
    python -m venv s1-env
    ```
3. Activate venv
    ```
    # mac/linux
    source s1-env/bin/activate

    # windows
    .\s1-env\Scripts\activate.bat
    ```
4. Install dependencies
    ```
    pip install -r requirements.txt
    ```
5. Launch Jupyter Lab
    ```
    jupyter lab
    ```
