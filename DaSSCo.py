import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.joinpath('MassDigitizer')))

import MassDigitizer.__main__ as main

if __name__ == '__main__':
    main.main()
    pass