from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent / "src"))
from hda_project.pipeline import run_pipeline
if __name__ == "__main__":
    run_pipeline()
    print("Pipeline completed. Review reports/project_report.md and data/processed/.")
