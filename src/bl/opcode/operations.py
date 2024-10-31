'''
Created on १९ मे, २०१९

@author: JH-ANIC
'''
import inspect
from math import ceil, floor

class PerformOperation(object):
    '''
    classdocs
    '''
    ########Under Consideration###########
    _NO_OP = -1
    __POP_4M_STACK = 1 
    __PUSH_2_STACK= 2
    __EM_OPERATION = 3
    __SPL_INST = 4     #Jumps.... Revert.... Return... etc
    __SYSTEM_OPERATIONS = 5
    __SM_OPERATION = 6
    ####################
    __4M_OPL = 0
    __4M_ENVIRONMENT = 1
    __4M__CALCULATION = 2
    ####################
    '''FOR __SPL_INST'''
    __MODIFY_PC = 0
    ####################
    '''FOR SYS_OPER'''
    _RETURN = 1
    
    
    ##################################################################
    __STACK_WORD_LIMIT_IN_BYTES = 32 #256-bits
    __FREE_POINTER_ADDRESS = "40"
    ####################################################################################
    __NEW_INSTRUCTION = 0 # NEW INSTRUCTION
    __transaction_data = ""
    
    def __get_sign(self, number):
        return number>=0
       
    def __get_arithmetic_operation_result(self, instruction):
        print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        
        result = "0"
        if instruction._mnemonic in ["SMOD", "SDIV"]:
            operand_1 = self.__treat_2s_complement_signed_256_bit_integer(instruction._popped[0])
            operand_2 = self.__treat_2s_complement_signed_256_bit_integer(instruction._popped[1])
        else:    
            operand_1 = int(instruction._popped[0],16)
            operand_2 = int(instruction._popped[1],16)
        
        if len(instruction._popped) > 2:
            operand_3 = int(instruction._popped[3],16)
            if instruction._mnemonic == "ADDMOD":
                if operand_3!= 0:
                    result =  (operand_1 + operand_2) % operand_3
            
            elif instruction._mnemonic == "MULMOD":
                if operand_3!= 0:
                    result =  (operand_1 * operand_2) % operand_3
            
            else:
                print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
                input()
                
        else:
            if instruction._mnemonic == "ADD":
                result = operand_1 + operand_2
            
            elif instruction._mnemonic == "MUL":
                result = operand_1 * operand_2
            
            elif instruction._mnemonic == "SUB":
                result = operand_1 - operand_2
            
            elif instruction._mnemonic == "DIV":
                operand_1 = self.__get_unsigned_256_bit_integer(operand_1)
                operand_2 = self.__get_unsigned_256_bit_integer(operand_2)
                if operand_2!=0:
                    result = operand_1 // operand_2

            elif instruction._mnemonic == "SDIV":
                print(operand_1, operand_2, sep = "\n")
                if operand_2!=0:
                    result = -2**255
                    if not (operand_1 == result and operand_2 == -1):
                        result = operand_1 / operand_2
                        result = floor(abs(result))* (-1 if result<0 else 1)
            
            elif instruction._mnemonic == "MOD":
                operand_1 = self.__get_unsigned_256_bit_integer(operand_1)
                operand_2 = self.__get_unsigned_256_bit_integer(operand_2)
                if operand_2!=0:
                    result = operand_1 % operand_2
            
            elif instruction._mnemonic == "SMOD":
                print(operand_1, operand_2, sep = "\n")
                if operand_2!=0:
                    result = abs(operand_1) % abs(operand_2)
                    result = result*(-1 if operand_1<0 else 1)
            
            elif instruction._mnemonic == "EXP":
                result = operand_1 ** operand_2
            
            elif instruction._mnemonic == "SIGNEXTEND":
                operand_2 = bin(operand_2)[2:].zfill(256)
                t = 256 - 8*(operand_1 + 1)
                operand_1 = ""
                for i in range(256):
                    if i<=t:
                        operand_1+=operand_2[t]
                    else:
                        operand_1+=operand_2[i]
                result = int(operand_1, 2)
                
            else:
                print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
                input()
                
        print("Result is:",result)        
        instruction._message = "Result of "+instruction._mnemonic+str(instruction._popped)+"=>\n"+hex(result)+" pushed to stack"
        
        return self.__PUSH_2_STACK, self.__4M__CALCULATION, self.__check_result(result)
        #return self.__PUSH_2_STACK, self.__4M__CALCULATION, result.to_bytes(self.__STACK_WORD_LIMIT_IN_BYTES, 'big', signed = False).hex()
    
    def __check_result(self, result):
        required_bytes = ceil(result.bit_length()/8)
        if required_bytes < self.__STACK_WORD_LIMIT_IN_BYTES:
            required_bytes = self.__STACK_WORD_LIMIT_IN_BYTES
        return result.to_bytes(required_bytes+1, 'big', signed = True).hex()[-64:]
                        
    def __get_comp_bit_logic_operation_result(self, instruction):
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        result = "Not handled in comp_bit_logic"
        operation = ""
        operand_1 = int(instruction._popped[0],16)
        operator = " error "
        if len(instruction._popped) > 1:
            operand_2 = int(instruction._popped[1],16)
            if instruction._mnemonic in ["SLT", "SGT"]:
                operand_1 = self.__treat_2s_complement_signed_256_bit_integer(instruction._popped[0])
                operand_2 = self.__treat_2s_complement_signed_256_bit_integer(instruction._popped[1])
            elif instruction._mnemonic in ["SAR"]:
                pass
            else:
                operand_1 = int(instruction._popped[0],16)
                operand_2 = int(instruction._popped[1],16)
                
            if instruction._mnemonic == "LT":
                operand_1 = self.__get_unsigned_256_bit_integer(operand_1)
                operand_2 = self.__get_unsigned_256_bit_integer(operand_2)
                result =  operand_1 < operand_2
                operator = " < "
            
            elif instruction._mnemonic == "GT":
                operand_1 = self.__get_unsigned_256_bit_integer(operand_1)
                operand_2 = self.__get_unsigned_256_bit_integer(operand_2)
                result =  operand_1 > operand_2
                operator = " > "
            
            elif instruction._mnemonic == "SLT":
                result =  operand_1 < operand_2
                operator = " <(signed) "
            
            elif instruction._mnemonic == "SGT":
                result =  operand_1 > operand_2
                operator = " >(signed) "
            
            elif instruction._mnemonic == "EQ":
                result =  operand_1 == operand_2
                operator = " == "
            
            elif instruction._mnemonic == "AND":
                result =  operand_1 & operand_2
                operator = " & "
            
            elif instruction._mnemonic == "OR":
                result =  operand_1 | operand_2
                operator = " | "
            
            elif instruction._mnemonic == "XOR":
                result =  operand_1 ^ operand_2
                operator = " ^ "
                
            elif instruction._mnemonic == "BYTE":
                result = "0"
                if operand_1 < 32:
                    result =  operand_2.to_bytes(32, 'big',signed=False)[operand_1]
                operator = " Byte of "
            
            elif instruction._mnemonic == "SHL":
                result = (operand_2 * (2**operand_1)) % (2**256) 
                operator = " << "
                print("operands", operand_1, operand_2, sep = "\n")
                print("result:", result.to_bytes(self.__STACK_WORD_LIMIT_IN_BYTES, 'big', signed = False).hex())
                
            elif instruction._mnemonic == "SHR":
                result = floor(operand_2 // (2**operand_1)) 
                operator = " >> "
                print("result:", result.to_bytes(self.__STACK_WORD_LIMIT_IN_BYTES, 'big', signed = False).hex())
                
            elif instruction._mnemonic == "SAR":
                operand_1 = self.__get_unsigned_256_bit_integer(int(instruction._popped[0],16))
                operand_2 = self.__treat_2s_complement_signed_256_bit_integer(instruction._popped[1])
                result = floor(operand_2 // (2**operand_1)) 
                result = result.to_bytes(self.__STACK_WORD_LIMIT_IN_BYTES, 'big', signed = True).hex()
                operator = " >>(signed) "
                print(result)
                
            else:
                print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
                input()
            operation = str(operand_1)+operator+str(operand_2)
        
        else:    
            if instruction._mnemonic == "ISZERO":
                result = operand_1==0
            elif instruction._mnemonic == "NOT":
                """256 bit length"""
                return self.__PUSH_2_STACK, self.__4M__CALCULATION, hex((1 << 256) - 1 - operand_1)[2:]
            
            else:
                #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
                input()
            operation = instruction._mnemonic+"("+str(operand_1)+")"
        instruction._message = "Result of "+operation+"=>\n"+str(result)+" pushed to stack"
        ### In case of Result Overflow
        
        if instruction._mnemonic in ["SAR"]:
            print(instruction._message)
        else:
            result = result.to_bytes(self.__STACK_WORD_LIMIT_IN_BYTES, 'big', signed = False).hex()
        return self.__PUSH_2_STACK, self.__4M__CALCULATION, result
    
    #Crypto
    def __get_cryptographic_operation_result(self, instruction):
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        
        if instruction._mnemonic == "SHA3":
            instruction._message = "Keccack_256 value pushed to stack"
            
            if len(instruction._popped)==2:
                instruction._is_pending = False
                return self.__SPL_INST,1,(int(instruction._popped[0],16),int(instruction._popped[1],16))
            else:
                #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
                input("Inner")
            
        else:
            #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
            input()
    #Environmental
    def __get_environmental_operation_result(self, instruction):
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        
        if instruction._mnemonic == "ADDRESS":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 4 
        
        elif instruction._mnemonic == "BALANCE":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 5, instruction._popped[0]  
        
        elif instruction._mnemonic == "ORIGIN":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 6 
        
        elif instruction._mnemonic == "CALLER":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 7 
        
        elif instruction._mnemonic == "CALLVALUE":
            instruction._message = "CALLVALUE"
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 0 #Provide popup msg to get input from user 3 used in get message
        
        elif instruction._mnemonic == "CALLDATALOAD":
            #print("Call data load",instruction._popped)
            index = int(instruction._popped[0],16)
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 2, index 
        
        elif instruction._mnemonic == "CALLDATASIZE":
            instruction._message = "Default CALLDATASIZE"
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 1
        
        elif instruction._mnemonic == "CALLDATACOPY":
            return self.__EM_OPERATION, (3,int(instruction._popped[0], 16)//16,instruction._popped[1:])
        
        elif instruction._mnemonic == "CODESIZE":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 3
        
        elif instruction._mnemonic == "CODECOPY":
            instruction._message = "CODE copied to EVM Memory"
            return self.__EM_OPERATION, (2, int(instruction._popped[0], 16)//16, instruction._popped[1:])
        
        elif instruction._mnemonic == "GASPRICE":
            input("Check.... GASPRIZE")
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 9
        
        elif instruction._mnemonic == "EXTCODESIZE":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 8, instruction._popped[0]
        
        elif instruction._mnemonic == "EXTCODECOPY":
            return self.__EM_OPERATION, (4, int(instruction._popped.pop(1), 16)//16, instruction._popped)
            
        elif instruction._mnemonic == "RETURNDATASIZE":
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 11
            
        elif instruction._mnemonic == "RETURNDATACOPY":
            #operation, location, data = instruction
            return self.__EM_OPERATION, (5, int(instruction._popped.pop(0), 16)//16, instruction._popped)
        
        elif instruction._mnemonic == "EXTCODEHASH":
            """
            Need to add condition for the dead account to return 0 to be pushed
            """
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 8, instruction._popped[0]
        
        else:
            input("Fire in Environment Types...")
    
    
    def __get_stack_memory_storage_flow_operation_result(self, instruction):
        #print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")        
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        if instruction._mnemonic == "MLOAD":
            instruction._message = "Loaded from EVM Memory"
            return self.__EM_OPERATION,(0,int(instruction._popped[0], 16),"")  #Address of the free pointer
        
        elif instruction._mnemonic == "MSTORE":
            instruction._message = "Stored to EVM Memory"
            return self.__EM_OPERATION,(1,int(instruction._popped[0],16), instruction._popped[1])
        
        elif instruction._mnemonic == "MSTORE8":
            instruction._message = "Stored a single byte to EVM Memory"
            return self.__EM_OPERATION,(1,int(instruction._popped[0],16), instruction._popped[1])
        
        elif instruction._mnemonic == "SLOAD":
            instruction._message = "Loaded from Storage Memory"
            instruction._is_pending = False
            return self.__SM_OPERATION, 2, (int(instruction._popped[0],16))#0, "", "40"  #Address of the free pointer
        
        elif instruction._mnemonic == "SSTORE":
            instruction._message = "Stored a word to Storage Memory"
            return self.__SM_OPERATION, 1, (int(instruction._popped[0],16), instruction._popped[1])# location, data
        
        elif instruction._mnemonic == "JUMP":
            new_address = int(instruction._popped[0],16)
            instruction._message = "Updating Program Counter to " + hex(new_address)
            return self.__SPL_INST, self.__MODIFY_PC, new_address - int(instruction._address,16)-1
            
        elif instruction._mnemonic == "JUMPI":
            new_address, condition = instruction._popped
            new_address = int(new_address,16)
            value = 0
            if int(condition,16):
                instruction._message = "Updating Program Counter to " + hex(new_address)
                value = new_address - int(instruction._address,16)-1
            else:
                instruction._message = "Condition False... No need to alter PC"
            return self.__SPL_INST, self.__MODIFY_PC, value#0, "", "40"  #Address of the free pointer
        
        elif instruction._mnemonic == "PC":
            instruction._message = "Stored Program counter prior to this instruction to Stack"
            return None#0, "", "40"  #Address of the free pointer
        
        elif instruction._mnemonic == "MSIZE":
            instruction._message = "Stored the size of active memory in bytes to Stack"
            return None#0, "", "40"  #Address of the free pointer
        
        elif instruction._mnemonic == "GAS":
            instruction._message = "Stored the amount of available gas, including the corresponding reduction for the cost of this instruction."
            return self.__PUSH_2_STACK, self.__4M_ENVIRONMENT, 10# 0, "", "40"  #Address of the free pointer

        
        elif instruction._mnemonic == "JUMPDEST":
            instruction._message = "It is valid destination for jumps"
            return (self.__NEW_INSTRUCTION,) #self.__SPL_INST, self._NO_OP, self.__instruction._address
        
        else:
            input("Not Handled "+instruction._mnemonic)
            
    
    def __treat_2s_complement_signed_256_bit_integer(self, hex_value):#without 0x prefix in string
        """
            Handled wrong operands with wrong operator 
            This can happen while working with assembly code in solidity program Need to verify                 
        """
        return int.from_bytes(bytes.fromhex(hex_value), 'big', signed=True)    
    
    def __get_unsigned_256_bit_integer(self,number):
        if number < 0:
            #print(number, "=>", end =" ")
            number =  2**256 + number
            #print(number)
        return number

    def __get_ex_dup_operation_result(self, instruction):
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        
        if instruction._mnemonic.startswith("SWAP"):
            #print("IN SWAPPED")
            temp = instruction._popped[0]
            instruction._popped[0] = instruction._popped[-1]
            instruction._popped[-1] = temp
            instruction._message = "Swapped..."
            return self.__PUSH_2_STACK, self.__4M__CALCULATION, instruction._popped[::-1]
        
        elif instruction._mnemonic.startswith("DUP"):
            instruction._push = 0
            instruction._popped.insert(0,instruction._popped[-1])
            #print(instruction._popped)
            instruction._message = "Duplicated"
            return self.__PUSH_2_STACK, self.__4M__CALCULATION, instruction._popped[::-1]
        
        else:
            input("ERror")
    
    def __get_system_operation_result(self, instruction):
        #print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="\n")
        
        if instruction._mnemonic == "CREATE":
            return self.__SYSTEM_OPERATIONS, 2, instruction._popped
        elif instruction._mnemonic == "CALL":
            return self.__SYSTEM_OPERATIONS, 3, (0, instruction._popped)
        elif instruction._mnemonic == "CALLCODE":
            return self.__SYSTEM_OPERATIONS, 3, (1, instruction._popped)
        elif instruction._mnemonic == "RETURN":
            instruction._message = "Returned Code from EVM Memory"
            return self.__SYSTEM_OPERATIONS, self._RETURN, int(instruction._popped[0],16), int(instruction._popped[1],16)
        elif instruction._mnemonic == "DELEGATECALL":
            return self.__SYSTEM_OPERATIONS, 3, (2, instruction._popped)
        elif instruction._mnemonic == "INVALID":
            return (self.__SPL_INST,-2) # Need to Check
        elif instruction._mnemonic == "STATICCALL":
            return self.__SYSTEM_OPERATIONS, 3, (3, instruction._popped)
        elif instruction._mnemonic == "SELFDESTRUCT": #SELFDESTRUCT
            return self.__SYSTEM_OPERATIONS, self._NO_OP
        elif instruction._mnemonic == "STOP":
            return self.__SYSTEM_OPERATIONS, 0
        
    def __get_log_operation_result(self, instruction):
        pass
    
    def __get_other_operation_result(self, instruction):
        pass
    
    def __get_termination_operation_result(self, instruction):
        pass
    
    def execute_instruction(self, instruction):
        result = None
        if not instruction:
            return (self.__NEW_INSTRUCTION,)
        instruction.additional = 0
        if instruction.category == "arithmetic":
            return self.__get_arithmetic_operation_result(instruction)
        elif instruction.category == "comp_bit_logic":
            return self.__get_comp_bit_logic_operation_result(instruction)
        elif instruction.category == "crypto":
            return self.__get_cryptographic_operation_result(instruction)
        #####checked
        elif instruction.category == "environment":
            return self.__get_environmental_operation_result(instruction)
        elif instruction.category == "ex_dup":#duplicate
            return self.__get_ex_dup_operation_result(instruction)
        elif instruction.category == "system":#need to merge with sm later..... its return
            return self.__get_system_operation_result(instruction)
        elif instruction.category == "log":
            return self.__get_log_operation_result(instruction)
        elif instruction.category == "stack_memory_storage_flow":
            return self.__get_stack_memory_storage_flow_operation_result(instruction)
        else:
            print(instruction._mnemonic, instruction.category, inspect.currentframe().f_code.co_name, sep="||")
            input()
        return result

#Following class is added for testing PerformOperation purpose

class Instruction:
    def __init__(self, operands, category, mnemonic):
        self._mnemonic = mnemonic
        self._popped = operands
        self.category = category
    
if  __name__ == "__main__":
    print(0)
    executor = PerformOperation()
    print(1)
    instruction = Instruction([\
    "00000000000000000000000000000000000000000000000000000000000000f8", 
    "7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff"],"comp_bit_logic","SAR")
    print(1)
    executor.execute_instruction(instruction)
    
    
    
#     instruction = Instruction([\
#     "0000000000000000000000000000000000000000000000000000000000000017", 
#     "0000000000000000000000000000000000000000000000000000000000000003"],"arithmetic","MOD")
#     
#     
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "SMOD"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "DIV"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "SDIV"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction.category = "comp_bit_logic"
#     instruction._mnemonic = "LT"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "SLT"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "GT"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     instruction._mnemonic = "SGT"
#     executor.execute_instruction(instruction)
#     #print(instruction._message)
#     