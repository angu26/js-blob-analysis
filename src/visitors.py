from esprima import NodeVisitor

class IntegerLiteralCollector(NodeVisitor):
    def __init__(self):
        self.literals = []
    
    def visit_Literal(self, node):
        if isinstance(node.value, int):
            self.literals.append(node.value)
        self.generic_visit(node)

class StringLiteralCollector(NodeVisitor):
    def __init__(self):
        self.literals = []
    
    def visit_Literal(self, node):
        if isinstance(node.value, str):
            self.literals.append(node.value)
        self.generic_visit(node)

class VariableDeclaratorLiteralCollector(NodeVisitor):
    def __init__(self):
        self.literals = {}
    
    def visit_VariableDeclarator(self, node):
        if hasattr(node, 'init') and node.init.type == 'Literal':
            self.literals[node.id.name] = node.init.value
        self.generic_visit(node)

class CallExpressionCollector(NodeVisitor):
    def __init__(self, called_function_indentifier: str):
        self.call_nodes = []
        self.function_id = called_function_indentifier

    def visit_CallExpression(self, node):
        if node.callee.type == 'Identifier' and node.callee.name == self.function_id:
            self.call_nodes.append(node)
        self.generic_visit(node)