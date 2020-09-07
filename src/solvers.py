#
# Informed Search Methods
#
# Implementation of various backtracking-based solvers
#

from enum import Enum
from collections import deque


class SolverType(Enum):
    """Solver types enum"""

    GTBT = 1  # Generate-and-test Backtracking
    BT = 2  # Cronological Backtracking
    BJ = 3  # Backjumping
    CBJ = 4  # Conflict-Directed Backjumping


def revise(cn, i, j):
    """Remove values in the domain of i if they
    don't allow variable j to take any value.
    """
    to_rem = set()
    dom_i = cn.get_domain(i)
    for val_i in dom_i:
        dom_j = cn.get_domain(j)
        # TODO: This is somewhat tailored for sudoku, ask if okay, otherwise generalize
        if len(dom_j) == 1 and val_i in dom_j:
            to_rem.add(val_i)
    if to_rem:
        dom_i -= to_rem
        return True
    return False


def init_constraint_queue(cn):
    """Instantiate a queue with all constraints, including symmetric duplicates
    as the algorithm provided in the article does not assume constraints
    to be a symmetric relation.
    """
    # pylint: disable=consider-using-enumerate
    constraint_queue = deque(cn.get_constraints())
    for i in range(len(constraint_queue)):
        i, j = constraint_queue[i]
        constraint_queue.append((j, i))
    return constraint_queue


def make_arc_consistent(cn):
    """
    Makes the cn constraint network arc-consistent (use the AC-3 algorithm).
    (there are no unary-constraints so you can omit making it first node-consistent).
    """
    queue = init_constraint_queue(cn)
    while queue:
        i, j = queue.popleft()
        if revise(cn, i, j):
            for h in cn.get_vars_in_contraint_with(i):
                if h != j:  # TODO: not checking h != i is Sudoku specific, okay'
                    queue.append((h, i))


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
        # Node counter
        nonlocal num_nodes
        num_nodes += 1
        # Algorithm starts here
        if i >= cn.num_variables():
            return cn.consistent_all(A)
        for v in cn.get_domain(i):
            A.append(v)
            solved = GTB(cn, i + 1, A)
            if solved:
                return True
            A.pop()
        return False

    def BT(cn, i, A):
        # Node counter
        nonlocal num_nodes
        num_nodes += 1
        # Algorithm starts here
        for v in cn.get_domain(i):
            A.append(v)
            if cn.consistent_other(i, A) and (
                i == cn.num_variables() - 1 or BT(cn, i + 1, A)
            ):
                return True
            A.pop()
        return False

    def BJ(cn, i, A):
        # Node counter
        nonlocal num_nodes
        num_nodes += 1
        # Algorithm starts here
        return_depth = -1
        for v in cn.get_domain(i):
            A.append(v)
            max_check_lvl = consistent_upto_level(cn, i, A)
            if i == max_check_lvl:
                if i == cn.num_variables() - 1:
                    return True, -1
                solved, max_check_lvl = BJ(cn, i + 1, A)
                if solved:
                    return True, -1
                if max_check_lvl < i:
                    A.pop()
                    return False, max_check_lvl
            return_depth = max(return_depth, max_check_lvl)
            A.pop()
        return False, return_depth

    def CBJ(cn, i, A, CS):
        # Node counter
        nonlocal num_nodes
        num_nodes += 1
        # Algorithm starts here
        CS[i] = {-1}
        for v in cn.get_domain(i):
            A.append(v)
            h = consistent_upto_level(cn, i, A)
            if h < i:
                CS[i].add(h)
            else:
                if i == cn.num_variables() - 1:
                    CS[i].add(i - 1)
                    return True, -1
                solved, r_depth = CBJ(cn, i + 1, A, CS)
                if solved:
                    return True, -1
                if r_depth < i:
                    A.pop()
                    return False, r_depth
            r_depth = max(CS[i])
            CS[r_depth] = CS[r_depth].union(CS[i].difference({r_depth}))
            A.pop()
        return False, r_depth

    num_nodes = 0
    assignment = []
    ConflictSet = [set() for _ in range(0, cn.num_variables())]

    print("Solving ...", st)
    if st == SolverType.GTBT:
        solved = GTB(cn, 0, assignment)
    elif st == SolverType.BT:
        solved = BT(cn, 0, assignment)
    elif st == SolverType.BJ:
        (solved, _) = BJ(cn, 0, assignment)
    elif st == SolverType.CBJ:
        (solved, _) = CBJ(cn, 0, assignment, ConflictSet)
    return (assignment, num_nodes)
