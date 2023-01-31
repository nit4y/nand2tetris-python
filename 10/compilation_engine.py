"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import xml.etree.ElementTree as ET
from jack_tokenizer import JackTokenizer
import consts

class CompilationEngine:
    """Gets input from a JackTokenizer and emits its parsed structure into an
    output stream.
    """

    def __init__(self, input_file):
        """
        Creates a new compilation engine with the given input and output. The
        next routine called must be compileClass()
        :param input_stream: The input stream.
        :param output_stream: The output stream.
        """
        # Your code goes here!
        # Note that you can write to output_stream like so:
        # output_stream.write("Hello world! \n")
        self.tokenizer = JackTokenizer(input_file)
        self.root: ET.Element = None
        self.stack: list[ET.Element] = []

    
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

            self.compile_identifier()

            self.tokenizer.advance()

            self.compile_symbol()

            self.tokenizer.advance()
            
            while (self.tokenizer.keyword() in ["STATIC", "FIELD"]):
                self.compile_class_var_dec()

            while (self.tokenizer.keyword() in ["FUNCTION", "CONSTRUCTOR", "METHOD"]):
                self.compile_subroutine()

            self.compile_symbol()

            self.pop_from_stack()
            
            return self.root


    def compile_class_var_dec(self):
        """Compiles a static declaration or a field declaration."""
        # Your code goes here!
        el = self.create_child_to_open_tag("classVarDec")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()
        
        self.compile_tvar_name()

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
        
        self.compile_keyword()

        self.tokenizer.advance()

        if (self.tokenizer.token_type() == consts.KEYWORD):
            self.compile_keyword()

        elif (self.tokenizer.token_type() == consts.IDENTIFIER):
            self.compile_identifier()

        self.tokenizer.advance()

        self.compile_identifier()

        self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_parameter_list()

        self.compile_symbol()

        self.tokenizer.advance()

        el = self.create_child_to_open_tag("subroutineBody")
        self.stack.append(el)
        
        self.compile_symbol()

        self.tokenizer.advance()

        while self.tokenizer.keyword() == "VAR":
            self.compile_var_dec()

        self.compile_statements()

        self.compile_symbol()

        self.pop_from_stack()
        self.pop_from_stack()

        self.tokenizer.advance()

    def compile_parameter_list(self):
        """Compiles a (possibly empty) parameter list, not including the 
        enclosing "()".
        """
        # Your code goes here!
        el = self.create_child_to_open_tag("parameterList")
        self.stack.append(el)
        
        while self.tokenizer.token_type() != consts.SYMBOL:

            if self.tokenizer.token_type() == consts.KEYWORD:
                self.compile_keyword()

            elif self.tokenizer.token_type() == consts.IDENTIFIER:
                self.compile_identifier()

            self.tokenizer.advance()

            self.compile_identifier()

            self.tokenizer.advance()
            
            if self.tokenizer.symbol() == consts.COMMA:
                self.compile_symbol()
                self.tokenizer.advance()

        self.pop_from_stack()

    def pop_from_stack(self):
        if len(self.stack[-1]) == 0:
            self.stack[-1].text = "\n" + "  " * (len(self.stack)-1)
        self.stack.pop()

    def compile_var_dec(self):
        """Compiles a var declaration."""
        # Your code goes here!
        el = self.create_child_to_open_tag("varDec")
        self.stack.append(el)
        

        self.compile_keyword()

        self.tokenizer.advance()
        
        self.compile_tvar_name()

        self.pop_from_stack()

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
        self.compile_identifier()
        self.tokenizer.advance()

        if self.tokenizer.symbol() == ".":

            self.compile_symbol()

            self.tokenizer.advance()

            self.compile_identifier()

            self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression_list()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_symbol()

        self.pop_from_stack()

        self.tokenizer.advance()

    def compile_let(self):
        """Compiles a let statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("letStatement")

        self.stack.append(el)

        self.compile_keyword()

        self.tokenizer.advance()

        self.compile_identifier()

        self.tokenizer.advance()

        if self.tokenizer.symbol() == "[":
            self._compile_arr_proc()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

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
        
        self.compile_keyword()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_expression()

        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.compile_symbol()

        self.pop_from_stack()
        self.tokenizer.advance()


    def compile_return(self):
        """Compiles a return statement."""
        # Your code goes here!
        el = self.create_child_to_open_tag("returnStatement")
        self.stack.append(el)
        
        self.compile_keyword()

        self.tokenizer.advance()

        if self.tokenizer.symbol() != ";" and self.tokenizer.token_type() != consts.SYMBOL:
            self.compile_expression()

        self.compile_symbol()

        self.pop_from_stack()
        self.tokenizer.advance()


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

        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_symbol()

        self.tokenizer.advance()
        self.compile_statements()

        self.compile_symbol()

        self.tokenizer.advance()

        if self.tokenizer.keyword() == 'ELSE' and self.tokenizer.token_type() == consts.KEYWORD:
            self._compile_kw_in_if()

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
        el = self.create_child_to_open_tag("expression")
        self.stack.append(el)

        self.compile_term()

        while self.tokenizer.token_type() == consts.SYMBOL and self.tokenizer.symbol() in consts.OPERATORS:
            self.compile_symbol()
            self.tokenizer.advance()
            self.compile_term()

        self.pop_from_stack()


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

        el = self.create_child_to_open_tag("term")
        self.stack.append(el)

        t = self.tokenizer.token_type()

        if t == consts.INT_CONST:
            self.compile_int_const()

        elif t == consts.STRING_CONST:
            self.compile_string_const()

        elif t == consts.KEYWORD:
            self.compile_keyword()

        elif t == consts.IDENTIFIER:
            self.compile_identifier()

            self.tokenizer.advance()
            
            if self.tokenizer.symbol() == "[":
                should_advance = True
                self._compile_bracket_in_term()

            elif self.tokenizer.symbol() == ".":
                should_advance = True
                self._compile_dot_in_term()

            elif self.tokenizer.symbol() == "(":
                should_advance = True
                self._compile_paran_in_term()
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

        self.pop_from_stack()


    def _compile_paran_in_term_v2(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

        self.compile_symbol()


    def _compile_paran_in_term(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression_list()

        self.compile_symbol()


    def _compile_bracket_in_term(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression()

        self.compile_symbol()


    def _compile_dot_in_term(self):

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_identifier()

        self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()

        self.compile_expression_list()

        self.compile_symbol()


    def compile_expression_list(self):
        """Compiles a (possibly empty) comma-separated list of expressions."""
        # Your code goes here!
        el = self.create_child_to_open_tag("expressionList")
        self.stack.append(el)

        if self.tokenizer.symbol() != ")" and  self.tokenizer.token_type() != consts.SYMBOL:
            self.compile_expression()

            while self.tokenizer.symbol() == consts.COMMA and self.tokenizer.token_type() == consts.SYMBOL:
                self.compile_symbol()

                self.tokenizer.advance()

                self.compile_expression()

        if self.tokenizer.symbol() =="(":
            self.compile_expression()

            while self.tokenizer.symbol() == consts.COMMA and self.tokenizer.token_type() == consts.SYMBOL:
                self.compile_symbol()
                self.tokenizer.advance()
                self.compile_expression()

        self.pop_from_stack()


    def compile_tvar_name(self):
        if self.tokenizer.token_type() == consts.KEYWORD:
            self.compile_keyword()

        elif self.tokenizer.token_type() == consts.IDENTIFIER:
            self.compile_identifier()

        self.tokenizer.advance()

        self.compile_identifier()

        self.tokenizer.advance()

        while self.tokenizer.symbol() == consts.COMMA:
            self.compile_symbol()

            self.tokenizer.advance()

            self.compile_identifier()

            self.tokenizer.advance()

        self.compile_symbol()

        self.tokenizer.advance()


    def _spaced_st(self, st: str):
        return " " + st + " "

    def create_child_to_open_tag(self, name: str):
        return ET.SubElement(self.stack[-1], (name))
    
    def compile_int_const(self):
        el = self.create_child_to_open_tag(consts.INT_CONST_STR)
        el.text =  self._spaced_st(self.tokenizer.identifier())


    def compile_string_const(self):
        el = self.create_child_to_open_tag(consts.STR_CONST_STR)
        el.text = self._spaced_st(self.tokenizer.identifier())
        
    def compile_identifier(self):
        el = self.create_child_to_open_tag(consts.IDENTIFIER_STR)
        el.text = self._spaced_st(self.tokenizer.identifier())


    def compile_keyword(self):
        el = self.create_child_to_open_tag(consts.KEYWORD_STR)
        el.text = self._spaced_st(self.tokenizer.keyword().lower())


    def compile_symbol(self):
        sym = self.tokenizer.symbol()
        el = self.create_child_to_open_tag(consts.SYMBOL_STR)
        el.text = self._spaced_st(sym)


    
