from src.solvers import SolverType, solve, make_arc_consistent, revise
from src.constraintnetwork import ConstraintNetwork
from .utils import ALL_CONSTRAINTS, sudoku_csp_1, sudoku_csp_2


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


def test_revise():
    csp = sudoku_csp_1()
    assert revise(csp, 46, 45)
    assert 7 not in csp.get_domain(46)
    assert not revise(csp, 46, 45)
    for j in csp.get_vars_in_contraint_with(46):
        revise(csp, 46, j)
    assert csp.get_domain(46) == {6}

    csp = sudoku_csp_2()
    for i in range(81):
        if len(csp.get_domain(i)) > 1:
            continue
        for j in csp.get_vars_in_contraint_with(i):
            assert not revise(csp, i, j)

    for j in csp.get_vars_in_contraint_with(80):
        revise(csp, 80, j)
    assert csp.get_domain(80) == {3, 8}


def test_arc_consistency():
    for csp in [sudoku_csp_1(), sudoku_csp_2()]:
        make_arc_consistent(csp)
        for i in range(csp.num_variables()):
            for a in csp.get_domain(i):
                for j in csp.get_vars_in_contraint_with(i):
                    dj = csp.get_domain(j)
                    assert len(dj) != 0
                    assert len(dj) > 1 or a not in dj
    # AC3 should "solve" the easy one
    csp = sudoku_csp_1()
    make_arc_consistent(csp)
    for i in range(81):
        assert len(csp.get_domain(i)) == 1
