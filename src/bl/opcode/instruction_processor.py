'''
Created on १६ मे, २०१९

@author: JH-ANIC
'''

from src.bl.opcode.instruction_info import InstructionInfo
from src.bl.opcode.operations import PerformOperation

class InstructionProcessor(PerformOperation):
    '''
    classdocs
    '''
    ######### processors code information #############
    __NEW_INSTRUCTION = 0
    __POP_4M_STACK = 1
    __PUSH_2_STACK= 2
    __EM_OPERATION = 3
    __SPL_INST = 4
    #######
    __4M_OPL = 0
    __4M_ENVIRONMENT = 1
    __4M__CALCULATION = 2
    
    
    def __init__(self):
        self.__instruction = None
        self.__opcodes_executed = ""
    
    
    def set_instruction(self, opcode):
        #self.__address = opcode[0].strip()
        self.__instruction = InstructionInfo(opcode)
        self.push_counter = 0
        self.pop_counter = 0
        print("Opcode::", self.__instruction.get_opcode())
        self.__opcodes_executed += self.__instruction.get_opcode()
        
    def get_message(self, case, opcode = None):
        if case < 0:
            self.__instruction._is_pending = False
            return "Address:"+self.__instruction._address+" ,Marked as a valid destination for a jump"
        else:
            return self.__instruction.get_message(case, opcode)
    
    
    def get_mnemonic(self):
        return self.__instruction._mnemonic
    
    
    def req_mem_exp(self):
        return self.__instruction._check_memory_expansion
    
    
    def get_gas_requirment(self):
        print(self.__instruction)
        return self.__instruction._gas_required
    
    
    def get_executed_opcodes(self):
        return self.__opcodes_executed
    
        
    def process_instruction(self):
        if not self.__instruction: #or
            return self.execute_instruction(self.__instruction)
        
        elif self.__instruction._is_pending: 
            if self.__instruction._pop > self.pop_counter:
                self.pop_counter+=1
                return (self.__POP_4M_STACK,)
                
            elif self.__instruction._push > self.push_counter:
                if self.__instruction._mnemonic.startswith("PUSH"):
                    return (self.__PUSH_2_STACK, self.__4M_OPL, int(self.__instruction._mnemonic[4:]))
                    
                else:
                    if self.__instruction.additional == 1:
                        result = self.execute_instruction(self.__instruction)#self.__instruction.get_additional_information()
                        #print("Instruction:",result, self.__instruction._mnemonic, self.__instruction.category)
                        return result
                         
                    else:
                        #print("Other Type...", self.__instruction._mnemonic, self.__instruction.category)
                        input("Waiting for error")
                
            else: #NPP Instructions
                
                return self.execute_instruction(self.__instruction)
                
        
        elif not self.__instruction._is_pending:
            self.pop_counter = 0
            self.push_counter = 0
            #print("Not pending..... Anything")
            if self.__instruction.additional == 1:
                result = self.execute_instruction(self.__instruction)#self.__instruction.get_additional_information()
                #print("Additional Information check:",self.__instruction._mnemonic, result)
                return result
            else:
                return (self.__NEW_INSTRUCTION,)
        