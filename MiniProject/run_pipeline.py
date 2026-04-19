import sys
import os
import subprocess

def run_script(script_path):
    print(f"==================== Running {script_path} ====================")
    result = subprocess.run([sys.executable, script_path], cwd=os.path.dirname(script_path))
    if result.returncode != 0:
        print(f"Error running {script_path}")
        sys.exit(1)
    print("\n")

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, "src")
    
    scripts = [
        "data_generation.py",
        "data_engineering.py",
        "eda_visualization.py",
        "geospatial_analysis.py",
        "modeling.py"
    ]
    
    for script in scripts:
        run_script(os.path.join(src_dir, script))

    print("All pipeline steps successfully executed!")

if __name__ == "__main__":
    main()
