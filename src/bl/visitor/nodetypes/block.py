'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger

from src.bl.visitor import nodetypes as ntypes

class Block(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        
        children = node_info.get('children')
        self.set_cfg_id("Block")
        self.set_name(_previous)
        
        '''CFG'''
        self.current_cfg_node = self.construct_cfg_node(None) #Starting Point
        if not self.current_cfg_node:
            raise Exception("Required new DG here")
        
        self.__ETS_node_info(children)
        
        if _is_cfg_node:
            _is_cfg_node.subgraph(self.current_cfg_node)
            
       
        
    def __ETS_node_info(self, children):
        
        self.set_cfg_id("Block")
        
        self.entry_node = None
        self.exit_node = None # also represents return nodes
        
#         no_of_children = len(children)
        entry_node, exit_node, temp = None, None, None
        
#         if no_of_children > 0:
#             child = children.pop(0)
#             print(child.get('name'))
#             input("DW-BC?")
#             child_node = getattr(ntypes, child.get('name'))(child, self.is_in_loop(), self.current_cfg_node)
#             print(child_node)
#             self.update_used_dec_def(child_node)
#             self.entry_node, exit_node = child_node.get_entry_exit_nodes()
#             print("Test:", child_node.get_name(), self.entry_node.get_cfg_id(), self.entry_node.get_name())
#             temp = exit_node
#             if temp:
#                 self.logger.info(str(temp.get_imf()))
           
        java_code = "{"+"\n"
        
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self.is_in_loop(), self.current_cfg_node)
            self.update_used_dec_def(child_node)
            entry_node, exit_node = child_node.get_entry_exit_nodes()
            if not self.entry_node:
                self.entry_node = entry_node
            '''
            print(child_node.__class__)
            print("Java code is here ")
            print(type(java_code))
            print(type(child_node.get_java_equivalent_code()))
            '''
            print("checking block childnodes for handling member access ",child_node.get_java_equivalent_code())
            '''
            print(type("\n"))
            '''
            '''
            child_to_check = ""
            child_to_check = child_node.get_java_equivalent_code()  # child_to_check has been used in place of child_node.get_java_equivalent_code() 
            if "msg.value" in child_to_check:
                java_code += "//"+ child_node.get_java_equivalent_code() +"\n"
                continue
            
            if child_to_check.strip().startswith("require"):
                java_code += "//"+ child_node.get_java_equivalent_code() +"\n"
                continue
            
            
            java_code += child_node.get_java_equivalent_code() +"\n"
            '''
#             if child_node.get_name() in ["For"]:
#                 self.draw_edges_from_BCR(child_node.current_cfg_node, child_node.loop_cn)
#                 self.draw_edges_from_BCR(child_node.current_cfg_node, child_node.exit_node)
                #self.current_cfg_node.subgraph(child_node.current_cfg_node) 
            n_name = child_node.get_name()
            
            if n_name in ["Return", "Break", "Continue"]:                
                #internal stmts cfg also possible with entry and exit node info instead
                if n_name == "Return":
                    return_node = self.get_return_node()
                    if not exit_node: #Literals Identifiers etc
                        exit_node = entry_node
                    if temp:
                        temp.set_next_node(child_node, self.current_cfg_node)#75 at 72
                    exit_node.set_next_node(return_node, self.current_cfg_node, extra = False)
                else:
                    b_node, c_node = self.get_break_continue()
                    
                    if n_name == "Continue":
                        if temp:
                            temp.set_next_node(c_node, self.current_cfg_node, extra = False)
                    else: #For Break
                        if temp:
                            temp.set_next_node(b_node, self.current_cfg_node, extra = False)
                        
                temp = None
            else:
                if temp:
                    temp.set_next_node(entry_node, self.current_cfg_node, spec = "cnt" if entry_node.get_name() == "cnt" else None )
                else:
                    exit_node.set_unreachable()
                temp = exit_node
                
            if temp:
                print(temp.get_name())
                self.logger.info(str(temp.get_imf()))
            
            child_to_check = ""
            parameter = ""
            child_to_check = child_node.get_java_equivalent_code()  # child_to_check has been used in place of child_node.get_java_equivalent_code() 
            if "msg.value" in child_to_check:
                java_code += "//"+ child_node.get_java_equivalent_code() +"\n"
                continue
            
            if child_to_check.strip().startswith("require"):
                java_code += "//"+ child_node.get_java_equivalent_code() +"\n"
                continue
            
            if "msg.sender" in child_to_check and ("+" in child_to_check or "-" in child_to_check):
                java_code += "//"+ child_node.get_java_equivalent_code() +"\n"
                continue
            
            if "msg.sender.send" in child_to_check:
                start_index = child_to_check.find("(")+1
                end_index = child_to_check.find(")")
                parameter = child_to_check[start_index:end_index].strip()
                java_code += "Account accountInstance = new Account('""', 0.0f);\n"
                java_code += "return accountInstance.send" + "(" + parameter + ");\n" 
                continue
            
            if "msg.sender.transfer" in child_to_check:
                start_index = child_to_check.find("(")+1
                end_index = child_to_check.find(")")
                parameter = child_to_check[start_index:end_index].strip()
                java_code += "Account accountInstance = new Account('""', 0.0f);\n"
                java_code += "return accountInstance.transfer" + "(" + parameter + ");\n" 
                continue
            
            java_code += child_node.get_java_equivalent_code() +"\n"
            
            
        self.exit_node = temp
        java_code+="}"+"\n"
        
        self.set_java_equivalent_code(java_code)
        #print("block checking ")
        #print(self.exit_node)
        #block_desc = exit_node.get_java_equivalent_code()
        #print(block_desc)
        
        #print(block_desc)
        
    def get_imf(self):
        return "Block", self.get_name()

