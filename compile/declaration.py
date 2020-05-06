from typing import Union

from compile.constants import STD_FILENAMES
from compile.context import *
from visitor.nodes import *


class ScriptFile:
    def __init__(self, ast: ScriptFileNode, context: GlobalContext, import_std=True):
        self.global_context = context
        self.context = context.new_file_context()

        if import_std:
            for f in STD_FILENAMES:
                self.context.import_script(self.global_context.get(f))

        for i in ast.imports:
            self.context.import_script(self.global_context.get(i.identifier.value))

        for d in ast.top_level_declarations:
            if isinstance(d, ConstantDeclarationNode):
                Constant(d, self.context)
            elif isinstance(d, FunctionDeclarationNode):
                Function(d, self.context)
            elif isinstance(d, PropertyDeclarationNode):
                Property(d, self.context)
            elif isinstance(d, StructDeclarationNode):
                Struct(d, self.context)
            elif isinstance(d, ScriptDeclarationNode):
                Script(d, self.context)

        return


class Constant:
    def __init__(self, node: ConstantDeclarationNode, context):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value
        self.expression = Expression(node.expression, context)
        self.resolving = False
        self.type = None
        self.value = None
        context.add(self.identifier, None, self)

    def resolve(self):
        if self.resolving:
            raise RuntimeError('Failed to resolve constant (possible circular dependency)')
        self.resolving = True
        self.expression.simplify()
        self.resolving = False
        if isinstance(self.expression.value, NumberLiteralNode):
            self.type = 'Number'
            self.value = self.expression.value.value
            return self.expression.value
        elif isinstance(self.expression.value, BooleanLiteralNode):
            self.type = 'Boolean'
            self.value = self.expression.value.value
            return self.expression.value
        else:
            raise RuntimeError('Failed to resolve constant')


class Function:
    def __init__(self, node: FunctionDeclarationNode, context: Context):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value

        if node.receiver:
            self.receiver = FunctionParameter('this', node.receiver.value)
        else:
            self.receiver = None

        self.parameters = [FunctionParameter(p.identifier.value, p.user_type) for p in node.parameters]

        if self.receiver:
            self.full_parameters = [self.receiver] + self.parameters
            self.signature = (self.receiver.type,) + tuple(p.type for p in self.parameters)
        else:
            self.full_parameters = self.parameters
            self.signature = tuple(p.type for p in self.parameters)

        self.body = FunctionBody(node.body)

        context.add(self.identifier, self.signature, self)


class Property:
    def __init__(self, node: PropertyDeclarationNode, context: Context):
        self.context = context
        self.variant = node.variant
        self.expression = node.expression
        self.getter = node.getter
        self.setter = node.setter

        if self.variant == 'var':
            if not self.expression and not (self.getter and self.setter):
                raise RuntimeError('Property var has no expression and lacks a getter or setter')
        elif self.variant == 'val':
            if not self.expression and not self.getter:
                raise RuntimeError('Property val has no expression and lacks a getter')
        elif self.variant == 'pit':
            if not self.expression and not self.setter:
                raise RuntimeError('Property pit has no expression and lacks a setter')


class Getter:
    def __init__(self, node: GetterNode, context: Context):
        self.modifiers = node.modifiers
        self.body = FunctionBody(node.body)


class Setter:
    def __init__(self, node: SetterNode, context: Context):
        self.modifiers = node.modifiers
        self.parameter_name = node.parameter_name.value
        self.body = FunctionBody(node.body)


class Struct:
    def __init__(self, node: StructDeclarationNode, context: FileContext):
        self.context = context.new_struct_context()
        self.identifier = node.identifier.value
        self.fields = node.fields

        for d in node.body:
            if isinstance(d, ConstantDeclarationNode):
                Constant(d, self.context)
            elif isinstance(d, FunctionDeclarationNode):
                Function(d, self.context)
            elif isinstance(d, PropertyDeclarationNode):
                Property(d, self.context)

        context.add(self.identifier, None, self)


class Script:
    def __init__(self, node: ScriptDeclarationNode, context: FileContext):
        self.context = context.new_script_context()
        self.identifier = node.identifier.value
        self.parameters = {}

        for p in node.parameters:
            param_name = p.value
            allocation = self.context.entity_data.allocate()
            self.context.add(param_name, None, allocation)
            self.parameters[param_name] = allocation

        for d in node.body:
            if isinstance(d, ConstantDeclarationNode):
                Constant(d, self.context)
            elif isinstance(d, FunctionDeclarationNode):
                Function(d, self.context)
            elif isinstance(d, PropertyDeclarationNode):
                Property(d, self.context)

        context.add(self.identifier, None, self)


class FunctionBody:
    def __init__(self, block):
        self.block = block


DEFAULT_TYPE = 'Number'


class FunctionParameter:
    def __init__(self, name, user_type):
        self.name = name
        self.type = user_type
        if not self.type:
            self.type = DEFAULT_TYPE


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
            matches = self.context.find(node.text, None)
            if matches and isinstance(matches[0], Constant):
                return matches[0].resolve()
        return node
