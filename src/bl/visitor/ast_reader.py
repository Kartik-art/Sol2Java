'''
Created on Jul 26, 2019
@author: JH-ANIC
'''
from src.bl.visitor.node_processor import Node
import src.bl.visitor.nodetypes as node_types


class ASTToCFGObject(object):
    
    def __init__(self, source_code, ast_data, _src_label = False):
        Node.reset(source_code , _src_label)
        self.__cfg_object = getattr(node_types, ast_data['name'])(ast_data, None)
        print("AST::",Node.get_java_code())
        self.__java_source_code = Node.get_java_code()
        
    def get_cfg_object(self):
        return self.__cfg_object
    
    def get_java_code(self):
        return self.__java_source_code
