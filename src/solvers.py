#
# Informed Search Methods
#
# Implementation of various backtracking-based solvers
#

from enum import Enum
from collections import deque
from itertools import chain


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

    # Try all values in the domain of i
    for val_i in dom_i:
        dom_j = cn.get_domain(j)

        # If D_j = {val_i}, they conflict and no need for D_i to contain val_i
        # This only works for non-equal constraints but since our network is
        # only made for them, that is fine.
        if len(dom_j) == 1 and val_i in dom_j:
            to_rem.add(val_i)

    # If we found domain values to remove
    if to_rem:
        dom_i -= to_rem  # dom_i = dom_i \setminus to_rem
        return True

    # If no values to remove from D_i are found, we return false
    return False


def init_constraint_queue(cn):
    """Instantiate a queue with all constraints, including symmetric duplicates
    as the algorithm provided in the article does not assume constraints
    to be a symmetric relation.
    """
    # Convert constraints into a queue with all constraints (a, b)
    # and for each such constraint we also add (b, a)
    return deque(
        chain(
            cn.get_constraints(),
            ((b, a) for a, b in cn.get_constraints())
        )
    )


def make_arc_consistent(cn):
    """
    Makes the cn constraint network arc-consistent (use the AC-3 algorithm).
    (there are no unary-constraints so you can omit making it first node-consistent).
    """
    queue = init_constraint_queue(cn)  # includes symmetric duplicates

    # Until the queue is empty, caused by no more revisions being available
    while queue:
        i, j = queue.popleft()

        # If we removed a value from the domain of i
        if revise(cn, i, j):

            # We try again removing from all peers but j, against i.
            # No need to check h != i as that is never the case in our network.
            for h in cn.get_vars_in_contraint_with(i):
                if h != j:
                    queue.append((h, i))


def solve(st, cn):
    """
    Use the specified backtracking algorithm (st) to solve the CSP problem (cn).
    Returns a tuple (assignment, nodes), where the former is the solution (an empty list
    if not found) and the latter the number of nodes generated.
    """
    # pylint: disable=too-many-statements, unused-variable

    def consistent_upto_level(cn, i, A):
        for j in range(0, i):
            if not cn.consistent(i, j, A):
                return j
        return i

    def GTB(cn, i, A):
        nonlocal num_nodes
        num_nodes += 1
        if i >= cn.num_variables():
            return cn.consistent_all(A)
        for v in cn.get_sorted_domain(i):
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

        # Try all assignments of x_i in D_i
        for v in cn.get_sorted_domain(i):

            # Assign current value
            A.append(v)

            # If a solution is found
            if cn.consistent_other(i, A) and (
                i == cn.num_variables() - 1 or BT(cn, i + 1, A)
            ):
                return True

            # Remove current value
            A.pop()

        # If all values in D_i are exhausted we fail
        return False

    def BJ(cn, i, A):
        # Node counter
        nonlocal num_nodes
        num_nodes += 1

        # Init return_depth to a value less then all levels
        return_depth = -1

        # Try all assignments of x_i in D_i
        for v in cn.get_sorted_domain(i):

            # Assign current value
            A.append(v)

            # Lowest index of variable that is not consistent with i, or i if all are
            max_check_lvl = consistent_upto_level(cn, i, A)

            # If consistent with variables x_0,...,x_{i-1}
            if i == max_check_lvl:
                # We found a solution as all variables are expanded and consistent
                if i == cn.num_variables() - 1:
                    return True, -1

                # Recursion
                solved, max_check_lvl = BJ(cn, i + 1, A)

                # If the recursive call yields a solution, we just return right away
                if solved:
                    return True, -1

                # If the recursion call wants us to backjump over current node
                if max_check_lvl < i:
                    A.pop()                      # Remove current value
                    return False, max_check_lvl  # return fail and 'jumping destination'

            # After iterations are exhausted, return_depth will have the deepest level
            # among those that fail first given each value assigned to x_i, that is
            # max(min(j such that (i,j) are inconsistent for x_i = v) for v in D_i)
            return_depth = max(return_depth, max_check_lvl)

            # Remove current value
            A.pop()

        # If all values in D_i fail, return failure and the 'jumping destination'
        return False, return_depth

    def CBJ(cn, i, A, CS):
        # Node counter
        nonlocal num_nodes
        num_nodes += 1

        # Init CS[i] to a singleton wich value is less then all levels
        CS[i] = {-1}

        # Try all assignments of x_i in D_i
        for v in cn.get_sorted_domain(i):

            # Assign current value
            A.append(v)

            # Lowest index of variable that is not consistent with i, or i if all are
            h = consistent_upto_level(cn, i, A)

            if h < i:  # If not consistent
                # Add the lowest index that fails to the conflict set
                CS[i].add(h)
            else:  # If consistent
                # We found a solution as all variables are expanded and consistent
                if i == cn.num_variables() - 1:
                    return True, -1

                # Recursion
                solved, r_depth = CBJ(cn, i + 1, A, CS)

                # If the recursive call yields a solution, we just return right away
                if solved:
                    return True, -1

                # If the recursion call wants us to backjump over current node
                if r_depth < i:
                    A.pop()                # Remove current value
                    return False, r_depth  # return fail and 'jumping destination'

            # Remove current value
            A.pop()

        # At each iteration there are two possible ways to add to the current
        # conflict set, either the lowest level of inconsistency caused by the
        # current value assigned (much like done in backjumping) and then the
        # recursion call can pass up values to this current node. We set r_depth
        # to the deepest level among all levels in the conflict set.
        r_depth = max(CS[i])

        # Pass up causes of failures, disregarding the failure of the node we pass
        # to. That is, we find the node we can jump to and copy all the elements
        # of the current node's conflict set, except that node, to its conflict set.
        # CS[r_d] = CS[r_d] \cup (CS[i] \setminus {r_d})
        CS[r_depth].update(CS[i])
        CS[r_depth].discard(r_depth)

        # If all values in D_i fail, return failure and the 'jumping distance'
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
