'''
Created on Feb 20, 2021

@author: ACER
'''
from . import Node, get_logger

from src.bl.visitor import nodetypes as ntypes


class EmitStatement(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+ str(self.get_ast_id()))
        
        self.set_cfg_id()
        #self.generate_cfg_node()
        emit_stmt = ""
        children = node_info.get('children')
        print("Emit statement being executed ")
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self, False)
            emit_stmt = child_node.get_java_equivalent_code()
        self.construct_cfg_node(None)
        self.convert_to_java(emit_stmt)  #written by hp
        
    def convert_to_java(self, emit_stmt):
        # java_code = self.get_java_code()        
        # java_code = "" if java_code == "" else java_code+"\n"
        java_code = "// " + "emit " + emit_stmt + ";" 
        self.set_java_equivalent_code(java_code)
   