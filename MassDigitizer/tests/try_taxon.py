import sys
from pathlib import Path

# Below line is needed for accessing internal dependencies 
sys.path.append(str(Path(__file__).parent.parent.joinpath('')))

# Internal dependencies
from models import taxon

testObject = taxon.Taxon(29)

