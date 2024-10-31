'''
Created on २७ जून, २०१९

@author: JH-ANIC
'''
from src.dl.gas_usage import GasUses
from src.bl.memory.ethereum_machine import EthereumStateMachine as esm
from math import floor
from sha3 import keccak_256
from rlp import encode

class Transaction(object):
    
    __miner = None
    """
        s; o; g; p; v; i; e; w
        s; o; r; c; g; p; v; ~v; d/i; e; w)
    """
    def __init__(self, nonce, gas_price, gas_limit, recipient, value, init_data, sender, origin, contract_addr = None, signature = None):
        self.__nonce = nonce
        self.__gas_price = gas_price
        self.__gas_limit = gas_limit
        self.__recipient = recipient
        self.value = value
        self.__signature = signature #(v, r, s)Yet to work on this
        self.__init_or_data = init_data
        ###
        self.__accrued_subset = AccruedSubset() 
        self.__sender = sender
        self.__origin = origin
        self.__contract_addr = contract_addr
        self.__esm = esm.get_ethereum_state()
        self.__output_data = None
        
        #####if None then only calculate intrinsic else remaining gas
        self.__intrinsic_gas = self.__get_intrinsic_gas() if recipient else 0
        self.__remaining_gas = self.__gas_limit - self.__intrinsic_gas
        
        self.__sender_account = self.__esm.get_account(self.__sender)
        self.__contract_account = self.__esm.get_account(self.__contract_addr) 
        self.__self_destr = []
        self.__touched_acc = []


    def set_remaining_gas(self, value):
        self.__remaining_gas = value


    def get_recipient(self):
        return self.__recipient

        
        
    def get_output_data(self):
        return self.__output_data


    def set_output_data(self, value):
        self.__output_data = value


    def del_output_data(self):
        del self.__output_data


    @classmethod
    def set_miner(cls, miner):
        cls.__miner = miner
        
        
    def get_call_value(self):
        return self.value
    
    
    def get_gas_price(self):
        return self.__gas_price
    
    
    def get_gas_limit(self):
        return self.__gas_limit
        
    
    def get_contract_addr(self):
        return self.__contract_addr
    
    
    def get_sender_account(self):
        return self.__sender_account
    
    
    def get_contract_account(self):
        return self.__contract_account
        
    
    def get_sender(self):
        return self.__sender
    
    
    def get_esm(self):
        return self.__esm
    
    
            
    def get_total_gas_used(self):
        return self.__gas_limit - self.__remaining_gas        
        
    
    def get_transaction_data(self):
        return self.__init_or_data

    
    
            
    def get_remaining_gas(self):
        return self.__remaining_gas
    
            
    def message_call(self, parameters):
        pass
        
    
    def __create_call(self, ):     
        pass
        
    
    def __get_up_front_cost(self):
        return self.__gas_limit*self.__gas_price + self.value
    
    

    def is_sufficient_gas(self, gas_required):
        if self.__remaining_gas - gas_required < 0:
            #self.__remaining_gas = 0
            raise("Out of GAS ::Required more Gas")
        else:
            self.__remaining_gas -= gas_required

    
    def start_execution(self):
        self.__validate_tx()
        ##Execution begins from here...
        self.__sender_account.incr_nonce()
        self.__sender_account.update_balance(self.__get_up_front_cost()*-1)
        
        msg = "Transaction Type:: "+ ("Message Call\n" if self.__contract_addr else "Deploy Contract\n")
        msg+= "Gas Consumed:: " + str(self.__intrinsic_gas)
        #Input Data Cost can be displayed separately 
        return msg 
        #(provisional_state, remaining_gas, accrued_subset, status) = self.__process_execution()
        
        #returned_bal = self.__process_accrued_subset(accrued_subset)
        
        #self.__finalize_state(provisional_state, remaining_gas, returned_bal)
        
        
        
    def finalize_state(self):
        
        returned_bal = 0
        if len(self.__self_destr):
            price = GasUses.get_price("Rselfdestruct")
            v_address = 0
            for address in self.__self_destr:
                account = self.__esm.get_account(address)
                if account:
                    v_address += 1
                    account.update_refund_counter(price)
                else:
                    raise Exception("Invalid accoiunt")
            returned_bal += v_address*price
            
        
        total_gas_remained = self.__remaining_gas + min(floor((self.__gas_limit - self.__remaining_gas)/2), returned_bal)
        #copy storage...........total_gas_remained
        self.__sender_account.update_balance(total_gas_remained * self.__gas_price)
        self.__esm.get_account(self.__miner).update_balance((self.__gas_limit - total_gas_remained) * self.__gas_price)
        
        for accounts in [self.__touched_acc, self.__self_destr]:
            for address in accounts:
                account = self.__esm.get_account(address)
                if not account.get_runtime_bytes()():
                    self.__esm.delete_account(address)
        
        esm.set_ethereum_state(self.__esm)
        
        
    def __validate_tx(self):  
        if not self.__sender:
            raise Exception("Invalid Transaction:: Sender")
               
        if not self.__sender_account:
            raise Exception("Invalid Transaction:: Sender")
        
        if self.__signature:
            raise Exception("Invalid Transaction:: Signature")
        
        if self.__nonce != self.__sender_account.get_nonce():
            raise Exception("Invalid Transaction:: Nonce")
        
        if self.__gas_limit < self.__intrinsic_gas:
            raise Exception("Invalid Transaction:: Out-Of-GAS")
        
        if self.__get_up_front_cost() > self.__sender_account.get_balance():
            raise Exception("Invalid Transaction:: Out-Of-Balance")
        
    
    def __get_intrinsic_gas(self):
        zero = 0
        nonzero = 0
        print(self.__init_or_data)
        print("asfdaf...")
        
        for k in range(0, len(self.__init_or_data), 2):
            if self.__init_or_data[k:k+2] == "00":
                zero+=1
            else:
                nonzero+=1
        print(zero, nonzero)
        return GasUses.get_price("Gtransaction") \
            + zero*GasUses.get_price("Gtxdatazero") \
            + nonzero*GasUses.get_price("Gtxdatanonzero") \
            + (0 if self.__contract_addr else GasUses.get_price("Gtxcreate"))
    

    def generate_new_address(self):
        print("Self...", self)
        return "0x"+keccak_256(encode([self.__sender_account.get_address(),self.__sender_account.get_nonce()-1])).hexdigest()[-40:]    
    
    
    output_data = property(get_output_data, set_output_data, del_output_data, "output_data's docstring")
    recipient = property(get_recipient, None, None, None)
        
            

    
class AccruedSubset(object):
        
    def __init__(self):
        self.__r = 0;       #return balance
        self.__s = [];    #self-destruct accounts
        self.__logs = [];   #logs if any (Yet to Work on this)
        self.__t = [];    #list of touched accounts
        
        
    def get_subset(self):
        return self.__r, self.__s, self.__logs, self.__t
        
        
    def get_r(self):
        return self.__r


    def get_s(self):
        return self.__s


    def get_logs(self):
        return self.__logs


    def get_t(self):
        return self.__t


    def set_r(self, value):
        self.__r = value


    def set_s(self, value):
        self.__s = value


    def set_logs(self, value):
        self.__logs = value


    def set_t(self, value):
        self.__t = value


    def del_r(self):
        del self.__r


    def del_s(self):
        del self.__s


    def del_logs(self):
        del self.__logs


    def del_t(self):
        del self.__t

    r = property(get_r, set_r, del_r, "r's docstring")
    s = property(get_s, set_s, del_s, "s's docstring")
    logs = property(get_logs, set_logs, del_logs, "logs's docstring")
    t = property(get_t, set_t, del_t, "t's docstring")