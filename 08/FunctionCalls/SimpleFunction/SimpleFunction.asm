
//function SimpleFunction.test 2

(SimpleFunction.test)

@0
D=A
@SP
M=M+1
A=M-1
M=D

@LCL
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

@0
D=A
@SP
M=M+1
A=M-1
M=D

@LCL
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

//push local 0

@LCL
D=M
@0
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//push local 1

@LCL
D=M
@1
A=D+A
D=M
@SP
A=M
M=D
@SP
M=M+1

//add

@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

//not

@SP
A=M-1
M=!M

//push argument 0

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

//add

@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

//push argument 1

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

//sub

@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1

//return

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
0;JMP
