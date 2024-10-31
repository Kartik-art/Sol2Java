'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node
from src.bl.visitor.nodetypes.source_unit import SourceUnit


class Literal(Node):
    
    def __init__(self, node_info,  _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.argumentTypes = None
        self.hexvalue = None
        self.isConstant = None
        self.isLValue = None
        self.isPure = None
        self.lValueRequested = None
        self.subdenomination = None
        self.token = None
        self.type = None
        self.value = None
        self.id = None
        
        self.__ETS_node_info(node_info.get('attributes'))
        if _is_cfg_node:
            self.set_cfg_id()
            self.construct_cfg_node(_is_cfg_node)   
        SourceUnit.insert_operands_info(self.id, self)
        
        self.set_java_equivalent_code(self.value)
        
            
    def get_argument_types(self):
        return self.argumentTypes


    def get_hexvalue(self):
        return self.hexvalue


    def get_is_constant(self):
        return self.isConstant


    def get_is_lvalue(self):
        return self.isLValue


    def get_is_pure(self):
        return self.isPure


    def get_l_value_requested(self):
        return self.lValueRequested


    def get_subdenomination(self):
        return self.subdenomination


    def get_token(self):
        return self.token


    ''' Returning token... instead of type'''
    def get_type(self):
        return self.token


    def get_value(self):
        return self.value


    def get_id(self):
        return self.id
    

    def get_imf(self):
        return self.value if self.get_type() == "number" else '"'+self.value +'"'
    
    
    def set_type(self, value):
        self.type = value


    def set_value(self, value):
        self.value = value
        if self.get_subdenomination():
            self.value += " "+ self.subdenomination
        

    def set_id(self, value):
        self.id = value
        
        
    def __ETS_node_info(self, info):
        self.argumentTypes = info.get('argumentTypes')
        self.hexvalue = info.get('hexvalue')
        self.isConstant = info.get('isConstant')
        self.isLValue = info.get('isLValue')
        self.isPure = info.get('isPure')
        self.lValueRequested = info.get('lValueRequested')
        self.subdenomination = info.get('subdenomination')
        self.token = info.get('token')
        self.type = info.get('type')
        self.set_value(info.get('value'))
        self.id = self.get_ast_id()    
        
    

