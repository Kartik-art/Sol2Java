from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
from copy import deepcopy

class IfStatement(Node):
    def __init__(self, node_info, _previous = None, _is_cfg_node = True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.entry_node = None
        self.condition = None
        self.true_block = True
        self.false_block = True
        self.exit_node = Node("JN_IF")
        
        self.set_cfg_id("IF")
        self.set_name("IF")
        
        '''CFG'''
        self.current_cfg_node = self.construct_cfg_node(None) #Starting Point
        self.exit_node.construct_cfg_node(None)
        
        children = self.__ETS_node_info(node_info) 
         
        condition_node = children.pop(0)
        self.condition = getattr(ntypes, condition_node.get('name'))(condition_node, "If_C", self.current_cfg_node)
        self.update_used_dec_def(self.condition)
        
        self.entry_node = self.condition
        
        count = len(children)
        
        if self.true_block:
            true_block = children.pop(0)
            self.true_block = getattr(ntypes, true_block.get('name'))(true_block, "If_T" if count > 1 else "If_TO", self.current_cfg_node)
        self.__link_blocks(self.true_block, "T")
        
        self.update_used_dec_def(self.condition)
        if len(children) == 0:
            self.false_block = None
            
        if self.false_block:
            false_block = children.pop(0)
            self.false_block = getattr(ntypes, false_block.get('name'))(false_block, "If_F", self.current_cfg_node)
        
        self.__link_blocks(self.false_block, "F")
        
        if self.exit_node.get_previous_count() == 0:
            self.exit_node.set_unreachable()
        
        self.update_used_dec_def(self.true_block)    
        self.update_used_dec_def(self.false_block)
        
        self.exit_node.update_used_dec_def(self)
        self.exit_node.update_used_dec_def(self)  
        if _is_cfg_node:
            _is_cfg_node.subgraph(self.current_cfg_node)
            
        
        print("checking if_statement")  #written by hp, line 62 to 66
        print("entry_node: ", self.entry_node)
        print("condition: ", self.condition)
        print("true_block: ", self.true_block)
        print("false_block: ",  self.false_block)
        
        self.convert_to_java()
        
        
    def convert_to_java(self):
        java_code = "if" + "(" + self.condition.get_java_equivalent_code() + ")"+self.true_block.get_java_equivalent_code()
        if self.false_block:
            java_code+= "else" + self.false_block.get_java_equivalent_code()     
        self.set_java_equivalent_code(java_code)
        
    def __ETS_node_info(self, info):
        attributes = info.get('attributes')
        if attributes:
            self.false_block = attributes.get('falseBody', True)
            self.true_block = attributes.get('trueBody', True)
            
        children = info.get("children")
        indices = []
        for index, child in enumerate(children[1:]):
            if child.get('name') != 'Block':
                indices.append(index)
        
        for index in indices:
            block_stmts = children.pop(index+1)
            block_stmts = {'id':block_stmts.get('id')*-1, 'src':block_stmts.get('src'), 'name':'Block', 'children':[deepcopy(block_stmts)]} 
            children.insert(index+1, block_stmts)
        return children
            
    def get_imf(self):
        return "IF", self.get_name()


    def __link_blocks(self, _block, btype):
        if _block:
            entry_node, exit_node = _block.get_entry_exit_nodes()
            self.entry_node.set_next_node(entry_node, self.current_cfg_node, btype)
            #in case of return from condition exit_node doesnt exists
            if exit_node:
                exit_node.set_next_node(self.exit_node, self.current_cfg_node)
        else:
            self.entry_node.set_next_node(self.exit_node, self.current_cfg_node, btype)
            
            