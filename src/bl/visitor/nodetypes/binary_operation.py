from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes
from src.bl.visitor.nodetypes.optmodules.expressionimf import ExpressionIMF

class BinaryOperation(Node):
    
    def __init__(self, node_info, _previous=None, _is_cfg_node=True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing ' + self.__class__.__name__ + str(self.get_ast_id()))
        
        self.__operator = None
        self.type = None
        self.set_name(_previous)
        
        if _is_cfg_node:
            self.set_cfg_id()
        
        self.__ETS_node_info(node_info.get('attributes'))    
        
        self.__imf_repr = {self.__operator: []}
        
        children = node_info.get('children')
        java_code = ""

        # Variables to hold LHS and RHS
        lhs = None
        rhs = None

        # Iterate over children nodes (LHS and RHS)
        for i, child in enumerate(children):
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
            
            # Capture LHS and RHS
            if i == 0:
                lhs = child_node.get_java_equivalent_code()
                print(f"LHS for binary operation: {lhs}")
            elif i == 1:
                rhs = child_node.get_java_equivalent_code()
                print(f"RHS for binary operation: {rhs}")
            
            # Check if node type is uint256 or uint128 for BigInteger syntax
            if self.type in ["uint256", "uint128"]:
                # Mapping from Solidity operators to BigInteger method names, now including modulus
                operator_to_method = {
                    '+': 'add',
                    '-': 'subtract',
                    '*': 'multiply',
                    '/': 'divide',
                    '%': 'mod'  # Added handling for modulus operation
                }
                method_name = operator_to_method.get(self.__operator, None)
                if method_name is None:
                    raise ValueError(f"Unsupported operator for {self.type}: {self.__operator}")
    
                # Construct the Java code using BigInteger method calls for the first and second child
                if i == 0:
                    java_code = lhs
                elif i == 1:
                    java_code = f"{java_code}.{method_name}({rhs})"
                else:
                    raise Exception("Binary operation should not have more than two operands.")
            else:
                # Proceed as before for types other than uint256 and uint128
                if i == 0:
                    java_code = lhs + " "
                elif i == 1:
                    # Analyze the operator, lhs, and rhs to apply custom logic
                    if self.__operator in ['=', '!='] and rhs == 'String(0)':
                        if self.__operator == '!=':
                            # Translate the operation as the custom String comparison logic
                            java_code = f"!{lhs}.equals(\"0x0000000000000000000000000000000000000000\")"
                        elif self.__operator == '=':
                            # Translate equality to Java-style String comparison
                            java_code = f"{lhs}.equals(\"0x0000000000000000000000000000000000000000\")"
                    else:
                        # Default translation for other operators or when rhs is not "String(0)"
                        java_code += self.get_operator() + " " + rhs
                else:
                    raise Exception("Binary operation should not have more than two operands.")

            print("Datatype in binary operation: ", type(child_node.get_java_equivalent_code()))

        # Enhancement logic to handle 'uint256' type with '==' and '0' after existing logic
        if self.type == "bool" and self.__operator == '==' and rhs == '0':
            java_code = f"{lhs}.equals(BigInteger.ZERO)"
        
        if _is_cfg_node:
            self.construct_cfg_node(_is_cfg_node)

        self.set_java_equivalent_code(java_code)

    def get_imf(self):
        return self.__imf_repr 
        
    def __ETS_node_info(self, info):
        self.set_operator(info.get('operator'))
        self.set_type(info.get('type'))
        
    def get_operator(self):
        return self.__operator

    def get_type(self):
        return self.type

    def set_operator(self, value):
        self.__operator = value

    def set_type(self, value):
        self.type = value

    def __str__(self):
        return "\n imf: " + str(self.get_imf()) + \
            "\n used: " + str(self.used) + \
            "\n defined: " + str(self.dec_def) + \
            "\n source code:" + self.get_source_code()
