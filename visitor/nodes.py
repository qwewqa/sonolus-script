class ScriptFileNode:
    def __init__(self, imports, top_level_declarations):
        self.imports = imports
        self.top_level_declarations = top_level_declarations


class ImportHeaderNode:
    def __init__(self, identifier):
        self.identifier = identifier


class IdentifierNode:
    def __init__(self, value):
        self.value = [v.value for v in value]
        self.text = '.'.join(self.value)


class SimpleIdentifierNode:
    def __init__(self, value):
        self.value = value
        self.text = value


class ArchetypeDeclarationNode:
    def __init__(self, identifier, is_input, script, defaults):
        self.identifier = identifier
        self.script = script
        self.input = is_input
        self.defaults = defaults


class LevelvarDeclarationNode:
    def __init__(self, identifier):
        self.identifier = identifier


class ArchetypeDefault:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value


class ScriptDeclarationNode:
    def __init__(self, identifier, parameters, body):
        self.identifier = identifier
        self.parameters = parameters
        self.body = body


class StructDeclarationNode:
    def __init__(self, modifiers, identifier, fields, body):
        self.modifiers = modifiers
        self.identifier = identifier
        self.fields = fields
        self.body = body


class CallbackDeclarationNode:
    def __init__(self, order, identifier, body):
        self.order = order
        self.identifier = identifier
        self.body = body


class PropertyDeclarationNode:
    def __init__(self, modifiers, variant, identifier, expression, getter, setter):
        self.modifiers = modifiers
        self.variant = variant
        self.identifier = identifier
        self.expression = expression
        self.getter = getter
        self.setter = setter


class GetterNode:
    def __init__(self, modifiers, body):
        self.modifiers = modifiers
        self.body = body


class SetterNode:
    def __init__(self, modifiers, parameter_name, user_type, body):
        self.user_type = user_type
        self.modifiers = modifiers
        self.parameter_name = parameter_name
        self.body = body


class ConstantDeclarationNode:
    def __init__(self, modifiers, identifier, expression):
        self.modifiers = modifiers
        self.identifier = identifier
        self.expression = expression


class InfixExpressionNode:
    def __init__(self, lhs, op=None, rhs=None):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs


class UnaryExpressionNode:
    def __init__(self, value, op=None):
        self.value = value
        self.op = op


class FunctionCallNode:
    def __init__(self, arguments):
        self.arguments = arguments


class MemberAccessNode:
    def __init__(self, value):
        self.value = value


class ValueArgumentNode:
    def __init__(self, value, name=None):
        self.value = value
        self.name = name


class NumberLiteralNode:
    def __init__(self, value):
        self.value = value


class BooleanLiteralNode:
    def __init__(self, value):
        self.value = value


class IfExpressionNode:
    def __init__(self, condition, tbranch, fbranch):
        self.condition = condition
        self.tbranch = tbranch
        self.fbranch = fbranch


class WhileExpressionNode:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class FunctionDeclarationNode:
    def __init__(self, modifiers, receiver, identifier, parameters, body):
        self.modifiers = modifiers
        self.receiver = receiver
        self.identifier = identifier
        self.parameters = parameters
        self.body = body


class ParameterNode:
    def __init__(self, identifier, user_type):
        self.identifier = identifier
        self.user_type = user_type


class StructFieldNode:
    def __init__(self, is_const, identifier, user_type):
        self.is_const = is_const
        self.identifier = identifier
        self.user_type = user_type
