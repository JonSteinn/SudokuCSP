import pathlib
from typing import List, Union
import requests

from src.sudoku import generate_domains_single, generate_constraints
from src.constraintnetwork import ConstraintNetwork


ALL_CONSTRAINTS = {
    (35, 62),
    (30, 32),
    (1, 18),
    (0, 2),
    (30, 49),
    (29, 33),
    (27, 33),
    (30, 66),
    (74, 75),
    (0, 19),
    (56, 64),
    (0, 36),
    (54, 64),
    (15, 17),
    (13, 17),
    (15, 51),
    (19, 21),
    (50, 52),
    (48, 52),
    (70, 80),
    (19, 55),
    (18, 25),
    (16, 25),
    (47, 56),
    (34, 53),
    (34, 70),
    (11, 12),
    (69, 71),
    (14, 59),
    (11, 29),
    (10, 13),
    (39, 44),
    (37, 44),
    (68, 75),
    (35, 44),
    (66, 75),
    (55, 72),
    (9, 63),
    (10, 64),
    (7, 17),
    (7, 34),
    (0, 1),
    (31, 32),
    (29, 32),
    (51, 60),
    (0, 18),
    (31, 49),
    (2, 18),
    (56, 63),
    (5, 68),
    (60, 80),
    (28, 36),
    (26, 53),
    (74, 79),
    (50, 51),
    (72, 79),
    (70, 79),
    (50, 68),
    (13, 21),
    (20, 24),
    (18, 24),
    (45, 72),
    (46, 73),
    (10, 12),
    (41, 43),
    (32, 40),
    (39, 43),
    (61, 71),
    (10, 46),
    (41, 77),
    (9, 16),
    (67, 75),
    (7, 16),
    (55, 59),
    (8, 80),
    (6, 17),
    (60, 62),
    (5, 50),
    (31, 48),
    (62, 79),
    (3, 4),
    (6, 51),
    (1, 4),
    (60, 79),
    (30, 35),
    (28, 35),
    (26, 35),
    (76, 78),
    (27, 36),
    (74, 78),
    (1, 55),
    (72, 78),
    (22, 23),
    (25, 70),
    (20, 23),
    (22, 40),
    (19, 24),
    (46, 55),
    (20, 74),
    (36, 39),
    (32, 39),
    (41, 42),
    (61, 70),
    (41, 59),
    (40, 43),
    (11, 15),
    (9, 15),
    (65, 74),
    (57, 58),
    (8, 16),
    (55, 58),
    (6, 16),
    (37, 47),
    (57, 75),
    (6, 33),
    (37, 64),
    (62, 78),
    (1, 3),
    (30, 34),
    (2, 4),
    (4, 67),
    (0, 4),
    (1, 20),
    (29, 35),
    (1, 37),
    (27, 35),
    (76, 77),
    (74, 77),
    (58, 66),
    (25, 52),
    (0, 72),
    (17, 53),
    (21, 23),
    (19, 23),
    (21, 57),
    (36, 38),
    (18, 27),
    (36, 72),
    (40, 42),
    (16, 61),
    (11, 14),
    (12, 15),
    (10, 15),
    (40, 76),
    (8, 15),
    (37, 46),
    (68, 77),
    (11, 65),
    (66, 77),
    (35, 80),
    (2, 3),
    (33, 34),
    (0, 3),
    (31, 34),
    (53, 62),
    (29, 34),
    (2, 20),
    (0, 20),
    (7, 70),
    (0, 54),
    (28, 38),
    (17, 35),
    (28, 55),
    (21, 22),
    (52, 53),
    (50, 53),
    (21, 39),
    (15, 69),
    (52, 70),
    (13, 23),
    (20, 26),
    (18, 26),
    (13, 40),
    (47, 74),
    (12, 14),
    (34, 42),
    (10, 14),
    (32, 59),
    (68, 76),
    (12, 48),
    (66, 76),
    (9, 18),
    (67, 77),
    (55, 61),
    (31, 33),
    (7, 52),
    (2, 19),
    (31, 50),
    (51, 78),
    (3, 6),
    (1, 6),
    (31, 67),
    (3, 23),
    (28, 37),
    (76, 80),
    (27, 38),
    (74, 80),
    (72, 80),
    (26, 71),
    (24, 25),
    (27, 72),
    (22, 25),
    (13, 22),
    (20, 25),
    (24, 42),
    (21, 26),
    (19, 26),
    (48, 57),
    (22, 76),
    (36, 41),
    (12, 13),
    (43, 44),
    (32, 41),
    (41, 44),
    (12, 30),
    (43, 61),
    (11, 17),
    (9, 17),
    (67, 76),
    (57, 60),
    (55, 60),
    (8, 35),
    (57, 77),
    (63, 64),
    (62, 80),
    (3, 5),
    (1, 5),
    (5, 22),
    (6, 69),
    (3, 22),
    (2, 6),
    (0, 6),
    (3, 39),
    (78, 79),
    (29, 37),
    (76, 79),
    (27, 37),
    (58, 68),
    (27, 54),
    (1, 73),
    (22, 24),
    (23, 25),
    (21, 25),
    (19, 25),
    (22, 58),
    (23, 59),
    (38, 40),
    (36, 40),
    (38, 74),
    (42, 44),
    (73, 75),
    (40, 44),
    (18, 63),
    (11, 16),
    (12, 17),
    (42, 78),
    (10, 17),
    (57, 59),
    (39, 48),
    (8, 17),
    (59, 76),
    (57, 76),
    (5, 21),
    (4, 5),
    (3, 21),
    (2, 5),
    (0, 5),
    (4, 22),
    (29, 36),
    (33, 53),
    (58, 67),
    (1, 9),
    (2, 56),
    (23, 24),
    (54, 55),
    (21, 24),
    (23, 41),
    (54, 72),
    (17, 71),
    (38, 39),
    (21, 75),
    (38, 56),
    (18, 45),
    (49, 76),
    (42, 43),
    (73, 74),
    (13, 76),
    (42, 60),
    (14, 16),
    (16, 79),
    (12, 16),
    (34, 44),
    (10, 16),
    (34, 61),
    (59, 75),
    (14, 50),
    (9, 20),
    (33, 35),
    (64, 66),
    (31, 35),
    (9, 54),
    (4, 21),
    (33, 52),
    (35, 52),
    (53, 80),
    (55, 63),
    (2, 38),
    (3, 8),
    (33, 69),
    (1, 8),
    (30, 39),
    (0, 9),
    (28, 73),
    (15, 24),
    (49, 58),
    (19, 28),
    (13, 58),
    (14, 15),
    (36, 43),
    (45, 46),
    (34, 43),
    (14, 32),
    (45, 63),
    (32, 77),
    (69, 78),
    (11, 19),
    (12, 66),
    (9, 19),
    (9, 36),
    (10, 20),
    (57, 62),
    (55, 62),
    (64, 65),
    (35, 51),
    (33, 51),
    (5, 7),
    (63, 66),
    (3, 7),
    (1, 7),
    (8, 71),
    (2, 8),
    (5, 41),
    (0, 8),
    (31, 39),
    (29, 56),
    (3, 75),
    (24, 26),
    (22, 26),
    (24, 60),
    (48, 75),
    (38, 42),
    (36, 42),
    (73, 77),
    (43, 79),
    (11, 18),
    (44, 80),
    (59, 61),
    (10, 19),
    (57, 61),
    (41, 50),
    (39, 50),
    (61, 78),
    (5, 6),
    (63, 65),
    (8, 53),
    (5, 23),
    (4, 7),
    (2, 7),
    (0, 7),
    (62, 69),
    (78, 80),
    (29, 38),
    (60, 69),
    (3, 57),
    (4, 58),
    (1, 11),
    (1, 28),
    (25, 26),
    (23, 26),
    (54, 57),
    (25, 43),
    (54, 74),
    (38, 41),
    (23, 77),
    (20, 47),
    (75, 76),
    (73, 76),
    (44, 62),
    (59, 60),
    (10, 18),
    (41, 49),
    (39, 49),
    (59, 77),
    (39, 66),
    (40, 50),
    (4, 6),
    (55, 65),
    (64, 68),
    (4, 23),
    (4, 40),
    (35, 71),
    (1, 10),
    (30, 41),
    (2, 74),
    (0, 11),
    (54, 56),
    (30, 75),
    (56, 73),
    (54, 73),
    (15, 26),
    (20, 29),
    (21, 30),
    (15, 60),
    (16, 17),
    (19, 64),
    (14, 17),
    (45, 48),
    (36, 45),
    (16, 34),
    (38, 45),
    (41, 48),
    (40, 49),
    (34, 79),
    (71, 80),
    (14, 68),
    (69, 80),
    (11, 38),
    (66, 67),
    (55, 64),
    (64, 67),
    (35, 53),
    (9, 72),
    (63, 68),
    (30, 40),
    (51, 52),
    (2, 10),
    (0, 10),
    (30, 57),
    (31, 41),
    (51, 69),
    (0, 27),
    (31, 58),
    (56, 72),
    (5, 77),
    (17, 25),
    (15, 25),
    (15, 42),
    (26, 62),
    (70, 71),
    (19, 46),
    (50, 77),
    (38, 44),
    (36, 44),
    (45, 47),
    (73, 79),
    (40, 48),
    (71, 79),
    (11, 20),
    (69, 79),
    (12, 21),
    (32, 49),
    (61, 80),
    (7, 8),
    (65, 67),
    (5, 8),
    (63, 67),
    (10, 55),
    (7, 25),
    (2, 9),
    (31, 40),
    (62, 71),
    (5, 59),
    (60, 71),
    (17, 24),
    (29, 74),
    (26, 44),
    (54, 59),
    (50, 59),
    (24, 78),
    (25, 79),
    (38, 43),
    (22, 49),
    (46, 47),
    (75, 78),
    (73, 78),
    (46, 64),
    (71, 78),
    (61, 62),
    (43, 51),
    (59, 62),
    (32, 48),
    (61, 79),
    (10, 37),
    (41, 68),
    (65, 66),
    (7, 24),
    (6, 8),
    (4, 8),
    (8, 25),
    (6, 25),
    (64, 70),
    (62, 70),
    (6, 42),
    (60, 70),
    (3, 12),
    (4, 76),
    (56, 58),
    (1, 46),
    (54, 58),
    (25, 61),
    (22, 31),
    (75, 77),
    (20, 65),
    (18, 19),
    (21, 66),
    (38, 47),
    (36, 47),
    (45, 50),
    (42, 51),
    (16, 70),
    (6, 7),
    (37, 38),
    (59, 66),
    (57, 66),
    (66, 69),
    (6, 24),
    (64, 69),
    (37, 55),
    (8, 24),
    (11, 74),
    (63, 70),
    (56, 57),
    (2, 29),
    (56, 74),
    (0, 63),
    (17, 44),
    (72, 73),
    (21, 48),
    (15, 78),
    (52, 79),
    (38, 46),
    (47, 49),
    (36, 46),
    (45, 49),
    (36, 63),
    (16, 52),
    (32, 34),
    (40, 67),
    (12, 23),
    (66, 68),
    (11, 56),
    (32, 68),
    (9, 10),
    (12, 57),
    (65, 69),
    (63, 69),
    (9, 27),
    (51, 53),
    (2, 11),
    (33, 42),
    (7, 61),
    (0, 45),
    (28, 29),
    (31, 76),
    (17, 26),
    (28, 46),
    (27, 30),
    (54, 61),
    (52, 61),
    (26, 80),
    (13, 14),
    (13, 31),
    (47, 48),
    (48, 49),
    (47, 65),
    (46, 49),
    (75, 80),
    (48, 66),
    (73, 80),
    (32, 33),
    (14, 22),
    (12, 22),
    (43, 53),
    (32, 50),
    (12, 39),
    (43, 70),
    (67, 68),
    (65, 68),
    (10, 73),
    (7, 26),
    (37, 41),
    (7, 43),
    (64, 72),
    (8, 44),
    (3, 14),
    (6, 78),
    (28, 45),
    (27, 29),
    (58, 60),
    (3, 48),
    (56, 60),
    (29, 46),
    (54, 60),
    (27, 46),
    (27, 63),
    (24, 33),
    (46, 48),
    (77, 79),
    (22, 67),
    (75, 79),
    (18, 21),
    (14, 21),
    (45, 52),
    (43, 52),
    (42, 53),
    (39, 40),
    (37, 40),
    (59, 68),
    (8, 26),
    (66, 71),
    (39, 57),
    (64, 71),
    (6, 26),
    (57, 68),
    (63, 72),
    (5, 13),
    (6, 60),
    (3, 13),
    (3, 30),
    (27, 28),
    (58, 59),
    (56, 59),
    (29, 45),
    (27, 45),
    (58, 76),
    (1, 64),
    (28, 32),
    (2, 65),
    (72, 75),
    (77, 78),
    (23, 50),
    (17, 80),
    (18, 20),
    (49, 51),
    (47, 51),
    (45, 51),
    (38, 65),
    (46, 52),
    (18, 54),
    (44, 52),
    (42, 52),
    (42, 69),
    (37, 39),
    (68, 70),
    (57, 67),
    (66, 70),
    (59, 67),
    (9, 12),
    (67, 71),
    (65, 71),
    (37, 73),
    (63, 71),
    (5, 12),
    (4, 13),
    (33, 44),
    (58, 75),
    (2, 47),
    (30, 31),
    (33, 78),
    (28, 31),
    (30, 48),
    (27, 32),
    (72, 74),
    (54, 63),
    (23, 32),
    (17, 62),
    (15, 16),
    (13, 16),
    (15, 33),
    (49, 50),
    (47, 50),
    (19, 20),
    (18, 36),
    (49, 67),
    (48, 51),
    (46, 51),
    (19, 37),
    (13, 67),
    (44, 51),
    (34, 35),
    (16, 24),
    (32, 35),
    (34, 52),
    (68, 69),
    (14, 41),
    (69, 70),
    (9, 11),
    (67, 70),
    (65, 70),
    (12, 75),
    (37, 43),
    (9, 45),
    (4, 12),
    (35, 43),
    (33, 43),
    (64, 74),
    (53, 71),
    (33, 60),
    (7, 79),
    (28, 30),
    (29, 31),
    (28, 47),
    (27, 31),
    (58, 62),
    (56, 62),
    (28, 64),
    (54, 62),
    (29, 65),
    (13, 15),
    (13, 49),
    (48, 50),
    (24, 69),
    (46, 50),
    (70, 78),
    (18, 23),
    (14, 23),
    (45, 54),
    (34, 51),
    (67, 69),
    (10, 11),
    (39, 42),
    (37, 42),
    (10, 28),
    (35, 42),
    (64, 73),
    (7, 15),
    (8, 62),
    (63, 74),
    (5, 32),
    (29, 30),
    (60, 61),
    (58, 61),
    (56, 61),
    (29, 47),
    (60, 78),
    (3, 66),
    (27, 47),
    (28, 34),
    (24, 51),
    (72, 77),
    (79, 80),
    (77, 80),
    (20, 22),
    (18, 22),
    (49, 53),
    (47, 53),
    (45, 53),
    (20, 56),
    (44, 71),
    (39, 41),
    (61, 69),
    (9, 14),
    (39, 75),
    (65, 73),
    (5, 14),
    (63, 73),
    (55, 57),
    (6, 15),
    (55, 74),
    (1, 2),
    (4, 49),
    (58, 77),
    (30, 33),
    (28, 33),
    (1, 19),
    (30, 50),
    (27, 34),
    (74, 76),
    (56, 65),
    (72, 76),
    (25, 34),
    (54, 65),
    (20, 21),
    (23, 68),
    (49, 52),
    (47, 52),
    (20, 38),
    (19, 22),
    (48, 53),
    (46, 53),
    (44, 53),
    (18, 72),
    (36, 37),
    (19, 73),
    (16, 26),
    (36, 54),
    (16, 43),
    (68, 71),
    (40, 41),
    (11, 13),
    (9, 13),
    (40, 58),
    (65, 72),
    (14, 77),
    (11, 47),
    (55, 56),
    (37, 45),
    (4, 14),
    (55, 73),
    (4, 31),
}

ALL_CONSTRAINTS_4X4 = [
    (0, 1),
    (0, 2),
    (0, 3),
    (0, 4),
    (0, 5),
    (0, 8),
    (0, 12),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (1, 9),
    (1, 13),
    (2, 3),
    (2, 6),
    (2, 7),
    (2, 10),
    (2, 14),
    (3, 6),
    (3, 7),
    (3, 11),
    (3, 15),
    (4, 5),
    (4, 6),
    (4, 7),
    (4, 8),
    (4, 12),
    (5, 6),
    (5, 7),
    (5, 9),
    (5, 13),
    (6, 7),
    (6, 10),
    (6, 14),
    (7, 11),
    (7, 15),
    (8, 9),
    (8, 10),
    (8, 11),
    (8, 12),
    (8, 13),
    (9, 10),
    (9, 11),
    (9, 12),
    (9, 13),
    (10, 11),
    (10, 14),
    (10, 15),
    (11, 14),
    (11, 15),
    (12, 13),
    (12, 14),
    (12, 15),
    (13, 14),
    (13, 15),
    (14, 15),
]


def gen_csp_from_board(board):
    assert len(board) == 81
    doms = generate_domains_single(board)
    constraints = generate_constraints()
    csp = ConstraintNetwork(len(board))
    for c_1, c_2 in constraints:
        csp.add_ne_constraint(c_1, c_2)
    for i, dom in enumerate(doms):
        csp.set_domain(i, dom)
    return csp


def gen_csp_from_str(s):
    board = list(map(int, s.replace("\n", "").replace(".", "0")))
    return gen_csp_from_board(board)


sudoku_csp_1 = lambda: gen_csp_from_str(
    """427568193
683197524
915342867
132685749
598734612
7..2..35.
349851276
871926435
256473981"""
)
sudoku_csp_2 = lambda: gen_csp_from_str(
    """.6....91.
2.3.1568.
...6.3254
.2...13..
15..4...6
...2..89.
..6..2.79
4.7.9..62
9127..5.."""
)
sudoku_csp_3 = lambda: gen_csp_from_str(
    """3...682..
41.27.5.9
....4.318
591......
..7...4..
......851
625.1....
1.4.95.23
..382...5"""
)

sudoku_csp_4 = lambda: gen_csp_from_str(
    """3...8....
...7....5
1........
......36.
..2..4...
.7.......
....6.13.
.452.....
......8.."""
)

sudoku_csp_5 = lambda: gen_csp_from_str(
    """.3..5..4.
..8.1.5..
46.....12
.7.5.2.8.
...6.3...
.4.1.9.3.
25.....98
..1.2.6..
.8..6..2."""
)


def get_all_from_file(fname, puzzle_path):
    with open(puzzle_path.joinpath(fname).as_posix()) as f:
        puzzles = []
        puzzle = []
        for line in f.readlines():
            line = line.strip()
            if line and (line[0] == "." or line[0].isnumeric()):
                line = line.replace(".", "0").replace(",", "")
                puzzle.extend(map(int, line))
            if len(puzzle) == 81:
                puzzles.append(puzzle)
                puzzle = []
    return puzzles


def get_all_puzzles():
    puzzle_path = pathlib.Path(__file__).parent.parent.joinpath("src", "puzzles")
    all_puzz = get_all_from_file("sudoku_easy.txt", puzzle_path)
    all_puzz.extend(get_all_from_file("sudoku_hard.txt", puzzle_path))
    all_puzz.extend(get_all_from_file("custom.txt", puzzle_path))
    return list(map(gen_csp_from_board, all_puzz))


def sud_4x4_to_domains(board):
    return [{x} if x else {1, 2, 3, 4} for x in board]


def csp_from_4x4_str(string):
    csp = ConstraintNetwork(16)
    for i, d in enumerate(sud_4x4_to_domains(map(int, string))):
        csp.set_domain(i, d)
    for i, j in ALL_CONSTRAINTS_4X4:
        csp.add_ne_constraint(i, j)
    return csp


_API_URL = "https://sugoku.herokuapp.com/solve"
_SOL_DATA_FIELD = "solution"
_PUZZLE_DATA_FIELD = "board"


def flatten_sudoku(sudoku_matrix: List[List[int]]) -> List[int]:
    """2D sudoku list to 1D"""
    return [val for row in sudoku_matrix for val in row]


def unflatten_sudoku(sudoku_list: List[int]) -> List[List[int]]:
    """1D sudoku list to 2D"""
    return [sudoku_list[i : i + 9] for i in range(0, 81, 9)]


def sudoku_string_to_list(sudoku_string: str) -> List[int]:
    """One line sudoku str to 1D list"""
    return list(map(int, sudoku_string))


def sudoku_string_to_matrix(sudoku_string: str) -> List[List[int]]:
    """One line sudoku str to 2D list"""
    return unflatten_sudoku(sudoku_string_to_list(sudoku_string))


def fetch_sudoku_solution(sudoku: Union[str, List[int]]) -> List[int]:
    """Fetch a solution for a sudoku puzzle and return it in a 1D list form."""
    req_data = {
        _PUZZLE_DATA_FIELD: str(
            sudoku_string_to_matrix(sudoku)
            if isinstance(sudoku, str)
            else unflatten_sudoku(sudoku)
        )
    }
    req = requests.post(_API_URL, data=req_data)
    assert req.status_code == 200
    return flatten_sudoku(req.json()[_SOL_DATA_FIELD])


t_suites = """060008029703005060020610403201740008006002504400106230804500102600081340502004000
310070000800390015040080067004001002280907540900046081023009804400713020096008003
003008072100500006205036001008900004000720080756040920030080409000610030842009000
530026409000900201942001000010009700059407832020080100176034000080190604090600013
074600000030100760010508349092061030083000071100937006927006010000709520001402090
007005000526094178900200600063002097002150400059700002200040960078901045690500001
007300405000020900253064870090740360000030080836209047100802603600000018082610004
290500007700000400004738012902003064800050070500067200309004005000080700087005109
034060901700012680080009000023050790007020005500078030010590000000000413078130020
370650892004002060006100000000426705140000080005800200009080400003200058480069001
020001630090500400806049002900005701000900300352076800009004506080050000045600018
293050000000096028800040305908000001014680200000009034082400000000062480036070510
040000179002008054006005008080070910050090030019060040300400700570100200928000060
005020001087350046400060500050900000070035410693140857741500608000284005500000304
608730000200000460000064820080005701900618004031000080860200039050000100100456200
024001080000700320605830900002000890000208160810094000283006000400109032000300408
008040000000007010954060273007000300289405001000701502000000020025809430406072100
020604030450100206600005100004003000095201380200500907510000603807352000000000058
400700650000640002276800001002000005035024080800069307008900760040286000100000098
080020000040500320020309046600090004000640501134050700360004002407230600000700450""".splitlines()
