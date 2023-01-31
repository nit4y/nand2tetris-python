
//push constant 0

@0
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 32767

@32767
D=A
@SP
M=M+1
A=M-1
M=D

//sub

@SP
AM=M-1
D=M
@SP
AM=M-1
M=M-D
@SP
M=M+1

//push constant 2

@2
D=A
@SP
M=M+1
A=M-1
M=D

//lt					   //true
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
@LT.XNEG.0
D;JLT
@LT.XPOS.0
D;JGT
@LT.NO.OF.0
0;JMP
(LT.XNEG.0)
    @R13
    D=M
    @LT.XNEG.YPOS.0
    D;JGT
    @LT.NO.OF.0
    0;JMP
(LT.XPOS.0)
    @R13
    D=M
    @LT.XPOS.YNEG.0
    D;JLT

(LT.NO.OF.0)
@R13
D=M
@R14
D=D-M
@LT.FALSE.0
D;JLE
@SP
A=M
M=-1
@LT.TRUE.0
0;JMP
(LT.FALSE.0)
    @SP
    A=M
    M=0
(LT.TRUE.0)
    @LT.END.0
    0;JMP

(LT.XPOS.YNEG.0)
    @SP
    A=M
    M=0
    @LT.END.0
    0;JMP
    
(LT.XNEG.YPOS.0)
    @SP
    A=M
    M=-1

(LT.END.0)
@SP
M=M+1
