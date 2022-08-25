import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('MassDigitizer')))

import home_screen as home

def main() -> None:
    print("* Mass Digitizer for DaSSCo *")
    home.init()


    # TODO start background processes? 





if __name__ == "__main__":
    main()