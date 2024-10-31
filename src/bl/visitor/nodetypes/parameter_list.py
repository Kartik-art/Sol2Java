'''
Created on Nov 30, 2020

@author: ACER
'''


from . import Node, get_logger

from src.bl.visitor import nodetypes as ntypes


class ParameterList(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
#         print('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        children = node_info.get('children')
        self.entry_node = None
        self.exit_node = None
        
        if _is_cfg_node:
            self.set_cfg_id("Parameter")
        
        processed = 0
        no_of_parameters = len(children)
        curr_node = None
        
        if not _previous:
            raise Exception("Unexpected Function DG missing")
        java_code = "("
        
        while no_of_parameters > processed:
            child = children.pop(0)
            child_node = getattr(ntypes, child.get('name'))(child, _previous, _is_cfg_node)
            #if not child_node.type_declaration_only:
            if not self.entry_node:
                self.entry_node = child_node
            else:
                curr_node.set_next_node(child_node, _is_cfg_node)
            curr_node = child_node
            
            self.logger.info(str(curr_node.get_imf()))
            #EIF
            processed += 1  
            
            print("checking para_list ", child_node)
            if processed > 1:
                java_code += ", "
            java_code += child_node.get_java_equivalent_code()[:-1]
            
              
        self.exit_node = curr_node
        java_code += ")"
        self.set_java_equivalent_code(java_code)
        
        
    def get_imf(self):
        return self.get_cfg_id()
    
#         if self.entry_node:
#             print("Entry:", self.entry_node.get_cfg_id())
#         if self.exit_node:
#             print("Exit:", self.exit_node.get_cfg_id())
#         input("Check Entry Exit")