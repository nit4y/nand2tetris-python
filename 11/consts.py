
import re

IDENTIFIER_STR = "identifier"
KEYWORD_STR = "keyword"
SYMBOL_STR = "symbol"
INT_CONST_STR = "integerConstant"
STR_CONST_STR = "stringConstant"

REGEX_IDENTIFIER = re.compile("^\s*([a-zA-Z_][a-zA-Z1-9_]*)\s*")
REGEX_EMPTY_TEXT = re.compile("\s*")
REGEX_DIGIT = re.compile("^\s*(\d+)\s*")
REGEX_STRING = re.compile("^\s*\"(.*)\"\s*")
REGEX_KEYWORD = re.compile("^\s*(false|do|if|null|this|let|else|while|return|static|field|var|int|char|boolean|void|true|class|method|constructor|function)\s*")
REGEX_SYMBOL = re.compile("^\s*([{}()\[\].,;+\-*/&|~>=<])\s*")
REGEX_COMMENTS = "(//.*)|(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)"


KEYWORDS = [
    "CLASS",
    "DO", 
    "IF", 
    "ELSE", 
    "WHILE", 
    "RETURN", 
    "FUNCTION", 
    "CONSTRUCTOR", 
    "INT",
    "BOOLEAN", 
    "CHAR",
    "METHOD",
    "VOID", 
    "VAR", 
    "STATIC", 
    "FIELD", 
    "LET",
    "TRUE", 
    "FALSE",
    "NULL", 
    "THIS"
]

LEGAL_EXPRESSIONS = [
    "TRUE", 
    "FALSE",
    "NULL", 
    "THIS"
]

KEYWORD = "KEYWORD"

SYMBOL = "SYMBOL"

INT_CONST = "INT_CONST"

STRING_CONST = "STRING_CONST"

IDENTIFIER = "IDENTIFIER"

OPERATORS = [
    "+", 
    "/", 
    "-",
    "<", 
    ">", 
    "=", 
    "*", 
    "&", 
    "|",
    "^",
    "#",
    "~"
]

OPERATORS_TO_VM_CODE = {
    "+": "add", 
    "/": "call Math.divide 2", 
    "-": "sub",
    ">": "gt", 
    "<": "lt", 
    "=": "eq",
    "*": "call Math.multiply 2", 
    "&": "and", 
    "|": "or",
    "^": "shiftleft",
    "#": "shiftright",
    "~": "not",
}

UNARY_TO_VM = {
    "~": "not",
    "-": "neg",
    "^": "shiftleft",
    "#": "shiftright",
}

COMMA = ","

EMPTY = ""

KIND_TO_SEGMENT = {
    "ARG": "argument",
    "VAR": "local",
    "STATIC": "static",
    "FIELD": "this",
}

PRIMITIVE_TYPES = {
    "int",
    "char",
    "boolean"
}
