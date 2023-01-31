"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import os
from consts import *

class CodeWriter:
    """Translates VM commands into Hack assembly code."""

    def __init__(self, output_stream: typing.TextIO, input_stream: typing.TextIO) -> None:
        """Initializes the CodeWriter.

        Args:
            output_stream (typing.TextIO): output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.file = output_stream
        self.set_file_name(input_stream.name)#(self.file.name)
        self.diff = 0
        self.curr_func = "Sys.init"
        self.call_stack = []
        self.func_diff = func_diff

    def set_file_name(self, filename: str) -> None:
        """Informs the code writer that the translation of a new VM file is 
        started.

        Args:
            filename (str): The name of the VM file.
        """
        # Your code goes here!
        # This function is useful when translating code that handles the
        # static segment. For example, in order to prevent collisions between two
        # .vm files which push/pop to the static segment, one can use the current
        # file's name in the assembly variable's name and thus differentiate between
        # static variables belonging to different files.
        # To avoid problems with Linux/Windows/MacOS differences with regards
        # to filenames and paths, you are advised to parse the filename in
        # the function "translate_file" in Main.py using python's os library,
        # For example, using code similar to:
        # input_filename, input_extension = os.path.splitext(os.path.basename(input_file.name))
        self.input_filename, self.input_extension = os.path.splitext(os.path.basename(filename))


    def write_add(self):
        self.file.write(
"""
@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1
"""
        )

    def write_sub(self):
        self.file.write(
"""
@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1"""
        )

    def write_neg(self):
        self.file.write(
"""
@SP
A=M-1
M=-M"""
        )

    def write_eq(self):
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@COND.FALSE.{diff}
D;JNE
@SP
A=M
M=-1
@COND.TRUE.{diff}
0;JMP
(COND.FALSE.{diff})
    @SP
    A=M
    M=0
(COND.TRUE.{diff})
@SP
M=M+1
""".format_map({
                "diff": str(self.diff)
            })
        )
        self.diff += 1

    def write_lt(self):
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@LT.XNEG.{diff}
D;JLT
@LT.XPOS.{diff}
D;JGT
@LT.NO.OF.{diff}
0;JMP
(LT.XNEG.{diff})
    @R13
    D=M
    @LT.XNEG.YPOS.{diff}
    D;JGT
    @LT.NO.OF.{diff}
    0;JMP
(LT.XPOS.{diff})
    @R13
    D=M
    @LT.XPOS.YNEG.{diff}
    D;JLT
(LT.NO.OF.{diff})
@R13
D=M
@R14
D=D-M
@LT.FALSE.{diff}
D;JLE
@SP
A=M
M=-1
@LT.TRUE.{diff}
0;JMP
(LT.FALSE.{diff})
    @SP
    A=M
    M=0
(LT.TRUE.{diff})
    @LT.END.{diff}
    0;JMP
(LT.XPOS.YNEG.{diff})
    @SP
    A=M
    M=0
    @LT.END.{diff}
    0;JMP
(LT.XNEG.YPOS.{diff})
    @SP
    A=M
    M=-1
(LT.END.{diff})
@SP
M=M+1""".format_map({
                "diff": str(self.diff)
            })
        )
        self.diff += 1

    def write_and(self):
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M&D""".format_map({
                "diff": str(self.diff)
            })
        )
        self.diff += 1

    def write_or(self):
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M|D""".format_map({
                "diff": str(self.diff)
            })
        )

    def write_not(self):
        self.file.write(
"""
@SP
A=M-1
M=!M"""
        )

    def write_gt(self):
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@R13
M=D
@SP
M=M-1
A=M
D=M
@R14
M=D
@R14
D=M
@GT.XPOS.{diff}
D;JGT
@GT.XNEG.{diff}
D;JLT
@GT.NO.OF.{diff}
0;JMP
(GT.XPOS.{diff})
    @R13
    D=M
    @GT.XPOS.YNEG.{diff}
    D;JLT
    @GT.NO.OF.{diff}
    0;JMP
(GT.XNEG.{diff})
    @R13
    D=M
    @GT.XNEG.YPOS.{diff}
    D;JGT
(GT.NO.OF.{diff})
@R13
D=M
@R14
D=M-D
@GT.FALSE.{diff}
D;JLE
@SP
A=M
M=-1
@GT.TRUE.{diff}
0;JMP
(GT.FALSE.{diff})
    @SP
    A=M
    M=0
(GT.TRUE.{diff})
    @GT.END.{diff}
    0;JMP
(GT.XNEG.YPOS.{diff})
    @SP
    A=M
    M=0
    @GT.END.{diff}
    0;JMP
(GT.XPOS.YNEG.{diff})
    @SP
    A=M
    M=-1
(GT.END.{diff})
@SP
M=M+1""".format_map({
                "diff": str(self.diff)
            })
        )
        self.diff += 1

    def write_shiftleft(self):
        self.file.write(
"""
@SP
A=M-1
M=M<<"""
        )
    
    def write_shiftright(self):
        self.file.write(
"""
@SP
A=M-1
M=M>>"""
        )

    def write_arithmetic(self, command: str) -> None:
        """Writes assembly code that is the translation of the given 
        arithmetic command. For the commands eq, lt, gt, you should correctly
        compare between all numbers our computer supports, and we define the
        value "true" to be -1, and "false" to be 0.

        Args:
            command (str): an arithmetic command.
        """
        if command == "add":
            self.write_add()
        elif command == "sub":
            self.write_sub()
        elif command == "neg":
            self.write_neg()
        elif command == "eq":
            self.write_eq()
        elif command == "lt":
            self.write_lt()
        elif command == "and":
            self.write_and()
        elif command == "or":
            self.write_or()
        elif command == "gt":
            self.write_gt()
        elif command == "not":
            self.write_not()
        elif command == "shiftleft":
            self.write_shiftleft()
        elif command == "shiftright":
            self.write_shiftright()
        else:
            print("ERROR: UNKNOWN COMMAND: " + command)

    def write_pop_temp(self, segment: str, index: int):
        self.file.write(
"""
@{segment}
D=A
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D""".format_map({
                "segment": SEGMENT_TO_ADDRESS[segment],
                "index": index

            })
        )

    
    def write_pop_latt(self, segment: str, index: int):
        self.file.write(
"""
@{segment}
D=M
@{index}
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D""".format_map({
                "segment": SEGMENT_TO_ADDRESS[segment],
                "index": index

            })
        )

    def write_pop_static(self, index: int):
        self.file.write(
"""
@SP
AM=M-1
D=M
@{file_name}.{index}
M=D""".format_map({
                "file_name": self.input_filename,
                "index": index
            })
        )

    def write_pop_pointer(self, index: int):
        choice = self.dis_or_dat(index)
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@{choice}
M=D""".format_map({
                "choice": choice,
            })
        )
    
    def write_pop(self, segment: str, index: int) -> None:
        if segment in ["local", "argument", "this", "that"]:
            self.write_pop_latt(segment, index)
        elif segment == "temp":
            self.write_pop_temp(segment, index)
        elif segment == "static":
            self.write_pop_static(index)
        elif segment == "pointer":
            self.write_pop_pointer(index)
    
    def write_push_constant(self, value: int):
        self.file.write(
"""
@{val}
D=A
@SP
M=M+1
A=M-1
M=D""".format_map({
                "val": value
            })
        )

    def write_push_latt(self, segment: str, index: int):
        self.file.write(
"""
@{segment}
D=M
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1""".format_map({
                "segment": SEGMENT_TO_ADDRESS[segment],
                "index": index

            })
        )

    def write_push_static(self, index: int):
        self.file.write(
"""
@{file_name}.{index}
D=M
@SP
A=M
M=D
@SP
M=M+1""".format_map({
                "file_name": self.input_filename,
                "index": index
            })
        )

    def dis_or_dat(self, index: int):
        return {
            "0": "THIS",
            "1": "THAT"
        }[str(index)]

    def write_push_pointer(self, index: int):
        choice = self.dis_or_dat(index)
        self.file.write(
"""
@{choice}
D=M
@SP
A=M
M=D
@SP
M=M+1""".format_map({
                "choice": choice,
            })
        )

    def write_push_temp(self, segment: str, index: int):
        self.file.write(
"""
@{segment}
D=A
@{index}
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1""".format_map({
                "segment": SEGMENT_TO_ADDRESS[segment],
                "index": index

            })
        )
        

    def write_push(self, segment: str, index: int) -> None:
        if segment == "constant":
            self.write_push_constant(index)
        elif segment in ["local", "argument", "this", "that"]:
            self.write_push_latt(segment, index)
        elif segment == "temp":
            self.write_push_temp(segment, index)
        elif segment == "static":
            self.write_push_static(index)
        elif segment == "pointer":
            self.write_push_pointer(index)

    def write_push_pop(self, command: str, segment: str, index: int) -> None:
        """Writes assembly code that is the translation of the given 
        command, where command is either C_PUSH or C_POP.

        Args:
            command (str): "C_PUSH" or "C_POP".
            segment (str): the memory segment to operate on.
            index (int): the index in the memory segment.
        """
        # Your code goes here!
        # Note: each reference to "static i" appearing in the file Xxx.vm should
        # be translated to the assembly symbol "Xxx.i". In the subsequent
        # assembly process, the Hack assembler will allocate these symbolic
        # variables to the RAM, starting at address 16.
        if command == "push":
            self.write_push(segment, index)
        elif command == "pop": 
            self.write_pop(segment, index)

    def write_label(self, label: str) -> None:
        """Writes assembly code that affects the label command. 
        Let "Xxx.foo" be a function within the file Xxx.vm. The handling of
        each "label bar" command within "Xxx.foo" generates and injects the symbol
        "Xxx.foo$bar" into the assembly code stream.
        When translating "goto bar" and "if-goto bar" commands within "foo",
        the label "Xxx.foo$bar" must be used instead of "bar".

        Args:
            label (str): the label to write.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.file.write(
"""
({func}${label})""".format_map({
            #"file": self.input_filename,
            "func": self.curr_func,#self.call_stack[-1],
            "label": label
        }))
    
    def write_goto(self, label: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        match = """{func}${label}""".format_map({
            #"file": self.input_filename,
            "func": self.curr_func,#self.call_stack[-1]
            "label": label
        })

        self.file.write(
"""
@{match}
0;JMP""".format_map({"match": match}))

    def write_goto_func(self, func: str) -> None:
        """Writes assembly code that affects the goto command.

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        self.file.write(
"""
@{func}
0;JMP""".format_map({"func": func}))
        self.call_stack.append(func)
        #self.curr_func = func

    def increment_func_runner(self, func_name: str):
        try:
            self.func_diff[func_name]+=1
        except KeyError:
            self.func_diff[func_name] = 0

    def write_if(self, label: str) -> None:
        """Writes assembly code that affects the if-goto command. 

        Args:
            label (str): the label to go to.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        match = """{func}${label}""".format_map({
            #"file": self.input_filename,
            "func": self.curr_func,#self.call_stack[-1],
            "label": label
        })
        self.file.write(
"""
@SP
M=M-1
A=M
D=M
@1
D=D+A
@{match}
D;JEQ""".format_map({"match": match}))
    
    def write_function(self, function_name: str, n_vars: int) -> None:
        """Writes assembly code that affects the function command. 
        The handling of each "function Xxx.foo" command within the file Xxx.vm
        generates and injects a symbol "Xxx.foo" into the assembly code stream,
        that labels the entry-point to the function's code.
        In the subsequent assembly process, the assembler translates this 
        symbol into the physical address where the function code starts.

        Args:
            function_name (str): the name of the function.
            n_vars (int): the number of local variables of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "function function_name n_vars" is:
        # (function_name)       // injects a function entry label into the code
        # repeat n_vars times:  // n_vars = number of local variables
        #   push constant 0     // initializes the local variables to 0
        self.file.write(
"""
({func_name})""".format_map({"func_name":function_name}))
        self.call_stack.append(function_name)
        self.curr_func = function_name
        for i in range(int(n_vars)):
            self.write_push_constant(0)
            #self.write_pop_latt("local", i)
    
    def write_call(self, function_name: str, n_args: int) -> None:
        """Writes assembly code that affects the call command. 
        Let "Xxx.foo" be a function within the file Xxx.vm.
        The handling of each "call" command within Xxx.foo's code generates and
        injects a symbol "Xxx.foo$ret.i" into the assembly code stream, where
        "i" is a running integer (one such symbol is generated for each "call"
        command within "Xxx.foo").
        This symbol is used to mark the return address within the caller's 
        code. In the subsequent assembly process, the assembler translates this
        symbol into the physical memory address of the command immediately
        following the "call" command.

        Args:
            function_name (str): the name of the function to call.
            n_args (int): the number of arguments of the function.
        """
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "call function_name n_args" is:
        # push return_address   // generates a label and pushes it to the stack
        # push LCL              // saves LCL of the caller
        # push ARG              // saves ARG of the caller
        # push THIS             // saves THIS of the caller
        # push THAT             // saves THAT of the caller
        # ARG = SP-5-n_args     // repositions ARG
        # LCL = SP              // repositions LCL
        # goto function_name    // transfers control to the callee
        # (return_address)      // injects the return address label into the code
        self.increment_func_runner(function_name)
        return_address = """{func_name}$ret.{func_diff}""".format_map(
            {
                #"filename": self.input_filename,
                "func_name": function_name,
                "func_diff": self.func_diff[function_name]
            }
        )
        self.file.write(
"""
@{return_address}
D=A
@SP
M=M+1
A=M-1
M=D
@LCL
D=M
@SP
M=M+1
A=M-1
M=D
@ARG
D=M
@SP
M=M+1
A=M-1
M=D
@THIS
D=M
@SP
M=M+1
A=M-1
M=D
@THAT
D=M
@SP
M=M+1
A=M-1
M=D
@SP
D=M
@5
D=D-A
@{num_of_args}
D=D-A
@ARG
M=D
@SP
D=M
@LCL
M=D""".format_map({
    "return_address": return_address, 
    "num_of_args": str(n_args)
    })
        )
        self.write_goto_func(function_name)
        self.file.write(
"""
({return_address})""".format_map({"return_address": return_address})
        )
        

    
    def write_return(self) -> None:
        """Writes assembly code that affects the return command."""
        # This is irrelevant for project 7,
        # you will implement this in project 8!
        # The pseudo-code of "return" is:
        # frame = LCL                   // frame is a temporary variable
        # return_address = *(frame-5)   // puts the return address in a temp var
        # *ARG = pop()                  // repositions the return value for the caller
        # SP = ARG + 1                  // repositions SP for the caller
        # THAT = *(frame-1)             // restores THAT for the caller
        # THIS = *(frame-2)             // restores THIS for the caller
        # ARG = *(frame-3)              // restores ARG for the caller
        # LCL = *(frame-4)              // restores LCL for the caller
        # goto return_address           // go to the return address
        self.file.write(
"""
@LCL
D=M
@R13
M=D
@5
D=D-A
A=D
D=M
@R14
M=D
@SP
M=M-1
A=M
D=M
@ARG
A=M
M=D
@ARG
D=M
@SP
M=D+1
@R13
M=M-1
A=M
D=M
@THAT
M=D
@R13
M=M-1
A=M
D=M
@THIS
M=D
@R13
M=M-1
A=M
D=M
@ARG
M=D
@R13
M=M-1
A=M
D=M
@LCL
M=D
@R14
A=M
0;JMP"""
        )
        self.call_stack.pop()
    
    
    