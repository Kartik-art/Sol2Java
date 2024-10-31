'''
Created on Dec 12, 2020

@author: ACER
'''
from . import Node, get_logger

from src.bl.visitor import nodetypes as ntypes

class ArrayTypeName(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)    
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.type = None
        self.length = None
        
        self.__ETS_node_info(node_info.get('attributes')) 
        children = node_info.get('children')
        child = children.pop(0)
        child_node = getattr(ntypes, child.get('name'))(child, self, False)
        #print(child_node.get_java_equivalent_code())    #written by hp
        dt_name = child_node.get_type()
        #print(dt_name)
        #TODO need to process to extract user declared type
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self, False)
            array_size = child_node.get_java_equivalent_code()    #written by hp
            #print("array size is ",array_size)    #written by hp
        self.set_data_type(dt_name)
        
        
        print("checking array type_name ")
        print(self.type)
        print(self.length)
        
        
        self.convert_to_java()
        
    def convert_to_java(self):
        
        java_code = ""
        java_type = self.get_java_equivalent_type()
        #print(java_type)
        
        java_code += java_type + "["+  "]" 
        #if not r_value: 
        #    java_code = java_type + " " + self.get_variable_name() + ";"
        #else:
        #    java_code = java_type + " " + self.get_variable_name() + " = " + r_value + ";"
        
        self.set_java_equivalent_code(java_code)
        
       
    def get_java_equivalent_type(self):
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
        
        type_name = self.get_type()
        type_size = None
        mapping_check = "mapping"
        if type_name[0:3] == "uin":
            type_size = type_name[4:]
            type_name = "uint"
        
        elif type_name[0:3] == "int":
            type_size = type_name[3:]    
            type_name = "int"
            
        elif type_name[0:7] == "address":
            type_name = "address"
            
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
        self.set_length(info.get('length'))
        self.set_type(info.get('type'))    
        
        
    def set_data_type(self, dt_name):
        self.data_type = dt_name
    
    
    def get_data_type(self):
        return self.data_type
    
        
    def get_type(self):
        return self.type


    def get_length(self):
        return self.__length


    def set_type(self, value):
        self.type = value


    def set_length(self, value):
        self.__length = value


