import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('')))

import home_screen as home
import data_access as db
import specify_interface as sp

def main() -> None:
    print()
    print("* Mass Digitizer for DaSSCo *")
    home.init()

    # TODO start background processes? 

if __name__ == "__main__":
    main()