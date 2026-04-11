# streamlit-app
Repo with streamlit app for "Ready, Set, Publish: Write Your First Python Package" workshop




uv init --lib data-analytics --python 3.13
uv sync
select pytjom interpreter
uv add "data-analytics==0.1.0.dev1" \
  --extra-index-url https://test.pypi.org/simple/
  
Run streamlit app:


One-time setup
From the repo root (streamlit-app):

uv sync
That creates/updates the project venv and installs what’s in pyproject.toml (including Streamlit).

Run the app
uv run streamlit run src/app.py
Equivalent:

uv run python -m streamlit run src/app.py
Stay in the project root when you run it so paths and imports match how the project is laid out.

Optional: activate the venv yourself
source .venv/bin/activate   # on Windows Git Bash/WSL/Linux
streamlit run src/app.py
uv run is usually enough: it uses the project’s .venv without activating it.

Note: src/app.py imports data_analytics. If that isn’t installed as a dependency or on PYTHONPATH, uv run streamlit run src/app.py may fail on import until that package is wired up in pyproject.toml or you run with the right PYTHONPATH. If you hit an import error, say what it prints and we can align the project config.