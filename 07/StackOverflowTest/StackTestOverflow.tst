// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/07/StackArithmetic/StackTest/StackTest.tst

load StackTestOverflow.asm,
output-file StackTestOverflow.out,
compare-to StackTestOverflow.cmp,
output-list RAM[0]%D2.6.2 RAM[256]%D2.6.2 RAM[257]%D2.6.2 RAM[258]%D2.6.2 RAM[259]%D2.6.2;

set RAM[0] 256,  // initializes the stack pointer

repeat 1000 {    // enough cycles to complete the execution
  ticktock;
}

// outputs the stack pointer (RAM[0]) and 
// the stack contents: RAM[256]-RAM[265]
output;