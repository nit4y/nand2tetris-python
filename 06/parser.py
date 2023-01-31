"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
from code import Code
from symbol_table import SymbolTable

import re


TEMP_START = 5

def sanitize(s: str) -> str:
    s = s.replace(' ', '')
    s = s.replace('\n', '')
    s = s.replace('\t', '')
    s = re.sub(r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)', '', s)
    return s

def determine_command_type(s: str):
    if s[0] == "@":
            return "A_COMMAND"
    if s[0] == "(":
        return "L_COMMAND"
    return "C_COMMAND"

class Command:
    """Encapsulates a command properties
    """
    def __init__(self, raw: str) -> None:
        self.dest = "null"
        self.comp = "null"
        self.jump = "null"
        self.type = "null"
        if not sanitize(raw).strip():
            return
        self.raw = raw
        self.sanitized = sanitize(raw)
        self.type = determine_command_type(self.sanitized)

        

        if self.type == "C_COMMAND":
            eindex = self.sanitized.find("=")
            if eindex == -1:
                eindex=0
                self.dest = "null"
            else:
                self.dest = self.sanitized[:eindex]

            cindex = self.sanitized.find(";")

            if cindex == -1:
                self.jump = "null"
                self.comp = self.sanitized[eindex+1:]
            else:
                self.jump = self.sanitized[cindex+1:]
                self.comp = self.sanitized[eindex:cindex]



class Parser:
    """Encapsulates access to the input code. Reads an assembly program
    by reading each command line-by-line, parses the current command,
    and provides convenient access to the commands components (fields
    and symbols). In addition, removes all white space and comments.
    """

    def __init__(self, input_file: typing.TextIO) -> None:
        """Opens the input file and gets ready to parse it.

        Args:
            input_file (typing.TextIO): input file.
        """
        # A good place to start is to read all the lines of the input:
        # input_lines = input_file.read().splitlines()
        self.file = input_file
        self.command = None
        self.has_more = True
        self.coder = Code()
        self.symbols = SymbolTable()

    def has_more_commands(self) -> bool:
        """Are there more commands in the input?

        Returns:
            bool: True if there are more commands, False otherwise.
        """
        return self.has_more

    def advance(self) -> None:
        """Reads the next command from the input and makes it the current command.
        Should be called only if has_more_commands() is true.
        """
        try:
            line = next(self.file)
            while not sanitize(line).strip():
                line = next(self.file)
            self.command = Command(line)
        except StopIteration:
            self.has_more = False

    def command_type(self) -> str:
        """
        Returns:
            str: the type of the current command:
            "A_COMMAND" for @Xxx where Xxx is either a symbol or a decimal number
            "C_COMMAND" for dest=comp;jump
            "L_COMMAND" (actually, pseudo-command) for (Xxx) where Xxx is a symbol
        """
        return self.command.type
        

    def symbol(self) -> str:
        """
        Returns:
            str: the symbol or decimal Xxx of the current command @Xxx or
            (Xxx). Should be called only when command_type() is "A_COMMAND" or 
            "L_COMMAND".
        """
        if self.command_type() == "A_COMMAND":
            return self.command.sanitized[1:]
        elif self.command_type() == "L_COMMAND":
            return self.command.sanitized[1:len(self.command.sanitized)-1]

    def dest(self) -> str:
        """
        Returns:
            str: the dest mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.command.dest

    def comp(self) -> str:
        """
        Returns:
            str: the comp mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.command.comp

    def jump(self) -> str:
        """
        Returns:
            str: the jump mnemonic in the current C-command. Should be called 
            only when commandType() is "C_COMMAND".
        """
        return self.command.jump
    

    def translate_c(self):
        starter = self.command_type()
        if self.command.comp.find(">") >= 0 or self.command.comp.find("<") >= 0:
            starter = "SHIFT"
        return self.coder.starter(starter) + \
            self.coder.comp(self.command.comp) + \
                self.coder.dest(self.command.dest) + \
                    self.coder.jump(self.command.jump)
    
    def translate_a(self):
        return str(
            '{0:016b}'.format(
                self.symbols.get_address(
                    self.symbol()
                    )))

