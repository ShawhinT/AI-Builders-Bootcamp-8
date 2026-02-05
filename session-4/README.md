# Session 4: AI Agents & Tool Use

Links:
- [Example 1: YouTube Agent](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-4/example_1-youtube_agent.ipynb)
- [Example 2: Notion MCP Agent](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-4/example_2-notion_mcp_agent.ipynb)

## How to run the examples

### uv

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8
    uv sync
    ```
3. Launch Jupyter Lab
    ```
    uv run jupyter lab
    ```

### Python/pip

1. Clone this repo
   ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8
    python -m venv s4-env
    ```
3. Activate venv
    ```
    # mac/linux
    source s4-env/bin/activate
    
    # windows
    .\s4-env\Scripts\activate.bat
    ```
4. Install dependencies
    ```
    pip install -e .
    ```
5. Launch Jupyter Lab
    ```
    jupyter lab
    ```
