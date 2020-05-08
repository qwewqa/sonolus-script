from __future__ import annotations

from typing import Set

from compile.context import *


class Compiler:
    def __init__(self, path):
        self.context = GlobalContext(path)
        self.context.get('test')
        self.nodes: Set[SNode] = set()
        self.entry_nodes = {}
        scripts = [s for s in self.context.find_all(signature=None) if isinstance(s, Script)]
        for s in scripts:
            self.process_script(s)
        return

    def process_script(self, script: Script):
        for c in script.callbacks:
            node = self.optimize_node(c.to_expression_body().to_node())
            self.add_node(node)
            self.entry_nodes[f'{script.identifier}.{c.identifier}'] = node

    def add_node(self, node: SNode):
        self.nodes.add(node)
        if hasattr(node, 'arguments'):
            for n in node.arguments:
                self.add_node(n)
        return node

    def map_indexes(self):
        return {node: i for i, node in enumerate(self.nodes)}

    def optimize_node(self, node: Union[FunctionSNode, ValueSNode]) -> Union[FunctionSNode, ValueSNode]:
        if isinstance(node, ValueSNode):
            return node
        op = node.name
        optimized = node
        if op == 'Execute':
            args = []
            for a in node.arguments:
                if isinstance(a, FunctionSNode) and a.name == 'Execute':
                    args.extend(a.arguments)
                else:
                    args.append(a)
            args = [self.optimize_node(a) for a in args]
            args = [a for a in args[:-1] if self.node_has_side_effects(a)] + [args[-1]]
            if len(args) == 1:
                optimized = args[0]
            else:
                optimized = FunctionSNode(
                    'Execute',
                    args
                )
        else:
            optimized = FunctionSNode(
                op,
                [self.optimize_node(a) for a in node.arguments]
            )

        if optimized == node:
            return optimized
        else:
            return self.optimize_node(optimized)

    def node_has_side_effects(self, node: Union[FunctionSNode, ValueSNode]) -> bool:
        if isinstance(node, ValueSNode):
            return False
        else:
            if node.name == 'Set':
                return True
            return any(self.node_has_side_effects(a) for a in node.arguments)


class SNode:
    def __init__(self):
        pass


class FunctionSNode(SNode):
    def __init__(self, name: str, arguments: List):
        super().__init__()
        self.name = name
        self.arguments = arguments

    def __eq__(self, other):
        return isinstance(other, FunctionSNode) and self.name == other.name and self.arguments == other.arguments

    def __hash__(self):
        return (self.name, tuple(self.arguments)).__hash__()

    def __repr__(self):
        return f'{self.name}: [{", ".join([a.__repr__() for a in self.arguments])}]'


class ValueSNode(SNode):
    def __init__(self, value: float):
        super().__init__()
        self.value = value

    def __eq__(self, other):
        return isinstance(other, ValueSNode) and self.value == other.value

    def __hash__(self):
        return self.value.__hash__()

    def __repr__(self):
        return f'Value: [{self.value}]'


from compile.declaration import *
