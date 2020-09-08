from src.constraintnetwork import ConstraintNetwork
from src.solvers import solve, SolverType

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


def sud_4x4_to_domains(board):
    return [{x} if x else {1, 2, 3, 4} for x in board]


def csp_from_4x4_str(string):
    csp = ConstraintNetwork(16)
    for i, d in enumerate(sud_4x4_to_domains(map(int, string))):
        csp.set_domain(i, d)
    for i, j in ALL_CONSTRAINTS_4X4:
        csp.add_ne_constraint(i, j)
    return csp

c = csp_from_4x4_str("3410020000200143")
#print(solve(SolverType.GTBT, c))
print(solve(SolverType.BT, c))
print(solve(SolverType.BJ, c))
#print(solve(SolverType.CBJ, c))


a = """0
1
2
3
4
5
6
7
8
9
10
10
9
10
11
12
13
10
11
12
13
14
15""".split()


b="""0
1
2
3
4
5
6
7
8
9
10
9
10
11
12
13
10
11
12
13
14
15""".split()

print(a)
print(b)


"""
3410
0200
0020
0143
"""
