import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('src')))

import MassDigitizer.home_screen as home

def main() -> None:
    print("* Mass Digitizer for DaSSCo *")
    home.start()








if __name__ == "__main__":
    main()