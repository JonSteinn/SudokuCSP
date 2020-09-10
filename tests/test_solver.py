from src.solvers import SolverType, solve, make_arc_consistent, revise
from src.constraintnetwork import ConstraintNetwork
from .utils import (
    ALL_CONSTRAINTS,
    sudoku_csp_1,
    sudoku_csp_2,
    sudoku_csp_3,
    sudoku_csp_4,
    sudoku_csp_5,
    get_all_puzzles,
    csp_from_4x4_str,
    t_suites,
    fetch_sudoku_solution,
    gen_csp_from_board
)


def test_node_count_BT():
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

    assert solve(SolverType.BT, csp_from_4x4_str("0320200000010140"))[1] == 26
    # Backtracking done by hand, expands 2+6+2 additional nodes to the 16
    """
    .32.
    2...
    ...1
    .142
    """


def test_node_count_BJ():
    # Backjumping should save us one node in this one
    c = csp_from_4x4_str("3410020000200143")
    _, bt_n = solve(SolverType.BT, c)
    _, bj_n = solve(SolverType.BJ, c)
    assert bt_n > bj_n
    assert bt_n == 23
    assert bj_n == 22
    """
    3410
    .2..
    ..2. <--- this 2
    .143

    The 'this 2' initially fails because we set the first cell in the row to 2
    and in backtracking we jump back one and try different values there while
    backjumping goes all the way to the first in the row. There are other backjumps
    but 'by coincidence' there backtracking has exhausted their possiblities at the
    same time so beside that one jump, they expand the same, that is BJ safes a
    single expansion.
    """


def test_node_count_CBJ():
    csp = sudoku_csp_5()
    make_arc_consistent(csp)
    _, n0 = solve(SolverType.BT, csp)
    _, n1 = solve(SolverType.BJ, csp)
    _, n2 = solve(SolverType.CBJ, csp)
    assert n2 < n1 < n0
    assert n0 == 520
    assert n1 == 504
    assert n2 == 496


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
    all_puzz = get_all_puzzles()
    all_puzz.extend([sudoku_csp_1(), sudoku_csp_2(), sudoku_csp_3(), sudoku_csp_4()])
    for csp in all_puzz:
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


x3 = "359168274418273569762549318591482736837651492246937851625314987184795623973826145"


def test_correct_solution_BT():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    sol, _ = solve(SolverType.BT, csp)
    assert sol == expected


def test_correct_solution_BT_with_AC3():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    make_arc_consistent(csp)
    sol, _ = solve(SolverType.BT, csp)
    assert sol == expected


def test_correct_solution_BJ():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    sol, _ = solve(SolverType.BJ, csp)
    assert sol == expected


def test_correct_solution_BJ_with_AC3():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    make_arc_consistent(csp)
    sol, _ = solve(SolverType.BJ, csp)
    assert sol == expected


def test_correct_solution_CBJ():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    sol, _ = solve(SolverType.CBJ, csp)
    assert sol == expected


def test_correct_solution_CBJ_with_AC3():
    expected = list(map(int, x3))
    csp = sudoku_csp_3()
    make_arc_consistent(csp)
    sol, _ = solve(SolverType.CBJ, csp)
    assert sol == expected


def test_test_suites():
    for i, sud in enumerate(t_suites):
        e = fetch_sudoku_solution(sud)
        s, n1 = solve(SolverType.CBJ, gen_csp_from_board(list(map(int, sud))))
        assert s == e
        s, n2 = solve(SolverType.BJ, gen_csp_from_board(list(map(int, sud))))
        assert s == e
        if i < 8:
            s, n3 = solve(SolverType.BT, gen_csp_from_board(list(map(int, sud))))
            assert s == e
        else:
            n3 = n2 + 1
        assert n1 < n2 < n3


def test_test_suites_with_ac3():
    for i, sud in enumerate(t_suites):
        g1 = gen_csp_from_board(list(map(int, sud)))
        g2 = gen_csp_from_board(list(map(int, sud)))
        g3 = gen_csp_from_board(list(map(int, sud)))
        make_arc_consistent(g1)
        make_arc_consistent(g2)
        make_arc_consistent(g3)
        s1, n1 = solve(SolverType.BT, g1)
        s2, n2 = solve(SolverType.BJ, g2)
        s3, n3 = solve(SolverType.CBJ, g3)
        if i == 11:
            assert n1 > n2 > n3
            assert (n1, n2, n3) == (427, 353, 316)
        else:
            assert n1 == n2 == n3 == 81
        s4 = fetch_sudoku_solution(sud)
        assert s1 == s2 == s3 == s4
