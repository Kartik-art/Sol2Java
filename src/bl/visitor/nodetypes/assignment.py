import sys
sys.path.append("C:\\Users\\KARTIK KAUSHIK\\Desktop\\eclipse-workspace\\Ethero_Pashanti_Vishleshna_Tool_21\\src\\bl\\visitor")
from node_processor import Node, get_logger
from src.bl.visitor import nodetypes as ntypes

from src.bl.visitor.nodetypes.optmodules.expressionimf import ExpressionIMF

class Assignment(Node):
    
    def __init__(self, node_info, _previous=None, _is_cfg_node=True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing ' + self.__class__.__name__ + str(self.get_ast_id()))
        
        self.__is_constant = None
        self.__is_lvalue = None
        self.__is_pure = None
        self.__l_value_requested = None
        self.__operator = None
        self.__prefix = None   
        self.type = None
        self.s_operator = None
        
        self.__ETS_node_info(node_info.get('attributes'))

        children = node_info.get('children')
        
        if _is_cfg_node:
            self.set_cfg_id()
            self.construct_cfg_node(_is_cfg_node)
        
        # Handling the LValue
        child = children[0]    
        child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
        l_value = child_node.get_java_equivalent_code()
        
        # Handling the RValue
        child = children[1]
        child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
        r_value = child_node.get_java_equivalent_code()
        
        # Check if LValue is a double mapping (e.g., _allowances[msg.sender][spender])
        if self.is_double_mapping(l_value):
            self.handle_double_mapping(l_value, r_value)
        else:
            # Handle normal assignments
            self.convert_to_java(l_value, r_value, self.__operator)
        
    def is_double_mapping(self, l_value):
        # Check for two pairs of square brackets in the LValue string
        return l_value.count('[') == 2 and l_value.count(']') == 2

    def handle_double_mapping(self, l_value, r_value):
        # Extract the base and the keys from the LValue
        base, first_key, second_key = self.extract_keys(l_value)
        java_code = f"{base}.get({first_key}).put({second_key}, {r_value});"
        self.set_java_equivalent_code(java_code)

    def extract_keys(self, l_value):
        # Extract the base, first key, and second key from LValue like _allowances[msg.sender][spender]
        base = l_value.split('[')[0]
        first_key = l_value.split('[')[1].split(']')[0]
        second_key = l_value.split('[')[2].split(']')[0]
        return base, first_key, second_key

    def convert_to_java(self, l_value, r_value, ___operator):
        java_code = l_value + " " + ___operator + " " + r_value + ";"
        self.set_java_equivalent_code(java_code)
           
    def get_imf(self):
        return self.__imf_repr 
    
    def __ETS_node_info(self, info):
        self.set_is_constant(info.get('isConstant'))
        self.set_is_lvalue(info.get('isLValue'))
        self.set_is_pure(info.get('isPure'))
        self.set_l_value_requested(info.get('lValueRequested'))
        self.set_operator(info.get('operator'))
        self.set_prefix(info.get('prefix'))
        self.set_type(info.get('type'))
        
        if self.__operator != "=":
            self.s_operator = self.__operator[:-1]
            self.__s_imf_repr = {self.s_operator: []}

    def get_is_constant(self):
        return self.__is_constant

    def get_is_lvalue(self):
        return self.__is_lvalue

    def get_is_pure(self):
        return self.__is_pure

    def get_l_value_requested(self):
        return self.__l_value_requested

    def get_operator(self):
        return self.__operator

    def get_prefix(self):
        return self.__prefix

    def get_type(self):
        return self.type
    
    def set_is_constant(self, value):
        self.__is_constant = value

    def set_is_lvalue(self, value):
        self.__is_lvalue = value

    def set_is_pure(self, value):
        self.__is_pure = value

    def set_l_value_requested(self, value):
        self.__l_value_requested = value

    def set_operator(self, value):
        self.__operator = value

    def set_prefix(self, value):
        self.__prefix = value

    def set_type(self, value):
        self.type = value
