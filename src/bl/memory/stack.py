'''
Created on ६ मे, २०१९

@author: JH-ANIC
'''

class StackMemory(object):
    '''
    classdocs
    '''
    __operands_list = None
    
    def __init__(self, operands):
        self.__operands_list = operands
    
    def push(self, data, pos=0):
        print(data, type(data))
        self.__operands_list.insert(pos, data)
        
    def pop(self):
        popped_data = None
        if len(self.__operands_list)>0:
            popped_data = self.__operands_list.pop(0)           
        else:
            #Error Stack is empty
            pass
        return popped_data
    
    def clear(self):
        self.__operands_list.clean()