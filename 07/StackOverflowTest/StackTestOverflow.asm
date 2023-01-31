
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

//push constant 2

@2
D=A
@SP
M=M+1
A=M-1
M=D

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

//lt					   //false

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
@LT.XNEG.1
D;JLT
@LT.XPOS.1
D;JGT
@LT.NO.OF.1
0;JMP
(LT.XNEG.1)
    @R13
    D=M
    @LT.XNEG.YPOS.1
    D;JGT
    @LT.NO.OF.1
    0;JMP
(LT.XPOS.1)
    @R13
    D=M
    @LT.XPOS.YNEG.1
    D;JLT

(LT.NO.OF.1)
@R13
D=M
@R14
D=D-M
@LT.FALSE.1
D;JLE
@SP
A=M
M=-1
@LT.TRUE.1
0;JMP
(LT.FALSE.1)
    @SP
    A=M
    M=0
(LT.TRUE.1)
    @LT.END.1
    0;JMP

(LT.XPOS.YNEG.1)
    @SP
    A=M
    M=0
    @LT.END.1
    0;JMP
    
(LT.XNEG.YPOS.1)
    @SP
    A=M
    M=-1

(LT.END.1)
@SP
M=M+1

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

//gt					   //false

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
@GT.XPOS.2
D;JGT
@GT.XNEG.2
D;JLT
@GT.NO.OF.2
0;JMP
(GT.XPOS.2)
    @R13
    D=M
    @GT.XPOS.YNEG.2
    D;JLT
    @GT.NO.OF.2
    0;JMP
(GT.XNEG.2)
    @R13
    D=M
    @GT.XNEG.YPOS.2
    D;JGT

(GT.NO.OF.2)
@R13
D=M
@R14
D=M-D
@GT.FALSE.2
D;JLE
@SP
A=M
M=-1
@GT.TRUE.2
0;JMP
(GT.FALSE.2)
    @SP
    A=M
    M=0
(GT.TRUE.2)
    @GT.END.2
    0;JMP

(GT.XNEG.YPOS.2)
    @SP
    A=M
    M=0
    @GT.END.2
    0;JMP
    
(GT.XPOS.YNEG.2)
    @SP
    A=M
    M=-1

(GT.END.2)
@SP
M=M+1

//push constant 2

@2
D=A
@SP
M=M+1
A=M-1
M=D

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

//gt					   //true
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
@GT.XPOS.3
D;JGT
@GT.XNEG.3
D;JLT
@GT.NO.OF.3
0;JMP
(GT.XPOS.3)
    @R13
    D=M
    @GT.XPOS.YNEG.3
    D;JLT
    @GT.NO.OF.3
    0;JMP
(GT.XNEG.3)
    @R13
    D=M
    @GT.XNEG.YPOS.3
    D;JGT

(GT.NO.OF.3)
@R13
D=M
@R14
D=M-D
@GT.FALSE.3
D;JLE
@SP
A=M
M=-1
@GT.TRUE.3
0;JMP
(GT.FALSE.3)
    @SP
    A=M
    M=0
(GT.TRUE.3)
    @GT.END.3
    0;JMP

(GT.XNEG.YPOS.3)
    @SP
    A=M
    M=0
    @GT.END.3
    0;JMP
    
(GT.XPOS.YNEG.3)
    @SP
    A=M
    M=-1

(GT.END.3)
@SP
M=M+1
