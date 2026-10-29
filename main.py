import sys
import shutil
from pathlib import Path

# Add src to sys.path
ROOT = Path(__file__).resolve().parent
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from ninflam.cli import load_config, run_preprocessing_pipeline
from ninflam.pipeline.train import run_training_pipeline

def main():
    print("=" * 80)
    print(" NeuroSafeNet: Full Reproducible Pipeline (Preprocessing + Training)")
    print("=" * 80)

    cfg = load_config()

    print("\n>>> [1/2] Running Preprocessing Pipeline...")
    run_preprocessing_pipeline(cfg)

    print("\n>>> [2/2] Running Model Training & Cross-Validation Pipeline...")
    run_training_pipeline(cfg)

    # Ensure all results are mirrored to ../results for Code Ocean
    results_dir = Path("../results")
    if results_dir.exists():
        print(f"\n[Code Ocean] Ensuring outputs are synced to {results_dir.resolve()}...")
        out_dir = Path("outputs")
        if out_dir.exists():
            for item in out_dir.iterdir():
                dest = results_dir / item.name
                if item.is_dir():
                    shutil.copytree(item, dest, dirs_exist_ok=True)
                else:
                    shutil.copy2(item, dest)

    print("\n" + "=" * 80)
    print(" Finished! All analysis reproduced successfully.")
    print("=" * 80)

if __name__ == "__main__":
    main()

