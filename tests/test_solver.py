from src.solvers import SolverType, solve
from src.constraintnetwork import ConstraintNetwork
from .utils import ALL_CONSTRAINTS


def test_bt():
    csp = ConstraintNetwork(81)
    for a, b in ALL_CONSTRAINTS:
        csp.add_ne_constraint(a, b)
    doms = [
        {4},
        {2},
        {7},
        {5},
        {6},
        {8},
        {1},
        {9},
        {3},
        {6},
        {8},
        {3},
        {1},
        {9},
        {7},
        {5},
        {2},
        {4},
        {9},
        {1},
        {5},
        {3},
        {4},
        {2},
        {8},
        {6},
        {7},
        {1},
        {3},
        {2},
        {6},
        {8},
        {5},
        {7},
        {4},
        {9},
        {5},
        {9},
        {8},
        {7},
        {3},
        {4},
        {6},
        {1},
        {2},
        {7},
        {1, 2, 3, 4, 5, 6, 7, 8, 9},
        {1, 2, 3, 4, 5, 6, 7, 8, 9},
        {2},
        {1, 2, 3, 4, 5, 6, 7, 8, 9},
        {1, 2, 3, 4, 5, 6, 7, 8, 9},
        {3},
        {5},
        {1, 2, 3, 4, 5, 6, 7, 8, 9},
        {3},
        {4},
        {9},
        {8},
        {5},
        {1},
        {2},
        {7},
        {6},
        {8},
        {7},
        {1},
        {9},
        {2},
        {6},
        {4},
        {3},
        {5},
        {2},
        {5},
        {6},
        {4},
        {7},
        {3},
        {9},
        {8},
        {1},
    ]
    for i, d in enumerate(doms):
        csp.set_domain(i, d)
    sol, nodes = solve(SolverType.BT, csp)

    e_sol, e = [6, 4, 1, 9, 8], 0
    for x, y in zip(doms, sol):
        if len(x) == 1:
            assert x.pop() == y
        else:
            assert e_sol[e] == y
            e += 1

    assert nodes == 81 + 9
    # You must expand 81 nodes to get a solution
    # When you get to the first ., you will assign it
    # 4 (1,2,3 fail) and continue to the next variable.
    # This chain of events will endure until the variable
    # below the first . will be also set to 4 and we will
    # backtrack all the way up to the first . and then
    # continue with the correct solution, a total of 9
    # additional nodes explored.
    """
    427568193
    683197524
    915342867
    132685749
    598734612
    7..2..35.
    349851276
    871926435
    256473981
    """
