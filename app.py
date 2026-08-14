from pathlib import Path
import runpy

dashboard_app = Path(__file__).parent / "dashboard" / "app.py"

runpy.run_path(dashboard_app)