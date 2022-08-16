import sys
import easygui
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('src')))

easygui.msgbox(str(Path(__file__).parent.joinpath('src')), "DEBUG")

import MassDigitizer.__main__ as main

if __name__ == '__main__':
    print(str(Path(__file__).parent.joinpath('src')))
    main()