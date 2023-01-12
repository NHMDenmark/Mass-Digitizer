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

sTime = time.strftime('{%Y-%m-%d_%H,%M,%S}').replace("{", "").replace("}", "")
pathString = util.getLogsPath()
filePath = os.path.expanduser(pathString)
sys.path.append(str(pathlib.Path(__file__).parent.parent.joinpath(filePath)))
logName = f"DaSSCo_py{sTime}.log"
logFilePath = str(Path(filePath).joinpath(f'{logName}'))


logging.basicConfig(filename=logFilePath, encoding='utf-8', level=logging.DEBUG, force=True)

logging.debug('DaSSCo initial app log write! --- !!!!!!!!!!')
# l = util.buildLogger('DaSSCo_py')

def main() -> None:
    try:
        logging.debug("* Mass Digitizer for DaSSCo *")
    except Exception as e:
        logging.debug(str(e))

    home = home_screen.HomeScreen()

    # TODO start background processes? 

if __name__ == "__main__":
    main()