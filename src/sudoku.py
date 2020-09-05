#
# Informed Search Methods
#
# Converts Sudoku puzzles to constraints for our Simple-CSP solver.
#

import sys
from pathlib import Path


def read_puzzles(name):
    """
    Reads in Sudoku puzzle specifications from a file. The puzzles must be separated by
    one or more separator lines. A separator line is any line starting with a
    alpha-letter (a-z, A-Z) or the '#' symbol. The format for specifying each puzzle is
    flexible as long as:
      - The digits 1-9 specify a filled cell and the letter '.' (or the digit 0) an
        empty cell. The digits (and '.') are process in a left-to-right and
        top-to-bottom order, that is, the first digit (or '.') encountered specifies the
        value of the top-left most cell, the second, the top-second-leftmost, ..., and
        the last one the bottom-right-most cell.
      - There are exactly 81 cell values specified.
    The routine returns a list of puzzles. Each puzzle is represented as a list of 81
    digits (0-9).
    """
    puzzles = []
    puzzle = []
    with open(name) as f:
        for line in f:
            if line and (line[0] == '#' or line[0].isalpha()):
                if puzzle:
                    assert len(puzzle) == 81
                    puzzles.append(puzzle)
                    puzzle = []
                continue
            for c in line:
                if c.isdigit():
                    puzzle.append(int(c))
                elif c == '.':
                    puzzle.append(0)
        if puzzle:
            assert len(puzzle) == 81
            puzzles.append(puzzle)
    return puzzles


def write_puzzle_constraints(name, constraints):
    """
    Writes the constraints to a file in a format consistent with 'SimpleCSP' format.
    """
    with open(name, 'w') as f:
        for c in constraints:
            f.write('(')
            f.write(str(c[0]))
            f.write(',')
            f.write(str(c[1]))
            f.write(')\n')


def write_puzzles_domains(name, puzzles):
    """
    Writes the domains (for possibly multiple puzzle instances) to a file in a format
    consistent with 'SimpleCSP' format.
    """
    with open(name, 'w') as f:
        first_puzzle = True
        for puzzle in puzzles:
            if not first_puzzle:
                f.write('#\n')
            else:
                first_puzzle = False
            for domain in puzzle:
                f.write(str(domain))
                f.write('\n')


def generate_domains(puzzles):
    """
    Generate variable domains from the puzzle instances.
    Returns a list. Each element in the list is a list of sets with proper variable
    domain values (where the first set is the domain for variable 0, the second for
    variable 1 ect.)
    """

    # ********** YOU IMPLEMENT THIS **********

    return []


def generate_constraints():
    """
    The routine returns a list of non-equal constraints representing which pairs of
    cells cannot take the same value. Each constraint is represented as a tuple of two
    integer values, e.g. as (0,1). The value 0 refers to the top-left-most cell, the
    value 1 the top-2nd-left-most, ..., and the value 80 the bottom-right-most cell. As
    non-equal constraints are symmetrical there is no need to generate the symmetri,
    e.g., generate (0,1) but not (1,0).
    """

    # ********** YOU IMPLEMENT THIS **********

    return []


def main():
    """
    'soduko.txt' is the default expected input file name, but it can be overwritten by
    specifying an alternative name as a command-line argument.

    Usage:  sudoku [filename]
    Reads Sudoku puzzle-instances from a file and outputs 'SimpleCSP' compatible
    constraints- and domains files, called 'filename_cst.txt' and 'filename_dom.txt',
    respectively.
    """
    name = 'sudoku'
    input_puzzle_file = name + '.txt'
    if len(sys.argv) == 2:
        input_puzzle_file = sys.argv[1]
        name = Path(input_puzzle_file).stem
        assert len(name) > 0
    output_domains_file = name + "_dom.txt"
    output_constraints_file = name + "_cst.txt"

    print('Processing puzzles from file', input_puzzle_file)
    puzzles = read_puzzles(input_puzzle_file)
    print('Read in', len(puzzles), 'Sudoku puzzle instances.')

    print('Generating and writing domains to file', output_domains_file)
    domains = generate_domains(puzzles)
    write_puzzles_domains(name + "_dom.txt", domains)

    print('Generating and writing constraints to file', output_constraints_file)
    constraints = generate_constraints()
    write_puzzle_constraints(output_constraints_file, constraints)


if __name__ == "__main__":
    main()
