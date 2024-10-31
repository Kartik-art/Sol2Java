'''
Created on May 27, 2022

@author: ACER
'''

class Sample(object):
    '''
    classdocs
    '''
    __st_instance = None
    
    def __init__(self):
        pass
    
    
    def __new__(cls):
        if not cls.__st_instance:
            cls.__st_instance = super(Sample, cls).__new__(cls)
            cls.__st_instance.__recorder = dict()
            cls.__st_instance.__curr_node = None
        return cls.__st_instance
    
    
    def get_node(self):
        return self.__curr_node
    
    def set_node(self, value):
        self.__curr_node = value
        
        
if __name__=="__main__":
    s = Sample()