import sys
from pathlib import Path

# Below line is needed for accessing internal dependencies 
sys.path.append(str(Path(__file__).parent.parent.joinpath('')))

import home_screen
import data_access
import specify_interface

def main() -> None:
    print()
    print("* Mass Digitizer for DaSSCo *")

    home = home_screen.HomeScreen()

    # TODO start background processes? 

if __name__ == "__main__":
    main()