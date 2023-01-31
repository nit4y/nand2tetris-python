
//push constant 17

@17
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 17

@17
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

//push constant 17

@17
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 16

@16
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
@COND.FALSE.1
D;JNE
@SP
A=M
M=-1
@COND.TRUE.1
0;JMP
(COND.FALSE.1)
    @SP
    A=M
    M=0
(COND.TRUE.1)
@SP
M=M+1

//push constant 16

@16
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 17

@17
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
@COND.FALSE.2
D;JNE
@SP
A=M
M=-1
@COND.TRUE.2
0;JMP
(COND.FALSE.2)
    @SP
    A=M
    M=0
(COND.TRUE.2)
@SP
M=M+1

//push constant 892

@892
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 891

@891
D=A
@SP
M=M+1
A=M-1
M=D

//lt

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
@LT.XNEG.3
D;JLT
@LT.XPOS.3
D;JGT
@LT.NO.OF.3
0;JMP
(LT.XNEG.3)
    @R13
    D=M
    @LT.XNEG.YPOS.3
    D;JGT
    @LT.NO.OF.3
    0;JMP
(LT.XPOS.3)
    @R13
    D=M
    @LT.XPOS.YNEG.3
    D;JLT

(LT.NO.OF.3)
@R13
D=M
@R14
D=D-M
@LT.FALSE.3
D;JLE
@SP
A=M
M=-1
@LT.TRUE.3
0;JMP
(LT.FALSE.3)
    @SP
    A=M
    M=0
(LT.TRUE.3)
    @LT.END.3
    0;JMP

(LT.XPOS.YNEG.3)
    @SP
    A=M
    M=0
    @LT.END.3
    0;JMP
    
(LT.XNEG.YPOS.3)
    @SP
    A=M
    M=-1

(LT.END.3)
@SP
M=M+1

//push constant 891

@891
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 892

@892
D=A
@SP
M=M+1
A=M-1
M=D

//lt

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
@LT.XNEG.4
D;JLT
@LT.XPOS.4
D;JGT
@LT.NO.OF.4
0;JMP
(LT.XNEG.4)
    @R13
    D=M
    @LT.XNEG.YPOS.4
    D;JGT
    @LT.NO.OF.4
    0;JMP
(LT.XPOS.4)
    @R13
    D=M
    @LT.XPOS.YNEG.4
    D;JLT

(LT.NO.OF.4)
@R13
D=M
@R14
D=D-M
@LT.FALSE.4
D;JLE
@SP
A=M
M=-1
@LT.TRUE.4
0;JMP
(LT.FALSE.4)
    @SP
    A=M
    M=0
(LT.TRUE.4)
    @LT.END.4
    0;JMP

(LT.XPOS.YNEG.4)
    @SP
    A=M
    M=0
    @LT.END.4
    0;JMP
    
(LT.XNEG.YPOS.4)
    @SP
    A=M
    M=-1

(LT.END.4)
@SP
M=M+1

//push constant 891

@891
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 891

@891
D=A
@SP
M=M+1
A=M-1
M=D

//lt

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
@LT.XNEG.5
D;JLT
@LT.XPOS.5
D;JGT
@LT.NO.OF.5
0;JMP
(LT.XNEG.5)
    @R13
    D=M
    @LT.XNEG.YPOS.5
    D;JGT
    @LT.NO.OF.5
    0;JMP
(LT.XPOS.5)
    @R13
    D=M
    @LT.XPOS.YNEG.5
    D;JLT

(LT.NO.OF.5)
@R13
D=M
@R14
D=D-M
@LT.FALSE.5
D;JLE
@SP
A=M
M=-1
@LT.TRUE.5
0;JMP
(LT.FALSE.5)
    @SP
    A=M
    M=0
(LT.TRUE.5)
    @LT.END.5
    0;JMP

(LT.XPOS.YNEG.5)
    @SP
    A=M
    M=0
    @LT.END.5
    0;JMP
    
(LT.XNEG.YPOS.5)
    @SP
    A=M
    M=-1

(LT.END.5)
@SP
M=M+1

//push constant 32767

@32767
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 32766

@32766
D=A
@SP
M=M+1
A=M-1
M=D

//gt

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
@GT.XPOS.6
D;JGT
@GT.XNEG.6
D;JLT
@GT.NO.OF.6
0;JMP
(GT.XPOS.6)
    @R13
    D=M
    @GT.XPOS.YNEG.6
    D;JLT
    @GT.NO.OF.6
    0;JMP
(GT.XNEG.6)
    @R13
    D=M
    @GT.XNEG.YPOS.6
    D;JGT

(GT.NO.OF.6)
@R13
D=M
@R14
D=M-D
@GT.FALSE.6
D;JLE
@SP
A=M
M=-1
@GT.TRUE.6
0;JMP
(GT.FALSE.6)
    @SP
    A=M
    M=0
(GT.TRUE.6)
    @GT.END.6
    0;JMP

(GT.XNEG.YPOS.6)
    @SP
    A=M
    M=0
    @GT.END.6
    0;JMP
    
(GT.XPOS.YNEG.6)
    @SP
    A=M
    M=-1

(GT.END.6)
@SP
M=M+1

//push constant 32766

@32766
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

//gt

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
@GT.XPOS.7
D;JGT
@GT.XNEG.7
D;JLT
@GT.NO.OF.7
0;JMP
(GT.XPOS.7)
    @R13
    D=M
    @GT.XPOS.YNEG.7
    D;JLT
    @GT.NO.OF.7
    0;JMP
(GT.XNEG.7)
    @R13
    D=M
    @GT.XNEG.YPOS.7
    D;JGT

(GT.NO.OF.7)
@R13
D=M
@R14
D=M-D
@GT.FALSE.7
D;JLE
@SP
A=M
M=-1
@GT.TRUE.7
0;JMP
(GT.FALSE.7)
    @SP
    A=M
    M=0
(GT.TRUE.7)
    @GT.END.7
    0;JMP

(GT.XNEG.YPOS.7)
    @SP
    A=M
    M=0
    @GT.END.7
    0;JMP
    
(GT.XPOS.YNEG.7)
    @SP
    A=M
    M=-1

(GT.END.7)
@SP
M=M+1

//push constant 32766

@32766
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 32766

@32766
D=A
@SP
M=M+1
A=M-1
M=D

//gt

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
@GT.XPOS.8
D;JGT
@GT.XNEG.8
D;JLT
@GT.NO.OF.8
0;JMP
(GT.XPOS.8)
    @R13
    D=M
    @GT.XPOS.YNEG.8
    D;JLT
    @GT.NO.OF.8
    0;JMP
(GT.XNEG.8)
    @R13
    D=M
    @GT.XNEG.YPOS.8
    D;JGT

(GT.NO.OF.8)
@R13
D=M
@R14
D=M-D
@GT.FALSE.8
D;JLE
@SP
A=M
M=-1
@GT.TRUE.8
0;JMP
(GT.FALSE.8)
    @SP
    A=M
    M=0
(GT.TRUE.8)
    @GT.END.8
    0;JMP

(GT.XNEG.YPOS.8)
    @SP
    A=M
    M=0
    @GT.END.8
    0;JMP
    
(GT.XPOS.YNEG.8)
    @SP
    A=M
    M=-1

(GT.END.8)
@SP
M=M+1

//push constant 57

@57
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 31

@31
D=A
@SP
M=M+1
A=M-1
M=D

//push constant 53

@53
D=A
@SP
M=M+1
A=M-1
M=D

//add

@SP
AM=M-1
D=M
@SP
AM=M-1
M=D+M
@SP
M=M+1

//push constant 112

@112
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

//neg

@SP
A=M-1
M=-M

//and

@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M&D

//push constant 82

@82
D=A
@SP
M=M+1
A=M-1
M=D

//or

@SP
M=M-1
A=M
D=M
@SP
A=M-1
M=M|D

//not

@SP
A=M-1
M=!M
