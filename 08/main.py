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
from parser_new import Parser
from code_writer import CodeWriter

def init_bootstrap(code_writer: CodeWriter, output_file: typing.TextIO):
    """
    Initilizes the vm with a bootstrap

    Args:
        output_file (typing.TextIO): output file stream
    """
    output_file.write(
"""@256
D=A
@SP
M=D
"""
    )
    code_writer.write_call("Sys.init", 0)


def translate_file(
        input_file: typing.TextIO, output_file: typing.TextIO,
        bootstrap: bool) -> None:
    """
    Translates a single file.

    Args:
        input_file (typing.TextIO): the file to translate.
        output_file (typing.TextIO): writes all output to this file.
        bootstrap (bool): if this is True, the current file is the 
            first file we are translating.
    """
    
    parser = Parser(input_file)
    code_writer = CodeWriter(output_file, input_file)
    if bootstrap:
        init_bootstrap(code_writer, output_file)
        code_writer.write_return()
    parser.advance()
    while parser.has_more_commands():
        # FOR DEBUG
        #code_writer.file.writelines("\n//" + parser.command.raw)
        if parser.command.type == "C_PUSH":
            code_writer.write_push(parser.command.arg1, parser.command.arg2)
        elif parser.command.type == "C_POP":
            code_writer.write_pop(parser.command.arg1, parser.command.arg2)
        elif parser.command.type == "C_ARITHMETIC":
            code_writer.write_arithmetic(parser.command.short)
        elif parser.command.type == "C_IF":
            code_writer.write_if(parser.command.arg1)
        elif parser.command.type == "C_GOTO":
            code_writer.write_goto(parser.command.arg1)
        elif parser.command.type == "C_CALL":
            code_writer.write_call(parser.command.arg1, parser.command.arg2)
        elif parser.command.type == "C_RETURN":
            code_writer.write_return()
        elif parser.command.type == "C_LABEL":
            code_writer.write_label(parser.command.arg1)
        elif parser.command.type == "C_FUNCTION":
            code_writer.write_function(parser.command.arg1, parser.command.arg2)
        parser.advance()
        
if "__main__" == __name__:
    # Parses the input path and calls translate_file on each input file.
    # This opens both the input and the output files!
    # Both are closed automatically when the code finishes running.
    # If the output file does not exist, it is created automatically in the
    # correct path, using the correct filename.
    if not len(sys.argv) == 2:
        sys.exit("Invalid usage, please use: VMtranslator <input path>")
    argument_path = os.path.abspath(sys.argv[1])
    if os.path.isdir(argument_path):
        files_to_translate = [
            os.path.join(argument_path, filename)
            for filename in os.listdir(argument_path)]
        output_path = os.path.join(argument_path, os.path.basename(
            argument_path))
    else:
        files_to_translate = [argument_path]
        output_path, extension = os.path.splitext(argument_path)
    output_path += ".asm"
    bootstrap = True
    with open(output_path, 'w') as output_file:
        for input_path in files_to_translate:
            filename, extension = os.path.splitext(input_path)
            if extension.lower() != ".vm":
                continue
            with open(input_path, 'r') as input_file:
                translate_file(input_file, output_file, bootstrap)
            bootstrap = False
