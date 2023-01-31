import re
from consts import *


def sanitize(s: str) -> str:
    for spacer in [' ', '\n', '\t']:
        s = s.strip(spacer)
    s = re.sub(r'(?://[^\n]*|/\*(?:(?!\*/).)*\*/)', '', s)
    return s

class Command:
    """Encapsulates a command properties
    """

    def __init__(self, raw: str) -> None:
        self.raw: str = raw
        self.sanitized: str = sanitize(raw)
        
        self.arg1: str = None
        self.arg2: int = None
        self.type: int = None

        self.parse_and_set_command(self.sanitized)
    

    def parse_and_set_command(self, s: str):
        """
        Gets a sanitized string command
        Returns:
                str: the type of the current VM command.
                "C_ARITHMETIC" is returned for all arithmetic commands.
                For other commands, can return:
                "C_PUSH", "C_POP", "C_LABEL", "C_GOTO", "C_IF", "C_FUNCTION",
                "C_RETURN", "C_CALL".
        """
        
        parts = s.split()
        
        if len(parts) == 1:
            self.short = parts[0]
            self.arg1 = parts[0]
            self.type = COMMANDS[parts[0]]
        elif len(parts) == 3:
            try:
                self.short = parts[0]
                self.type = COMMANDS[parts[0]]
                self.arg1 = parts[1]
                self.arg2 = parts[2]
            except (ValueError, KeyError) as e:
                print("ERROR: " + e + "wrong command: [" + self.sanitized + "]")
        elif len(parts) == 2:
            self.type = COMMANDS[parts[0]]
            self.arg1 = parts[1]
        else:
            print("ERROR: wrong command: [" + self.sanitized + "]")
        
