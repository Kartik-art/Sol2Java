'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
import sys
sys.path.append("C:\\Users\\KARTIK KAUSHIK\\Desktop\\eclipse-workspace\\Ethero_Pashanti_Vishleshna_Tool_21\\src\\bl\\visitor\\nodetypes")
from src.bl.visitor.nodetypes.assignment import Assignment
 
class IndexAccess(Node):
    
    def __init__(self, node_info, _previous = None, cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.argumentTypes = None
        self.is_constant = False
        self.is_lvalue = True
        self.is_pure = False
        self.lvalue_requested = False
        self.type  = None
        self.__ETS_node_info(node_info.get('attributes'))
        
        children = node_info.get('children')
        
        self.__imf_repr = []
        
        child_list = [] #written by hp to handle index access
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self, False)
            '''
            print("checking index access 2", child_node.get_java_equivalent_code())
            child_type_to_be_used_by_assignment = child_node.type
            print("child_type_to_be_used_by_assignment is ", child_type_to_be_used_by_assignment)
            print(child_node.type)
            print(self.argumentTypes)
            print(self.is_constant)
            print(self.is_lvalue)
            print(self.is_pure)
            print(self.lvalue_requested)
            print(self.type)
            '''
            child_list.append(child_node.get_java_equivalent_code())
            x = child_node.get_imf()
            if isinstance(x, tuple) and len(self.__imf_repr)==0:
                self.__imf_repr.extend(list(x))
            else: 
                self.__imf_repr.append(child_node.get_imf())
            #Used.. Defined
            self.used.extend(child_node.used)
            self.dec_def.extend(child_node.dec_def)
        #print(child_list)
        self.convert_to_java(child_list)
        print("checking index access ")
        print(self.argumentTypes)
        print(self.is_constant)
        print(self.is_lvalue)
        print(self.is_pure)
        print(self.lvalue_requested)
        print(self.type)
        
        #obj=Assignment(node_info)
        #print(obj.name)
    
    #def child_type(self, child_type_to_be_used_by_assignment):
    #    return child_type_to_be_used_by_assignment
        
    def convert_to_java(self, child_list):
        #if child_type[0:7] == "mapping" :
             
        java_code = " " + child_list[0] + "[" + child_list[1] + "]"
        self.set_java_equivalent_code(java_code)
        
    def get_imf(self):
        return tuple(self.__imf_repr)
  
        
    def get_argument_types(self):
        return self.argumentTypes


    def get_is_constant(self):
        return self.is_constant


    def get_is_lvalue(self):
        return self.is_lvalue


    def get_is_pure(self):
        return self.is_pure


    def get_lvalue_requested(self):
        return self.lvalue_requested


    def get_type(self):
        return self.type


    def set_argument_types(self, value):
        self.argumentTypes = value


    def set_is_constant(self, value):
        self.is_constant = value


    def set_is_lvalue(self, value):
        self.is_lvalue = value


    def set_is_pure(self, value):
        self.is_pure = value


    def set_lvalue_requested(self, value):
        self.lvalue_requested = value


    def set_type(self, value):
        self.type = value
    
    
    def __ETS_node_info(self, info):
        self.set_argument_types(info.get('argumentTypes'))
        self.set_is_constant(info.get('isConstant'))
        self.set_is_lvalue(info.get('isLValue'))
        self.set_is_pure(info.get('isPure'))
        self.set_lvalue_requested(info.get('lValueRequested'))
        self.set_type(info.get('type'))
        