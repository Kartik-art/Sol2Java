'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger
from src.bl.visitor.nodetypes.source_unit import SourceUnit
from src.bl.visitor import nodetypes as ntypes

class ModifierDefinition(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
#         print('processing '+self.__class__.__name__+ str(self.get_ast_id()))
        """
        Node Specific Parameters
        """
        self.mod_name = None
        self.visibility = None
        self.id = None
        
        self.__ETS_node_info(node_info.get('attributes'))
        
        
        print("checking modifier definition ")
        
#         self.set_cfg_id("Modifier")
    
#         self.entry_node = Node("START_"+ self.mod_name)
#         self.exit_node = Node("STOP_"+ self.mod_name)
#         self.exit_node.set_name("return")
        '''CFG'''
#         current_cfg_node = self.construct_cfg_node(None) #Starting Point
#         self.entry_node.construct_cfg_node(None)
#         self.exit_node.construct_cfg_node(None)
        
    
        
    def get_imf(self):
        return None, self.mod_name
    
    
    def get_start_node(self):
        return self.entry_node
    
    
    def __ETS_node_info(self, info):
        self.mod_name = info.get('name')
        self.visibility = info.get('visibility')
        self.id = self.get_ast_id()


    def get_visibility(self):
        return self.visibility
    
    def get_mod_name(self):
        return self.mod_name


   


       