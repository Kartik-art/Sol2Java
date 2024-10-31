'''
Created on Dec 21, 2020

@author: ACER
'''
from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes


class SourceUnit(Node):
    
    token_info = dict()
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__)
        self.__contracts = []
        self.set_cfg_id("Source Code")
        self.current_cfg_node = self.construct_cfg_node(None)
        
        children = node_info.get('children')
        
        java_code = ""
        
        for child in children[1:]:
            child_node = getattr(ntypes, child.get('name'))(child, _previous, self.current_cfg_node)
            self.__contracts.append(child_node)
            _java_code = child_node.get_java_equivalent_code()
            java_code += _java_code if _java_code else ""
            
        self.set_java_equivalent_code(java_code)
        Node.set_java_code(self.get_java_equivalent_code()) 
        
    def get_dgraph(self):
        return self.current_cfg_node
    
    def get_contracts(self):
        return self.__contracts
            
    @staticmethod       
    def insert_operands_info(_id, obj):
        if _id in SourceUnit.token_info:
            if type(_id) is str:
                return SourceUnit.token_info.get(_id)
        else:
            SourceUnit.token_info[_id] = obj
            
            
    def get_token_info(self):
        return self.token_info
 