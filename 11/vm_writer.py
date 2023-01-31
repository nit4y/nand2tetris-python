"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing

SEGMENT_TO_SEG_VM_NAME = {
    "CONST": "constant",
    "LOCAL": "local",
    "ARG": "argument",
    "STATIC": "static",
    "THIS": "this",
    "THAT": "that",
    "POINTER": "pointer",
    "TEMP": "temp",
}

class VMWriter:
    """
    Writes VM commands into a file. Encapsulates the VM command syntax.
    """

    def __init__(self, output_stream: typing.TextIO) -> None:
        """Creates a new file and prepares it for writing VM commands."""
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.file = output_stream

    def write_push(self, segment: str, index: int) -> None:
        """Writes a VM push command.

        Args:
            segment (str): the segment to push to, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP"
            index (int): the index to push to.
        """
        # Your code goes here!
        self.file.write("""push {segment} {index}\n""".format_map({
            "segment": segment,
            "index": index
        }))

    def write_pop(self, segment: str, index: int) -> None:
        """Writes a VM pop command.

        Args:
            segment (str): the segment to pop from, can be "CONST", "ARG", 
            "LOCAL", "STATIC", "THIS", "THAT", "POINTER", "TEMP".
            index (int): the index to pop from.
        """
        # Your code goes here!
        self.file.write("""pop {segment} {index}\n""".format_map({
            "segment": segment,
            "index": index
        }))

    def write_arithmetic(self, command: str) -> None:
        """Writes a VM arithmetic command.

        Args:
            command (str): the command to write, can be "ADD", "SUB", "NEG", 
            "EQ", "GT", "LT", "AND", "OR", "NOT", "SHIFTLEFT", "SHIFTRIGHT".
        """
        # Your code goes here!
        if len(command.split()) > 1:
            self.file.write(command + '\n')
        else:
            self.file.write(command.lower() + '\n')

    def write_label(self, label: str) -> None:
        """Writes a VM label command.

        Args:
            label (str): the label to write.
        """
        # Your code goes here!
        self.file.write("""label {label}\n""".format_map({
            "label": label,
        }))

    def write_goto(self, label: str) -> None:
        """Writes a VM goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.file.write("""goto {label}\n""".format_map({
            "label": label,
        }))

    def write_if(self, label: str) -> None:
        """Writes a VM if-goto command.

        Args:
            label (str): the label to go to.
        """
        # Your code goes here!
        self.file.write("""if-goto {label}\n""".format_map({
            "label": label,
        }))

    def write_call(self, name: str, n_args: int) -> None:
        """Writes a VM call command.

        Args:
            name (str): the name of the function to call.
            n_args (int): the number of arguments the function receives.
        """
        # Your code goes here!
        self.file.write("""call {name} {n_args}\n""".format_map({
            "name": name,
            "n_args": n_args
        }))

    def write_function(self, name: str, n_locals: int) -> None:
        """Writes a VM function command.

        Args:
            name (str): the name of the function.
            n_locals (int): the number of local variables the function uses.
        """
        # Your code goes here!
        self.file.write("""function {name} {n_locals}\n""".format_map({
            "name": name,
            "n_locals": n_locals
        }))

    def write_return(self) -> None:
        """Writes a VM return command."""
        # Your code goes here!
        self.file.write("""return\n""")
    
    def write_string_const(self, st: str) -> None:
        # allocate new string object
        self.write_push("constant", len(st))
        self.write_call('String.new', 1)
        for char in st:
            ascii_code = ord(char)
            self.write_push('constant', ascii_code)
            self.write_call('String.appendChar', 2)

