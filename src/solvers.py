#
# Informed Search Methods
#
# Implementation of various backtracking-based solvers
#

from enum import Enum


class SolverType(Enum):
    """Solver types enum"""
    GTBT = 1        # Generate-and-test Backtracking
    BT = 2          # Cronological Backtracking
    BJ = 3          # Backjumping
    CBJ = 4         # Conflict-Directed Backjumping


def make_arc_consistent(cn):
    """
    Makes the cn constraint network arc-consistent (use the AC-3 algorithm).
    (there are no unary-constraints so you can omit making it first node-consistent).
    """

    # ********** YOU IMPLEMENT THIS **********

    return


def solve(st, cn):
    """
    Use the specified backtracking algorithm (st) to solve the CSP problem (cn).
    Returns a tuple (assignment, nodes), where the former is the solution (an empty list
    if not found) and the latter the number of nodes generated.
    """

    def consistent_upto_level(cn, i, A):
        for j in range(0, i):
            if not cn.consistent(i, j, A):
                return j
        return i

    def GTB(cn, i, A):
        # print(A)
        nonlocal num_nodes
        num_nodes += 1
        if i >= cn.num_variables():
            return cn.consistent_all(A)
        for v in cn.get_domain(i):
            A.append(v)
            solved = GTB(cn, i+1, A)
            if solved:
                return True
            A.pop()
        return False

    def BT(cn, i, A):
        nonlocal num_nodes
        num_nodes += 1
        for v in cn.get_domain(i):
            # print(f"{i} : {v}{'*' if len(cn.get_domain(i))==1 else ''}")
            A.append(v)
            if not cn.consistent_other(i, A):
                A.pop()
                continue
            if i == cn.num_variables() - 1:
                return True
            solved = BT(cn, i+1, A)
            if solved:
                return True
            A.pop()
        return False

    def BJ(cn, i, A):
        # TODO

        return (False, 0)

    def CBJ(cn, i, A, CS):
        # TODO

        return (False, 0)

    num_nodes = 0
    assignment = []
    ConflictSet = [set() for _ in range(0, cn.num_variables())]

    print('Solving ...', st)
    if st == SolverType.GTBT:
        solved = GTB(cn, 0, assignment)
    elif st == SolverType.BT:
        solved = BT(cn, 0, assignment)
    elif st == SolverType.BJ:
        (solved, _) = BJ(cn, 0, assignment)
    elif st == SolverType.CBJ:
        (solved, _) = CBJ(cn, 0, assignment, ConflictSet)
    return (assignment, num_nodes)
