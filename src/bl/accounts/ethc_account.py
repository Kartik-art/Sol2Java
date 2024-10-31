'''
Created on २ जून, २०१९

@author: JH-ANIC
'''
from src.bl.accounts.account import Account
from src.bl.memory.storage import Storage
from hashlib import sha256
from datetime import datetime

class ETHCAccount(Account):
        
    def __init__(self, file_name, source_code, address, runtime_bytes,storage_info,mapping,const_size,opcode,func_constr_details, balance=0):
        super(self.__class__, self).__init__(balance, address, runtime_bytes, Storage(storage_info))
        self.__file_name = file_name
        self.__source_code = source_code
        self.__opcodes = opcode
        self.__functions_details, self.__constructor_details, self.__ffunctions, self.__fconstructor = func_constr_details
        self.__mapping = mapping
        self.__const_size = const_size


    def get_mapping(self):
        return self.__mapping


    def get_const_size(self):
        return self.__const_size


    def del_mapping(self):
        del self.__mapping


    def del_const_size(self):
        del self.__const_size


    def get_opcodes(self):
        return self.__opcodes


    def set_opcodes(self, value):
        self.__opcodes = value


    def del_opcodes(self):
        del self.__opcodes
   

    def get_file_name(self):
        return self.__file_name


    def get_source_code(self):
        return self.__source_code


    def get_functions_details(self):
        return self.__functions_details


    def get_constructor_details(self):
        return self.__constructor_details


    def get_ffunctions(self):
        return self.__ffunctions


    def get_fconstructor(self):
        return self.__fconstructor


    def set_file_name(self, value):
        self.__file_name = value


    def set_source_code(self, value):
        self.__source_code = value


    def set_functions_details(self, value):
        self.__functions_details = value


    def set_constructor_details(self, value):
        self.__constructor_details = value


    def set_ffunctions(self, value):
        self.__ffunctions = value


    def set_fconstructor(self, value):
        self.__fconstructor = value


    def del_file_name(self):
        del self.__file_name


    def del_source_code(self):
        del self.__source_code


    def del_functions_details(self):
        del self.__functions_details


    def del_constructor_details(self):
        del self.__constructor_details


    def del_ffunctions(self):
        del self.__ffunctions


    def del_fconstructor(self):
        del self.__fconstructor

    
    def generate_hash(self):
        #print("Self...", self)
        return "0x"+sha256((str(self)+datetime.now().__str__()).encode('utf-8')).hexdigest()[:40]
#         data= bytes.fromhex(hex(id(self))[2:]).hex()
#         return "0x"+sha256(sha256(bytes.fromhex(data)).digest()).digest()[::-1].hex()[:40]
    
    
    
    file_name = property(get_file_name, set_file_name, del_file_name, "file_name's docstring")
    #source_code = pr__source_codesource_code, set_source_code, del_source_code, "source_code's do__source_code    functions_details = property(get_functions_details, set_functions_details, del_functions_details, "functions_details's docstring")
    constructor_details = property(get_constructor_details, set_constructor_details, del_constructor_details, "constructor_details's docstring")
    ffunctions = property(get_ffunctions, set_ffunctions, del_ffunctions, "ffunctions's docstring")
    fconstructor = property(get_fconstructor, set_fconstructor, del_fconstructor, "fconstructor's docstring")
    opcode = property(get_opcodes, set_opcodes, del_opcodes, "opcode's docstring")
    mapping = property(get_mapping, None, del_mapping, "mapping's docstring")
    const_size = property(get_const_size, None, del_const_size, "const_size's docstring")
#     def set_contract_address(self, runtime_binary):
#         if not self.runtime_binary:
#             self.runtime_binary = runtime_binary
#             #Calculate the hash of the object and return this as the contract address
#             self.contract_address = self.__generate_hash()
            
"""
New Type: Tuple
Sample 
struct R { uint8 x; uint8[2] y; T t1;}
struct T { uint x; uint16 y; }
###
Fun:
function f5(R memory m)public{}

Input:
Expected Encoding: ['uint8', 'uint8[2]', ['uint','uint16']]
Observed: [['uint8', 'uint8[2]', ['uint256', 'uint16']]]


###
Fun:
function f5(int256[],R memory m, bool y)public{}

Input:
Expected Encoding: 'uint256[]', ['uint8', 'uint8[2]', ['uint256','uint16']],'bool'
Observed:         ['uint256[]', ['uint8', 'uint8[2]', ['uint256', 'uint16']], 'bool']

"""    
