'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger

from src.bl.visitor.nodetypes.source_unit import SourceUnit

class ElementaryTypeNameExpression(Node):
    
    def __init__(self, node_info, _previous = None, cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.__type = None
        self.__value = None
        self.__isConstant = None
        self.__isLValue = None
        self.__isPure = None
        self.__lValueRequested = None
        self.id = None
        self.__ETS_node_info(node_info.get('attributes'))
        SourceUnit.insert_operands_info(str(self.id), self)
        
        
        print("checking elementary type name expression ")
        print(self.__type)
        print(self.__value)
        print(self.__isConstant)
        print(self.__isLValue)
        print(self.__isPure)
        print(self.__lValueRequested)
        print(self.id)
        a = self.get_value()
        print("a is ", a)
        
        
        self.convert_to_java()
        
    def convert_to_java(self):
        
        java_type = self.get_java_equivalent_type()
        #print(java_type)
        
        java_code = java_type
         
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
            "bytes" : "byte[]"
            }
        
        # integer_type_size = {
        #     64 : "big"
        #     }
        
        type_name = self.get_value()
        type_size = None
        if type_name[0:3] == "uin":
            type_size = type_name[4:]
            type_name = "uint"
        
        elif type_name[0:3] == "int":
            type_size = type_name[3:]    
            type_name = "int"
        
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
    
    def get_is_constant(self):
        return self.__isConstant


    def get_is_lvalue(self):
        return self.__isLValue


    def get_is_pure(self):
        return self.__isPure


    def get_l_value_requested(self):
        return self.__lValueRequested


    def set_is_constant(self, value):
        self.__isConstant = value


    def set_is_lvalue(self, value):
        self.__isLValue = value


    def set_is_pure(self, value):
        self.__isPure = value


    def set_l_value_requested(self, value):
        self.__lValueRequested = value
            
    
    def get_imf(self):
        return self.get_equivalent_elementary_types(self.get_value())
    

    def get_type(self):
        return self.__type


    def get_value(self):
        return self.__value


    def set_type(self, value):
        self.__type = value


    def set_value(self, value):
        self.__value = value
        
    
    
    def get_variable_name(self):
        return self.get_value()

    def __ETS_node_info(self, info):
        self.set_type(info.get('type'))
        self.set_value(info.get('value'))
        self.set_is_constant(info.get("isConstant"))
        self.set_is_lvalue(info.get("isLValue"))
        self.set_is_pure(info.get("isPure"))
        self.set_l_value_requested(info.get("lValueRequested"))
        self.id = self.get_ast_id()
        