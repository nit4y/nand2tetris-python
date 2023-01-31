
@ARG
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THAT
M=D

@0
D=A
@SP
M=M+1
A=M-1
M=D

@THAT
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@1
D=A
@SP
M=M+1
A=M-1
M=D

@THAT
D=M
@1
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@2
D=A
@SP
M=M+1
A=M-1
M=D

@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1

@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D
(FibonacciSeries.main$MAIN_LOOP_START)
@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@1
D=D+A
@FibonacciSeries.main$COMPUTE_ELEMENT
D;JNE

@FibonacciSeries.main$END_PROGRAM
0;JMP
(FibonacciSeries.main$COMPUTE_ELEMENT)
@THAT
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@THAT
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

@THAT
D=M
@2
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@THAT
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@SP
M=M+1
A=M-1
M=D

@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

@SP
M=M-1
A=M
D=M
@THAT
M=D

@ARG
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

@1
D=A
@SP
M=M+1
A=M-1
M=D

@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1

@ARG
D=M
@0
D=D+A
@R13
M=D
@SP
AM=M-1
D=M
@R13
A=M
M=D

@FibonacciSeries.main$MAIN_LOOP_START
0;JMP
(FibonacciSeries.main$END_PROGRAM)