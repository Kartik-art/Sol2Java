'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger
from src.bl.visitor import nodetypes as ntypes

class UserDefinedTypeName(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = False):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+str(self.get_ast_id()))
        
        self.__contract_scope = None
        self.__name = None
        self.__referenced_declaration = None
        self.__type  = None
        self.__ETS_node_info(node_info.get('attributes'))
    
        print("checking user defined typename ")
        #type_name_name = self.__name
        print(self.__name)
        print(self.__referenced_declaration)
        print(self.__type)
        typee = self.__type # reqd to handle struct object
        self.convert_to_java()

    def convert_to_java(self):
        # java_code = self.get_java_code()        
        # java_code = "" if java_code == "" else java_code+"\n"
        java_type = self.__type
        if java_type[0:6] == "struct":
            java_code = " "
        else:
            java_code = self.__name
        self.set_java_equivalent_code(java_code)
    
    def get_contract_scope(self):
        return self.__contract_scope


    def get_name(self):
        return self.__name


    def get_referenced_declaration(self):
        return self.__referenced_declaration


    def get_type(self):
        return self.__type


    def set_contract_scope(self, value):
        self.__contract_scope = value


    def set_name(self, value):
        self.__name = value


    def set_referenced_declaration(self, value):
        self.__referenced_declaration = value


    def set_type(self, value):
        self.__type = value


    def __ETS_node_info(self, info):
        self.set_contract_scope(info.get('contractScope'))
        self.set_name(info.get('name'))
        self.set_referenced_declaration(info.get('referencedDeclaration'))
        self.set_type(info.get('type').strip())
        print("checking user defined typename 2")
        #print(self.get_contract_scope())
        #print(self.get_name())
        #print(self.get_referenced_declaration())
        #print(self.get_type())
        