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
from parser import Parser
from itertools import tee


def assemble_file(
        input_file: typing.TextIO, output_file: typing.TextIO) -> None:
    """Assembles a single file.

    Args:
        input_file (typing.TextIO): the file to assemble.
        output_file (typing.TextIO): writes all output to this file.
    """
    # Your code goes here!
    # A good place to start is to initialize a new Parser object:
    # parser = Parser(input_file)
    # Note that you can write to output_file like so:
    # output_file.write("Hello world! \n")

    # FIRST PASS
    first, second = tee(input_file)
    parser = Parser(first)
    counter = 0
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            if not parser.symbols.contains(parser.symbol()):
                parser.symbols.add_entry(parser.symbol(), counter)
        else:
            counter+=1
        
        
    # SECOND PASS
    parser = Parser(second)
    while parser.has_more_commands():
        parser.advance()
        if parser.command_type() == "L_COMMAND":
            continue
        elif parser.command_type() == "A_COMMAND":
            if not parser.symbols.contains(parser.symbol()):
                parser.symbols.add_new_entry(parser.symbol())
            output_file.write(parser.translate_a() +  '\n')
        elif parser.command_type() == "C_COMMAND":
            output_file.write(parser.translate_c() +  '\n')
        

if "__main__" == __name__:
    # Parses the input path and calls assemble_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: Assembler <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_assemble = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
    else:
        files_to_assemble = [argument_path]
    for input_path in files_to_assemble:
        filename, extension = os.path.splitext(input_path)
        if extension.lower() != ".asm":
            continue
        output_path = filename + ".hack"
        with open(input_path, 'r') as input_file, \
                open(output_path, 'w') as output_file:
            assemble_file(input_file, output_file)
