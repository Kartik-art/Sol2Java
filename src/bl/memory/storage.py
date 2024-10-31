'''
Created on १५ जून, २०१९

@author: JH-ANIC
'''

class Storage(object):

    def __init__(self, params):
        self.__sm_index_info, self.__s_memory = params

        
    def get_s_memory(self):
        return self.__s_memory


    def get_sm_index_info(self):
        return self.__sm_index_info


    def set_s_memory(self, value):
        self.__s_memory = value


    def set_sm_index_info(self, value):
        self.__sm_index_info = value


    def del_s_memory(self):
        del self.__s_memory


    def del_sm_index_info(self):
        del self.__sm_index_info

    
    def store_s_memory(self, key, value, append = True):
        if append:
            self.__s_memory[key].append(value)
        else:
            self.__s_memory[key]=value
            
    s_memory = property(get_s_memory, set_s_memory, del_s_memory, "s_memory's docstring")
    sm_index_info = property(get_sm_index_info, set_sm_index_info, del_sm_index_info, "sm_index_info's docstring")

    