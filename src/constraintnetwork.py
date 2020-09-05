#
# Informed Search Methods
#
# A class for processing constraint networks.
# You do not want to change anything in hee!
#
class ConstraintNetwork:

    @staticmethod
    def ordered_pair( i, j):
        if i < j:
            return (i, j)
        else:
            return (j, i)

    def __init__(self, n):
        """
        Constructor: n is the number of variables the constraint network should have.
        """
        self.num_vars = n
        self.constraints_all = []
        self.constraints = [ set() for _ in range(0,n) ]
        self.domains = [ set() for _ in range(0,n) ]

    def __str__(self):
        """
        Enables us to print the network or get as a string.
        """
        s = ''
        for d in self.domains:
            s += str(d) + '\n'
        for c in self.constraints_all:
            s += str(c) + ' '
        return s

    def num_variables(self):
        """
        Returns the number of variables in the network.
        """
        return self.num_vars

    def set_domain(self, i, domain):
        """
        Sets the domain of variable i.
        """
        assert 0 <= i < self.num_vars
        self.domains[i] = domain.copy()

    def get_domain(self, i):
        """
        Returns the domain of variable i.
        """
        assert 0 <= i < self.num_vars
        return self.domains[i]

    def add_ne_constraint(self, i, j):
        """
        Adds a not-equal constraint between variables i and j.
        """
        assert 0 <= i < self.num_vars
        assert 0 <= j < self.num_vars
        assert i != j
        ( i, j ) = self.ordered_pair(i, j)
        self.constraints_all.append((i, j))
        self.constraints[i].add(j)
        self.constraints[j].add(i)
        return

    def get_constraints(self):
        """
        Returns a list of all constraints.
        """
        return self.constraints_all

    def get_vars_in_contraint_with(self, i):
        """
        Returns a set of variables sharing a constraint with variable i
        """
        assert 0 <= i < self.num_vars
        return self.constraints[i]

    def consistent_values(self, i, j, vi, vj):
        """
        Returns True if there is no constraint between variables i and j violated by their current assigned values,
        otherwise False.
        """
        assert 0 <= i < self.num_vars
        assert 0 <= j < self.num_vars
        assert i != j
        return j not in self.constraints[i] or vi != vj

    def consistent(self, i, j, A):
        """
        Returns True if there is no constraint between variables i and j violated by their current assignment,
        otherwise False.
        """
        assert 0 <= i < self.num_vars
        assert 0 <= j < self.num_vars
        assert i != j
        return j not in self.constraints[i] or A[i] != A[j]

    def consistent_other(self, i, A):
        """
        Returns True if there is no constraint between variable i and all variables j<i violated by
        their current assignment, otherwise False.
        """
        assert len(A) <= self.num_vars
        assert 0 <= i < len(A)
        for j in range(len(A)):
            if i != j and not self.consistent(i,j,A):
                return False
        return True

    def consistent_all(self, A):
        """
        Returns True if there is no constraint between all pair of variables i and j, where i,j < len(A), by
        their current assignment, otherwise False.
        """
        assert len(A) <= self.num_vars
        for i in range(len(A)):
            if not self.consistent_other(i, A):
                return False
        return True
