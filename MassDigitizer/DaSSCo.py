import sys
from pathlib import Path
import logging
import pathlib
import time
import os

# Below line is needed for accessing internal dependencies 
sys.path.append(str(Path(__file__).parent.parent.joinpath('')))

import home_screen
import util
# import specify_interface

util.buildLogger()

def main() -> None:
    try:
        util.logging.debug("* Mass Digitizer for DaSSCo *")
    except Exception as e:
        util.logging.debug(str(e))

    home = home_screen.HomeScreen()

    # TODO start background processes? 

if __name__ == "__main__":
    main()