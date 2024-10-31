'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes

class FunctionCall(Node):
    
    def __init__(self, node_info, _previous = None, cfg_node = True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        if cfg_node:
            self.set_cfg_id()
        
        self.__argument_types = None
        self.__is_constant = None
        self.__is_lvalue = None
        self.__is_pure = None
        self.__is_struct_constructor_call = None
        self.__l_value_requested = None 
        self.__names = None
        self.__type = None
        self.__type_conversion = None
        
        self.__imf_repr = []
        self.__ETS_node_info(node_info.get('attributes'))
        
        children = node_info.get('children')
        child = children.pop(0)
        child_node = getattr(ntypes, child.get('name'))(child, self, False)
        func_name = child_node.get_java_equivalent_code()
        self.__imf_repr.append(child_node.get_imf())
        params = []
        param = ""
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self, False)
            func_param = child_node.get_java_equivalent_code()
            param += func_param + ","   #extract all parameters passed into the  function and inserting comma between them 
            params.append(child_node.get_imf())
            
        self.__imf_repr.append(params)
        
        param = param[:-1]  #last character is a colon, so drop it 
        self.convert_to_java(func_name, param)
        
    def convert_to_java(self, func_name, param):
        java_code = func_name + "(" + param + ")" 
        self.set_java_equivalent_code(java_code)

    def get_argument_types(self):
        return self.__argument_types


    def get_is_constant(self):
        return self.__is_constant


    def get_is_lvalue(self):
        return self.__is_lvalue


    def get_is_pure(self):
        return self.__is_pure


    def get_is_struct_constructor_call(self):
        return self.__is_struct_constructor_call


    def get_l_value_requested(self):
        return self.__l_value_requested


    def get_names(self):
        return self.__names


    def get_type(self):
        return self.__type


    def get_type_conversion(self):
        return self.__type_conversion


    def get_imf(self):
        return tuple(self.__imf_repr)


    def set_argument_types(self, value):
        self.__argument_types = value


    def set_is_constant(self, value):
        self.__is_constant = value


    def set_is_lvalue(self, value):
        self.__is_lvalue = value


    def set_is_pure(self, value):
        self.__is_pure = value


    def set_is_struct_constructor_call(self, value):
        self.__is_struct_constructor_call = value


    def set_l_value_requested(self, value):
        self.__l_value_requested = value


    def set_names(self, value):
        self.__names = value


    def set_type(self, value):
        self.__type = value


    def set_type_conversion(self, value):
        self.__type_conversion = value


    def set_imf_repr(self, value):
        self.__imf_repr = value
        

    def __ETS_node_info(self, info):
        self.set_argument_types(info.get('argumentTypes'))
        self.set_is_constant(info.get('isConstant'))
        self.set_is_lvalue("isLValue")
        self.set_is_pure(info.get('isPure'))
        self.set_is_struct_constructor_call("isStructConstructorCall")
        self.set_l_value_requested(info.get('lValueRequested'))
        self.set_names("names")
        self.set_type(info.get('type'))
        self.set_type_conversion("type_conversion")
    
    
        