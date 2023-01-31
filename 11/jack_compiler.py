"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import os
import sys
import typing
from compilation_engine import CompilationEngine
from jack_tokenizer import JackTokenizer
from symbol_table import SymbolTable
from vm_writer import VMWriter


def compile_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Compiles a single file.

    Args:
        input_file (typing.TextIO): the file to compile.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # This function should be relatively similar to "analyze_file" in
    # JackAnalyzer.py from the previous project.
    tokenizer = JackTokenizer(input_file)
    vm_writer = VMWriter(output_file)
    engine = CompilationEngine(tokenizer, vm_writer)

    engine.compile_class()


if "__main__" == __name__:
    # Parses the input path and calls compile_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: JackCompiler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".jack":
            continue
        output_path = filename + ".vm"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            compile_file(input_file, output_file)
