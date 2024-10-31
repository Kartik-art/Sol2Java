'''
Created on १५ जून, २०१९

@author: JH-ANIC
'''
from src.bl.compiler.output_generator import CompiledOutputGenerator
from src.bl.accounts.ethc_account import ETHCAccount

class ContractManager(object):
    
    __execution_environment = None #(index, max_length, instruction_processor), opcode, stack, memory, (self.storage_index_info, self.contract_information)
    __ethereum_state = None
    
    def __init__(self, source_code = None, file_name = None):
        if not file_name:
            self.__file_name = "Temp File"#file_name[file_name.rindex('\\')+1:]
        else:
            self.__file_name = file_name
            
        self.__source_code = source_code
        self.helper = CompiledOutputGenerator(self.__source_code)
        #self.helper.set_contract(self.helper.get_contracts_list()[0])
        self.__functions_details, self.__constructor_details, self.__ffunctions, self.__fconstructor = self.__get_functions_constructor()
        self.__opcode = self.helper.get_opcodes()
        
        
    def pop_execution_environment(self):
        if self.__execution_environment:
            if len(self.__execution_environment):
                return self.__execution_environment.pop()
            else:
                return None
        else:
            return "ERROR CODE XX"


    def push_execution_environment(self, value):
        #(index, max_length, instruction_processor), opcode, stack, memory, (self.storage_index_info, self.contract_information)
        if not self.__execution_environment:
            self.__execution_environment = []
        self.__execution_environment.append(value)


    def del_execution_environment(self):
        del self.__execution_environment
    
        
    def deploy_contract(self, address, runtime_bytes, storage_info, const_size, contract_name, balance=0):
        return ETHCAccount(self.__file_name+"::"+contract_name, 
                           self.__source_code, address, runtime_bytes, storage_info, 
                           self.helper.get_source_mapping(), 
                           const_size, self.helper.get_opcodes(), 
                           self.__get_functions_constructor())
        
        
        
    def reload_methods(self, value):
        self.helper.set_contract(value)
        self.__functions_details, self.__constructor_details, self.__ffunctions, self.__fconstructor = self.__get_functions_constructor()
        
    
    def get_source_code(self):
        return self.__source_code
   
    def set_source_code(self, value):
        self.__source_code = value
        self.helper.reinitialize_helper(value)

    def get_ffunctions(self):
        return self.__ffunctions

    def get_fconstructor(self):
        return self.__fconstructor

    def set_functions_details(self, value):
        self.__functions_details = value

    def set_constructor_details(self, value):
        self.__constructor_details = value
   
    def set_ffunctions(self, value):
        self.__ffunctions = value

    def set_fconstructor(self, value):
        self.__fconstructor = value
        
    def __get_functions_constructor(self):
        fun_cons = eval(str(self.helper.get_abi())) #Need to optimize 
        ffunctions = dict()
        fconstructor = None
        constructor_index = None
        
        def get_types_list(members, is_tuple = False, is_AT = ''):
            types_list = list()
            for item in members:
                if item['type'].startswith('tuple'):
                    types_list.append(get_types_list(item['components'], True, is_AT = item['type'][5:]))
                else:
                    types_list.append(item['type'])
            if is_tuple:
                return str(tuple(types_list))+is_AT    #str("["+','.join(types_list)+"]")+is_AT
            return types_list
        
        for index,member in enumerate(fun_cons):
            if 'type' in member.keys():
                if member['type']=='constructor':
                    constructor_index = index
                    member['input_types'] = [item['type']for item in member.pop('inputs')]
                    fconstructor = member
                elif member['type']=='function':
                    fun_name = member.pop('name')
                    member['input_types'] = get_types_list(member.pop('inputs'))#self.__get_formatted_types(member.pop('inputs'))
                    member['output_types'] = [item['type']for item in member.pop('outputs')]
                    member.pop('type')
                    fun_name+="("+','.join(member['input_types'])+")"
                    ##Due to Tuple
                    ffunctions[''.join(filter(lambda k: k not in [' ', '\'', '\"'], fun_name))]=member 
                    
        constructor = None
        if constructor_index is not None:
            constructor = fun_cons.pop(constructor_index)
        #print(fun_cons, constructor, ffunctions, fconstructor)
        return fun_cons, constructor, ffunctions, fconstructor
        
        
    #source_code = prop__source_codeurce_code, set_source_code, "source_code's docs__source_code  ffunctions = property(get_ffunctions, set_ffunctions,"ffunctions's docstring")
    fconstructor = property(get_fconstructor, set_fconstructor, "fconstructor's docstring")
    execution_environment_stack = property(pop_execution_environment, push_execution_environment, del_execution_environment, "execution_environment_stack's docstring")
    