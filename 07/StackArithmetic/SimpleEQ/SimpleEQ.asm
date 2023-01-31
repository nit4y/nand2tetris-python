
//push constant 7

@7
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 7

@7
D=A
@SP
M=M+1
A=M-1
M=D

//eq

@SP
M=M-1
A=M
D=M
@SP
M=M-1
A=M
D=D-M
@COND.FALSE.0
D;JNE
@SP
A=M
M=-1
@COND.TRUE.0
0;JMP
(COND.FALSE.0)
    @SP
    A=M
    M=0
(COND.TRUE.0)
@SP
M=M+1
