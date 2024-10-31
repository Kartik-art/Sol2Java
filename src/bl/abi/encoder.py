from re import match,search
from math import ceil
class Encoder:    
    DT = ['bytes','string']
    DT_E = '[]'
    
    DT_RE = '^((string)|(bytes))(\[\d*\])*$'
    DT_RE_LEN = '^((.*(\[\]))|(string)|(bytes))$'
    TYPES = '^((u?(int|fixed)\d+)|(bytes\d+)|(address)|(bool)|(function))(\[\d+\])+$'# dont change [][3],[2][]
    
    TUPLE = '^\(.*\)'
    
    
    def __init__(self, fun_sign_or_byte_code, args_info, method = True):
        exec('true = "true"; false = "false"')
        self.data = fun_sign_or_byte_code
        self.is_method = method
        #print(args_info)
        self.arg_info = None
        if args_info[1]:
            self.arg_info = (eval("["+args_info[0]+"]"),args_info[1])
        
        
    def get_input_string(self):
        from sha3 import keccak_256
        arguments = []
        if self.arg_info:
            arguments = self.generate_data_part()
        if self.is_method:
            arguments.insert(0,keccak_256(self.data.encode(encoding='utf_8', errors='strict')).hexdigest()[:8])
        elif self.data:#?
            arguments.insert(0,self.data)
        return ''.join(arguments)
    
    
    def generate_data_part(self):
        data_part = []
        
        def fixed_to_bytes(data):
            '''Under development:::Need to Go through documentation'''
            pass
        
        def intc_to_bytes(data,pos=None):
            data = data.to_bytes(32,'big', signed=(data<0)).hex()
            #print("Adding", data) 
            if pos is not None: #Can be zero....
                data_part[pos] = data
            else:
                data_part.append(data)
            
            #print("In int",data_part, sep="\n")

        def string_to_bytes(data):
            #print("String:",data)
            d_len = ceil(len(data)/32)
            #data_part.append(intc_to_bytes(str(d_len)))
            data = bytes(data,'utf-8').hex()
            i=0
            while d_len>1:
                data_part.append(data[i:i+64])
                i=i+64
                d_len -= 1
            data_part.append(data[i:i+64].ljust(d_len*64,'0'))
            
#         def address_to_bytes(data):
#             data_part.append(data[2:].zfill(64)) #Symbol removed
        
        def bool_to_bytes(data):
            result = '1'
            if data == 'false':
                result = '0'
            data_part.append(result.zfill(64))
            #print("In bool",data_part, sep="\n")
            
            
        def address_to_bytes(data):
            #print(data)
            data_part.append(hex(data)[2:].zfill(64))
            
        def bytesX_to_bytes(data, size=None):
            #print(data, type(data))
            hexvalue = hex(data)[2:]
            string_to_bytes("".join([chr(int(s, 16)) for s in [hexvalue[i:i+2] for i in range(0,len(hexvalue),2)]]))

        
        def modified_type(temp_type):
            #print(temp_type)
            '''TODO::: if... elif can be combined since modified struct'''
            if self.DT_E in temp_type:
                return temp_type[:temp_type.rindex('[')]
            elif '[' in temp_type:#[2][3] case
                #data_part.pop(-1)# Need to validate this condition
                return temp_type[:temp_type.rindex('[')]
            else:
                return ''
        
        def process_further(arg_type,items, end = None):
            if end:
                mtype = modified_type(arg_type[end:])
                #print("S...MTypes", mtype, items, len(items))
                if mtype == '':#### dynamic struct within struct
                    #process((items,len(items)*(arg_type[:end])),old_index=len(data_part))
                    pass
                #print("S....Items are:", items,len(items),arg_type[:end]+mtype)
                arg_info = (items,len(items)*[arg_type[:end]+mtype])
                #print(arg_info)
                process(arg_info,old_index=len(data_part))
            
            else:
                mtype = modified_type(arg_type)
                #print("MTypes", mtype)
                if mtype == '':
                    return True
                #print("Items are:", items, type(items))
                l_args = [mem for mem in items]  ###Not required can be replaced
                #mtype = mtype[:mtype.rindex('[')]
                arg_info = (l_args,len(items)*[mtype])
                #arg_info = (l_args,mtype)
                process(arg_info,old_index=len(data_part))
                
        def modified_int_value(data, unsigned = False, size=256):
            ans = data%2**(size)
            if not unsigned:
                if ans > 2**(size-1)-1 or ans < -2**(size-1):          
                    if ans > (2**(size-1)-1):
                        ans = ans - 2**(size)
            return ans
        
        """
        TYPES = '^((u?(int|fixed)\d+)|(bytes\d+)|(address)|(bool)|(function))(\[\d+\])+$'
        """
        def is_DT(struct_members):
            for member in struct_members:
                if type(member) == str:
                    if (match(self.DT_RE,member) or self.DT_E in member) and not match(self.TYPES, member):###Need to verify...
                        return True
                else:
                    return is_DT(member)
            return False
        
        
        def get_AT(struct_members):
            #print(struct_members)
            #print(struct_members.startswith("("))
            temp_list = []
            for index,letter in enumerate(struct_members):
                if letter == "(":
                    temp_list.append("(")
                elif letter == ')':
                    temp_list.pop()
                    if len(temp_list) == 0:
                        return index+1
           
        def process(arg_info, p_round = 0, old_index=0):
            #print('ps')
            
            args, arg_types = arg_info
            #print("======Arg INfo====\n",arg_info)
            #print(arg_info, "P_round", p_round)
            for index,arg_type in enumerate(arg_types):
                condition = False
                value_type = False
                #####
                    #"""Handle Struct Types using if...else""" #<str> vs <list>
                #####
                #print(type(arg_type))
                if arg_type.startswith("("):
                    a_part_end = get_AT(arg_type)
                    a_part = arg_type[a_part_end:]
                    #print("Part:",a_part)
                    if len(a_part) and p_round == 0:
                        if "[]" in a_part or is_DT(eval(arg_type[:a_part_end])):
                            data_part.append('SA')
                            #intc_to_bytes(len(args[index]))
#                                 process_further(arg_type, args[index])
                    elif p_round==1 and (is_DT(eval(arg_type[:a_part_end])) or "[]" in a_part):  #Can be combined with below condition
                        if is_DT(eval(arg_type[:a_part_end])) or "[]" in a_part:
                            intc_to_bytes((len(data_part)-old_index)*32, pos=index+old_index)
                            if "[]" in a_part:
                                intc_to_bytes(len(args[index]))
                        #print("StO",arg_type,args[index]) 
                        process_further(arg_type, args[index], a_part_end)
                        
                    else:
                        arg_type = eval(arg_type)
                        #print("In Struct")
                        #print(args[index], arg_type)
                        if p_round == 0:
                            if is_DT(arg_type):
                                #print("DT:", arg_type)
                                data_part.append('S')
                            else:
                                process((args[index], arg_type), 0, old_index=len(data_part))
                        else:
                            if p_round == 1 and is_DT(arg_type):
                                intc_to_bytes((len(data_part)-old_index)*32, pos=index+old_index)
                                process((args[index], arg_type), 0, old_index=len(data_part))
                
                else:
                    if match(self.DT_RE,arg_type) or self.DT_E in arg_type:
                        #print("""Other Types""")
                        #print("Type",arg_type,"value:",args[index], "OI:",old_index)
                        if p_round == 0 and not match(self.TYPES,arg_type):
                            data_part.append('N')
                            #print(data_part)
                        elif p_round == 1:
                            if not match(self.TYPES,arg_type): 
                                intc_to_bytes((len(data_part)-old_index)*32, pos=index+old_index)
                                if match(self.DT_RE_LEN,arg_type):
                                    intc_to_bytes(len(args[index]))
                            #print(arg_type,args[index])
                            condition = process_further(arg_type,args[index])
                        
                    elif p_round == 0 and match(self.TYPES,arg_type):
                        #print("CP1",arg_type,args[index])
                        condition = process_further(arg_type,args[index])
                    
                    else:
                        value_type = True
                        
                #print("Condition:", condition,"p_round",p_round,"value_type", value_type,"INdex",index,"data",args[index])
                if (not p_round and value_type) or (condition and p_round):
                    data = args[index]
                    #print("type",arg_type)
                    #print("data",data)
                    g=search('([a-z]*)(\d*)(.*)', arg_type) #Condition Under Evaluation...
                    extracted_DT = g.group(1)
                    
                    #print("Extracted:",extracted_DT)
                    if extracted_DT in ['uint','int']:
                        x = g.group(2)
#                         int_val = string_to_int(data)
                        int_val = modified_int_value(data, extracted_DT.startswith('u'), size=int(x))
                        intc_to_bytes(int_val)
                    
                    elif extracted_DT in ['address','function']:#function type?
                        address_to_bytes(data)
                    elif extracted_DT in ['bytes']:
                        bytesX_to_bytes(data)
                    elif extracted_DT in ['bool']:
                        bool_to_bytes(data)
                    elif extracted_DT in ['string']:
                        string_to_bytes(data)
                        
            if p_round == 0:
                process(arg_info,1,old_index)
                        
        def validate(value, val_type):
            pass
        
        args, arg_types = self.arg_info
        #print(self.arg_info)
        for index,arg_type in enumerate(arg_types):
            validate(args[index], arg_type)
            #print('val')
        
        process(self.arg_info)
#         for i in data_part:
#             print(i)
        return data_part
    
if __name__=='__main__':
    x = Encoder('f5(uint256[],(uint8,uint8[2],(uint256,uint16)),bool)',("[(1,1),(2,2)]",["('uint256','uint16')[]"])).get_input_string()
    #print(x)

"""
Expected:: f5(uint256[],(uint8,uint8[2],(uint256,uint16))[],bool)
("[10],[[10,[1,2],[10,11]]],false",['uint256[]',"['uint8','uint8[2]','''['uint256','uint16']'''][]",'bool'])
===========
[10],[[10,[1,2],[10,11]]],false
0x7de15881
0000000000000000000000000000000000000000000000000000000000000060
00000000000000000000000000000000000000000000000000000000000000a0
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002
000000000000000000000000000000000000000000000000000000000000000a
000000000000000000000000000000000000000000000000000000000000000b


S
[10,"IITP"]
0000000000000000000000000000000000000000000000000000000000000020
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000040
0000000000000000000000000000000000000000000000000000000000000004
4949545000000000000000000000000000000000000000000000000000000000

[10],[10,[1,2],[10,11]],false
0x48dd6b5a
00000000000000000000000000000000000000000000000000000000000000e0
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002
000000000000000000000000000000000000000000000000000000000000000a
000000000000000000000000000000000000000000000000000000000000000b
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000000a

[[1,1],[2,2]]
0xca72fd93
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000002
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002
0000000000000000000000000000000000000000000000000000000000000002
f5(uint256[],(uint8,uint8[2],(uint256,uint16)),bool)
"[10],[10,[1,2],[10,11]],false";;['uint256[]',['uint8','uint8[2]',['uint256','uint16']],'bool']

0x48dd6b5a
00000000000000000000000000000000000000000000000000000000000000e0
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002
000000000000000000000000000000000000000000000000000000000000000a
000000000000000000000000000000000000000000000000000000000000000b
0000000000000000000000000000000000000000000000000000000000000000
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000000a



function f5(int256[],R memory m, bool y)public{}
struct R { uint8 x; uint8[2] y; T t1;}
struct T { uint x; uint16 y; }
['uint256[]', ['uint8', 'uint8[2]', ['uint256', 'uint16']], 'bool']
Input:




["tuple(uint8,uint8[2],tuple(uint256,uint16))"]
[uint8 x; uint8[2] y; [uint x; uint16 y;]];; [12,[12,12],[10,10]]
000000000000000000000000000000000000000000000000000000000000000c
000000000000000000000000000000000000000000000000000000000000000c
000000000000000000000000000000000000000000000000000000000000000c
000000000000000000000000000000000000000000000000000000000000000a
000000000000000000000000000000000000000000000000000000000000000a



[uint, uint[], [uint, uint]]
[1,[10],[1,1]]

0x754b219f
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000080
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
000000000000000000000000000000000000000000000000000000000000000a

tuple{uint, uint, tuple{uint, uint}}
[1,1,[1,1]]
0x42a46cb3
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001




tuple(uint,string);; [1,"IITP"]
0x3c2596b6
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000040
0000000000000000000000000000000000000000000000000000000000000004
4949545000000000000000000000000000000000000000000000000000000000

tuple(uint, uint),tuple(uint, uint[]) ;[1,1],[1,[1]]
0x6f72b4fd
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000060
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000040
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001

tuple(uint, uint[]), [1,[2]]
0x113abca8
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000040
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002


tuple(uint, uint), uint
0x99f352ec
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001

tuple(uint, uint)
0xe5198423
000000000000000000000000000000000000000000000000000000000000000a
0000000000000000000000000000000000000000000000000000000000000014

tuple{uint, uint[], tuple{uint, uint}}
[1,[1],[1,1]]

0xb086e43
0000000000000000000000000000000000000000000000000000000000000002
0000000000000000000000000000000000000000000000000000000000000000
1000000000000000000000000000000000000000000000000000000000000008
00000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000001






0x51af50f4
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000020
000000000000000000000000000000000000000000000000000000000000002f
6161616161616161616161616161616161616161616161616161616161616161
6161616161616161616161616161610000000000000000000000000000000000


[1234, -560], uint8[2]
["ak","aksh","akshay"],string[3]
===
0x33f347da
0000000000000000000000000000000000000000000000000000000000000020
0000000000000000000000000000000000000000000000000000000000000040
00000000000000000000000000000000000000000000000000000000000000c0
0000000000000000000000000000000000000000000000000000000000000003
00000000000000000000000000000000000000000000000000000000000000d2
00000000000000000000000000000000000000000000000000000000000000fb
000000000000000000000000000000000000000000000000000000000000003c
0000000000000000000000000000000000000000000000000000000000000003
0000000000000000000000000000000000000000000000000000000000000001
0000000000000000000000000000000000000000000000000000000000000002
0000000000000000000000000000000000000000000000000000000000000000

600,500
0x8607eca9
0000000000000000000000000000000000000000000000000000000000000058
00000000000000000000000000000000000000000000000000000000000000f4

-260,-500
0x8607eca9
00000000000000000000000000000000000000000000000000000000000000fc
000000000000000000000000000000000000000000000000000000000000000c

256,-1
0x8607eca9
0000000000000000000000000000000000000000000000000000000000000000
00000000000000000000000000000000000000000000000000000000000000ff

400
0x2d5a4690
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff90
0000000000000000000000000000000000000000000000000000000000000070

0x2d5a4690
0000000000000000000000000000000000000000000000000000000000000059
0000000000000000000000000000000000000000000000000000000000000070

130
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff82::-126
0000000000000000000000000000000000000000000000000000000000000070

-128,-129
0x2d5a4690
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80
000000000000000000000000000000000000000000000000000000000000007f

-257
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff


ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff80
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff81


0x2d5a4690
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffcf
ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff

"""
#def rlp_encode(self, input_arg):
#         if isinstance(input_arg,str):
#             if len(input_arg) == 1 and ord(input_arg) < 0x80: 
#                 return input_arg    
#             else: 
#                 return self.encode_length(len(input_arg), 0x80) + input_arg
#         elif isinstance(input_arg,list):
#             output = ''
#             for item in input_arg: 
#                 output += str(self.rlp_encode(item))
#             return self.encode_length(len(output), 0xc0) + output
# 
#     def encode_length(self, L,offset):
#         if L < 56:
#             return chr(L + offset)
#         elif L < 256**8:
#             BL = self.to_binary(L)
#             return chr(len(BL) + offset + 55) + BL
#         else:
#             raise Exception("input too long")
#     
#     def to_binary(self,x):
#         if x == 0:
#             return ''
#         else: 
#             return self.to_binary(int(x / 256)) + chr(x % 256)





