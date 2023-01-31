"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import xml.etree.ElementTree as ET
from jack_tokenizer import JackTokenizer
from vm_writer import VMWriter
import consts
from symbol_table import SymbolTable

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, tokenizer: JackTokenizer, writer: VMWriter):
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tokenizer: JackTokenizer = tokenizer
        self.root: ET.Element = None
        self.stack: list[ET.Element] = []
        self.symbol_table = SymbolTable()
        self.writer: VMWriter = writer

        self.op_stack = []

        self.l_count = 0

        self.lcl_count = 0

        self.lcl_args = {}

    
    def compile_class(self):
        """Compiles a complete class."""
        # Your code goes here!
        
        if self.tokenizer.has_more_tokens():

            self.tokenizer.advance()

            el = ET.Element("class")
            self.stack.append(el)

            self.root = el

            self.compile_keyword()

            self.tokenizer.advance()

            # update symbol table with class name
            self.compile_identifier()
            self.symbol_table.curr_class = self.tokenizer.identifier()

            self.tokenizer.advance()

            self.compile_symbol()

            self.tokenizer.advance()
            
            while (self.tokenizer.keyword() in ["STATIC", "FIELD"]):
                self.compile_class_var_dec(self.tokenizer.keyword())

            while (self.tokenizer.keyword() in ["FUNCTION", "CONSTRUCTOR", "METHOD"]):
                self.compile_subroutine()

            self.compile_symbol()

            self.pop_from_stack()
            
            return self.root


    def compile_class_var_dec(self, var_kind: str):
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        el = self.create_child_to_open_tag("classVarDec")
        self.stack.append(el)

        self.compile_keyword()

        self.tokenizer.advance()
        
        self.compile_tvar_name(var_kind)

        self.pop_from_stack()

    def compile_subroutine(self):
        """
        Compiles a complete method, function, or constructor.
        You can assume that classes with constructors have at least one field,
        you will understand why this is necessary in project 11.
        """
        # Your code goes here!
        el = self.create_child_to_open_tag("subroutineDec")
        self.stack.append(el)
        
        #
        with_this = False
        ctor = False
        if self.tokenizer.keyword() == "METHOD":
            with_this = True
        elif self.tokenizer.keyword() == "CONSTRUCTOR":
            ctor = True
        
        self.symbol_table.start_subroutine(with_this)
        #
        self.compile_keyword()

        self.tokenizer.advance()

        if (self.tokenizer.token_type() == consts.KEYWORD):
            self.compile_keyword()

        elif (self.tokenizer.token_type() == consts.IDENTIFIER):
            self.compile_identifier()
            
        self.tokenizer.advance()
        
        #
        func_name = self.tokenizer.identifier()
        self.symbol_table.curr_subrn = func_name
        #
        self.compile_identifier()

        self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()

        arg_num = self.compile_parameter_list()

        self.compile_symbol()

        self.tokenizer.advance()

        if with_this:
            arg_num+=1
        
        el = self.create_child_to_open_tag("subroutineBody")
        self.stack.append(el)
        
        self.compile_symbol()

        self.tokenizer.advance()

        var_num = 0
        while self.tokenizer.keyword() == "VAR":
            nested_vars = self.compile_var_dec()
            var_num+=nested_vars
        #
        func_complete_name = (self.symbol_table.curr_class)+ "." + func_name
        self.writer.write_function(func_complete_name, var_num)
        #
        if with_this:
            self.writer.write_push("argument", 0)
            self.writer.write_pop("pointer", 0)
        if ctor:
            self.writer.write_push("constant", self.symbol_table.var_count("FIELD"))
            self.writer.write_call("Memory.alloc", 1)
            self.writer.write_pop("pointer", 0)
        #

        self.compile_statements()

        self.compile_symbol()

        self.pop_from_stack()
        self.pop_from_stack()

        self.tokenizer.advance()

    def compile_parameter_list(self) -> int:
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        el = self.create_child_to_open_tag("parameterList")
        self.stack.append(el)
        
        var_type = ""
        arg_num = 0
        while self.tokenizer.token_type() != consts.SYMBOL:
            
            if self.tokenizer.token_type() == consts.KEYWORD:
                var_type = self.tokenizer.keyword()
                self.compile_keyword()

            elif self.tokenizer.token_type() == consts.IDENTIFIER:
                var_type = self.tokenizer.identifier()
                self.compile_identifier()

            self.tokenizer.advance()

            self.symbol_table.define(self.tokenizer.identifier(), var_type, "ARG")
            self.compile_identifier()

            self.tokenizer.advance()
            
            if self.tokenizer.symbol() == consts.COMMA:
                self.compile_symbol()
                self.tokenizer.advance()
            arg_num+=1

        self.pop_from_stack()
        return arg_num

    def pop_from_stack(self):
        if len(self.stack[-1]) == 0:
            self.stack[-1].text = "\n" + "  " * (len(self.stack)-1)
        self.stack.pop()

    def compile_var_dec(self) -> int:
        """Compiles a var declaration."""
        # Your code goes here!
        el = self.create_child_to_open_tag("varDec")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()
        
        var_num = self.compile_tvar_name("VAR")

        self.pop_from_stack()

        return var_num

    def compile_statements(self):
        """Compiles a sequence of statements, not including the enclosing 
        "{}".
        """
        # Your code goes here!
        el = self.create_child_to_open_tag("statements")
        self.stack.append(el)

        while self.tokenizer.token_type() == consts.KEYWORD:
            if self.tokenizer.keyword() == "LET":
                self.compile_let()
                
            elif self.tokenizer.keyword() == "IF":
                self.compile_if()

            elif self.tokenizer.keyword() == "WHILE":
                self.compile_while()

            elif self.tokenizer.keyword() == "DO":
                self.compile_do()

            elif self.tokenizer.keyword() == "RETURN":
                self.compile_return()

        self.pop_from_stack()

    def compile_do(self):
        """Compiles a do statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("doStatement")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()

        #
        callee_name = self.tokenizer.identifier()
        arg_num = 0
        method_call = False
        #
        self.compile_identifier()
        self.tokenizer.advance()

        record = self.symbol_table._record_of(callee_name)

        if self.tokenizer.symbol() == ".":
            #
            if record:
                arg_num+=1
                callee_name = record.type
                self.writer.write_push(consts.KIND_TO_SEGMENT[record.kind], record.num)
            callee_name+=self.tokenizer.symbol()
            #
            self.compile_symbol()

            self.tokenizer.advance()
            
            #
            callee_name+=self.tokenizer.identifier()
            #
            self.compile_identifier()

            self.tokenizer.advance()
        else:
            if not record:
                method_call = True
                arg_num+=1
                callee_name = self.symbol_table.curr_class + "." + callee_name

        if method_call:
            self.writer.write_push("pointer", 0)

        self.compile_symbol()

        self.tokenizer.advance()

        arg_num += self.compile_expression_list()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_symbol()

        self.pop_from_stack()

        self.tokenizer.advance()

        
        self.writer.write_call(callee_name, arg_num)

        self.writer.write_pop("temp", 0)

    def compile_let(self):
        """Compiles a let statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("letStatement")

        self.stack.append(el)

        self.compile_keyword()

        self.tokenizer.advance()

        var_name = self.tokenizer.identifier()
        self.compile_identifier()

        self.tokenizer.advance()

        #record = self.symbol_table._record_of(var_name)
        #if record:
        #    self.writer.write_push(consts.KIND_TO_SEGMENT[record.kind], record.num)

        arr_assign = False
        if self.tokenizer.symbol() == "[":
            record = self.symbol_table._record_of(var_name)
            if record:
                self.writer.write_push(consts.KIND_TO_SEGMENT[record.kind], record.num)
            self._compile_arr_proc()
            self.writer.write_arithmetic("ADD")
            arr_assign = True

        self.compile_symbol(True) # True because it should be a defition like let x **=** 10

        self.tokenizer.advance()

        var_type = self.compile_expression()

        if arr_assign:
            self.writer.write_pop("temp", 0)
            self.writer.write_pop("pointer", 1)
            self.writer.write_push("temp", 0)
            self.writer.write_pop("that", 0)
        else:
            if self.symbol_table.kind_of(var_name) is None:
                self.symbol_table.define(var_name, var_type, "VAR")
            self.writer.write_pop(self.symbol_table.segment_of(var_name), self.symbol_table.index_of(var_name))
        #

        self.compile_symbol()

        self.pop_from_stack()

        self.tokenizer.advance()


    def _compile_arr_proc(self):
        
        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

        self.compile_symbol()

        self.tokenizer.advance()


    def compile_while(self):
        """Compiles a while statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("whileStatement")
        self.stack.append(el)

        #
        true_label = self._generate_labels()
        false_label = self._generate_labels()
        self.writer.write_label(true_label)
        #

        self.compile_keyword()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        #
        self.writer.write_arithmetic("NOT")
        self.writer.write_if(false_label)
        #

        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.compile_symbol()

        self.writer.write_goto(true_label)

        self.writer.write_label(false_label)

        self.pop_from_stack()
        self.tokenizer.advance()


    def compile_return(self):
        """Compiles a return statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("returnStatement")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()

        ret_type = "void"
        if self.tokenizer.symbol() != ";" and self.tokenizer.token_type() != consts.SYMBOL:
            ret_type = self.compile_expression()

        self.compile_symbol()

        self.pop_from_stack()
        self.tokenizer.advance()

        if ret_type == "void":
            self.writer.write_push("constant", "0")
        
        if self.symbol_table.curr_subrn == "new":
            self.writer.write_push("pointer", 0)
        self.writer.write_return()


    def _generate_labels(self) -> str:
        label = self.symbol_table.curr_class + "." + \
            self.symbol_table.curr_subrn + "." + \
            str(self.l_count)
        self.l_count+=1
        return label

    def compile_if(self):
        """Compiles a if statement, possibly with a trailing else clause."""
        # Your code goes here!
        el = self.create_child_to_open_tag("ifStatement")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        #
        self.writer.write_arithmetic("NOT")
        false_label = self._generate_labels()
        true_label = self._generate_labels()
        self.writer.write_if(false_label)
        #

        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.compile_symbol()

        self.tokenizer.advance()
        
        #
        self.writer.write_goto(true_label)
        #

        self.writer.write_label(false_label)
        if self.tokenizer.keyword() == 'ELSE' and self.tokenizer.token_type() == consts.KEYWORD:
            self._compile_kw_in_if()

        #
        self.writer.write_label(true_label)
        #
        self.pop_from_stack()


    def _compile_kw_in_if(self):
        self.compile_keyword()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.compile_symbol()
        self.tokenizer.advance()


    def compile_expression(self):
        """Compiles an expression."""
        # Your code goes here!

        # TODO: call codeWrite algo
        ops_start = len(self.op_stack)

        el = self.create_child_to_open_tag("expression")
        self.stack.append(el)

        expression_type = None

        expression_type = self.compile_term()

        while self.tokenizer.token_type() == consts.SYMBOL and self.tokenizer.symbol() in consts.OPERATORS:
            self.compile_symbol()
            self.tokenizer.advance()
            term_type = self.compile_term()
            if not expression_type:
                expression_type = term_type

        while len(self.op_stack) > ops_start:
            self.write_op_from_stack()

        self.pop_from_stack()

        return expression_type

    def write_op_from_stack(self):
        self.writer.write_arithmetic(self.op_stack[-1])
        self.op_stack.pop()


    def compile_term(self):
        """Compiles a term. 
        This routine is faced with a slight difficulty when
        trying to decide between some of the alternative parsing rules.
        Specifically, if the current token is an identifier, the routing must
        distinguish between a variable, an array entry, and a subroutine call.
        A single look-ahead token, which may be one of "[", "(", or "." suffices
        to distinguish between the three possibilities. Any other token is not
        part of this term and should not be advanced over.
        """
        # Your code goes here!
        
        should_advance = True
        term_type = None
        func_call = False
        func_name = ""
        arg_count = 0

        el = self.create_child_to_open_tag("term")
        self.stack.append(el)

        t = self.tokenizer.token_type()

        if t == consts.INT_CONST:
            term_type = "INT"
            self.compile_int_const()

        elif t == consts.STRING_CONST:
            term_type = "STRING"
            self.compile_string_const()

        elif t == consts.KEYWORD:
            if not term_type:
                term_type = self.symbol_table.type_of(self.tokenizer.keyword())
            self.compile_keyword()

        elif t == consts.IDENTIFIER:
            
            dot_call = False

            if not term_type:
                term_type = self.symbol_table.type_of(self.tokenizer.identifier())
            self.compile_identifier()
            segment = self.symbol_table.segment_of(self.tokenizer.identifier())
            if segment:
                dot_call = True
                index = self.symbol_table.index_of(self.tokenizer.identifier())
                self.writer.write_push(segment, index)
            else: #its a function so run function
                func_call = True
            func_name = self.tokenizer.identifier()
            

            self.tokenizer.advance()
            
            if self.tokenizer.symbol() == "[":
                #record = self.symbol_table._record_of(func_name)
                #if record:
                #    self.writer.write_push(consts.KIND_TO_SEGMENT[record.kind], record.num)
                #else:
                #    pass
                should_advance = True
                self._compile_bracket_in_term()
                self.writer.write_arithmetic("ADD")
                self.writer.write_pop("pointer", 1)
                self.writer.write_push("that", 0)
                

            elif self.tokenizer.symbol() == ".":
                func_call = True
                func_call = self.tokenizer.identifier()
                record = self.symbol_table._record_of(func_name)
                if record:
                    func_name = record.type
                #    self.writer.write_push(consts.KIND_TO_SEGMENT[record.kind], record.num)
                func_name+="."
                func_name, arg_count = self._compile_dot_in_term(func_name)
                if dot_call:
                    arg_count+=1
                should_advance = True

            elif self.tokenizer.symbol() == "(":
                should_advance = True
                func_name = self.symbol_table.curr_class + "." + func_name
                arg_count = self._compile_paran_in_term()
            else:
                should_advance = False

        elif self.tokenizer.symbol() == "(":
            self._compile_paran_in_term_v2()

        elif self.tokenizer.symbol() in ["~","-"]:
            self.compile_symbol()
            self.tokenizer.advance()
            self.compile_term()
            should_advance = False

        if should_advance:
            self.tokenizer.advance()

        if func_call:
            self.writer.write_call(func_name, arg_count)

        self.pop_from_stack()
        
        return term_type


    def _compile_paran_in_term_v2(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

        self.compile_symbol()


    def _compile_paran_in_term(self):

        self.compile_symbol()

        self.tokenizer.advance()

        param_num = self.compile_expression_list()

        self.compile_symbol()

        return param_num


    def _compile_bracket_in_term(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

        self.compile_symbol()


    def _compile_dot_in_term(self, func_name: str = None):

        self.compile_symbol()

        self.tokenizer.advance()
        
        func_name+=self.tokenizer.identifier()
        self.compile_identifier()

        self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()

        arg_count = self.compile_expression_list()

        self.compile_symbol()

        return func_name, arg_count


    def compile_expression_list(self) -> int:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        el = self.create_child_to_open_tag("expressionList")
        self.stack.append(el)

        exp_counter = 0

        if self.tokenizer.symbol() != ")" and  self.tokenizer.token_type() != consts.SYMBOL:
            exp_counter+=1
            self.compile_expression()
            

            while self.tokenizer.symbol() == consts.COMMA and self.tokenizer.token_type() == consts.SYMBOL:
                exp_counter+=1
                self.compile_symbol()

                self.tokenizer.advance()

                self.compile_expression()

        if self.tokenizer.symbol() =="(":
            exp_counter+=1
            self.compile_expression()

            while self.tokenizer.symbol() == consts.COMMA and self.tokenizer.token_type() == consts.SYMBOL:
                exp_counter+=1
                self.compile_symbol()
                self.tokenizer.advance()
                self.compile_expression()

        self.pop_from_stack()

        return exp_counter


    def compile_tvar_name(self, var_kind: str) -> int:

        var_count = 1

        if self.tokenizer.token_type() == consts.KEYWORD:
            var_type = self.tokenizer.keyword()
            self.compile_keyword()

        elif self.tokenizer.token_type() == consts.IDENTIFIER:
            var_type = self.tokenizer.identifier()
            self.compile_identifier()
            

        self.tokenizer.advance()

        self.symbol_table.define(self.tokenizer.identifier(), var_type, var_kind)
        self.compile_identifier()

        self.tokenizer.advance()

        while self.tokenizer.symbol() == consts.COMMA:
            var_count+=1

            self.compile_symbol()

            self.tokenizer.advance()

            self.symbol_table.define(self.tokenizer.identifier(), var_type, var_kind)
            self.compile_identifier()

            self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()
        return var_count


    def _spaced_st(self, st: str):
        return " " + st + " "

    def create_child_to_open_tag(self, name: str):
        return ET.SubElement(self.stack[-1], (name))
    
    def compile_int_const(self):
        self.writer.write_push("constant", self.tokenizer.identifier())
        el = self.create_child_to_open_tag(consts.INT_CONST_STR)
        el.text =  self._spaced_st(self.tokenizer.identifier())


    def compile_string_const(self):
        self.writer.write_string_const(self.tokenizer.identifier())
        el = self.create_child_to_open_tag(consts.STR_CONST_STR)
        el.text = self._spaced_st(self.tokenizer.identifier())
        
    def compile_identifier(self):
        ident = self.tokenizer.identifier()
        el = self.create_child_to_open_tag(consts.IDENTIFIER_STR)
        el.text = self._spaced_st(ident)


    def compile_keyword(self):
        kw = self.tokenizer.keyword().lower()
        if kw in ["true", "false", "null"]:
            self.writer.write_push("constant", 0)
            if kw == "true":
                self.writer.write_arithmetic("NOT")
            return
        elif kw == "this":
            self.writer.write_push("pointer", 0)
        el = self.create_child_to_open_tag(consts.KEYWORD_STR)
        el.text = self._spaced_st(kw)


    def compile_symbol(self, is_def = False):
        sym = self.tokenizer.symbol()
        if not is_def:             
            if sym in consts.OPERATORS_TO_VM_CODE:
                if sym in consts.UNARY_TO_VM and self.stack[-1].tag == "term":
                    self.op_stack.append(consts.UNARY_TO_VM[sym])
                else:
                    self.op_stack.append(consts.OPERATORS_TO_VM_CODE[sym])
        el = self.create_child_to_open_tag(consts.SYMBOL_STR)
        el.text = self._spaced_st(sym)


    
