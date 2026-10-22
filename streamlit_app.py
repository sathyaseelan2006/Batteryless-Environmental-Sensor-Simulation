"""
streamlit_app.py — Streamlit Community Cloud Entrypoint.
Delegates execution to app.py.
"""
from pathlib import Path
import runpy

app_file = Path(__file__).parent / "app.py"
runpy.run_path(str(app_file), run_name="__main__")
