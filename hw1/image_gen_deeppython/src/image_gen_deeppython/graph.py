import ast
import pprint

import networkx as nx

import matplotlib.pyplot as plt


class FibWalker(ast.NodeVisitor):
    def __init__(self):
        self.def_stack = []
        self.graph = nx.Graph()

    @property
    def in_func_def(self):
        return len(self.def_stack) > 0

    def proceed(self, stmt):
        super(self.__class__, self).generic_visit(stmt)

    def visit_Call(self, stmt):
        func_name = stmt.func.id

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.def_stack.append(func_name)

        self.graph.add_node(func_name)

        if parent_name:
            self.graph.add_edge(func_name, parent_name)

        # for arg in stmt.args:
        #     self.visit(arg)

        self.proceed(stmt)
        self.def_stack.pop()

    def visit_FunctionDef(self, stmt):
        func_name = stmt.name

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.def_stack.append(func_name)

        self.graph.add_node(func_name)

        if parent_name:
            self.graph.add_edge(func_name, parent_name)

        self.proceed(stmt)

        # Pop this function from the stack
        self.def_stack.pop()

    def visit_For(self, stmt):
        func_name = "for"

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.def_stack.append(func_name)

        self.graph.add_node(func_name)

        if parent_name:
            self.graph.add_edge(func_name, parent_name)

        self.proceed(stmt)

        self.def_stack.pop()

    def visit_While(self, stmt):
        func_name = "while"

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.def_stack.append(func_name)

        self.graph.add_node(func_name)

        if parent_name:
            self.graph.add_edge(func_name, parent_name)

        self.proceed(stmt)

        self.def_stack.pop()

    def visit_Yield(self, stmt):
        func_name = "yield"

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.def_stack.append(func_name)

        self.graph.add_node(func_name)

        if parent_name:
            self.graph.add_edge(func_name, parent_name)

        self.graph.add_edge(stmt.value.id, func_name)

        self.proceed(stmt)

        self.def_stack.pop()

    def visit_Assign(self, stmt):
        assignee = stmt.targets[0].id

        parent_name = None

        if self.def_stack:
            parent_name = self.def_stack[-1]

        self.graph.add_node(assignee)

        if parent_name:
            self.graph.add_edge(assignee, parent_name)

        self.proceed(stmt)


def main(filename = "fib.py"):
    with open(filename, 'r') as fin:
        src = fin.read()

    node = ast.parse(src)

    mw = FibWalker()

    mw.visit(node)

    nx.draw_networkx(mw.graph)

    # plt.show()
    plt.rc('pgf', texsystem='lualatex')
    plt.savefig("plot.pgf")


if __name__ == "__main__":
    main()
