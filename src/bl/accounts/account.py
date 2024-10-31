'''
Created on ८ जून, २०१९

@author: JH-ANIC
'''

class Account(object):
    '''
    classdocs
    '''
    def __init__(self, balance, address, runtime_bytes = "", storage_info = None):
        self.__balance = balance
        self.__is_usr_acc = False
        self.__runtime_bytes = runtime_bytes
        self.__storage_info = storage_info
        self.__refund_counter = 0
        self.__nonce = 1
        self.__address = address
                
        if type(self) == Account:
            self.__is_usr_acc = True
            self.__nonce = 0

    def update_refund_counter(self, value):
        self.__refund_counter += value
        
        
    def get_code_size(self):
        return len(self.get_runtime_bytes())//2
    
    def get_runtime_bytes(self):
        return self.__runtime_bytes

    
    def get_storage_info(self):
        return self.__storage_info


    def set_runtime_bytes(self, value):
        self.__runtime_bytes = value


    def set_storage_info(self, value):
        self.__storage_info = value


    def del_runtime_bytes(self):
        del self.__runtime_bytes


    def del_storage_info(self):
        del self.__storage_info
    
    
    def get_address(self):
        return self.__address


    def del_address(self):
        del self.__address


    def get_balance(self):
        return self.__balance


    def update_balance(self, amount):
        self.__balance+=amount
        
        
    def get_nonce(self):
        return self.__nonce


    def incr_nonce(self):
        self.__nonce+=1
        
        
    def is_usr_account(self):
        return self.__is_usr_acc
    
    
    def is_dead(self):
        return not self.get_runtime_bytes()
    
    
    def del_balance(self):
        del self.__balance


    def del_nonce(self):
        del self.__nonce

    
#     def normalize_address(x, allow_blank=False):
#         if allow_blank and x == '':
#             return ''
#         if len(x) in (42, 50) and x[:2] == '0x':
#             x = x[2:]
#         if len(x) in (40, 48):
#             x = bytes.fromhex(x).decode('utf-8')
#         if len(x) == 24:
#             assert len(x) == 24 and sha256(x[:20])[:4] == x[-4:]
#             x = x[:20]
#         if len(x) != 20:
#             raise Exception("Invalid address format: %r" % x)
#         return x
    
#         data= bytes.fromhex(hex(id(self))[2:]).hex()
#         return "0x"+sha256(sha256(bytes.fromhex(data)).digest()).digest()[::-1].hex()[:40]
    
    balance = property(get_balance, del_balance, "balance's docstring")
    nonce = property(get_nonce, del_nonce, "nonce's docstring")
    usr_address = property(get_address, del_address, "address's docstring")
    runtime_bytes = property(get_runtime_bytes, set_runtime_bytes, del_runtime_bytes, "runtime_bytes's docstring")
    storage_info = property(get_storage_info, set_storage_info, del_storage_info, "storage_info's docstring")
        
    
    
        