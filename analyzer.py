import ast


class PyAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self._stats = {"variables": [], "loops": [], "logic": []}

    @property
    def variables(self):
        return self._stats["variables"]

    @property
    def loops(self):
        return self._stats["loops"]

    @property
    def logic(self):
        return self._stats["logic"]

    def visit_Import(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_ImportFrom(self, node):
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node):
        for target in node.targets:
            self._stats["variables"].append(target.id)
        print('Node type: Assign and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node):
        # print('Node type: BinOp and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    def visit_Expr(self, node):
        # print('Node type: Expr and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    # def visit_Num(self, node):
        # print('Node type: Num and fields: ', node._fields)

    def visit_Name(self, node):
        # print('Node type: Name and fields: ', node._fields)
        ast.NodeVisitor.generic_visit(self, node)

    # def visit_Str(self, node):
        # print('Node type: Str and fields: ', node._fields)
