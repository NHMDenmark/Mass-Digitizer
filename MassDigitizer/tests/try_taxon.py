import sys
from pathlib import Path

# Below line is apparently needed for accessing internal dependencies for some reason 
sys.path.append(str(Path(__file__).parent.parent.joinpath('')))

# Internal dependencies
from models import taxon

testObject = taxon.Taxon(29)

