
TEMP_START = 5

SEGMENT_TO_ADDRESS = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "constant": "SP",
    "temp": "5",

}

C_ARITHMETIC = "C_ARITHMETIC"

ARITHMETIC_COMMANDS = [
        "sub", 
        "add", 
        "neg", 
        "eq", 
        "and", 
        "or", 
        "not", 
        "shiftleft", 
        "shiftright", 
        "gt", 
        "lt"
        ]

COMMANDS = {
    **dict.fromkeys(ARITHMETIC_COMMANDS, C_ARITHMETIC),
    "pop": "C_POP",
    "push": "C_PUSH",
    "label": "C_LABEL",
    "goto": "C_GOTO",
    "if": "C_IF",
    "if-goto": "C_IF",
    "func": "C_FUNCTION",
    "function": "C_FUNCTION",
    "return": "C_RETURN",
    "call": "C_CALL",
}

SEGMENTS = {
    "constant", 
    "local",
    "argument", 
    "this", 
    "that", 
    "temp"
}

func_diff = {}
