// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/08/FunctionCalls/IntermidiateFunction/IntermidiateFunction.tst

load IntermidiateFunction.asm,
output-file IntermidiateFunction.out,
compare-to IntermidiateFunction.cmp,
output-list RAM[0]%D1.6.1 RAM[256]%D1.6.1;

set RAM[0] 256,
set RAM[256] 0,

repeat 300 {
  ticktock;
}

output;
