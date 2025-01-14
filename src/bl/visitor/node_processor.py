'''
Created on Nov 30, 2020

@author: ACER
'''
from builtins import set
from copy import deepcopy
from src.bl.visitor.cfg_generator import CFGBuilder
import logging
import logging.handlers

class Node(object):
    __java_code = ""
    __cfg_node_number = 0
    __join_nodes = 0
    __source_code = None
    __cfg_builder = None
    #Need to add label for src or id
    __src_label = None
    
    __return_node = None
    __control_structures = []
    __elementary_types = dict()
    #logger = logging.getLogger('Visitor')
    __user_scope = None
    
    def __init__(self, node_info, _lb = None, jn_id = None):
        # For CFG
        self.entry_node = self
        self.exit_node = self
        self.next_node = None
        self.previous_node = None
        self.__previous_count = 0
        self.__imf_repr = None
        self.__src_indices = None
        self.data_type = None
        
        self.used = []
        self.dec_def = []
        self.visit_count = 0
        self.previous_count = 0
        self.used_def = set()
        self.__is_unreachable = False
        self.__visited = False
        self.__is_in_loop = _lb in ["L_B", "L_C", True]
        self.reset = True
        self.__node_type = None
        self.__java_equivalent_code = None
        if isinstance(node_info, str):
            if node_info in ["CN_F", "JN_F", "CN_W", "JN_W", "EN_DW", "JN_DW", "JN_IF", "CN_DW"]:
                if jn_id:
                    self.__join_node_id = jn_id 
                else:
                    Node.__join_nodes += 1
                    self.__join_node_id = Node.__join_nodes
                node_info = node_info + "_" + str(self.__join_node_id)       
            self.__cfg_id = node_info 
            self.__prev_skip = set()
            self.__ast_id = "None"
            self.__opp_node = None
            self.__name = "Reserved for labeling Info"
        
            
        else: 
            self.__node_type = node_info.get('name')
            self.__name = ""
            self.__ast_id = node_info.get('id')
            self.__cfg_id = None
            self.__children = []
            self.__used = []
            self.__defined = []
            self.__member_of = None
            self.__src_indices = node_info.pop('src').split(":")
            #self.__previous = _previous
            self.__cfg_node = None
            #extra
            self.__is_cfg_node = False
            #self._attributes = node_info.get('attributes') if node_info.get('attributes') else None
            self.__part_of_cfg = None
    
    
    def set_reset(self):
        self.reset = False
        
    def get_reset(self):
        return self.reset
    
                
    def is_in_loop(self):
        return self.__is_in_loop
    
    def set_visited(self):
        self.__visited = True
    
    
    def get_visited(self):
        return self.__visited
    
     
    def get_data_type(self):
        return self.data_type        
    
    
    def get_java_equivalent_code(self):
        return self.__java_equivalent_code
    
    
    def set_java_equivalent_code(self, _java_code):
        self.__java_equivalent_code = _java_code
    
    
    # def update_java_equivalent_code(self, _java_code):
    #     self.__java_equivalent_code += _java_code 
    
    
    @classmethod
    def get_java_code(cls):
        return cls.__java_code
    
    
    @classmethod
    def set_java_code(cls, _java_code):
        cls.__java_code = _java_code
    
    
    @classmethod
    def get_cfg_builder(cls):
        return cls.__cfg_builder
    
    
    def get_join_node_id(self):
        return self.__join_node_id
    
    
    def get_is_unreachable(self):
        return self.__is_unreachable
    
    
    def set_unreachable(self):
        self.__is_unreachable = True
        
    
    def get_equivalent_elementary_types(self, type_conv):
        if type_conv in self.__elementary_types:
            etc_id = self.__elementary_types.get(type_conv)
        else:
            etc_id = self.get_ast_id() 
            self.__class__.__elementary_types[type_conv] =  etc_id
        return etc_id
    
    
    def construct_cfg_node(self, _previous):
        builder = Node.__cfg_builder
        #builder.add_to_cfg(_previous)
        cfg_node = None
        src_code = self.get_source_code(None)
        cfg_id = self.get_cfg_id()
        
        #print("Looking for ", cfg_id ," having name " ,self.get_name(), "\nINFo:\n CFG ID: ", cfg_id)
        
        if self.get_cfg_id():
            cfg_node = builder.plot((self.get_cfg_id(), self.get_name()), src_code, _previous)
    
        return cfg_node
    
    
    @staticmethod
    def set_user_scope(value):
        Node.__user_scope = value
    
        
    def get_user_scope(self):
        return self.__user_scope    
        
            
    def set_opposite_node(self, _node):
        self.__opp_node = _node
        _node.__opp_node = self
        
    def get_opp_node(self):
        return self.__opp_node
          
    def update_used_dec_def(self, t_node):
        if t_node:
            self.used.extend(t_node.used)
            if t_node.is_in_loop():    
                for var in t_node.dec_def:
                    #print("For: ", var)
                    if var in self.used and var not in self.dec_def: 
                        self.used_def.add(var)
            self.dec_def.extend(t_node.dec_def)
         
            
    def set_used_dec_def(self, t_node):
        if t_node:
            self.used.extend(t_node.used)
            self.used_def = t_node.get_used_def()
            self.dec_def.extend(t_node.dec_def)
            
                    
    def get_dec_def(self):
        return self.dec_def
    
    
    def get_used(self):
        return self.used
    
    def get_used_def(self):
        return self.used_def
    
    def get_imf(self):
        return self.__imf_repr
    
    
    def update_visit_count(self):
        self.visit_count += 1 
        
    def get_visit_count(self):
        return self.visit_count

    def set_previous_skip(self, skip):
        self.__prev_skip = skip
        
    def get_previous_skip(self):
        return self.__prev_skip
        
    @classmethod
    def reset_function_init(cls, value):
        cls.__return_node = value
        cls.__control_structures = []
    
    
    def __str__(self):
        return "\n===================="   +   \
              "\n AST_ID:" + str(self.get_ast_id()) + \
              "\n CFG_ID:" + str(self.get_cfg_id()) + \
              "\n Name:" + self.get_name() if self.get_name() else ""+ \
              "\n Used:" + str(self.used) + \
              "\n Defined:" + str(self.dec_def) + \
              "===================\n"
            #               "\n Next:" + str(self.get_next_nodes()) + \
            
    def report_control_structure(self, value):
        Node.__control_structures.append(value)
        
        
    def extract_control_structure(self):
        return Node.__control_structures.pop()
    
    def get_break_continue(self):
        """Can be Empty"""
        pre_cs = Node.__control_structures[-1]
        return pre_cs.exit_node, pre_cs.loop_cn
        
        
    
    def get_return_node(self):
        return Node.__return_node
    
    
    def set_exit_node(self, value):
        if not self.exit_node:
            self.exit_node = value
        else:
            self.previous_node = self.__add_node(value, "p")
        
        
        self.exit_node = value
    
        
    def get_next_nodes(self):
        return self.next_node


    def get_previous_nodes(self):
        return self.previous_node

    #Break, Continue, Return
    def draw_edges_from_BCR(self, current_dg, bcr_node):
        t_nodes  = bcr_node.get_previous_nodes()
        label = bcr_node.get_name() 
        style = "filled"
        if label == "brk":
            ##AF2F01
            color = "red";  labelfontcolor = "red"; style = "dashed"
        elif label in ["return", "exit"]:
            #4d004d
            color = "#4d004d";  labelfontcolor = "#4d004d"; style = "bold"
        elif label == "cnt":
            #525202
            color = "darkgreen";  labelfontcolor = "darkgreen"; style = "bold"
        else:
            raise Exception("Unknown Node Type") 
             
        if isinstance(t_nodes, list):
            for t_node in t_nodes:
                current_dg.add_edge(str(t_node.get_cfg_id()), str(bcr_node.get_cfg_id()), _label = label, _color = color, _labelfontcolor = labelfontcolor, _style = style)
        else:
            current_dg.add_edge(str(t_nodes.get_cfg_id()), str(bcr_node.get_cfg_id()), _label = label, _color = color, _labelfontcolor = labelfontcolor, _style = style)
             
                
    def get_entry_exit_nodes(self):
        cfg_id = self.get_cfg_id()
        if type(cfg_id) == str:
            return self.entry_node, self.exit_node
        elif type(cfg_id)  == int:
            return self, self
        else:
            return None, None
    
    def set_next_node(self, _node, current_dgf = None, label = None, extra = True, spec = None):
        if _node:
            if not self.next_node:
                self.next_node = _node
            
            elif type(self.next_node) is list:
                self.next_node.extend(_node if type(_node) is list else [_node])
            
            else:
                self.next_node = [self.next_node, _node]
                
            _node.previous_count += 1
            _node.set_previous_node(self)
            
            if extra and self.get_is_unreachable():
                _node.set_unreachable()
                
            if not spec:
                if _node.get_name() == "cnt":
                    spec = "cnt"
            
           
        else:
            raise Exception("WError value None")
        
        if spec:
            color = "darkgreen";  labelfontcolor = "darkgreen"; style = "bold"
            current_dgf.add_edge(str(self.get_cfg_id()), str(_node.get_cfg_id()), _label = spec, _color = color, _labelfontcolor = labelfontcolor, _style = style)
            
        elif current_dgf and (self.is_eligible(_node.get_cfg_id())):
            current_dgf.add_edge(str(self.get_cfg_id()), str(_node.get_cfg_id()), label)
            #print(self.get_cfg_id(), _node.get_cfg_id(), current_dgf)
        else:
            print("Missing:::")
    
    def is_eligible(self, name):
        if type(name) is str:
            for x in ["CN_F", "CN_W", "EN_DW", "STOP_", "JN_F", "JN_W", "JN_DW"]:
                if name.startswith(x):
                    return False
        return True
    
    def set_node(self, curr_value, new_value):
        if not curr_value:
            return new_value
        else:
            if type(curr_value) is list:
                temp_curr_value = deepcopy(curr_value)
                temp_curr_value.extend(new_value if type(new_value) is list else [new_value])
                return temp_curr_value
            elif type(new_value) is list:
                temp_new_value = deepcopy(new_value)
                temp_new_value.insert(0, curr_value)
                return temp_new_value
            else:
                return [curr_value, new_value]    
    
       
    def set_previous_node(self, _node):
        self.__previous_count += 1
        if not self.previous_node:
            self.previous_node = _node
        elif type(self.previous_node) is list:
            self.previous_node.extend(_node if type(_node) is list else [_node])
        
        else:
            self.previous_node = [self.previous_node, _node]
    
    
    def get_previous_count(self):
        return self.__previous_count
    
    
    def del_next_node(self):
        del self.next_node


    def del_previous_node(self):
        del self.previous_node

    
    def __add_node(self, value, nl_type):
        values = None
        if nl_type == "n":
            values = self.get_next_nodes()
        else:
            values = self.get_previous_nodes()
            
        if type(values) is list:
            values.extend(value)
        else:    
            values = [values, value]
        return values
    

    def get_type_name_info(self):
        return self.get_cfg_id(), self.get_name()
    
    
    def get_name(self):
        return self.__name


    def set_name(self, value):
        self.__name = value


    def del_name(self):
        del self.__name


    def get_node_type(self):
        return self.__node_type


    def set_node_type(self, value):
        self.__node_type = value
        
#     def generate_cfg_node(self):
#         self.set_cfg_node(self.get_cfg_builder().generate_cfg_node(self.get_type_name_info(), self.get_source_code(), self.get_previous()))
#         

#     def add_to_cfg(self):
#         if self.__part_of_cfg:
#             print("=========Adding==========\n", self.__cfg_node)
#             self.__cfg_builder.append_to_cfg(self.__cfg_node)
    
    
    def get_node_info(self):
        return self.get_node_type, self.get_node_name()
    
    
    def get_cfg_node(self):
        return self.__cfg_node


    def set_cfg_node(self, value):
        self.__cfg_node, self.__part_of_cfg = value
        #print(self.__cfg_node, self.__part_of_cfg)
        
        
    def get_cfg_id(self):
        return self.__cfg_id


    def set_cfg_id(self, value = None):
        if value:
            self.__cfg_id = value
        else:
            Node.__cfg_node_number = Node.__cfg_node_number + 1
            self.__cfg_id = Node.__cfg_node_number
        

    def del_cfg_id(self):
        del self.__cfg_id


    def get_source_code(self, src_code = None):
        if src_code:
            return self.__source_code
        indices = self.get_src_indices()
        if indices:
            start, end = indices
            return self.__source_code[start: start+end]
        else:
            return ''
    


    def get_ast_id(self):
        return self.__ast_id


    def get_children(self):
        return self.__children

    def get_defined(self):
        return self.__defined


    def get_member_of(self):
        return self.__member_of


    def get_src_indices(self):
        if self.__src_indices:
            start, end, _ = (int(_) for _ in self.__src_indices)
            return (start, end)
        else:
            return (0, 0)

    def set_source_code(self, value):
        self.__source_code = value


    def set_cfg_builder(self, value):
        self.__cfg_builder = value


    def set_ast_id(self, value):
        self.__ast_id = value


    def set_children(self, value):
        self.__children = value


    def set_used(self, value):
        self.__used = value


    def set_defined(self, value):
        self.__defined = value


    def set_member_of(self, value):
        self.__member_of = value


    def set_src_indices(self, value):
        self.__src_indices = value

        
    @classmethod
    def reset(cls, source_code, src_label):
        cls.__cfg_node_number = 0
        cls.__source_code = source_code
        cls.__cfg_builder = CFGBuilder(src_label)
        cls.__join_nodes = 0
        
def get_logger(name):
    #if logging.handlers.
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s -%(asctime)s')
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger       
        