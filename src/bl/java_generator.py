'''
Created on Feb 3, 2022

@author: JH-ANIC
'''
from src.bl.compiler.output_generator import CompiledOutputGenerator
from src.bl.compiler.solc_selector import SolcSelector
from src.bl.visitor.ast_reader import ASTToCFGObject
import solcx
import sys
import os


class SolidityToJava(object):
    
    def __init__(self, file_path = None, file_name = None, _version = "0.5.9"):
        self.solidity_compiler_version = _version
        self.java_code = None
        self.solidity_code = self.__extract_source_code(file_path+file_name+".sol")
        self.java_code = self.generate_java_code(self.solidity_code)
    
    
    def get_java_code(self):
        return self.java_code
    
    def get_solidity_code(self):
        return self.solidity_code
    
    
    def generate_java_code(self, source_code):
        solidity_pragma = self.__extract_solidity_version(source_code)
        if not solidity_pragma:
            solidity_version = self.solidity_compiler_version
        else:
            solidity_version = SolcSelector.install_solc_pragma_solc(self, solidity_pragma)
        
        self.__initialize_solidity_compiler(solidity_version)  
        
        helper = CompiledOutputGenerator(source_code)
        ast_to_cfg_obj = ASTToCFGObject(source_code, helper.get_ast())        
        return ast_to_cfg_obj.get_java_code()
        
        
        
        
    def __initialize_solidity_compiler(self, solc_version):
        solidity_compiler_version= solc_version
        if solidity_compiler_version.startswith("v0"):
            if solidity_compiler_version not in solcx.get_installed_solc_versions():
                msg = "Wait a while downloading Solidity compiler"
                try:
                    solcx.install_solc(solc_version)
                except Exception as e:
                    sys.stderr.write("Error while downloading required Solidity compiler "+ str(solidity_compiler_version) + str(e))
                    sys.stderr.write("Check with different Solidity compiler version" + str(e))
                    return None
            solcx.set_solc_version(solidity_compiler_version)
        
    
    def __extract_source_code(self, file_name:str):
        if file_name.startswith("."):
            file_name = os.path.join(os.getcwd(), file_name)
        with open(file_name) as fd:
            source_code = fd.read()
        return source_code
    
    
    def __extract_solidity_version(self, source_code):
        """extract solidity version based on pragma"""
        for line_text in source_code.split('\n'):
            if line_text.startswith('pragma solidity'):
                return line_text
        return None


if __name__ == "__main__":
    solidity_to_java = SolidityToJava(".\\sample_codes\\", "0")
    print("Solidity Code is:")
    print(solidity_to_java.get_solidity_code())
    print("Java Code is:")
    print(solidity_to_java.get_java_code())
    
    
            