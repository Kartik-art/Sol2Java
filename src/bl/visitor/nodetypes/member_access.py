'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes


class MemberAccess(Node):
    
    def __init__(self, node_info, _previous = None, cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.__argument_types = None
        self.__is_constant = False
        self.__is_lvalue = True
        self.__is_pure = False
        self.__lvalue_requested = False
        self.__member_name = None
        self.__referenced_declaration = None
        self.__type  = None
        
        self.__ETS_node_info(node_info.get('attributes'))
        
        self.__imf_repr = []
        
        children = node_info.get('children')
        
        child = children.pop(0)
        child_node = getattr(ntypes, child.get('name'))(child, self, False)
        print("checking member access ", child_node.get_java_equivalent_code())
    
        childd = child_node.get_java_equivalent_code()  # written by hp to handle member access
        self.__imf_repr.append(child_node.get_imf())
        self.__imf_repr.append( self.__referenced_declaration if self.__referenced_declaration else self.__member_name)
        
        # Store the member name in an additional string
        member_name_str = self.__member_name
    
        print(self.__member_name)
        print(self.__type)
    
        # Pass both childd and the member_name_str to convert_to_java
        self.convert_to_java(childd, member_name_str)

    def convert_to_java(self, childd, member_name_str):
        # Compare the values of childd and member_name_str
        if childd == "msg" and member_name_str == "sender":
            java_code = "msg_sender"
        else:
            java_code = childd + "." + self.__member_name
    
        self.set_java_equivalent_code(java_code)
        
    def get_imf(self):
        return tuple(self.__imf_repr)
       
        
    def get_argument_types(self):
        return self.__argument_types


    def get_is_constant(self):
        return self.__is_constant


    def get_is_lvalue(self):
        return self.__is_lvalue


    def get_is_pure(self):
        return self.__is_pure


    def get_lvalue_requested(self):
        return self.__lvalue_requested


    def get_member_name(self):
        return self.__member_name


    def get_referenced_declaration(self):
        return self.__referenced_declaration


    def get_type(self):
        return self.__type


    def set_argument_types(self, value):
        self.__argument_types = value


    def set_is_constant(self, value):
        self.__is_constant = value


    def set_is_lvalue(self, value):
        self.__is_lvalue = value


    def set_is_pure(self, value):
        self.__is_pure = value


    def set_lvalue_requested(self, value):
        self.__lvalue_requested = value


    def set_member_name(self, value):
        self.__member_name = value


    def set_referenced_declaration(self, value):
        self.__referenced_declaration = value


    def set_type(self, value):
        self.__type = value

  
    def __ETS_node_info(self, info):
        self.set_argument_types(info.get('argumentTypes'))
        self.set_is_constant(info.get('isConstant'))
        self.set_is_lvalue(info.get('isLValue'))
        self.set_is_pure(info.get('isPure'))
        self.set_lvalue_requested(info.get('lValueRequested'))
        self.set_member_name(info.get('member_name'))
        self.set_referenced_declaration(info.get('referencedDeclaration'))
        self.set_type(info.get('type'))
    