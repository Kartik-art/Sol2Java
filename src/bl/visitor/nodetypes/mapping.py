'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
from Cython.Compiler.TreePath import type_name


class Mapping(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self._from = None
        self._to = None
        
        children = node_info.get('children')
        
        child = children.pop(0)
        child_node = getattr(ntypes, child.get('name'))(child, _previous, False)
        print("mapping check 2 ",child_node.get_java_equivalent_code())
        self._from = child_node.get_type()
        
        child = children.pop(0)
        child_node = getattr(ntypes, child.get('name'))(child, _previous, False)
        print("mapping check ",child_node.get_java_equivalent_code())
        #self._to = child_node.get_type()
        
        
        
        print("checking mapping ")
        print(self._from)
        print(self._to)
        
        java_type_from = self.get_java_equivalent_type(self._from)
        java_type_to = self.get_java_equivalent_type(self._to)
        self.convert_to_java(java_type_from, java_type_to)
        
    def convert_to_java(self, java_type_from, java_type_to):
        # java_code = self.get_java_code()
        #
        # java_code = "" if java_code == "" else java_code+"\n"
        #

        #java_type_from = self.get_java_equivalent_type(map_from_type)
        #java_type_to = self.get_java_equivalent_type(map_to_type)
        
        java_code = "Map<" + java_type_from + ", " + java_type_to + ">"
        '''
        
        '''
        self.set_java_equivalent_code(java_code)
    
    def get_java_equivalent_type(self, type_namee):
        type_dict = {
            "bool" : "boolean",
            "string" : "String",
            "uint" : "int",
            "int" : "int",
            "address" : "String",
            "bytes" : "byte[]",
            "Hashtable" : "Hashtable"
            }
        
        # integer_type_size = {
        #     64 : "big"
        #     }
        
        type_name = type_namee
        type_size = None
        mapping_check = "mapping"
        
        if type_name == None:
            type_name = "string"
            
        elif type_name[0:3] == "uin":
            type_size = type_name[4:]
            type_name = "uint"
        
        elif type_name[0:3] == "int":
            type_size = type_name[3:]    
            type_name = "int"
            
        elif type_name.startswith(mapping_check):
            type_name = "Hashtable"
        
        if type_size:
            type_size = type_size.split('[')[0] #written by hp to handle array
            type_size = int(type_size)  #written by hp
            
        if type_name[:5] == "bytes":
            type_name = "bytes"
        #if type_size:
            #type_size = int(type_size)
        
        type_name = type_dict.get(type_name)
        
        if type_size and type_size>=64:
            type_name = "big "+ type_name
            
        return type_name
        
    def __ETS_node_info(self, info):
        self.set_argument_types(info.get('argumentTypes'))
        self.set_is_constant(info.get('isConstant'))
        self.set_is_lvalue(info.get('isLValue'))
        self.set_is_pure(info.get('isPure'))
        self.set_lvalue_requested(info.get('lValueRequested'))
        self.set_member_name(info.get('member_name'))
        self.set_referenced_declaration(info.get('referencedDeclaration'))
        self.set_type(info.get('type'))
        
    