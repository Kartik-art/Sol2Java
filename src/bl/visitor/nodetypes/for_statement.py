'''
Created on Jan 5, 2020

@author: ACER
'''

from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
from copy import deepcopy
class ForStatement(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.initialization_expression = True
        self.condition = True
        self.loop_expression = True
        self.loop_statements = None
        
        self.set_cfg_id("For")
        self.set_name("For")
        
        '''CFG'''
        self.current_cfg_node = self.construct_cfg_node(None) #Starting Point
        
        
        self.report_control_structure(self)
        
        children = self.__ETS_node_info(node_info)
        
        self.entry_node = None
        self.loop_cn = Node("CN_F")
        self.exit_node = Node("JN_F", jn_id=self.loop_cn.get_join_node_id())
        
        self.loop_cn.set_name("cnt")
        self.exit_node.set_name("brk")
        
        self.loop_cn.construct_cfg_node(None)
        self.exit_node.construct_cfg_node(None)
        if self.initialization_expression:
            initialization_expression_info = children.pop(0)
            self.initialization_expression_node = getattr(ntypes, initialization_expression_info.get('name'))(initialization_expression_info, "For_E", self.current_cfg_node)
            self.entry_node = self.initialization_expression_node
            self.entry_node.set_next_node(self.loop_cn, self.current_cfg_node)
            self.logger.info(str(self.entry_node.get_imf()))
        else:
            self.entry_node = self.loop_cn
        
        self.report_control_structure(self)
       
        current_node = self.loop_cn
        
        if self.condition:
            condition_info = children.pop(0)     
            self.condition = getattr(ntypes, condition_info.get('name'))(condition_info, "L_C", self.current_cfg_node)
            self.update_used_dec_def(self.condition)
            
            current_node.set_next_node(self.condition, self.current_cfg_node)
            #self.condition.set_next_node(self.exit_node)
            current_node = self.condition
            self.logger.info(str(current_node.get_imf()))
            
        statements_info = children.pop(0)
        self.loop_statements = getattr(ntypes, statements_info.get('name'))(statements_info, "L_B", self.current_cfg_node)
        
        self.update_used_dec_def(self.loop_statements)
        #USED... DEF... for block
        #TODO:
        ####
        
        entry_node, exit_node = self.loop_statements.get_entry_exit_nodes()       

        """
        Need to consider condition for only continue or break (LOOP CONTAINING single break or continue stmt)
        """
        current_node.set_next_node(entry_node, self.current_cfg_node)
        current_node.set_next_node(self.exit_node, self.current_cfg_node)
        exit_node.set_next_node(self.loop_cn, self.current_cfg_node)
    
        self.loop_cn.set_used_dec_def(self)
        self.loop_cn.set_opposite_node(self.exit_node)
        self.exit_node.set_used_dec_def(self)
        
        
#         self.draw_edges_from_BCR(self.current_cfg_node, self.loop_cn)
        self.draw_edges_from_BCR(self.current_cfg_node, self.exit_node)
        
        
        assert(self.extract_control_structure() == self)
        
        #self.add_to_cfg()
        if _is_cfg_node:
            _is_cfg_node.subgraph(self.current_cfg_node)
        
        print("checking for loop ")
        print(self.loop_statements.get_java_equivalent_code())
        
        input_lines = self.loop_statements.get_java_equivalent_code()   #from here writing code to extract  the last line 
        lines = input_lines.split("\n")
        loop_inc_dec = lines[-3]                                        #initially extracting the last line and pasting it in round bracket
        loop_inc_dec_new = ""
        loop_stmts_2 = ""
        for i in range(len(loop_inc_dec)-1):
            loop_inc_dec_new += loop_inc_dec[i]
        k = len(lines) - 3
        for i in range(len(lines)): #then extracting all the lines except the last line and pasting it in loop statements
            if(i == k): #for better understanding print the loop_statements node yourself
                continue;
            else:
                loop_stmts_2 += lines[i]
                loop_stmts_2 += "\n"
        
        self.convert_to_java(loop_inc_dec_new, loop_stmts_2)
        
    def convert_to_java(self, loop_inc_dec_new, loop_stmts_2):
        java_code = "for" + "(" + self.entry_node.get_java_equivalent_code() + self.condition.get_java_equivalent_code()+ ";" + loop_inc_dec_new + ")" +  loop_stmts_2
        self.set_java_equivalent_code(java_code)
         
            
    def get_imf(self):
        return None, self.get_name()
    
    
#     def get_join_nodes(self):
#         return self.loop_cn, self.exit_node
    
    
    def __ETS_node_info(self, info):
        attributes = info.get('attributes')
        if attributes:
            self.initialization_expression = attributes.get('initializationExpression', True)
            self.condition = attributes.get('condition', True)
            self.loop_expression = attributes.get('loopExpression', True)
        
        children = info.get("children")
        if self.loop_expression:
            block_stmts = children.pop(-1)
            #print(block_stmts)
            loop_expression = children.pop(-1)
            
            if block_stmts.get('name') != 'Block':
                block_stmts = {'id':block_stmts.get('id')*-1, 'src':block_stmts.get('src'), 'name':'Block', 'children':[deepcopy(block_stmts)]}            
            block_stmts['children'].append(loop_expression)
            
            children.append(block_stmts)
            
        return children

