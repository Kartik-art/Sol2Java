'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes

class UsingForDirective(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
            
        self.set_name("For_Directive")
        self.set_cfg_id()
        child_nodes_list = [] #a list to maintain childnodes in order to  handle for directive
        
        for child in node_info.get("children"):
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id())
            print("child_node of for dir ", child_node.get_java_equivalent_code())
            child_nodes_list.append(child_node.get_java_equivalent_code())
            
        print("checking using for directive ")
        self.convert_to_java(child_nodes_list)
        
    def convert_to_java(self, child_nodes_list):
        java_code = "using " + child_nodes_list[0] + " for " + child_nodes_list[1] + ";"     
        
        # Check if the javaCode starts with "using SafeMath for "
        if (java_code.startswith("using SafeMath for ")): 
        # Change the javaCode to the desired line
            java_code = "private SafeMath safeMath = new SafeMath();";
            
        self.set_java_equivalent_code(java_code)
