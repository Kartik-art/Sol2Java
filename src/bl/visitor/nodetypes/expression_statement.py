from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes

class ExpressionStatement(Node):
    
    def __init__(self, node_info, _previous=None, _is_cfg_node=True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing ' + self.__class__.__name__ + str(self.get_ast_id()))
        
        self.set_cfg_id()
        
        self.__imf_repr = None
        
        children = node_info.get('children')
        if len(children) > 1:
            raise Exception("Error in the Expression Statement")
        else:
            child = children[0]
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
            java_equivalent_code = child_node.get_java_equivalent_code()
            
            if 'require' in java_equivalent_code:
                self.translate_require_statement(java_equivalent_code)
            else:
                self.set_java_equivalent_code(java_equivalent_code)
            
            self.used.extend(child_node.used)
            self.dec_def.extend(child_node.dec_def)
            
        self.construct_cfg_node(_is_cfg_node)
        
    def translate_require_statement(self, java_code):
        try:
            without_require = java_code.split('require(', 1)[1].rsplit(')', 1)[0]
            condition, message_with_comma = without_require.rsplit(',', 1)
            condition = condition.strip()

            # Extracting the message without quotes
            message = message_with_comma.strip().strip('"')

            # Preparing for BigInteger comparison by identifying and replacing comparison operators
            # This involves appending compareTo and adjusting the condition
            comparisons = {
                " == ": "compareTo",
                " != ": "compareTo",
                " <= ": "compareTo",
                " >= ": "compareTo",
                " < ": "compareTo",
                " > ": "compareTo"
            }

            for operator, method in comparisons.items():
                if operator in condition:
                    left_side, right_side = condition.split(operator, 1)  # Splitting the condition at the operator
                    condition = f"({left_side}).{method}({right_side})"

                    # Adjusting the compareTo result comparison
                    compareToAdjustment = {
                        " == ": " == 0",
                        " != ": " != 0",
                        " <= ": " <= 0",
                        " >= ": " >= 0",
                        " < ": " < 0",
                        " > ": " > 0"
                    }
                    condition += compareToAdjustment[operator]

            translated_code = f"if(!({condition})){{\nSystem.out.println(\"{message}\");\nSystem.exit(1);\n}}"
            self.set_java_equivalent_code(translated_code)
        except Exception as e:
            self.logger.error(f"Error translating require statement: {str(e)}")
            # Fallback to the original code if there's an error in parsing
            self.set_java_equivalent_code(java_code)

    def get_imf(self):
        return self.__imf_repr
    
    def __str__(self):
        return "\n imf: " + str(self.get_imf()) + \
            "\n used: " + str(self.used) + \
            "\n defined: " + str(self.dec_def) + \
            "\n source code:" + self.get_source_code()
