## Version comparer

Function that compares two string versions returning whether they are equals, or which one is greater than the other.   

#### Run the system:
python -m unittest discover ./tests/

### Return values
- 0: versions are equals
- 1: First version is greater than second one
- 2: Second version is greater than first one

#### Examples
from src.version_comparer import compare_versions
compare_versions('02.00.00', '01.00.00')
compare_versions('2', '2')
compare_versions('01.99.00', '01.100.00')

