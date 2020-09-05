#
# Informed Search Methods
#
# Simple-CSP solver.  Run with '-h' command-line argument to see usage.
# You do not want to change anything in heree!
#
#
import argparse
import re
import constraintnetwork
import solvers
from timeit import default_timer as timer

def log_string( str ):
    with open( 'output.txt', 'a' ) as f:
        f.write(str)
        f.write('\n')


def domain_from_str(str):
    d = set()
    for match in re.finditer(r'\d+', str):
        d.add(int(match.group()))
    return d


def read_domains_of_instances( name ):
    instances_domains = []
    try:
        with open(name) as f:
            domains = []
            for line in f:
                if line.strip() == '#':
                    instances_domains.append(domains)
                    domains = []
                else:
                    domains.append(domain_from_str(line))
            instances_domains.append(domains)
    except FileNotFoundError:
        print("File", "'"+name+"'", "not found.")
    return instances_domains


def read_binary_constraints( name ):
    constraints = []
    try:
        with open(name) as f:
            for line in f:
                iterator = re.finditer(r'\d+', line)
                c = []
                for match in iterator:
                    c.append(int(match.group()))
                assert len(c) == 2
                constraints.append((c[0], c[1]))
    except FileNotFoundError:
        print("File", "'" + name + "'", "not found.")
    return constraints


def make_constraint_network(constraints, domains, ac):
    csp = constraintnetwork.ConstraintNetwork( len(domains) )
    for c in constraints:
        csp.add_ne_constraint(c[0],c[1])
    for i in range(len(domains)):
        csp.set_domain(i, domains[i])
    if ac:
        solvers.make_arc_consistent(csp)
    return csp


#
# Main program
#

# Set up and parsee command-line arguments
ap = argparse.ArgumentParser()
ap.add_argument( "-g", "--gtbt", choices=['on','off'],default='on', help="Run the GTBT solver.")
ap.add_argument( "-b", "--bt",   choices=['on','off'],default='on', help="Run the the BT solver.")
ap.add_argument( "-j", "--bj",   choices=['on','off'],default='on', help="Run the BJ solver.")
ap.add_argument( "-c", "--cbj",  choices=['on','off'],default='on', help="Run the CBJ solver.")
ap.add_argument( "-i", "--instances", type=int, action='append', help="Run only specified puzzle instance.")
ap.add_argument( "-t", "--time",  choices=['on','off'],default='on', help="Display runtime (in seconds).")
ap.add_argument( "-a", "--arc",  choices=['on','off'],default='off', help="Make constraint network arc consistent.")
ap.add_argument( "-name", default='sudoku', help="Basename of constraint and instances files (e.g. sudoku).")

args = vars(ap.parse_args())
print(args)
solvers_to_run = []
if args['gtbt'] == 'on':
    solvers_to_run.append(solvers.SolverType.GTBT)
if args['bt'] == 'on':
    solvers_to_run.append(solvers.SolverType.BT)
if args['bj'] == 'on':
    solvers_to_run.append(solvers.SolverType.BJ)
if args['cbj'] == 'on':
    solvers_to_run.append(solvers.SolverType.CBJ)
if args['instances']:
    specific_instances_to_run = args['instances']
else:
    specific_instances_to_run = []
display_time = (args['time'] == 'on')
arc_consistent = (args['arc'] == 'on')
name = args['name']
input_cnstr_file = name + "_cst.txt"
input_domain_file = name + "_dom.txt"

# Read in CSP problem specification.
problem_constraints = read_binary_constraints(input_cnstr_file)
print('Read', len(problem_constraints), 'constraints.')
problem_instances = read_domains_of_instances(input_domain_file)
print('Read', len(problem_instances), 'problem instances.')

# Run the specified solvers on the given problem instances and log results (output.txt).
for solver_type in solvers_to_run:
    for i,instance in enumerate(problem_instances):
        if not specific_instances_to_run or i in specific_instances_to_run:
            csp = make_constraint_network(problem_constraints, instance, arc_consistent)
            start = timer()
            (solution, nodes) = solvers.solve(solver_type, csp)
            end = timer()
            if display_time:
                output = "{:3d} {:15s} {:10d} {:9.4f} {:s}".format(i, str(solver_type), nodes, end-start, str(solution))
            else:
                output = "{:3d} {:15s} {:10d} {:s}".format(i, str(solver_type),nodes, str(solution))
            print(output)
            log_string(output)