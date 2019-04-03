## Check lines intersection

Program that receives two lines from input and check if they overlap or not.  

#### Install dependencies:
pip install -r requirements.txt

#### Run the system:
python -m unittest discover ./tests/

### Return values
- 0: lines overlap
- 1: lines do not overlap
- 2: invalid input

#### Example command lines
python ./src/main.py 1,5 5,9

python ./src/main.py 1,5 2,6

For negative numbers is necessary to use an extra "--" in the command line:

python ./src/main.py -- -1,5 0,2

python ./src/main.py -- -1,5 0,-2