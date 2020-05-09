from __future__ import annotations

from collections import defaultdict
from typing import Set

from compile.context import *
from yaml import load
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper
import pathlib
import json
import os


class Compiler:
    def __init__(self, engine_path):
        search_path = pathlib.Path(engine_path).parent
        engine_def = load(open(engine_path, 'r'), Loader=Loader)

        self.context = GlobalContext(search_path)
        includes = engine_def['include']
        options = engine_def['options']
        level = engine_def['level']
        configuration = engine_def['configuration']

        for f in includes:
            self.context.get(f)

        self.nodes = set()
        self.entry_nodes = defaultdict(lambda: {})
        self.archetypes = {a.identifier: a for a in self.context.find_all(signature=None) if isinstance(a, Archetype)}
        self.scripts = list(set(a.script for a in self.archetypes.values()))
        for s in self.scripts:
            self.process_script(s)
        self.node_mappings = {n: i for i, n in enumerate(self.nodes)}
        self.script_mappings = {s: i for i, s in enumerate(self.scripts)}
        self.archetype_mappings = {a: i for i, a in enumerate(self.archetypes.values())}
        self.nodes_out = [n.to_dict(self.node_mappings) for n in self.nodes]
        self.archetypes_out = [a.to_dict(self.script_mappings) for a in self.archetypes.values()]
        self.scripts_out = [s.to_dict(self.node_mappings) for s in self.scripts]
        self.entities_out = []
        with open(os.path.join(search_path, level), 'r') as level_file:
            for l in level_file:
                s = l.split('(')
                arch = s[0]
                rargs = s[1]
                rargs = rargs.split(')')[0]
                rargs = rargs.split(',')
                args = {}
                for a in rargs:
                    if not a:
                        continue
                    s = a.split('=')
                    args[s[0].strip()] = float(s[1])
                self.entities_out.append(self.archetypes[arch].to_entity_dict(args, self.archetype_mappings))
        with open(os.path.join(search_path, 'options.json'), 'w') as options_file:
            json.dump(options, options_file)
        with open(os.path.join(search_path, 'level.json'), 'w') as level_file:
            json.dump({
                'configuration': configuration,
                'entities' : self.entities_out,
                'archetypes': self.archetypes_out,
                'scripts': self.scripts_out,
                'nodes': self.nodes_out
            }, level_file)


    def process_script(self, script: Script):
        for c in script.callbacks:
            node = self.optimize_node(c.to_expression_body().to_node())
            self.add_node(node)
            c.entry_node = node

    def add_node(self, node: SNode):
        self.nodes.add(node)
        if hasattr(node, 'arguments'):
            for n in node.arguments:
                self.add_node(n)
        return node

    def optimize_node(self, node: Union[FunctionSNode, ValueSNode]) -> Union[FunctionSNode, ValueSNode]:
        if isinstance(node, ValueSNode):
            return node
        op = node.name
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

    def to_dict(self, mappings):
        return {'func': self.name, 'args': [mappings[a] for a in self.arguments]}


class ValueSNode(SNode):
    def __init__(self, value: float):
        super().__init__()
        if isinstance(value, bool):
            self.value = 1 if value else 0
        else:
            self.value = value

    def __eq__(self, other):
        return isinstance(other, ValueSNode) and self.value == other.value

    def __hash__(self):
        return self.value.__hash__()

    def __repr__(self):
        return f'Value: [{self.value}]'

    def to_dict(self, mappings):
        return {'value': self.value}


from compile.declaration import *
