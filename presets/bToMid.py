import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from preset_runner import run_preset

if __name__ == '__main__':
    run_preset('bToMid')