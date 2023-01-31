"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import consts

class TableRecord:
    def __init__(self, type: str, kind: str, num: int) -> None:
        self.type = type
        self.num = num
        self.kind = kind
    
    def __str__(self) -> str:
        if self.type and self.kind:
            return self.type + "-" + self.kind + "-" + str(self.num) + "-"
        return ""
    
class Table:
    def __init__(self) -> None:
        self.data: dict[str, TableRecord] = {}
        self.counters = {
            "STATIC": 0, 
            "FIELD": 0, 
            "ARG": 0, 
            "VAR": 0
        }
        
    def add(self, name: str, type: str, kind: str) -> None:
        self.data[name] = TableRecord(type, kind, self.counters[kind])
        self.counters[kind]+=1
            
        


class SymbolTable:
    """A symbol table that associates names with information needed for Jack
    compilation: type, kind and running index. The symbol table has two nested
    scopes (class/subroutine).
    """

    def __init__(self) -> None:
        """Creates a new empty symbol table."""
        # Your code goes here!
        self.curr_class = ""
        self.curr_subrn = ""
        self.class_t =  Table()
        self.subr_t = Table()
        

    def start_subroutine(self, is_method: bool) -> None:
        """Starts a new subroutine scope (i.e., resets the subroutine's 
        symbol table).
        """
        # Your code goes here!
        self.subr_t = Table()
        if is_method:
            self.subr_t.add("this", self.curr_class, "ARG")

    def define(self, name: str, type: str, kind: str) -> None:
        """Defines a new identifier of a given name, type and kind and assigns 
        it a running index. "STATIC" and "FIELD" identifiers have a class scope, 
        while "ARG" and "VAR" identifiers have a subroutine scope.

        Args:
            name (str): the name of the new identifier.
            type (str): the type of the new identifier.
            kind (str): the kind of the new identifier, can be:
            "STATIC", "FIELD", "ARG", "VAR".
        """
        # Your code goes here!
        if kind in ["STATIC", "FIELD"]:
            self.class_t.add(name, type, kind)
        elif kind in ["ARG", "VAR"]:
            self.subr_t.add(name, type, kind)

    def var_count(self, kind: str) -> int:
        """
        Args:
            kind (str): can be "STATIC", "FIELD", "ARG", "VAR".

        Returns:
            int: the number of variables of the given kind already defined in 
            the current scope.
        """
        # Your code goes here!
        return self.subr_t.counters[kind] + self.class_t.counters[kind]
    
    def _record_of(self, name: str) -> TableRecord:
        try:
            return self.subr_t.data[name]
        except KeyError:
            try:
                return self.class_t.data[name]
            except KeyError:
                # if the code is error free:
                # means that we encountered a subroutine name or a class name
                return None
            
    def kind_of(self, name: str) -> str:
        """
        Args:
            name (str): name of an identifier.

        Returns:
            str: the kind of the named identifier in the current scope, or None
            if the identifier is unknown in the current scope.
        """
        # Your code goes here!
        record  = self._record_of(name)
        if record:    
            return self._record_of(name).kind

    def segment_of(self, name: str) -> str:
        record  = self._record_of(name)
        if record:    
            return consts.KIND_TO_SEGMENT[
                self._record_of(name).kind
                ]

    def type_of(self, name: str) -> str:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            str: the type of the named identifier in the current scope.
        """
        # Your code goes here!
        record  = self._record_of(name)
        if record:    
            return self._record_of(name).type

    def index_of(self, name: str) -> int:
        """
        Args:
            name (str):  name of an identifier.

        Returns:
            int: the index assigned to the named identifier.
        """
        # Your code goes here!
        record  = self._record_of(name)
        if record:    
            return self._record_of(name).num
