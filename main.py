import os
import pathlib
import sys
from antlr4 import *

from compile.context import GlobalContext
from grammar.ScriptLexer import ScriptLexer
from grammar.ScriptParser import ScriptParser
from visitor.visitor import ScriptVisitor


def main(argv):
    GlobalContext(pathlib.Path(os.path.abspath(argv[1])).parent).get(argv[1])


if __name__ == '__main__':
    main(sys.argv)
