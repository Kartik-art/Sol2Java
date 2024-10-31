'''
Created on ६ मे, २०१९

@author: JH-ANIC
'''
from src.dl.opcodes_instructions import EVMOpcodesAndInstructions as evm_op_info

class InstructionInfo():
    """operations types
           0 - Fetch from EVM Memory
           1 - Update to EVM Memory
           2 - Fetch from environment (i.e. user input at the time of execution)
    """
    #_evm_fetch = 0
    #_evm_update = 1
    #_environment = 2
    
    #_free_pointer_location = "40"
    #__opcode_info = evm_op_info()
    
    __required_popped = ["crypto","system","environment","stack_memory_storage_flow","comp_bit_logic","arithmetic","ex_dup"]
    
    def __init__(self, opcode = None):
        self.push_counter = 0
        instruction_info = None
        if opcode:
            self._address = opcode[0].strip()
            self._opcode = opcode[1].strip()
            instruction_info = evm_op_info.get_info(self._opcode)
            if not instruction_info:
                print("Error", opcode, "is not supported...")
            self._is_pending = False
            self._push = 0
            self._pop = 0
            self._popped = None
            self._mnemonic = ""
            self._message = ""
            self.category = ""
            self.additional  = 0
        if not instruction_info:
            pass
        
        elif len(instruction_info) == 7:
            self._is_pending = True
            self._push = instruction_info[2]
            self._pop = instruction_info[1]
            #self._popped = None
            self.category = instruction_info[4]
            self._mnemonic = instruction_info[0]
            if self._mnemonic not in ['PUSH', 'POP']:#Basic operations
                self.additional = int(self.category in ["crypto","comp_bit_logic","arithmetic","stack_memory_storage_flow", "environment", "system", "ex_dup"])
            if self.category in InstructionInfo.__required_popped:
                self._popped = []
            self._message = instruction_info[3]
            self._check_memory_expansion = (instruction_info[5] == 'Y')
            self._gas_required = instruction_info[6]
        
        else:
            raise Exception("Error in Instruction Info.... Check Info size")
    
    
    def get_opcode(self):
        return self._opcode
    
    
    def get_message(self, case, opcode = None):
        if case == 0:
            return self._message#, self._is_pending
        elif case == 1: #Pop
            if self.push_counter == 0:
                #For EVM Memory Operations Keeping track of popped items
                self._message = "("+opcode
            else:
                self._message = self._message+","+opcode
            #for evm_meomy_access, comp_bit_logic etc
            if self.category in InstructionInfo.__required_popped:
                    self._popped.append(opcode)
                    #print("popped",self._popped)
                    
            self.push_counter+=1
            if(self.push_counter == self._pop):
                self._message = self._message+")"
                self.push_counter = 0
                if self._push == 0:
                    self._is_pending = False
            return self._mnemonic+self._message
        
        elif case == 2: #Push
            if self.push_counter == 0:
                self._message = "("+opcode
            else:
                self._message = self._message+opcode
            self.push_counter+=1
            if(self.push_counter == self._push):
                self._message = self._message+")"
                self._is_pending = False
                self.push_counter = 0
            return self._mnemonic+self._message
        
        elif case == 3:##Other CASES, Boolean after operation
            self._is_pending = False
            return self._message
            
            
        else:
            print("Need to imp...A2")
    
