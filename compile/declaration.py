from typing import Union

from compile.process import STD_FILENAMES
from visitor.nodes import *


class ScriptFile:
    def __init__(self, ast: ScriptFileNode, context, import_std=True):
        self.global_context = context
        self.context = context.new_file_context()

        if import_std:
            for f in STD_FILENAMES:
                self.context.imported.append(self.global_context.get(f))

        for i in ast.imports:
            self.context.imported.append(self.global_context.get(i.identifier.value))

        constants = []
        for d in ast.top_level_declarations:
            if isinstance(d, ConstantDeclarationNode):
                constants.append(Constant(d, self.context))
        for c in constants:
            c.resolve()

        return


class Constant:
    def __init__(self, node: ConstantDeclarationNode, context):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value
        self.expression = Expression(node.expression, context)
        self.resolving = False
        context.add(self.identifier, (), self)

    def resolve(self):
        if self.resolving:
            raise RuntimeError('Failed to resolve constant (possible circular dependencies)')
        self.resolving = True
        self.expression.simplify()
        self.resolving = False
        if isinstance(self.expression.value, NumberLiteralNode) or isinstance(self.expression.value, BooleanLiteralNode):
            return self.expression.value
        else:
            raise RuntimeError('Failed to resolve constant')


class Expression:
    def __init__(self, node: Union[UnaryExpressionNode, InfixExpressionNode, NumberLiteralNode, BooleanLiteralNode],
                 context):
        self.context = context
        self.value = node

    def simplify(self):
        self.value = self.simplify_node(self.value)

    def simplify_node(self, node):
        if isinstance(node, UnaryExpressionNode):
            value = self.simplify_node(node.value)
            if isinstance(value, NumberLiteralNode):
                op = node.op
                inner_value = value.value
                if op == '-':
                    return NumberLiteralNode(-inner_value)
                elif op == '+':
                    return NumberLiteralNode(inner_value)
            elif isinstance(value, BooleanLiteralNode):
                op = node.op
                inner_value = value.value
                if op == '!':
                    return BooleanLiteralNode(not inner_value)
        elif isinstance(node, InfixExpressionNode):
            lhs = self.simplify_node(node.lhs)
            rhs = self.simplify_node(node.rhs)
            if isinstance(lhs, NumberLiteralNode) and isinstance(rhs, NumberLiteralNode):
                lhv = lhs.value
                rhv = rhs.value
                op = node.op
                if op == '+':
                    return NumberLiteralNode(lhv + rhv)
                elif op == '-':
                    return NumberLiteralNode(lhv - rhv)
                elif op == '*':
                    return NumberLiteralNode(lhv * rhv)
                elif op == '/':
                    return NumberLiteralNode(lhv / rhv)
                elif op == '**':
                    return NumberLiteralNode(lhv ** rhv)
                elif op == '==':
                    return BooleanLiteralNode(lhv == rhv)
                elif op == '!=':
                    return BooleanLiteralNode(lhv != rhv)
                elif op == '>=':
                    return BooleanLiteralNode(lhv >= rhv)
                elif op == '>':
                    return BooleanLiteralNode(lhv > rhv)
                elif op == '<=':
                    return BooleanLiteralNode(lhv <= rhv)
                elif op == '<':
                    return BooleanLiteralNode(lhv < rhv)
            elif isinstance(lhs, BooleanLiteralNode) and isinstance(rhs, BooleanLiteralNode):
                lhv = lhs.value
                rhv = rhs.value
                op = node.op
                if op == '&&':
                    return BooleanLiteralNode(lhv and rhv)
                elif op == '||':
                    return BooleanLiteralNode(lhv or rhv)
        elif isinstance(node, SimpleIdentifierNode) or isinstance(node, IdentifierNode):
            matches = self.context.find(node.text, ())
            if matches and isinstance(matches[0][1], Constant):
                return matches[0][1].resolve()
        return node
