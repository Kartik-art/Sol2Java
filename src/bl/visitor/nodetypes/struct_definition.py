'''
Created on Nov 30, 2020

@author: ACER
'''
from . import Node, get_logger, SourceUnit

from src.bl.visitor import nodetypes as ntypes

class StructDefinition(Node):
    
    def __init__(self, node_info, _previous = None, _is_cfg_node = True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing '+self.__class__.__name__+ str(self.get_ast_id()))
        
        self.__canonical_name = None
        self.__name = None
        self.__id = None
        self.__scope = None
        self.__visibility = None       
        self.__type_declaration_only = False
        self.__ETS_node_info(node_info.get('attributes'))
        
        self.construct_cfg_node(None)
        
        if self.__name == "":
            self.type_declaration_only = True
        else:
            self.dec_def.append(self.__id)
              
        if _is_cfg_node:
            self.set_cfg_id()
            self.entry_node = self
            self.exit_node = self
              
        children = node_info.get('children')
        
        java_childs = ""
        java_childs1 = ""   #for handling constructor in struct
        helper_string = ""
        helper_string1 = ""
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
            java_childs += child_node.get_java_equivalent_code() + "\n"
            java_childs1 += child_node.get_java_equivalent_code()
            print("java_childs_for_struct_constructor are ", java_childs1)
            print("For struct ", child_node.get_java_equivalent_code())
            elements = [element.strip() for element in java_childs1.split(";") if element.strip()]
            print("elements for struct are ", elements)
            self.update_used_dec_def(child_node)
            elements1 = java_childs1.split(";")
            elements2 = [elementt.split()[-1] for elementt in elements1 if elementt.strip()]
            print("individual elements of struct are ", elements2)
            string_args = ', '.join(elements)               # to store constructor arguments
            
            sentences = [f"this.{elementa} = {elementa};" for elementa in elements2]
            helper_string = "\n".join(sentences)    
            print("The coming helper string is ", helper_string)
        SourceUnit.insert_operands_info(str(self.__id), self)
        
        
        self.convert_to_java(java_childs, string_args, helper_string, helper_string1)
        
        
    def convert_to_java(self, java_childs, string_args, helper_string, helper_string1):
        # java_code = self.get_java_code()        
        # java_code = "" if java_code == "" else java_code+"\n"
        java_code = "class " + self.get_variable_name() + " {" + "\n" + java_childs + " }" + "\n" + "public " + self.get_variable_name() + "( " + string_args + ")"
        java_code += " {" + "\n" + helper_string + "\n" + "}"
        self.set_java_equivalent_code(java_code)
        
    
    def get_type(self):
        return "function"

    
    def get_variable_name(self):
        return self.get_name()
    
    
    def get_canonical_name(self):
        return self.__canonical_name


    def get_scope(self):
        return self.__scope

    
    def get_visibility(self):
        return self.__visibility


    def get_type_declaration_only(self):
        return self.__type_declaration_only


    def set_canonical_name(self, value):
        self.__canonical_name = value


    def set_scope(self, value):
        self.__scope = value


    def set_visibility(self, value):
        self.__visibility = value


    def set_type_declaration_only(self, value):
        self.__type_declaration_only = value
     
        
    def __ETS_node_info(self, info):
        self.__canonical_name = self.set_canonical_name(info.get("canonicalName"))
        self.__name = self.set_name(info.get("name"))
        self.__id = self.get_ast_id()
        self.__scope = self.set_scope(info.get("scope"))
        self.__visibility = self.set_visibility(info.get("visibility"))
          
    
