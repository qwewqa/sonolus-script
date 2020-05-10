from __future__ import annotations

import copy
from typing import Union, List, Optional, Dict

from compile.compile import *
from compile.constants import STD_FILENAMES, OPERATORS, BUILTINS
from compile.context import *
from visitor.nodes import *

Expression = Union[
    InfixExpressionNode, UnaryExpressionNode, NumberLiteralNode, BooleanLiteralNode, SimpleIdentifierNode]


class ScriptFile:
    def __init__(self, ast: ScriptFileNode, context: GlobalContext):
        self.global_context = context
        self.context = FileContext(context)
        self.imports = [i.identifier.value for i in ast.imports]

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
            elif isinstance(d, ArchetypeDeclarationNode):
                Archetype(d, self.context)
            elif isinstance(d, LevelvarDeclarationNode):
                Levelvar(d, self.context)
            else:
                raise RuntimeError('Unexpected tld')

    def process_imports(self):
        for f in STD_FILENAMES:
            self.context.import_script(self.global_context.get(f))

        for i in self.imports:
            self.context.import_script(self.global_context.get(i))


class Constant:
    def __init__(self, node: ConstantDeclarationNode, context):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value
        self.expression = ConstantExpression(node.expression, context)
        self.resolving = False
        self._type = None
        self._value = None
        context.add(self.identifier, None, self)

    @property
    def value(self):
        if not self._value:
            self.resolve()
        return self._value

    @property
    def type(self):
        if not self._type:
            self.resolve()
        return self._type

    def to_literal_node(self):
        if self.type == 'Number':
            return NumberLiteralNode(self.value)
        elif self.type == 'Boolean':
            return BooleanLiteralNode(self.value)

    def resolve(self):
        if self.resolving:
            raise RuntimeError('Failed to resolve constant (possible circular dependency)')
        self.resolving = True
        self.expression.simplify()
        self.resolving = False
        if isinstance(self.expression.value, NumberLiteralNode):
            self._type = 'Number'
            self._value = self.expression.value.value
            return self.expression.value
        elif isinstance(self.expression.value, BooleanLiteralNode):
            self._type = 'Boolean'
            self._value = self.expression.value.value
            return self.expression.value
        else:
            raise RuntimeError('Failed to resolve constant')


class Function:
    def __init__(self, node: FunctionDeclarationNode, context: Context, default_receiver: Optional[Struct] = None):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value

        if node.receiver:
            self.identifier = f'{node.receiver.value}.{self.identifier}'

        if node.receiver:
            self.receiver = FunctionParameter('this', node.receiver.value, self.context)
        elif default_receiver:
            self.receiver = FunctionParameter('this', default_receiver.identifier, self.context)
        else:
            self.receiver = None

        self.parameters = [FunctionParameter(p.identifier.value, p.user_type, self.context) for p in node.parameters]

        if self.receiver:
            self.full_parameters = [self.receiver] + self.parameters
            self.unresolved_signature = (self.receiver.type_string,) + tuple(p.type_string for p in self.parameters)
        else:
            self.full_parameters = self.parameters
            self.unresolved_signature = tuple(p.type_string for p in self.parameters)

        self.body = FunctionBody(node.body, context)

        self._signature = None

        context.add(self.identifier, self.unresolved_signature, self)

    @property
    def signature(self):
        if self._signature:
            return self._signature
        else:
            self._signature = tuple(self.context.find(n, None) for n in self.unresolved_signature)
            if any(not isinstance(s, Struct) for s in self._signature):
                raise RuntimeError('Error resolving signature')
            return self._signature

    def call(self, arguments):
        return self.body.call(self.full_parameters, arguments)


class Property:
    def __init__(self, node: PropertyDeclarationNode, context: Context):
        self.context = context
        self.modifiers = node.modifiers
        self.identifier = node.identifier.value
        self.variant = node.variant
        self.expression = node.expression
        self.getter = Getter(node.getter, self.context) if node.getter else None
        self.setter = Setter(node.setter, self.context) if node.setter else None
        self._value = None
        self._initializer = None

        if 'inline' in self.modifiers:
            if self.getter or self.setter or not self.expression:
                raise RuntimeError
            if self.variant in ('val', 'var'):
                self.getter = Getter(GetterNode([], [self.expression]), self.context)
            if self.variant in ('pit', 'var'):
                self.setter = Setter(
                    SetterNode([], SimpleIdentifierNode('value'), SimpleIdentifierNode('Any'),
                               [InfixExpressionNode(self.expression, '=', SimpleIdentifierNode('value'))]),
                    self.context)
            self.inline = True
        else:
            self.inline = False

        try:
            if 'shared' in self.modifiers:
                self.allocator = self.context.shared_allocator
            else:
                self.allocator = self.context.allocator
        except AttributeError:
            self.allocator = None

        if 'spawninit' in self.modifiers:
            if self.expression:
                raise RuntimeError
            self._value = RawValue(self.allocator.allocate())
        else:
            if self.variant == 'var':
                if not self.expression and not (self.getter and self.setter):
                    raise RuntimeError('Property var has no expression and lacks a getter or setter')
            elif self.variant == 'val':
                if not self.expression and not self.getter:
                    raise RuntimeError('Property val has no expression and lacks a getter')
            elif self.variant == 'pit':
                if not self.expression and not self.setter:
                    raise RuntimeError('Property pit has no expression and lacks a setter')

        self.context.add(self.identifier, None, self)

    def initialization_expression(self):
        return (self.initializer and InfixExpressionNode(self, '=', self.initializer)) or None

    @property
    def initializer(self):
        if self.value:
            return self._initializer
        else:
            return None

    def with_receiver(self, receiver):
        return PropertyWithReceiver(self, receiver)

    @property
    def value(self):
        if self._value:
            return self._value
        if self.expression and not self.inline:
            self._initializer = ExpressionBody([self.expression], self.context)
            if self._initializer.returns:
                self._value = self._initializer.returns.type.allocate_value_on(self.allocator)
        return self._value

    def get_getter(self, receiver=None):
        if self.getter:
            return self.getter.call(self.value, receiver)
        else:
            return self.value

    def get_setter(self):
        if self.setter:
            return None
        else:
            return self.value

    def call_setter(self, arg, receiver=None):
        if self.setter:
            return self.setter.call(arg, self.value, receiver)
        return None


class PropertyWithReceiver:
    def __init__(self, property: Property, receiver: StructConstruction):
        self.property = property
        self.receiver = receiver
        self.context = property.context
        self.modifiers = property.modifiers
        self.identifier = property.identifier
        self.variant = property.variant
        self.expression = property.expression
        self.getter = property.getter
        self.setter = property.setter

    def initialization_expression(self):
        return self.property.initialization_expression()

    @property
    def initializer(self):
        return self.property.initializer

    def with_receiver(self, receiver):
        return PropertyWithReceiver(self.property, receiver)

    @property
    def value(self):
        return self.property.value

    def get_getter(self, receiver=None):
        return self.property.get_getter(self.receiver)

    def get_setter(self):
        return self.property.get_setter()

    def call_setter(self, arg, receiver=None):
        return self.property.call_setter(arg, self.receiver)


class ScriptSpawn:
    def __init__(self, script: Script, arguments, context: Context):
        self.context = context
        self.script = script
        self.arguments = arguments

    def to_node(self):
        args = [RawValue(self.script.index, self.context)]
        block = []
        for arg in self.arguments:
            if isinstance(arg, ExpressionBody):
                ret = arg.returns
                block.append(arg)
            elif isinstance(arg, MemberAccess):
                ret = arg.resolve()
                block.append(arg)
            else:
                ret = arg

            if isinstance(ret, StructConstruction):
                if not (ret.type.identifier == 'Number' or ret.type.identifier == 'Boolean'):
                    raise RuntimeError
            elif not isinstance(ret, (RawValue, BuiltinFunctionCall)):
                raise RuntimeError
            args.append(ret)
        block.append(BuiltinFunctionCall('Spawn', 'None', args, self.context))
        return ExpressionBody(block, self.context).to_node()


class Getter:
    def __init__(self, node: GetterNode, context: Context):
        self.context = context
        self.modifiers = node.modifiers
        self.body = FunctionBody(node.body, context)

    def call(self, field: Optional[StructConstruction], receiver: Optional[StructConstruction]):
        params = []
        args = []
        if field:
            params.append(FunctionParameter('field', field.type.identifier, self.context))
            args.append(field)
        if receiver:
            params.append(FunctionParameter('this', receiver.type.identifier, self.context))
            args.append(receiver)
        return self.body.call(params, args)


class Setter:
    def __init__(self, node: SetterNode, context: Context):
        self.context = context
        self.modifiers = node.modifiers
        self.user_type = node.user_type.value
        self.parameter_name = node.parameter_name.value
        self.body = FunctionBody(node.body, context)

    def call(self, arg, field: Optional[StructConstruction], receiver: StructConstruction):
        params = [FunctionParameter(self.parameter_name, self.user_type, self.context)]
        args = [arg]
        if field:
            params.append(FunctionParameter('field', field.type.identifier, self.context))
            args.append(field)
        if receiver:
            params.append(FunctionParameter('this', receiver.type.identifier, self.context))
            args.append(receiver)
        return self.body.call(params, args)


class Struct:
    def __init__(self, node: StructDeclarationNode, context: Context):
        self.context = StructContext(context)
        self.identifier = node.identifier.value
        self.fields = [FunctionParameter(f.identifier.value, f.user_type, self.context) for f in node.fields]

        self._signature = None

        for d in node.body:
            if isinstance(d, ConstantDeclarationNode):
                Constant(d, self.context)
            elif isinstance(d, FunctionDeclarationNode):
                Function(d, self.context, default_receiver=self)
            elif isinstance(d, PropertyDeclarationNode):
                Property(d, self.context)

        context.add(self.identifier, None, self)

    def allocate_value_on(self, allocator: BlockAllocator):
        return StructConstruction(self, [(f.type.allocate_value_on(
            allocator) if f.type.identifier != 'Raw' else RawValue(allocator.allocate())) for f in self.fields],
                                  self.context)

    @property
    def signature(self):
        if self._signature:
            return self._signature
        self._signature = tuple(f.type for f in self.fields)
        return self._signature


class Archetype:
    def __init__(self, node: ArchetypeDeclarationNode, context: FileContext):
        self.context = context
        self.identifier = node.identifier.value
        self.script_identifier = node.script.value
        self.input = node.input
        self._script = None
        self.defaults = {d.identifier.value: float(d.value.value) for d in node.defaults}
        context.add_global(self.identifier, None, self)

    @property
    def script(self):
        if self._script:
            return self._script
        self._script = self.context.find(self.script_identifier, None)
        return self._script

    def to_dict(self, mapping):
        return {'script': mapping[self.script], 'input': self.input}

    def to_entity_dict(self, arguments, archetype_mappings):
        args = {}
        args.update(self.defaults)
        args.update(arguments)
        data = [0] * 32
        for a, v in args.items():
            data[self.script.parameter_indexes[a]] = v
        while data and data[-1] == 0:
            data.pop()
        return {
            'archetype': archetype_mappings[self],
            'data': {
                'index': 0,
                'values': data
            }
        } if data else {'archetype': archetype_mappings[self]}


class Levelvar:
    def __init__(self, node: LevelvarDeclarationNode, context: FileContext):
        self.context = context
        self.identifier = node.identifier.value
        self.value = RawValue(context.level_allocator.allocate())

        context.add(self.identifier, None, self.value)


class Script:
    def __init__(self, node: ScriptDeclarationNode, context: FileContext):
        self.context = ScriptContext(context)
        self.identifier = node.identifier.value
        self.callbacks = []
        self.initialize_properties = []
        self.parameters = {}
        self.index = None

        for p in node.parameters:
            param_name = p.value
            allocation = RawValue(self.context.entity_data.allocate())
            self.context.add(param_name, None, allocation)
            self.parameters[param_name] = allocation

        for d in node.body:
            if isinstance(d, ConstantDeclarationNode):
                Constant(d, self.context)
            elif isinstance(d, FunctionDeclarationNode):
                Function(d, self.context)
            elif isinstance(d, PropertyDeclarationNode):
                p = Property(d, self.context)
                if p.expression and not p.inline:
                    self.initialize_properties.append(p)
            elif isinstance(d, CallbackDeclarationNode):
                self.callbacks.append(Callback(d, self.context))

        if not any(c.identifier == 'initialize' for c in self.callbacks):
            self.callbacks.append(Callback.empty('initialize', self.context))

        next(c for c in self.callbacks if
             c.identifier == 'initialize').add_initialize_properties(self.initialize_properties)

        self.parameter_indexes = {n: p.allocation.index for n, p in self.parameters.items()}
        self.parameter_indexes.update({n[1:]: p.allocation.index for n, p in self.parameters.items()})

        context.add_global(self.identifier, None, self)

    def to_dict(self, mapping):
        return {c.identifier: {'index': mapping[c.entry_node], 'order': c.order} for c in self.callbacks}


class Callback:
    def __init__(self, node: CallbackDeclarationNode, context: Context):
        self.context = CallbackContext(context)
        self.identifier = node.identifier.value
        self._order = ConstantExpression(node.order, self.context) if node.order else 0
        self.body = FunctionBody(node.body, self.context, False)
        self.entry_node = None

    @property
    def order(self):
        if isinstance(self._order, ConstantExpression):
            self._order.simplify()
            self._order = self._order.value.value
        return self._order

    @staticmethod
    def empty(name: str, context: Context):
        return Callback(CallbackDeclarationNode(0, SimpleIdentifierNode(name), []), context)

    def add_initialize_properties(self, properties):
        self.body.initialize_properties = properties + self.body.initialize_properties

    def to_expression_body(self):
        return self.body.to_expression_body()


class FunctionBody:
    def __init__(self, block, context, create_child_context=True):
        if create_child_context:
            self.context = FunctionContext(context)
        else:
            self.context = context
        self.block = block
        self.expressions = []
        self.initialize_properties = []

        for s in block:
            if isinstance(s, FunctionDeclarationNode):
                Function(s, self.context)
            elif isinstance(s, StructDeclarationNode):
                Struct(s, self.context)
            elif isinstance(s, ConstantDeclarationNode):
                Constant(s, self.context)
            elif isinstance(s, PropertyDeclarationNode):
                p = Property(s, self.context)
                if p.expression and not p.inline:
                    self.initialize_properties.append(p)
            else:
                # this includes properties, since the assignment is done in order as part of the block
                self.expressions.append(s)

    def to_expression_body(self):
        while self.initialize_properties:
            self.expressions = [self.initialize_properties.pop().initialization_expression()] + self.expressions
        return ExpressionBody(self.expressions, self.context)

    def call(self, parameters: List[FunctionParameter],
             arguments: List[Union[RawValue, StructConstruction, ExpressionBody, MemberAccess]]):
        context = FunctionInvocationContext(self.context)
        pre_block = []
        for arg, p in zip(arguments, parameters):  # TODO: Type check
            while isinstance(arg, (ExpressionBody, MemberAccess)):
                if isinstance(arg, ExpressionBody):
                    pre_block.append(arg)
                    arg = arg.returns
                elif isinstance(arg, MemberAccess):
                    pre_block.append(arg)
                    arg = arg.resolve()
            context.add(p.name, None, arg)
        return ExpressionBody(pre_block + self.block, context)


DEFAULT_TYPE = 'Number'


class FunctionParameter:
    def __init__(self, name, user_type, context):
        self.context = context
        self.name = name
        self.type_string = user_type
        if isinstance(user_type, SimpleIdentifierNode):
            self.type_string = user_type.value
        self._type = None
        if not self.type_string:
            self.type_string = DEFAULT_TYPE

    @property
    def type(self):
        if self._type:
            return self._type
        self._type = self.context.find(self.type_string, None)
        if not isinstance(self._type, Struct):
            raise RuntimeError('Type')
        return self._type


class ConstantExpression:
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
        elif isinstance(node, SimpleIdentifierNode):
            match = self.context.find(node.value, None)
            if match:
                return match.to_literal_node()
        return node


class ExpressionBody:
    def __init__(self, block, context: Context):
        self.context = context
        self.block = block
        if not isinstance(self.block, list):
            self.block = [self.block]
        self.number = self.context.find('Number', None)
        self.boolean = self.context.find('Boolean', None)
        self.raw = self.context.find('Raw', None)
        self.expressions = [self.resolve_expression(e) for e in self.block]
        self.returns = None
        final = self.expressions[-1] if self.expressions else None
        if isinstance(final, StructConstruction):
            self.returns = final
            self.type = self.returns.type
        elif isinstance(final, ExpressionBody):
            self.returns = final.returns
            self.type = final.type
        elif isinstance(final, MemberAccess):
            self.returns = final
            self.type = final.type
        else:
            self.returns = None
            self.type = None

    def resolve_expression(self, expression) -> Union[StructConstruction,
                                                      BuiltinFunctionCall, ExpressionBody, Assignment,
                                                      IfExpression, MemberAccess, Struct, RawValue]:
        if isinstance(expression, NumberLiteralNode):
            return StructConstruction(self.number, [RawValue(expression.value, self.context)], self.context)
        elif isinstance(expression, BooleanLiteralNode):
            return StructConstruction(self.boolean, [RawValue(expression.value, self.context)], self.context)
        elif isinstance(expression, SimpleIdentifierNode):
            e = self.context.find(expression.value, None)
            this = self.context.find('this', None)
            this_find_result = isinstance(this, StructConstruction) and this.find(expression.value)
            if not e and this_find_result:
                e = this_find_result
            if isinstance(e, Property):
                e = e.with_receiver(this)
            return self.resolve_expression(e)
        elif isinstance(expression, Constant):
            return StructConstruction(self.context.find(expression.type),
                                      [RawValue(expression.value, self.context, None)], self.context)
        elif isinstance(expression, RawValue):
            return StructConstruction(self.raw, [expression], self.context)
        elif isinstance(expression, InfixExpressionNode):
            opname = OPERATORS.get(expression.op, expression.op)

            if opname == '=':
                lhs = expression.lhs
                rhs = self.resolve_expression(expression.rhs)
                if isinstance(lhs, SimpleIdentifierNode):
                    this = self.context.find('this', None)
                    this_find_result = isinstance(this, StructConstruction) and this.find(lhs.value)
                    if this_find_result:
                        lhs = this_find_result
                    else:
                        lhs = self.context.find(lhs.value, None)
                if isinstance(lhs, UnaryExpressionNode):
                    lhs = self.resolve_expression(lhs)
                if not isinstance(lhs, (Property, StructConstruction)):
                    raise RuntimeError('Can\'t assign')
                return Assignment(lhs, rhs)

            lhs = self.resolve_expression(expression.lhs)
            rhs = self.resolve_expression(expression.rhs)

            ops = ([lhs.type.context.find(opname, (lhs.type.identifier, rhs.type.identifier))] +
                   self.context.find_all(f'{lhs.type.identifier}.{opname}', (lhs.type.identifier, rhs.type.identifier)))

            op = next(f for f in ops if f and f.signature == (lhs.type, rhs.type) and 'operator' in f.modifiers)
            if not op:
                raise RuntimeError('Failed to find a matching function')

            return op.call([lhs, rhs])
        elif isinstance(expression, UnaryExpressionNode):
            value = expression.value
            op = expression.op

            if isinstance(op, list):  # Normal function call
                if isinstance(value, UnaryExpressionNode):
                    value = self.resolve_expression(value)

                arguments = [self.resolve_expression(a) for a in op]

                if isinstance(value, MemberAccess):
                    try:
                        sig_str = tuple(a.type.identifier for a in arguments)
                    except AttributeError:
                        raise RuntimeError
                    try:
                        sig = tuple(a.type for a in arguments)
                    except AttributeError:
                        raise RuntimeError

                    fun = value.resolve_with_receiver(sig_str, sig)
                    if not fun:
                        raise RuntimeError
                    return fun.call([value.receiver] + arguments)
                elif isinstance(value, SimpleIdentifierNode) and isinstance(self.context.find(value.value), Script):
                    return ScriptSpawn(self.context.find(value.value), arguments, self.context)
                else:
                    fun_identifier = value.value

                    if fun_identifier in BUILTINS:
                        return BuiltinFunctionCall(fun_identifier, self.raw, arguments, self.context)

                    try:
                        sig_str = tuple('Raw' if isinstance(a, RawValue) else a.type.identifier for a in arguments)
                    except AttributeError:
                        raise RuntimeError
                    try:
                        sig = tuple(self.raw if isinstance(a, RawValue) else a.type for a in arguments)
                    except AttributeError:
                        raise RuntimeError

                    struct = next((s for s in self.context.find_all(fun_identifier, None) if isinstance(s, Struct)),
                                  None)
                    if struct and struct.signature == sig:
                        return StructConstruction(struct, arguments, self.context)

                    fun = next((f for f in self.context.find_all(fun_identifier, sig_str) if
                                isinstance(f, Function) and f.signature == sig), None)
                    if not fun:
                        raise RuntimeError
                    return fun.call(arguments)
            elif isinstance(op, MemberAccessNode):
                value = self.resolve_expression(value)
                return MemberAccess(value, op.value.value, self.context)
            elif isinstance(op, str):  # TODO postfix
                opname = OPERATORS[f'b{expression.op}']
                value = self.resolve_expression(expression.value)

                ops = ([value.type.context.find(opname, (value.type.identifier,))] +
                       self.context.find_all(f'{value.type.identifier}.{opname}', (value.type.identifier,)))

                op = next(f for f in ops if f and f.signature == (value.type,) and 'operator' in f.modifiers)
                if not op:
                    raise RuntimeError('Failed to find a matching function')

                return op.call([value])
            else:
                raise NotImplementedError
        elif isinstance(expression, (Property, PropertyWithReceiver)):
            return expression.get_getter()
        elif isinstance(expression, Allocation):
            return StructConstruction(self.number, [RawValue(expression)], self.context)
        elif isinstance(expression, IfExpressionNode):
            condition = ExpressionBody(expression.condition, self.context)
            tbranch = ExpressionBody(expression.tbranch, self.context)
            if expression.fbranch:
                fbranch = ExpressionBody(expression.fbranch, self.context)
            else:
                fbranch = None
            return IfExpression(condition, tbranch, fbranch)
        elif isinstance(expression, StructConstruction):
            return expression
        elif isinstance(expression, ExpressionBody):
            return expression
        elif isinstance(expression, MemberAccess):
            return expression
        elif isinstance(expression, Struct):
            return expression
        elif isinstance(expression, RawValue):
            return expression
        elif isinstance(expression, BuiltinFunctionCall):
            return expression
        raise RuntimeError

    def to_node(self):
        args = [e.to_node() for e in self.expressions]
        args = [arg for arg in args if arg]
        return FunctionSNode(
            'Execute',
            args
        ) if args else ValueSNode(0)


class Assignment:
    def __init__(self, lhs: Union[Property, RawValue, StructConstruction],
                 rhs: Union[RawValue, StructConstruction, ExpressionBody, BuiltinFunctionCall, MemberAccess]):
        self.lhs = lhs
        self.rhs = rhs

    def to_node(self):
        if isinstance(self.lhs, Property):
            setter = self.lhs.call_setter(self.rhs)
            if setter:
                return setter.to_node()
            else:
                return Assignment(self.lhs.get_setter(), self.rhs).to_node()
        elif isinstance(self.lhs, RawValue):
            if isinstance(self.rhs, RawValue):
                return FunctionSNode(
                    'Set',
                    [
                        ValueSNode(self.lhs.allocation.block_id),
                        ValueSNode(self.lhs.allocation.index),
                        self.rhs.to_node()
                    ]
                )
            elif isinstance(self.rhs, StructConstruction):
                if self.rhs.type in ('Number', 'Boolean', 'Raw'):
                    return Assignment(self.lhs, self.rhs.arguments[0])
            elif isinstance(self.rhs, ExpressionBody):
                return FunctionSNode(
                    'Execute',
                    [self.rhs.to_node(),
                     Assignment(self.lhs, self.rhs.returns).to_node()
                     ]
                )
            elif isinstance(self.rhs, BuiltinFunctionCall):
                return FunctionSNode(
                    'Set',
                    [
                        ValueSNode(self.lhs.allocation.block_id),
                        ValueSNode(self.lhs.allocation.index),
                        self.rhs.to_node()
                    ]
                )
        elif isinstance(self.lhs, StructConstruction):
            if isinstance(self.rhs, RawValue):
                if self.lhs.type.identifier == 'Raw':
                    return Assignment(self.lhs.arguments[0], self.rhs).to_node()
                else:
                    raise RuntimeError
            elif isinstance(self.rhs, MemberAccess):
                return Assignment(self.lhs, self.rhs.resolve()).to_node()
            elif isinstance(self.rhs, ExpressionBody):
                return FunctionSNode(
                    'Execute',
                    [self.rhs.to_node(),
                     Assignment(self.lhs, self.rhs.returns).to_node()
                     ]
                )
            elif isinstance(self.rhs, StructConstruction):
                if self.lhs.type != self.rhs.type:
                    raise RuntimeError
                return FunctionSNode(
                    'Execute',
                    [Assignment(a, b).to_node() for a, b in zip(self.lhs.arguments, self.rhs.arguments)]
                )
        raise RuntimeError


class MemberAccess:
    def __init__(self, receiver: Union[Property, PropertyWithReceiver, MemberAccess, ExpressionBody, Struct, StructConstruction], name, context):
        self.context = context
        self.receiver = receiver
        self.name = name
        if isinstance(self.receiver, (Property, PropertyWithReceiver)):
            self.receiver = self.receiver.get_getter()
        if isinstance(self.receiver, Struct):
            self.receiver_type = self.receiver
        else:
            self.receiver_type = self.receiver.type

    @property
    def type(self):
        r = self.resolve()
        if isinstance(r, Struct):
            return r
        else:
            return r.type

    def resolve(self, signature=None):
        if signature is None and isinstance(self.receiver, StructConstruction) and self.receiver.find(self.name):
            r = self.receiver.find(self.name)
            if isinstance(r, (PropertyWithReceiver, Property)):
                return r.with_receiver(self.receiver).get_getter()
            else:
                return r
        r = self.receiver_type.context.find_direct(self.name, signature)
        if isinstance(r, (PropertyWithReceiver, Property)):
            return r.with_receiver(self.receiver).get_getter()
        else:
            return r

    def resolve_with_receiver(self, partial_signature, partial_resolved_signature):
        f = self.resolve((self.receiver_type.identifier,) + partial_signature)
        return f if f and f.signature == (self.receiver_type,) + partial_resolved_signature else None

    def to_node(self):
        if isinstance(self.receiver, (MemberAccess, ExpressionBody)):
            return FunctionSNode(
                'Execute',
                [self.receiver.to_node(), self.resolve().to_node()]
            )
        else:
            return FunctionSNode(
                'Execute',
                [self.resolve().to_node()]
            )


class BuiltinFunctionCall:
    def __init__(self, name, user_type, arguments: List[BuiltinFunctionCall, RawValue, StructConstruction],
                 context: Context):
        self.context = context
        self.name = name
        self.type = user_type
        self.arguments = arguments

    def to_node(self):
        return FunctionSNode(
            self.name,
            [a.to_node() for a in self.arguments]
        )


class IfExpression:
    def __init__(self, condition: ExpressionBody, tbranch: ExpressionBody, fbranch: Optional[ExpressionBody]):
        self.condition = condition
        self.tbranch = tbranch
        self.fbranch = fbranch
        if not self.condition.type or self.condition.type.identifier != 'Boolean':
            raise RuntimeError

    def to_node(self):
        if self.fbranch:
            return FunctionSNode(
                'Execute',
                [self.condition.to_node(),
                 FunctionSNode(
                     'If',
                     [self.condition.returns.to_node(), self.tbranch.to_node(), self.fbranch.to_node()]
                 )
                 ]
            )
        else:
            return FunctionSNode(
                'Execute',
                [self.condition.to_node(),
                 FunctionSNode(
                     'And',
                     [self.condition.returns.to_node(), self.tbranch.to_node()]
                 )
                 ]
            )


class StructConstruction:
    def __init__(self, struct: Struct, arguments: List[Union[RawValue, BuiltinFunctionCall, StructConstruction]],
                 context: Context):
        self.context = context
        self.arguments = arguments
        self.type = struct
        self.fields = {f.name: a for f, a in zip(self.type.fields, self.arguments)}
        self.field_metadata: Dict[str, FunctionParameter] = {f.name: f for f in self.type.fields}

        for f, a in zip(self.type.fields, self.arguments):
            if f.type.identifier == 'Raw' and isinstance(a, StructConstruction) and a.type.identifier != 'Raw':
                raise RuntimeError
            if f.type.identifier != 'Raw' and f.type != a.type:
                raise RuntimeError

    def find(self, name):
        return self.fields.get(name)

    def to_node(self):
        if len(self.arguments) != 1:
            return None
        else:
            return self.arguments[0].to_node()


class RawValue:
    def __init__(self, value, context: Optional[Context] = None, allocator: Optional[BlockAllocator] = None):
        if isinstance(value, Allocation):
            self.allocation = value
            self.context = None
            self.value = None
            return
        self.context = context
        self.value = value
        self.allocation = None
        if allocator:
            self.allocator = allocator
        else:
            try:
                self.allocator = self.context.allocator
            except AttributeError:
                self.allocator = None

    def allocate(self):
        if self.allocation:
            return
        self.allocation = self.allocator.allocate()

    def to_node(self):
        return FunctionSNode(
            'Get',
            [
                ValueSNode(self.allocation.block_id),
                ValueSNode(self.allocation.index)
            ]
        ) if self.allocation else ValueSNode(
            self.value
        )
