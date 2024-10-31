'''
Created on Nov 30, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor.nodetypes.source_unit import SourceUnit
from src.bl.visitor import nodetypes as ntypes

class NewExpression(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        children = node_info.get('children')
        self.data_type_name = None
        
        if len(children)>1:
            raise Exception("Not handled... MC IN NE")
        
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), _is_cfg_node)
            data_type = child_node.get_type()
            if " " in data_type:
                data_type = data_type[data_type.rindex(" ")+1:]
            self.data_type_name = data_type 
            self.used.extend(child_node.used)
            self.dec_def.extend(child_node.dec_def)
            self.set_java_equivalent_code(child_node.get_java_equivalent_code()) #written by hp
            print("checking new expression")
            print(child_node.get_java_equivalent_code())
            childd = child_node.get_java_equivalent_code()
            print(self.data_type)
            self.convert_to_java(childd)
        SourceUnit.insert_operands_info(str(self.get_ast_id()), self)
        
    def convert_to_java(self, childd):
        # java_code = self.get_java_code()        
        # java_code = "" if java_code == "" else java_code+"\n"
        java_code = "new " + childd + ";"
        self.set_java_equivalent_code(java_code)
        
            
        
        
    
    
    def get_imf(self):
        return self.get_ast_id()
    
    
    def get_variable_name(self):
        return "new "+self.data_type_name
    
    
    def get_type(self):
        return "new"