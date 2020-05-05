import os
import os.path
import pathlib

from antlr4 import *

from compile.declaration import ScriptFile
from compile.process import STD_FILENAMES
from grammar.ScriptLexer import ScriptLexer
from grammar.ScriptParser import ScriptParser
from visitor.visitor import ScriptVisitor
from visitor.nodes import *


class Context:
    def __init__(self, parent=None):
        self.parent = parent
        self.symbols = {}

    def add(self, name, signature, value):
        if name not in self.symbols:
            self.symbols[name] = {}
        if signature in self.symbols[name]:
            raise RuntimeError(f'Symbol {name} already exists in context')
        self.symbols[name][signature] = value

    def find(self, name, signature=None):
        if signature:
            return [s for s in
                    (list(self.symbols.get(name, {}).items()) + ((self.parent and self.parent.find(name)) or [])) if
                    s[0] == signature]
        else:
            return list(self.symbols.get(name, {}).items()) + ((self.parent and self.parent.find(name)) or [])


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

        self.initializing = True
        self.path = pathlib.Path(__file__).parent.parent.joinpath("./std")
        for filename in STD_FILENAMES:
            self.get(filename)
        self.path = path
        self.initializing = False

    def get(self, name):
        if name[-4:] == '.scc':
            name = name[:-4]
        if name not in self.symbols or () not in self.symbols[name]:
            self.add(name, (),
                     ScriptFile(read_script(os.path.join(self.path, f'{name}.ssc')), self, not self.initializing))
        return self.symbols[name][()]

    def new_file_context(self):
        return FileContext(self)


class FileContext(Context):
    def __init__(self, parent):
        super().__init__(parent)
        self.imported = []

    def new_script_context(self):
        return ScriptContext(self)

    def import_context(self, context):
        self.imported.append(context)

    def find_imported(self, name):
        return (list(self.symbols.get(name, {}).values()) + (self.parent and self.parent.find(name)) or [] +
                [s for f in self.imported for s in f.find(name)])


class ScriptContext(Context):
    def __init__(self, parent):
        super().__init__(parent)
        self.entity_data = BlockAllocator(22, 32)
        self.entity_memory = BlockAllocator(21, 64)
        self.entity_shared_memory = BlockAllocator(24, 32)

    def new_callback_context(self):
        return CallbackContext(self)


class CallbackContext(Context):
    def __init__(self, parent):
        super().__init__(parent)
        self.temporary_memory = BlockAllocator(100, 16)


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
