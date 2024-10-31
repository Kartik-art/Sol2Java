'''
Created on २७ जून, २०१९

@author: JH-ANIC
'''
from src.bl.accounts.account import Account

class EthereumStateMachine(object):
    '''
    classdocs
    '''
    DEFAULT_USER_ACCOUNTS = (  (1000000, "0xca35b7d915458ef540ade6068dfe2f44e8fa733c"),
                               (1000000, "0xaf35b7d915458ef540aae6068dfe2f44e8fa733c"),
                               (1000000, "0xcaafb7d915458ef540ade6068dfe2f44e8fa733c"))
    
    __ethereum_state = None
    
    
    def __init__(self, version="0.2"):
        self.version = version
        self.__accounts = dict()
        for balance, address in self.DEFAULT_USER_ACCOUNTS:
            self.add_usr_accounts(balance, address)   
          
    
    @classmethod        
    def get_ethereum_state(cls):
        
        return cls.__ethereum_state
    
    
    @classmethod
    def set_ethereum_state(cls, new_state):
        #print("check", new_state, type(new_state))
        
        if type(new_state) is EthereumStateMachine:
            cls.__ethereum_state = new_state
            #print("Current accounts::", cls.__ethereum_state.get_accounts())
        else:
            raise Exception("Not a valid state")
        
    
             
    def get_user_accounts(self):
        return list(filter(lambda a: self.__accounts[a].is_usr_account(), self.__accounts.keys()))
    
    
    def get_accounts(self):
        return self.__accounts
    
    
    def get_account(self, address):
        return self.__accounts.get(address)
    
    
    def get_contract_accounts(self):
        return list(filter(lambda a: not self.__accounts[a].is_usr_account(), self.__accounts.keys()))
    
    
    def add_usr_accounts(self, balance, address):
        self.add_account(address, Account(balance, address))
    
    
    def add_account(self, address, obj):
        #print("add:", address, self.get_account(address))
        if not self.get_account(address):
            self.__accounts[address] = obj
        else:
            raise Exception("Error :: Account Already Exists ")
        
        
    def delete_account(self, address):
        self.__accounts.pop(address, None)
    
