from __future__ import annotations

import os
import os.path
import pathlib
from typing import Optional

from antlr4 import *

from compile.constants import STD_FILENAMES
from grammar.ScriptLexer import ScriptLexer
from grammar.ScriptParser import ScriptParser
from visitor.visitor import ScriptVisitor


class Context:
    def __init__(self, parent: Optional[Context] = None):
        self.parent = parent
        self.symbols = {}
        self.native_symbols = {}
        self.imported = set()

    def add(self, name, signature, value, native=True):
        if name not in self.symbols:
            self.symbols[name] = {}
        if signature in self.symbols[name]:
            raise RuntimeError(f'Symbol {name} already exists in context')
        self.symbols[name][signature] = value
        if native:
            if name not in self.native_symbols:
                self.native_symbols[name] = {}
            self.native_symbols[name][signature] = value

    def add_global(self, name, signature, value):
        if self.parent:
            self.parent.add_global(name, signature, value)
        else:
            self.add(name, signature, value)

    def import_context(self, context):
        if context in self.imported or context is self:
            return
        for name, values in context.native_symbols.items():
            if name not in self.symbols:
                self.symbols[name] = {}
            for signature, value in values.items():
                if hasattr(value, 'modifiers') and 'private' in value.modifiers:
                    continue
                self.add(name, signature, value, False)
        self.imported.add(context)

    def find_all_direct(self, name=None, signature=None):
        if name:
            return [s[1] for s in
                    self.symbols.get(name, {}).items() if s[0] == signature]
        elif signature:
            return [s[1] for s in
                    [(v, r) for v in self.symbols.values() for r in v.values()] if s[0] == signature]
        else:
            return [r for v in self.symbols.values() for r in v.values()]

    def find_direct(self, name, signature=None):
        r = self.find_all_direct(name, signature)
        return (r and r[0]) or None

    def find_all(self, name=None, signature=None):
        if name:
            return [s[1] for s in
                    self.symbols.get(name, {}).items() if s[0] == signature] + (
                           self.parent and self.parent.find_all(name, signature) or [])
        elif signature:
            return [s[1] for s in
                    [(v, r) for v in self.symbols.values() for r in v.values()] if s[0] == signature] + (
                           self.parent and self.parent.find_all(name, signature) or [])
        else:
            return [r for v in self.symbols.values() for r in v.values()] + (
                    self.parent and self.parent.find_all(name, signature) or [])

    def find(self, name, signature=None):
        r = self.find_all(name, signature)
        return (r and r[0]) or None


def read_script(path):
    input_stream = FileStream(path)
    lexer = ScriptLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = ScriptParser(stream)
    tree = parser.scriptFile()
    return ScriptVisitor().visitScriptFile(tree)


class GlobalContext(Context):
    def __init__(self, path):
        super().__init__()
        self.level_allocator = BlockAllocator(0, 256)
        self.path = pathlib.Path(__file__).parent.parent.joinpath("./std")
        for filename in STD_FILENAMES:
            self.get(filename)
        self.path = path

    def get(self, name):
        if name[-4:] == '.scc':
            name = name[:-4]
        if name not in self.symbols or None not in self.symbols[name]:
            from compile.declaration import ScriptFile
            script = ScriptFile(read_script(os.path.join(self.path, f'{name}.ssc')), self)
            self.add(name, None, script)
            script.process_imports()
        return self.find(name, None)


class FileContext(Context):
    def __init__(self, parent: GlobalContext):
        super().__init__(parent)
        self.level_allocator = parent.level_allocator

    def import_script(self, script):
        self.import_context(script.context)


class StructContext(Context):
    pass


class ScriptContext(Context):
    def __init__(self, parent):
        super().__init__(parent)
        self.entity_data = BlockAllocator(22, 32)
        self.entity_memory = BlockAllocator(21, 64)
        self.entity_shared_memory = BlockAllocator(24, 32)
        self.allocator = self.entity_memory
        self.shared_allocator = self.entity_shared_memory

    def new_callback_context(self):
        return CallbackContext(self)


class CallbackContext(Context):
    def __init__(self, parent):
        super().__init__(parent)
        self.temporary_memory = BlockAllocator(100, 16)
        self.allocator = self.temporary_memory


class FunctionContext(Context):
    def __init__(self, parent):
        super().__init__(parent)


class FunctionInvocationContext(Context):
    def __init__(self, parent: Context):
        super().__init__(parent)
        if isinstance(parent, CallbackContext):
            self.allocator = parent.temporary_memory
        elif isinstance(parent, FunctionInvocationContext):
            self.allocator = parent.allocator
        else:
            self.allocator = None


class BlockAllocator:
    def __init__(self, block_id, size):
        self.block_id = block_id
        self.size = size
        self.index = 0

    def allocate(self):
        if self.index + 1 > self.size:
            raise RuntimeError(
                f'Allocation in block {self.block_id} exceeds capacity')
        alloc = Allocation(self.block_id, self.index)
        self.index += 1
        return alloc


class Allocation:
    def __init__(self, block_id, index):
        self.block_id = block_id
        self.index = index
