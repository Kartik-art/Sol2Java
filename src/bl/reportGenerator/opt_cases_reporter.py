'''
Created on May 25, 2022

@author: ACER
'''
from re import findall

class OPTCasesRecorder(object):
    __st_instance = None
    
    
    def __init__(self):
        pass
    
    
    @classmethod
    def reset(cls):
        cls.__st_instance = None
    
        
    def __new__(cls):
        if not cls.__st_instance:
            cls.__st_instance = super(OPTCasesRecorder, cls).__new__(cls)
            cls.__st_instance.__recorder = dict()
            cls.__st_instance.__curr_node = None
        return cls.__st_instance
    
            
    def __set_node(self, _node): 
        print("CFG ID:", _node.get_cfg_id())      
        if isinstance(_node.get_cfg_id(), str):
            return False
        self.__curr_node = _node
        return True
    
        
    def get_recorder(self):
        return self.__recorder


    def __report_case(self, case_id, line_no):
        values = self.__recorder.get(case_id, list())
        values.append(line_no)
        self.__recorder[case_id] = values
        
        
    def analyze(self, _node, expressions = None):
        if expressions:
            #common subexpression elimination
            self.__case5()
        
        else:                
            valid = self.__set_node(_node)
            if valid:
                name = self.__curr_node.get_name()
                
                #Reordering
#                 self.__case6()
#                 self.__case7()
#                 self.__case8()
                #Loops
                self.__case9_12(name)
                
                #Design
                if name in ["VariableDeclaration", "VariableDeclarationStatement"]:
                    self.__case13_16(name)
                    
#                 self.__case17()
#                 self.__case18()
#                 self.__case19()
                #Useless Code
#                 self.__case20()
#                 self.__case21()
#                 self.__case22()
#         
        print(self.__curr_node)
        print("Printing Records....")
        print(self.__recorder)
        input("WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW")
        
        
    def __insert_case(self, c_id, message="Test"):
        line_no = self.__curr_node.get_line_no()
        self.__report_case(c_id, [line_no, message])
        
    
    def __case5(self):
        '''
        Case 5: This case takes care of possibility of CSE
        '''
        self.__insert_case(5)#FROM OPT
    
        
    def __case6(self):
        '''
        Case 6: This case takes care of Expression reordering
        '''
        self.__insert_case(6)#FROM OPT 
        
    
    def __case7(self):
        '''
        Case 7: This case takes care of Expression rewriting :: operands reordering 
        '''
        self.__insert_case(7)#FROM OPT
    
    def __case8(self):
        '''
        Case 8: This case takes care of Blocks' reordering
        '''
        self.__insert_case(8)#FROM OPT Based on Conditional Node
    
    
    def __case9_12(self, loop_node):
        '''
        cases 9 to 12: Takes care of Loops...
        '''
        
        def __case9(self):
            '''
            Case 9: This case takes care of Loop_constant_expression
            '''
            self.__insert_case(9)#From AST 
        
        def __case10(self):
            '''
            Case 10: This case takes care of storage read
            '''
            self.__insert_case(10)#FROM AST
        
        def __case11(self):
            '''
            Case 11: This case takes care of storage write
            '''
            self.__insert_case(11)#FROM AST
        
        def __case12(self):
            '''
            Case 12: This case takes care of Unrolling
            '''
            self.__insert_case(12)#FROM AST
    
    
    
    def __case13_16(self, name):
        
        def __case13(lvalue):
            '''
            Case 13: This case takes care of Variable Visibility
            '''
            if lvalue.get_visibility() == "public":
                self.__insert_case(13, "public visibility found")
            
    
        def __case14(l_type, rvalue):
            '''
            Case 14: This case takes care of Default Assignment
            '''
            default_values = {
                "int" : "0",
                "string" : "",
                "address": "0",
                "bool"  : "false",
                "byte"  : "0",
                }

            if rvalue and rvalue.get_name() == "Literal":
                l_type = findall('int|byte|address|string|bool', l_type)
                l_type = None if not l_type else l_type[0]      
                if l_type in default_values:
                    value = rvalue.get_value()
                    print(value, type(value), l_type)
                    if l_type in ['byte']:
                        if value == "":
                            value = "0"
                        
                    if l_type not in ['bool', 'string']:
                        value = str(eval(value))
                    
                    if default_values.get(l_type, None) == value:
                        self.__insert_case(14, "Default Assignment must be removed")
                else:
                    raise Exception(l_type, "Not handled type")
        
            
        def __case15(t_info):
            '''
            Case 15: This case takes care of DataTypeSelection
            '''
            if t_info not in ['', '256']:
                self.__insert_case(15, "Better to prefer 256bit variable")
        
        
        def __case16(t_type):
            '''
            Case 16: This case takes care of UseOfBytes
            '''
            if "[" in t_type:
                t_type = t_type.split("[", 1)[0]
                if "byte" in t_type:
                    self.__insert_case(16, "byte array found, if possible must be replaced with bytesX")
            
            elif t_type == "string":
                self.__insert_case(16, "string type found, if possible must be replaced with bytesX")
                
                
            
        values = self.__curr_node.get_rvalues()
        rvalue = None

        if len(values) == 2:
            print(values[1].get_name())
            rvalue = values[1] 
        print(values[0].get_name())
        input("Cjeck") 
                
        lvalue = self.__curr_node if name == "VariableDeclaration" else values[0]
        
        __case13(lvalue)
        
        lvalue_type = lvalue.get_type().strip()
        
        __case16(lvalue_type)
        
        if rvalue:
            __case14(lvalue_type, rvalue)
            
        
        if "int" in lvalue_type and "[" not in lvalue_type:
            __case15(lvalue_type.split("int", 1)[1])
            
                
        
    def __case17(self):
        '''
        Case 17: This case takes care of Recursion
        '''
        self.__insert_case(17)
    
    
    def __case18(self):
        '''
        Case 18: This case takes care of loopFusion
        '''
        self.__insert_case(18)
    
    
    def __case19(self):
        '''
        Case 19: This case takes care of For/While Transformation
        '''
        self.__insert_case(19)
    
        
    def __case20(self):
        '''
        Case 20: This case takes care of assert vs require... require is much cheaper
        '''
        self.__insert_case(20)
    
    
    def __case21(self):
        '''
        Case 21: This case takes care of packing "Anything smaller than 32 byte"
        '''
        self.__insert_case(21)
    
    
    def __case22(self):
        '''
        Case 22: This case takes care of event detection
        '''
        self.__insert_case(22)
        
    
    def __case120(self):
        '''
        Case 20: This case takes care of unreachable code
        '''
        self.__insert_case(20)
    
    
    def __case121(self):
        '''
        Case 20: This case takes care of Dead Code
        '''
        self.__insert_case(21)
    
    
    def __case122(self):
        '''
        Case 20: This case takes care of Opaque Predicate
        '''
        self.__insert_case(22)
    