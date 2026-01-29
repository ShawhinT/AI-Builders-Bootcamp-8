# Session 3: RAG, Text Embeddings

Links:
- [Example 1: RAG with LlamaIndex](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-3/example_2-rag_with_llamaindex.ipynb)
- [Example 2: Analyzing Unstructured Survey Data](https://github.com/ShawhinT/AI-Builders-Bootcamp-8/blob/main/session-3/example_1-unstructured_survey_analysis.ipynb)


## How to run the examples

### uv

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-3
    uv sync
    ```
3. Launch Jupyter Lab
    ```
    uv run jupyter lab
    ```

### Base Python/Pip

1. Clone this repo
    ```
    git clone https://github.com/ShawhinT/AI-Builders-Bootcamp-8.git
    ```
2. Navigate to downloaded folder and create new venv
    ```
    cd AI-Builders-Bootcamp-8/session-3
    python -m venv s3-env
    ```
3. Activate venv
    ```
    # mac/linux
    source s3-env/bin/activate
    
    # windows
    .\s3-env\Scripts\activate.bat
    ```
4. Install dependencies
    ```
    pip install -r requirements.txt
    ```
5. Launch Jupyter Lab
    ```
    jupyter lab
    ```
