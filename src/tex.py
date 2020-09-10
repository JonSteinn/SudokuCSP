import pathlib


class Solution:
    BT, BJ, CBJ = range(3)
    _TYPE_STR_TO_INT = {"BT": 0, "BJ": 1, "CBJ": 2}
    _TYPE_INT_TO_STR = ["BT", "BJ", "CBJ"]

    def __init__(self, line):
        ind, alg, nodes, time, sol = (lambda a, b: (*a.split(), b))(*line.split(" ["))

        self.solution = list(map(int, sol.strip()[:-1].split(", ")))
        self.type = Solution._TYPE_STR_TO_INT[alg.split(".")[1]]
        self.puzzle = int(ind)
        self.nodes_expanded = int(nodes)
        self.time = float(time)

    def __str__(self):
        return (
            f"{self.puzzle:3d} "
            f"{Solution._TYPE_INT_TO_STR[self.type]:3s} "
            f"{self.nodes_expanded:10d} "
            f"{self.time:9.4f} "
            f"{str(self.solution):s}"
        )


class SolutionData:
    # This file's directory
    _PATH = pathlib.Path(__file__).parent.absolute()

    @classmethod
    def construct_from_file(cls, file_path):
        data = ([], [], [])
        with open(SolutionData._PATH.joinpath(file_path)) as f:
            for line in f.readlines():
                solution = Solution(line)
                data[solution.type].append(solution)
        return cls(data)

    def __init__(self, data=None):
        self.data = ([], [], []) if data is None else data

    def add_solution(self, solution):
        self.data[solution.type].append(solution)

    def to_latex_table(self, tab="  ", caption="TODO", label="TODO"):
        """Create a latex table from output data. Requires 'usepackage[table]{xcolor}'.
        """
        return "".join(
            (
                "\\begin{center}\n",
                f"{tab}\\begin{{table}}[ht]\n",
                f"{tab*2}\\centering\n",
                f'{tab*2}\\rowcolors{{2}}{{white}}{{gray!25}}\n'
                f"{tab*2}\\begin{{tabular}}{{cllllll}}\n",
                (
                    f"{tab*3}\\cellcolor[gray]{{0.7}} & \\multicolumn{{2}}{{c}}"
                    "{BT\\cellcolor[gray]{0.7}} & \\multicolumn{2}{c}{BJ"
                    "\\cellcolor[gray]{0.7}}  & \\multicolumn{2}{c}"
                    "{CBJ\\cellcolor[gray]{0.7}} \\\\\n"
                ),
                (
                    f"{tab*3}\\cellcolor[gray]{{0.7}} Test suite & "
                    "\\cellcolor[gray]{0.7}Nodes & \\cellcolor[gray]{0.7}Time & "
                    "\\cellcolor[gray]{0.7}Nodes & \\cellcolor[gray]{0.7}Time & "
                    "\\cellcolor[gray]{0.7}Nodes & \\cellcolor[gray]{0.7}Time \\\\\n"
                ),
                "".join(
                    (
                        f"{tab*3}{i} & {bt.nodes_expanded} & {bt.time} "
                        f"& {bj.nodes_expanded} & {bj.time} & {cbj.nodes_expanded} & "
                        f"{cbj.time}\\\\\n"
                        for i, (bt, bj, cbj) in enumerate(zip(*self.data))
                    )
                ),
                f"{tab*2}\\end{{tabular}}\n"
                f"{tab*2}\\caption{{{caption}}}\n"
                f"{tab*2}\\label{{tab:{caption}}}\n"
                f"{tab}\\end{{table}}\n"
                "\\end{center}",
            )
        )

    def __str__(self):
        return "\n".join(str(sol) for d in self.data for sol in d)


def puzzle_to_tikz(puzzle, tab='  ', caption='TODO', label='TODO'):
    """Create a tikz drawing of a puzzle"""
    return ''.join(
        (
            (
                f'{tab*2}\\begin{{tikzpicture}}[scale=\\scale, '
                'every node/.style={scale=\\scale}]\n'
            ),
            '\n'.join(
                (lambda v, y, x: (
                    f'{tab*3}\\node[anchor=center,scale=1.5] at'
                    f' ({x+.5}, {8.5-y}) {{${v}$}};'
                ))(val, *divmod(i, 9)) for i, val in enumerate(puzzle) if val
            ),
            f'\n{tab*3}\\draw[gray!50] (0,0) grid (9,9);\n',
            f'{tab*3}\\draw[line width=0.55mm, scale=3] (0, 0) grid (3, 3);\n',
            f'{tab*2}\\end{{tikzpicture}}\n'
        )
    )


def main():
    with open('sudoku.txt') as f:
        for line in f.readlines():
            if line[0] == '#':
                continue
            print(puzzle_to_tikz(map(int, line.strip())))


if __name__ == "__main__":
    main()

