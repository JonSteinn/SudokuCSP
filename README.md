# A Sudoku solver 
A Sudoku solver that can pre-process with AC-3 has the following variants:
* Chronological Backtracking
* Backjumping search
* Conflict-directed Backjumping search
This is an assignment in the course `Informed Search Methods in AI` at Reykjavík University.

## Report
A report about this project can be found [here](https://github.com/JonSteinn/SudokuCSP/raw/master/report/report.pdf).

## Install dev dependencies
```sh
# unix
python3 -m pip install -r requirements-dev.txt
# win
python -m pip install -r requirements-dev.txt
```

## Run
Run both `scsp.py` and `sudoku.py` from the `./src` folder as the provided code expects paths that way.
```sh
cd src # Navigate to the src folder before running

# unix
python3 sudoku.py
python3 scsp.py -h
# win
python sudoku.py
python scsp.py -h
```
