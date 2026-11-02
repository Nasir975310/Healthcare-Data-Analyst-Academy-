from pathlib import Path
import subprocess, sys
HERE=Path(__file__).resolve().parent
for script in ["operations_analysis.py","due_analysis.py","pv_quality_review.py"]:
    print(f"\n=== {script} ===", flush=True)
    subprocess.run([sys.executable,str(HERE/script)],check=True)
print("\nAll project scripts completed. Review outputs and limitations before portfolio publication.")
