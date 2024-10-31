from . import Node, get_logger, SourceUnit
from src.bl.visitor import nodetypes as ntypes

class VariableDeclaration(Node):
  
    def __init__(self, node_info, _previous=None, _is_cfg_node=True):
        super(self.__class__, self).__init__(node_info, _previous)
        self.logger = get_logger(self.__class__.__name__)
        self.logger.info('processing ' + self.__class__.__name__ + str(self.get_ast_id()))
      
        self.is_constant = None
        self.variable_name = None
        self.scope = None
        self.is_state_variable = None
        self.storage_location = None
        self.type = None
        self.value = None
        self.visibility = None      
        self.id = None
        self.data_type = None  
        self.type_declaration_only = False
      
        self.__ETS_node_info(node_info.get('attributes'))
      
        if self.variable_name == "":
            self.type_declaration_only = True
        else:
            self.dec_def.append(self.id)
            
        if _is_cfg_node:
            self.set_cfg_id()
            self.entry_node = self
            self.exit_node = self
            self.construct_cfg_node(None)
          
        children = node_info.get('children')
        child_node = None
      
        for child in children:
            child_node = getattr(ntypes, child.get('name'))(child, self.get_cfg_id(), False)
      
        r_value = None   
        if self.value:
            r_value = child_node.get_java_equivalent_code()
      
        self.__generate_data_type()
        SourceUnit.insert_operands_info(str(self.id), self)

        self.convert_to_java(r_value, self.type)
        print("checking variable declaration ")
        print(self.is_constant)
        print(self.variable_name)
        print(self.scope)
        print(self.is_state_variable)
        print(self.storage_location)
        print(self.type)
        print(self.value)
        print(self.visibility)
        print(self.id)
        print(self.data_type)
        print(self.type_declaration_only)
      
    def get_visibility_modifier(self):  # Mapping Solidity visibility to Java equivalents
        visibility_map = {
            "public": "public",
            "private": "private",
            "internal": "protected",  # 'internal' maps to 'protected' in Java
            "external": "public"      # 'external' is treated as 'public' in Java
        }
    
        # Return the Java equivalent of the Solidity visibility
        return visibility_map.get(self.visibility, "public")  # Default to 'public' if visibility is not set
  
    def convert_to_java(self, r_value, typee):
        # Get Java equivalent type
        java_type = self.get_java_equivalent_type()

        # Get the visibility modifier for Java (public/private/protected)
        visibility = self.get_visibility_modifier()

        if java_type == " ":  # Handle struct object, which should not be printed in Java
            java_code = " "   
            self.set_java_equivalent_code(java_code)
            return

        # Handling unsigned integers using SolidityUint
        if java_type == "SolidityUint":
            if not r_value:
                java_code = f"{visibility} SolidityUint {self.get_variable_name()} = new SolidityUint(BigInteger.ZERO, 256);"  # Default to 256 bits for simplicity
            else:
                java_code = f"{visibility} SolidityUint {self.get_variable_name()} = new SolidityUint(new BigInteger(\"{r_value}\"), 256);"  # Default size 256 for uint types
            self.set_java_equivalent_code(java_code)
            return
        
        # Handling bytes type using SolidityBytes
        if java_type == "SolidityBytes":
            if not r_value:
                java_code = f"{visibility} SolidityBytes {self.get_variable_name()} = new SolidityBytes();"  # Default empty SolidityBytes instance for dynamic bytes
            else:
                # Assuming r_value provides byte content, adjust as needed for actual encoding
                java_code = f"{visibility} SolidityBytes {self.get_variable_name()} = new SolidityBytes(new byte[] {{{r_value}}});"
            self.set_java_equivalent_code(java_code)
            return


        # Handling double mapping
        if typee.count('(') == 2:
            mappings = typee.split('=>')
            first_mapping_type = mappings[0].split('(')[1].strip()
            second_mapping_type = mappings[1].split('(')[1].split(')')[0].strip()
            value_type = mappings[2].split(')')[0].strip()

            first_mapping_type_java = self.get_java_equivalent_type_for_mapping(first_mapping_type)
            second_mapping_type_java = self.get_java_equivalent_type_for_mapping(second_mapping_type)
            value_type_java = self.get_java_equivalent_type_for_mapping(value_type)

            java_code = f"{visibility} HashMap<{first_mapping_type_java}, HashMap<{second_mapping_type_java}, {value_type_java}>> {self.get_variable_name()} = new HashMap<>();"
            self.set_java_equivalent_code(java_code)
            return

        # Handling single mapping
        if typee.startswith("mapping"):
            long_string = typee
            start_index = long_string.find("(") + 1
            end_index = long_string.find("=") - 1
            extracted_from = long_string[start_index:end_index].strip()

            start_index = long_string.find(">") + 2 if ">" in long_string else long_string.find(".") + 1
            end_index = long_string.find(")")
            extracted_to = long_string[start_index:end_index].strip()

            extracted_from_java = self.get_java_equivalent_type_for_mapping(extracted_from)
            extracted_to_java = self.get_java_equivalent_type_for_mapping(extracted_to)

            java_code = f"{visibility} HashMap<{extracted_from_java}, {extracted_to_java}> {self.get_variable_name()} = new HashMap<>();"
            self.set_java_equivalent_code(java_code)
            return

        # Handling arrays and simple types
        if '[' in typee:
            if not r_value:
                java_code = f"{visibility} {java_type} {self.get_variable_name()}[];"
            else:
                java_code = f"{visibility} {java_type} {self.get_variable_name()}[] = {r_value};"
        else:
            if not r_value:
                java_code = f"{visibility} {java_type} {self.get_variable_name()};"
            else:
                if java_type == "String":
                    java_code = f"{visibility} {java_type} {self.get_variable_name()} = \"{r_value}\";"
                elif java_type == "SolidityBytes":
                    java_code = f"{visibility} {java_type} {self.get_variable_name()} = new SolidityBytes(new byte[] {{{r_value}}});"
                elif java_type == "BigInteger":
                    java_code = f"{visibility} {java_type} {self.get_variable_name()} = new {java_type}(\"{r_value}\");"
                elif java_type == "EthereumAddress":
                    java_code = f"{visibility} EthereumAddress {self.get_variable_name()} = new EthereumAddress(\"{r_value}\");"
                else:
                    java_code = f"{visibility} {java_type} {self.get_variable_name()} = {r_value};"

        self.set_java_equivalent_code(java_code)

    def get_java_equivalent_type(self):
        type_dict = {
            "bool": "boolean",
            "string": "String",
            "address": "EthereumAddress",  # Changed to use EthereumAddress
            "bytes": "SolidityBytes",
            "Hashtable": "Hashtable"
        }
  
        type_name = self.get_type()
        # Handle contract inheritance
        if type_name.startswith("contract"):
            long_string = type_name
            parts = long_string.split(" ")
            type_name = parts[1]
            return type_name
      
        # Handle structure user-defined type
        if type_name.startswith("struct"):
            type_name = " "
            print("After modification typename is ", type_name)
            return type_name  
  
        # Handle all unsigned integers as SolidityUint
        if type_name.startswith("uint"):
            type_name = "SolidityUint"  # Use SolidityUint for all unsigned integers
  
        # Handle signed integers
        if type_name.startswith("int"):
            type_name = "int"
      
        # Handle address and mappings
        if type_name.startswith("address"):
            type_name = "EthereumAddress"  # Changed to use EthereumAddress
      
        if type_name.startswith("bytes"):
            type_name = "SolidityBytes"
      
        type_name = type_dict.get(type_name, type_name)  # Fallback to the original type if not mapped
        return type_name

    def get_java_equivalent_type_for_mapping(self, mapping_type):
        type_dict = {
            "bool": "boolean",
            "string": "String",
            "address": "EthereumAddress",  # Changed to use EthereumAddress
            "bytes": "SolidityBytes",
            "Hashtable": "Hashtable"
        }
  
        type_name = mapping_type
        # Handle contract inheritance
        if type_name.startswith("contract"):
            long_string = type_name
            parts = long_string.split(" ")
            type_name = parts[1]
            return type_name
      
        # Handle structure user-defined type
        if type_name.startswith("struct"):
            type_name = " "
            print("After modification typename is ", type_name)
            return type_name  
  
        # Handle unsigned integers as SolidityUint
        if type_name.startswith("uint"):
            type_name = "SolidityUint"
      
        # Handle signed integers
        if type_name.startswith("int"):
            type_name = "int"
      
        # Handle address and mappings
        if type_name.startswith("address"):
            type_name = "EthereumAddress"  # Changed to use EthereumAddress
      
        if type_name.startswith("bytes"):
            type_name = "SolidityBytes"
      
        type_name = type_dict.get(type_name, type_name)  # Fallback to the original type if not mapped
        return type_name

  
    def set_data_type(self, dt_name):
        self.data_type = dt_name
  
    def get_data_type(self):
        return self.data_type
  
    def __generate_data_type(self):
        self.data_type = str(self.get_type() + " " + self.get_storage_location()) if self.get_storage_location() != "default" else self.get_type()
  
    def get_imf(self):
        return self.id
  
    def __str__(self):
        return "\n is_constant: " + str(self.is_constant) + \
               "\n variable_name: " + str(self.variable_name) + \
               "\n is_state_variable: " + str(self.is_state_variable) + \
               "\n storage_location: " + str(self.storage_location) + \
               "\n type: " + str(self.type) + \
               "\n value: " + str(self.value) + \
               "\n visibility: " + str(self.visibility) + \
               "\n scope: " + str(self.scope) + \
               "\n imf: " + str(self.get_imf()) + \
               "\n used: " + str(self.used) + \
               "\n defined: " + str(self.dec_def) + \
               "\n source code: " + self.get_source_code() + \
               "\n id: " + str(self.id)
    
    def __ETS_node_info(self, info):
        self.set_is_constant(info.get('constant'))
        self.set_variable_name(info.get('name'))
        self.set_scope(info.get('scope'))
        self.set_is_state_variable(info.get('stateVariable'))
        self.set_storage_location(info.get('storageLocation'))
        self.set_type(info.get('type'))
        self.set_value(info.get('value', True))
        self.set_visibility(info.get('visibility'))
        self.id = self.get_ast_id()
    
    def get_is_constant(self):
        return self.is_constant
    
    def get_variable_name(self):
        return self.variable_name
    
    def get_scope(self):
        return self.scope
    
    def get_is_state_variable(self):
        return self.is_state_variable
    
    def get_storage_location(self):
        return self.storage_location
    
    def get_type(self):
        return self.type
    
    def get_value(self):
        return self.value
    
    def get_visibility(self):
        return self.visibility
    
    def set_is_constant(self, value):
        self.is_constant = value
    
    def set_variable_name(self, value):
        self.variable_name = value
    
    def set_scope(self, value):
        self.scope = value
    
    def set_is_state_variable(self, value):
        self.is_state_variable = value
    
    def set_storage_location(self, value):
        self.storage_location = value
    
    def set_type(self, value):
        self.type = value
    
    def set_value(self, value):
        self.value = value
    
    def set_visibility(self, value):
        self.visibility = value
    
