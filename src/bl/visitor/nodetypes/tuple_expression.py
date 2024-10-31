'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
from src.bl.visitor.nodetypes.identifier import Identifier

class TupleExpression(Node):
    
    def __init__(self, node_info, _previous = None, cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.__argument_types = None
        self.__is_constant = None
        self.__is_inline_array = None
        self.__is_lvalue = None
        self.__is_pure = None
        self.__l_value_requested = None 
        self.__type = None
        
        self.__imf_repr = []
        self.__ETS_node_info(node_info.get('attributes'))
        
        '''
        print("checking tuple expression again")
        print(self.__argument_types)
        print(self.__is_constant)
        print(self.__is_inline_array)
        print(self.__is_lvalue)
        print(self.__is_pure)
        print(self.__l_value_requested)
        print(self.__type)
        print("tuple expression again checking done ")
        '''
        
        children = node_info.get('children')
        java_code_string_new = ""
        java_code_string = ""
        java_code = ""
        
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self, False)
            #print("checking tuple expression")
            #print(child_node.get_java_equivalent_code())
            java_code_string += child_node.get_java_equivalent_code() + ", "
            self.__imf_repr.append(child_node.get_imf())
            
        for char in java_code_string:
            if char == ";":
                continue
            else:
                java_code_string_new += char
        
        java_code_string_new = java_code_string_new[:-2]
        java_code = "[" + java_code_string_new + "]"
        self.set_java_equivalent_code(java_code)
        #print("java code string new is ", java_code_string_new)

    def get_argument_types(self):
        return self.__argument_types


    def get_is_constant(self):
        return self.__is_constant


    def get_is_inline_array(self):
        return self.__is_inline_array


    def get_is_lvalue(self):
        return self.__is_lvalue


    def get_is_pure(self):
        return self.__is_pure


    def get_l_value_requested(self):
        return self.__l_value_requested


    def get_type(self):
        return self.__type


    def get_imf(self):
        return tuple(self.__imf_repr)


    def set_argument_types(self, value):
        self.__argument_types = value


    def set_is_constant(self, value):
        self.__is_constant = value


    def set_is_inline_array(self, value):
        self.__is_inline_array = value


    def set_is_lvalue(self, value):
        self.__is_lvalue = value


    def set_is_pure(self, value):
        self.__is_pure = value


    def set_l_value_requested(self, value):
        self.__l_value_requested = value


    def set_type(self, value):
        self.__type = value


    def __ETS_node_info(self, info):
        self.set_argument_types(info.get('argumentTypes'))
        self.set_is_constant(info.get('isConstant'))
        self.set_is_inline_array("isInlineArray")
        self.set_is_lvalue("isLValue")
        self.set_is_pure(info.get('isPure'))
        self.set_l_value_requested(info.get('lValueRequested'))
        self.set_type(info.get('type'))
        
        
        