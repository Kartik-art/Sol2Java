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
import time
import psutil
import re

def measure_peak_memory():
    process = psutil.Process(os.getpid())
    memory_before = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    return memory_before

def report_memory_usage(memory_before):
    process = psutil.Process(os.getpid())
    memory_after = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
    memory_used = memory_after - memory_before
    print(f"Memory Usage Increase: {memory_used:.2f} MB")
    


class SolidityToJava(object):
    
    def __init__(self, file_path=None, file_name=None, _version="0.5.9"):
        self.solidity_compiler_version = _version
        self.java_code = None
        self.solidity_code = self.__extract_source_code(file_path + file_name + ".sol")
        self.java_code = self.generate_java_code(self.solidity_code)
        
    def get_java_code(self):
        return self.java_code
    
    def get_solidity_code(self):
        return self.solidity_code
    
    def generate_java_code(self, source_code):
        start_parsing_time = time.time()
        solidity_pragma = self.__extract_solidity_version(source_code)
        if not solidity_pragma:
            solidity_version = self.solidity_compiler_version
        else:
            solidity_version = SolcSelector.install_solc_pragma_solc(self, solidity_pragma)
        
        self.__initialize_solidity_compiler(solidity_version)  
        
        # End of parsing timing
        end_parsing_time = time.time()
        
        # Start conversion timing
        start_conversion_time = time.time()
        
        helper = CompiledOutputGenerator(source_code)
        ast_to_cfg_obj = ASTToCFGObject(source_code, helper.get_ast())        
        
        # End conversion timing
        end_conversion_time = time.time()
        
        # Calculate durations
        parsing_duration = end_parsing_time - start_parsing_time
        conversion_duration = end_conversion_time - start_conversion_time
        
        print(f"Parsing took {parsing_duration:.2f} seconds.")
        print(f"Conversion took {conversion_duration:.2f} seconds.")
        
        return ast_to_cfg_obj.get_java_code()
    
    def generate_solidity_uint_class(self, file_path):
        """Reads the SolidityUint class from a text file and writes it to SolidityUint.java"""
        solidity_uint_text_file = os.path.join(file_path, "SolidityUint.txt")
        solidity_uint_java_file = os.path.join(file_path, "SolidityUint.java")
        
        # Debugging print statements for paths
        print(f"Looking for SolidityUint.txt at: {os.path.abspath(solidity_uint_text_file)}")
        
        # Check if the SolidityUint.txt file exists
        if os.path.exists(solidity_uint_text_file):
            print(f"SolidityUint.txt found at: {os.path.abspath(solidity_uint_text_file)}")
            
            # Read the content of SolidityUint.txt
            with open(solidity_uint_text_file, "r") as file:
                solidity_uint_content = file.read()
                print(f"Content of SolidityUint.txt:\n{solidity_uint_content}")
            
            # Write the content to SolidityUint.java
            with open(solidity_uint_java_file, "w") as java_file:
                java_file.write(solidity_uint_content)
            
            # Print the full path of where SolidityUint.java is created
            print(f"SolidityUint.java file has been created at: {os.path.abspath(solidity_uint_java_file)}")
        else:
            print(f"SolidityUint.txt file not found at: {os.path.abspath(solidity_uint_text_file)}")


    def generate_ethereum_address_class(self, file_path):
        """Reads the EthereumAddress class from a text file and writes it to EthereumAddress.java"""
        ethereum_address_text_file = os.path.join(file_path, "EthereumAddress.txt")
        ethereum_address_java_file = os.path.join(file_path, "EthereumAddress.java")
        
        # Debugging print statements for paths
        print(f"Looking for EthereumAddress.txt at: {os.path.abspath(ethereum_address_text_file)}")
        
        # Check if the EthereumAddress.txt file exists
        if os.path.exists(ethereum_address_text_file):
            print(f"EthereumAddress.txt found at: {os.path.abspath(ethereum_address_text_file)}")
            
            # Read the content of EthereumAddress.txt
            with open(ethereum_address_text_file, "r") as file:
                ethereum_address_content = file.read()
                print(f"Content of EthereumAddress.txt:\n{ethereum_address_content}")
            
            # Write the content to EthereumAddress.java
            with open(ethereum_address_java_file, "w") as java_file:
                java_file.write(ethereum_address_content)
            
            # Print the full path of where EthereumAddress.java is created
            print(f"EthereumAddress.java file has been created at: {os.path.abspath(ethereum_address_java_file)}")
        else:
            print(f"EthereumAddress.txt file not found at: {os.path.abspath(ethereum_address_text_file)}")
            
    def generate_solidity_bytes_class(self, file_path):
        """Reads the SolidityBytes class from a text file and writes it to SolidityBytes.java"""
        solidity_bytes_text_file = os.path.join(file_path, "SolidityBytes.txt")
        solidity_bytes_java_file = os.path.join(file_path, "SolidityBytes.java")
        
        # Debugging print statements for paths
        print(f"Looking for SolidityBytes.txt at: {os.path.abspath(solidity_bytes_text_file)}")
        
        # Check if the SolidityBytes.txt file exists
        if os.path.exists(solidity_bytes_text_file):
            print(f"SolidityBytes.txt found at: {os.path.abspath(solidity_bytes_text_file)}")
            
            # Read the content of SolidityBytes.txt
            with open(solidity_bytes_text_file, "r") as file:
                solidity_bytes_content = file.read()
                print(f"Content of SolidityBytes.txt:\n{solidity_bytes_content}")
            
            # Write the content to SolidityBytes.java
            with open(solidity_bytes_java_file, "w") as java_file:
                java_file.write(solidity_bytes_content)
            
            # Print the full path of where SolidityBytes.java is created
            print(f"SolidityBytes.java file has been created at: {os.path.abspath(solidity_bytes_java_file)}")
        else:
            print(f"SolidityBytes.txt file not found at: {os.path.abspath(solidity_bytes_text_file)}")

    def generate_solidity_fallback_class(self, file_path):
        """Reads the SolidityFallback class from a text file and writes it to SolidityFallback.java"""
        solidity_fallback_text_file = os.path.join(file_path, "SolidityFallback.txt")
        solidity_fallback_java_file = os.path.join(file_path, "SolidityFallback.java")
        
        # Debugging print statements for paths
        print(f"Looking for SolidityFallback.txt at: {os.path.abspath(solidity_fallback_text_file)}")
        
        # Check if the SolidityFallback.txt file exists
        if os.path.exists(solidity_fallback_text_file):
            print(f"SolidityFallback.txt found at: {os.path.abspath(solidity_fallback_text_file)}")
            
            # Read the content of SolidityFallback.txt
            with open(solidity_fallback_text_file, "r") as file:
                solidity_fallback_content = file.read()
                print(f"Content of SolidityFallback.txt:\n{solidity_fallback_content}")
            
            # Write the content to SolidityFallback.java
            with open(solidity_fallback_java_file, "w") as java_file:
                java_file.write(solidity_fallback_content)
            
            # Print the full path of where SolidityFallback.java is created
            print(f"SolidityFallback.java file has been created at: {os.path.abspath(solidity_fallback_java_file)}")
        else:
            print(f"SolidityFallback.txt file not found at: {os.path.abspath(solidity_fallback_text_file)}")

    def generate_blockchain_simulator_class(self, file_path):
        """Reads the BlockchainSimulator class from a text file and writes it to BlockchainSimulator.java"""
        blockchain_simulator_text_file = os.path.join(file_path, "BlockchainSimulator.txt")
        blockchain_simulator_java_file = os.path.join(file_path, "BlockchainSimulator.java")
        
        # Debugging print statements for paths
        print(f"Looking for BlockchainSimulator.txt at: {os.path.abspath(blockchain_simulator_text_file)}")
        
        # Check if the BlockchainSimulator.txt file exists
        if os.path.exists(blockchain_simulator_text_file):
            print(f"BlockchainSimulator.txt found at: {os.path.abspath(blockchain_simulator_text_file)}")
            
            # Read the content of BlockchainSimulator.txt
            with open(blockchain_simulator_text_file, "r") as file:
                blockchain_simulator_content = file.read()
                print(f"Content of BlockchainSimulator.txt:\n{blockchain_simulator_content}")
            
            # Write the content to BlockchainSimulator.java
            with open(blockchain_simulator_java_file, "w") as java_file:
                java_file.write(blockchain_simulator_content)
            
            # Print the full path of where BlockchainSimulator.java is created
            print(f"BlockchainSimulator.java file has been created at: {os.path.abspath(blockchain_simulator_java_file)}")
        else:
            print(f"BlockchainSimulator.txt file not found at: {os.path.abspath(blockchain_simulator_text_file)}")

    def generate_transaction_context_class(self, file_path):
        """Reads the TransactionContext class from a text file and writes it to TransactionContext.java"""
        transaction_context_text_file = os.path.join(file_path, "TransactionContext.txt")
        transaction_context_java_file = os.path.join(file_path, "TransactionContext.java")
        
        # Debugging print statements for paths
        print(f"Looking for TransactionContext.txt at: {os.path.abspath(transaction_context_text_file)}")
        
        # Check if the TransactionContext.txt file exists
        if os.path.exists(transaction_context_text_file):
            print(f"TransactionContext.txt found at: {os.path.abspath(transaction_context_text_file)}")
            
            # Read the content of TransactionContext.txt
            with open(transaction_context_text_file, "r") as file:
                transaction_context_content = file.read()
                print(f"Content of TransactionContext.txt:\n{transaction_context_content}")
            
            # Write the content to TransactionContext.java
            with open(transaction_context_java_file, "w") as java_file:
                java_file.write(transaction_context_content)
            
            # Print the full path of where TransactionContext.java is created
            print(f"TransactionContext.java file has been created at: {os.path.abspath(transaction_context_java_file)}")
        else:
            print(f"TransactionContext.txt file not found at: {os.path.abspath(transaction_context_text_file)}")


    
    def append_main_class_with_fallback(self, file_path, class_name):
        """
        Append a `Main` class to the Java file at `file_path`, using `class_name` as the primary contract.
        The `Main` class will wrap `class_name` in a `SolidityFallback` proxy and test defined and undefined methods.
        This modified version integrates `BlockchainSimulator` for account setup and state management.
        """
        main_class_content = f"""
        import java.lang.reflect.Method;
        import java.lang.reflect.Proxy;
        import java.math.BigInteger;
    
        // Main class to use {class_name} with SolidityFallback and BlockchainSimulator
        public class Main {{
            public static void main(String[] args) {{
                // Instantiate BlockchainSimulator and set up accounts
                BlockchainSimulator blockchainSimulator = new BlockchainSimulator();
                blockchainSimulator.addAccount("0x1234567890abcdef1234567890abcdef12345678", 1000);
                blockchainSimulator.addAccount("0xRecipientAddress", 500);
    
                // Instantiate the {class_name} contract and wrap it with fallback handling
                {class_name} originalContract = new {class_name}();
                IERC20 proxyContract = (IERC20) Proxy.newProxyInstance(
                        originalContract.getClass().getClassLoader(),
                        new Class<?>[]{{IERC20.class}},
                        new SolidityFallback.ContractInvocationHandler(originalContract)
                );
    
                // Test a defined method - should invoke normally and use BlockchainSimulator for state
                System.out.println("Testing defined method (transfer):");
                if (proxyContract.transfer(new EthereumAddress("0xRecipientAddress"), new SolidityUint(BigInteger.valueOf(100)))) {{
                    System.out.println("Transfer executed successfully.");
                }} else {{
                    System.out.println("Transfer failed.");
                }}
    
                // Test an undefined method to trigger fallback
                System.out.println("Testing undefined method (should trigger fallback):");
                try {{
                    Method undefinedMethod = proxyContract.getClass().getMethod("undefinedMethod");
                    undefinedMethod.invoke(proxyContract);
                }} catch (Exception e) {{
                    // Expected to invoke fallback method in SolidityFallback
                    System.out.println("Fallback method invoked as expected for undefinedMethod.");
                }}
            }}
        }}
        """
        # Append the `Main` class to the output file
        with open(file_path, "a") as file:
            file.write(main_class_content)

    
    def extract_contract_class_name(self, java_code):
        """
        Extracts the contract class name from Java code.
        Skips over specified class names (e.g., 'SafeMath') and continues to search 
        until it finds a different class name.
        """
        classes_to_skip = {"SafeMath"}  # Set of class names to skip
    
        # Search for all class declarations in the Java code
        matches = re.finditer(r'\bclass\s+(\w+)', java_code)
    
        for match in matches:
            class_name = match.group(1)
            # Check if the found class name is in the skip list
            if class_name not in classes_to_skip:
                return class_name
    
        # If no suitable class name is found, return None
        return None

        
    def __initialize_solidity_compiler(self, solc_version):
        solidity_compiler_version = solc_version
        if solidity_compiler_version.startswith("v0"):
            if solidity_compiler_version not in solcx.get_installed_solc_versions():
                msg = "Wait a while downloading Solidity compiler"
                try:
                    solcx.install_solc(solc_version)
                except Exception as e:
                    sys.stderr.write("Error while downloading required Solidity compiler " + str(solidity_compiler_version) + str(e))
                    sys.stderr.write("Check with different Solidity compiler version" + str(e))
                    return None
            solcx.set_solc_version(solidity_compiler_version)
    
    def __extract_source_code(self, file_name: str):
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

def remove_double_negations_and_fix_comparisons(lines):
    """
    Identify and remove double negations in any line of code.
    Specifically:
    1. For any line that contains two '!' symbols, remove them both.
    2. If one of the '!' symbols is part of a '!=', change '!=' to '=='.
    3. If '!' is not part of '!=', simply remove both '!' symbols.
    """
    modified_lines = []
    
    for line in lines:
        # Check if there are two '!' symbols in the line
        if line.count('!') >= 2:
            # Handle '!=' case: Replace '!=' with '=='
            line = line.replace('!=', '==')

            # Remove any remaining standalone '!'
            line = line.replace('!', '')
        
        # Add the modified (or original) line to the new list
        modified_lines.append(line)
    
    return modified_lines
        
def correct_function_signatures_and_initializations(lines):
    """
    Corrects function signatures that contain multiple access specifiers, unnecessary initializations,
    and improper initializations of SolidityUint in the return types and parameters.
    Also removes access specifiers from the parameters.
    """
    corrected_lines = []

    # Regular expression patterns
    double_access_specifiers_pattern = r'^\s*(public|private|protected)\s+(public|private|protected)?\s*'
    solidityuint_initialization_pattern = r'SolidityUint\s*=\s*new\s*SolidityUint\(.*?\)'
    
    # Pattern to detect and remove default initializations and access specifiers from function parameters
    default_param_pattern = r'(SolidityUint\s+\w+)\s*=\s*new\s*SolidityUint\(.*?\)'
    access_specifier_in_params_pattern = r'(protected|private|public)\s*'

    for line in lines:
        # Step 1: Remove extra access specifier if present
        corrected_line = re.sub(double_access_specifiers_pattern, r'\1 ', line)

        # Step 2: Remove SolidityUint initializations from both return type and parameters
        corrected_line = re.sub(solidityuint_initialization_pattern, 'SolidityUint', corrected_line.strip())

        # Step 3: Remove default parameter initializations from function parameters
        corrected_line = re.sub(default_param_pattern, r'\1', corrected_line)

        # Step 4: Remove any access specifiers (e.g., protected, public) inside the parameter list
        corrected_line = re.sub(access_specifier_in_params_pattern, '', corrected_line)

        corrected_lines.append(corrected_line + "\n")

    return corrected_lines
        
def handle_function_calls_with_double_mapping(lines):
    """Handle function calls where arguments contain double mappings and nested function calls, converting to Java syntax."""
    new_lines = []
    
    for index, line in enumerate(lines):
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)

        # First, match the outermost function (e.g., _approve), without capturing nested function calls yet
        outer_function_pattern = r'(\s*)(\w+)\((.*)\)'  # Group 1: Indentation, Group 2: Outer function name, Group 3: Outer arguments
        outer_match = re.search(outer_function_pattern, line)
        
        if outer_match:
            indentation = outer_match.group(1)  # Capture indentation (spaces or tabs before the function name)
            outer_function_name = outer_match.group(2)  # The outer function name (Group 2)
            outer_arguments = outer_match.group(3)  # Outer function's arguments (Group 3)

            # Split the outer function's arguments by commas
            argument_list = outer_arguments.split(',')

            # Now process each argument, check for nested functions or double mappings
            for i, arg in enumerate(argument_list):
                # Look for nested function calls inside arguments (e.g., sub(amount))
                nested_function_pattern = r'(\w+)\(([^()]*)\)'  # Match nested function calls, like sub(amount)
                nested_function_match = re.search(nested_function_pattern, arg)

                if nested_function_match:
                    # Capture the nested function details
                    nested_function_name = nested_function_match.group(1)  # Nested function name, e.g., sub
                    nested_arguments = nested_function_match.group(2)  # Nested function arguments, e.g., amount

                    # Check if the argument has double mappings (two sets of square brackets)
                    double_mapping_pattern = r'(\w+)\s*\[\s*([^\[\]]+)\s*\]\s*\[\s*([^\[\]]+)\s*\]'
                    double_mapping_match = re.search(double_mapping_pattern, arg)

                    if double_mapping_match:
                        var_outer = double_mapping_match.group(1)  # Outer variable (e.g., _allowances)
                        key_outer = double_mapping_match.group(2)  # First key (e.g., sender)
                        key_inner = double_mapping_match.group(3)  # Second key (e.g., spender)

                        # Convert double mapping into Java HashMap syntax (i.e., get(key1).get(key2))
                        java_double_mapping = f"{var_outer}.get({key_outer}).get({key_inner})"
                        
                        # Combine the double mapping with the nested function call (e.g., .sub(subtractedValue))
                        argument_list[i] = f"{java_double_mapping}.{nested_function_name}({nested_arguments})"
                else:
                    # Handle double mappings directly inside the outer function's arguments (without nested function call)
                    double_mapping_with_function_pattern = r'(\w+)\s*\[\s*([^\[\]]+)\s*\]\s*\[\s*([^\[\]]+)\s*\]'
                    double_mapping_match = re.search(double_mapping_with_function_pattern, arg)

                    if double_mapping_match:
                        var_outer = double_mapping_match.group(1)  # Outer variable (e.g., _allowances)
                        key_outer = double_mapping_match.group(2)  # First key (e.g., sender)
                        key_inner = double_mapping_match.group(3)  # Second key (e.g., spender)

                        # Replace with Java equivalent (HashMap syntax)
                        java_equivalent = f"{var_outer}.get({key_outer}).get({key_inner})"
                        argument_list[i] = java_equivalent

            # Reconstruct the outer function call with modified arguments
            new_arguments = ', '.join(argument_list)
            new_function_call = f"{indentation}{outer_function_name}({new_arguments})"  # Include indentation

            # Replace the original function call with the modified one
            line = line.replace(outer_match.group(0), new_function_call)

        # Append the modified or original line to the new_lines list
        new_lines.append(line + '\n')

    return new_lines
    
# New Implementation for handling comparisons within round brackets
def handle_comparisons_in_round_brackets(lines):
    """Identify and convert double mappings inside round brackets containing comparison statements to Java HashMap statements."""
    hashmap_replacements = []

    for index, line in enumerate(lines):
        # Check if the line contains round brackets
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)
        if '(' in line and ')' in line:
            # Extract the content inside round brackets
            pattern = r'\(([^()]+)\)'  # Captures content inside parentheses
            matches = re.findall(pattern, line)
            for match in matches:
                # Check for double mapping and comparison inside the parentheses
                comparison_pattern = r'(\w+)\s*\[\s*([^\[\]]+)\s*\]\s*\[\s*([^\[\]]+)\s*\]\s*([<>=!]+)\s*(\w+)'
                comparison_match = re.search(comparison_pattern, match)
                if comparison_match:
                    var_outer = comparison_match.group(1)  # Outer variable (e.g., _allowances)
                    key_outer = comparison_match.group(2)  # First key (e.g., sender)
                    key_inner = comparison_match.group(3)  # Second key (e.g., msg.sender)
                    operator = comparison_match.group(4)  # Comparison operator (e.g., >=)
                    rhs_var = comparison_match.group(5)  # RHS variable (e.g., amount)

                    # Generate the equivalent Java code for the comparison
                    java_comparison = f"{var_outer}.get({key_outer}).get({key_inner}).compareTo({rhs_var}) {operator.replace('=', '==')} 0"
                    hashmap_replacements.append((match, java_comparison))

        # Apply the replacements
        for original, replacement in hashmap_replacements:
            line = line.replace(original, replacement)

        lines[index] = line + '\n'

    return lines

def handle_mapping_return_statements_enhanced(lines):
    """Handle return statements that involve single or double mappings using string extraction"""
    for index, line in enumerate(lines):
        # Strip the line and normalize spaces
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)
        
        # Check if the line contains a return statement
        return_check_pattern = r'^\s*return\s+.*;'
        if re.search(return_check_pattern, line):
            # Extract variable name and keys from the return statement
            double_mapping_pattern = r'return\s+(\w+)\s*\[\s*([^\[\]]+)\s*\]\s*\[\s*([^\[\]]+)\s*\];'
            single_mapping_pattern = r'return\s+(\w+)\s*\[\s*([^\[\]]+)\s*\];'
            
            # Handle double mapping (e.g., return _allowances[owner][spender];)
            def replace_double_mapping(match):
                var_outer = match.group(1)  # Extracts the variable name (e.g., _allowances)
                key_outer = match.group(2)  # Extracts the first key (e.g., owner)
                key_inner = match.group(3)  # Extracts the second key (e.g., spender)
                return f"return {var_outer}.get({key_outer}).get({key_inner});"
            
            # Handle single mapping (e.g., return _balances[account];)
            def replace_single_mapping(match):
                var_outer = match.group(1)  # Extracts the variable name (e.g., _balances)
                key = match.group(2)  # Extracts the key (e.g., account)
                return f"return {var_outer}.get({key});"
            
            # Apply the appropriate replacement for single or double mappings
            line = re.sub(double_mapping_pattern, replace_double_mapping, line)
            line = re.sub(single_mapping_pattern, replace_single_mapping, line)
        
        # Replace the original line with the modified line
        lines[index] = line + '\n'
    
    return lines
    
    
def replace_msg_sender_with_global(lines):
    """
    Replace all occurrences of msg_sender with GlobalVariables.msg_sender in the generated Java code,
    except inside the GlobalVariables class.
    """
    inside_global_variables_class = False
    modified_lines = []
    
    for line in lines:
        stripped_line = line.strip()

        # Check if we are entering the GlobalVariables class
        if stripped_line.startswith("public class GlobalVariables"):
            inside_global_variables_class = True

        # Check if we are exiting the GlobalVariables class
        if inside_global_variables_class and stripped_line == "}":
            inside_global_variables_class = False

        # Perform the replacement if we are not inside the GlobalVariables class
        if not inside_global_variables_class:
            modified_line = line.replace("msg_sender", "GlobalVariables.msg_sender")
        else:
            # No replacement inside GlobalVariables class
            modified_line = line

        modified_lines.append(modified_line)
    
    return modified_lines

# Enhanced logic for handling mapping declarations and assignments
def handle_mapping_declarations_and_assignments_enhanced(lines):
    """Handle mapping declarations and assignments separately from return statements"""
    hashmaps = {}
    for index, line in enumerate(lines):
        line = line.strip()
        line = re.sub(r'\s+', ' ', line)
        
        # Identify all HashMap declarations
        match = re.match(r'HashMap<[^>]+>\s+(\w+)\s*=', line)
        if match:
            var_name = match.group(1)
            hashmaps[var_name] = True
        
        # Handle nested HashMap accesses (assignment)
        if len(hashmaps) > 0:
            nested_pattern = rf'({"|".join(map(re.escape, hashmaps.keys()))})\s*\[\s*([^\[\]]+)\s*\]\s*\[\s*([^\]]+)\]'
            
            def replace_nested(match):
                var_outer = match.group(1)
                key_outer = match.group(2)
                key_inner = match.group(3)
                return f"{var_outer}.get({key_outer}).get({key_inner})"
            
            line = re.sub(nested_pattern, replace_nested, line)
        
        # Handle single-level HashMap accesses (assignment)
        for var in hashmaps.keys():
            pattern = rf'{re.escape(var)}\s*\[\s*([^\]]+)\s*\]'
            replacement = rf'{var}.get(\1)'
            line = re.sub(pattern, replacement, line)
        
        # Handle assignments to HashMap entries
        assignment_pattern = rf'({"|".join(map(re.escape, hashmaps.keys()))})\s*\[\s*([^\]]+)\s*\]\s*=\s*(.+);'
        
        def replace_assignment(match):
            var = match.group(1)
            key = match.group(2)
            value = match.group(3)
            return f"{var}.put({key}, {value});"
        
        line = re.sub(assignment_pattern, replace_assignment, line)
        
        lines[index] = line + '\n'
    
    return lines, hashmaps
    
# Function to insert a new line before a class declaration if the previous line ends with '}'
def ensure_newline_before_class_declaration(lines):
    new_lines = []
    for index, line in enumerate(lines):
        # Check if the line ends with '}' (with possible spaces before it)
        if re.match(r'^\s*\}\s*class', line.strip()):
            # Insert a newline between '}' and 'class'
            split_line = re.sub(r'(\s*\})\s*(class)', r'\1\n\2', line)
            new_lines.append(split_line)
        else:
            new_lines.append(line)  # Add the current line as it is
    return new_lines
    

def fix_missing_constructor_names(lines):
    current_class_name = None  # Variable to store the class name
    new_lines = []
    
    for index, line in enumerate(lines):
        # Check if the line starts with 'class' to capture the class name
        class_match = re.match(r'^\s*class\s+(\w[\w\d_]*)\s*{', line.strip())
        if class_match:
            # Store the class name
            current_class_name = class_match.group(1)
            new_lines.append(line)
            continue

        # Check for constructor without class name, i.e., 'public (...)'
        constructor_match = re.match(r'^\s*public\svoid\s*\((.*)\)\s*{', line.strip())
        if constructor_match and current_class_name:
            # Extract the parameter list inside parentheses
            constructor_params = constructor_match.group(1)

            # Clean the parameters by removing initializations and access modifiers
            cleaned_params = clean_constructor_params(constructor_params)

            # Fix the constructor by adding the class name and cleaned parameters
            fixed_constructor = f'public {current_class_name}({cleaned_params}) {{'
            new_lines.append(fixed_constructor)
        else:
            new_lines.append(line)  # Add the current line as it is

    return new_lines

def clean_constructor_params(param_string):
    """
    Removes any access modifiers (like 'protected', 'private') and initializers from the parameter string.
    Example input: 'protected SolidityUint initialSupply = new SolidityUint(BigInteger.ZERO, 256)'
    Output: 'SolidityUint initialSupply'
    """
    cleaned_params = []
    params = param_string.split(',')

    for param in params:
        # Remove any initialization part (everything after '=' sign)
        param = param.split('=')[0].strip()

        # Split the remaining parts by space (e.g., 'protected SolidityUint initialSupply')
        param_parts = param.split()

        # Filter out the access modifiers ('protected', 'private', 'public') and ensure no extra initializers remain
        filtered_parts = [part for part in param_parts if part not in ['protected', 'private', 'public']]

        # Ensure only two parts remain: [datatype, variable name]
        if len(filtered_parts) >= 2:
            datatype = filtered_parts[0]  # First part is datatype (e.g., SolidityUint)
            variable_name = filtered_parts[1]  # Second part is the variable name (e.g., initialSupply)
            cleaned_param = f'{datatype} {variable_name}'
            cleaned_params.append(cleaned_param)

    # Join all cleaned parameters with commas for the constructor signature
    return ', '.join(cleaned_params)

def modify_get_statements(lines):
    """Modify statements like _balances.get(sender) = _balances.get(sender).sub(amount) to correct Java syntax."""
    modified_lines = []
    
    # Regex to detect assignments with 'get' on the left-hand side
    assignment_pattern = r'(\w+\.get\(\w+\))\s*=\s*(.+);'  # Matches LHS 'get' and anything on RHS
    
    for line in lines:
        line = line.strip()
        match = re.match(assignment_pattern, line)
        
        if match:
            lhs = match.group(1)  # Left-hand side with 'get'
            rhs = match.group(2)  # Right-hand side
            
            # Extract the variable and the key from the LHS
            lhs_variable_match = re.match(r'(\w+)\.get\((\w+)\)', lhs)
            if lhs_variable_match:
                var_name = lhs_variable_match.group(1)  # e.g., _balances
                key = lhs_variable_match.group(2)      # e.g., sender
                
                # Modify the LHS to use HashMap's 'put' method
                modified_lhs = f"{var_name}.put({key},"
                
                # Check if the RHS also contains a 'get' method and a function call
                rhs_nested_get_match = re.match(r'(\w+)\.get\((\w+)\)\.(\w+)\((.*)\)', rhs)
                if rhs_nested_get_match:
                    rhs_var = rhs_nested_get_match.group(1)   # e.g., _balances
                    rhs_key = rhs_nested_get_match.group(2)   # e.g., sender
                    function_call = rhs_nested_get_match.group(3)  # e.g., sub
                    function_arg = rhs_nested_get_match.group(4)   # e.g., amount
                    
                    # Modify the RHS to use HashMap's 'get' method followed by the function call
                    modified_rhs = f"{rhs_var}.get({rhs_key}).{function_call}({function_arg})"
                    
                    # Combine modified LHS and RHS into a valid statement
                    modified_line = f"{modified_lhs} {modified_rhs});"
                    modified_lines.append(modified_line + '\n')
                else:
                    # Handle cases where RHS does not contain a nested 'get', just a simple function call or value
                    modified_rhs = rhs
                    modified_line = f"{modified_lhs} {modified_rhs});"
                    modified_lines.append(modified_line + '\n')
            else:
                # If no match, just append the original line
                modified_lines.append(line + '\n')
        else:
            # If no match, just append the original line
            modified_lines.append(line + '\n')

    return modified_lines
 
def modify_big_integer_return_statements_and_comparisons(lines):
    """
    Recognize function bodies and modify:
    1. 'return 0;' to 'return BigInteger.ZERO;' if the function's return type is BigInteger.
    2. Statements that use 'compareTo(0)' to 'compareTo(BigInteger.ZERO)' within the function body.
    """
    inside_function = False  # Flag to detect when we are inside a function
    current_return_type = None  # Stores the current function's return type
    brace_count = 0  # To track the hierarchical braces
    modified_lines = []
    
    # Regex pattern to recognize function signatures with required access modifier
    function_signature_pattern = r'(public|private|protected)\s+(\w+)\s+(\w+)\s*\(.*\)\s*\{'
    
    # Regex to detect 'compareTo(0)' within function bodies
    compare_to_zero_pattern = r'\bcompareTo\s*\(\s*0\s*\)'
    
    # Loop through each line to identify functions and modify as needed
    for line in lines:
        # Check if the line matches a function signature
        function_match = re.match(function_signature_pattern, line.strip())
        
        if function_match:
            # Capture the return type (group 2) and function name (group 3)
            current_return_type = function_match.group(2)
            inside_function = True
            brace_count = 1  # Initialize brace count when function starts
        
        # If we are inside a function and the return type is BigInteger
        if inside_function and current_return_type == "BigInteger":
            # Check if the line contains 'return 0;'
            if 'return 0;' in line:
                # Modify the line to return BigInteger.ZERO
                line = line.replace('return 0;', 'return BigInteger.ZERO;')
            
            # Check if the line contains 'compareTo(0)' and replace it with 'compareTo(BigInteger.ZERO)'
            if re.search(compare_to_zero_pattern, line):
                line = re.sub(compare_to_zero_pattern, 'compareTo(BigInteger.ZERO)', line)
        
        # Track opening and closing braces to detect function scope
        brace_count += line.count('{') - line.count('}')
        
        # If brace count reaches zero, it means the function has ended
        if inside_function and brace_count == 0:
            inside_function = False  # Reset the flag when function ends
            current_return_type = None  # Reset the return type
        
        # Add the (possibly modified) line to the output
        modified_lines.append(line)
        
    return modified_lines

# New function to check, update zero address comparisons in if conditions, and remove extra parentheses
def add_get_address_to_zero_address_comparisons(lines):
    updated_lines = []
    # Adjusted pattern to handle the exact structure: "if((variable.equals("0x...40 hex chars..."))){" and capture variable name
    zero_address_pattern = re.compile(r'^if\(\((\w+)\.equals\("0x[0-9a-fA-F]{40}"\)\)\)\s*\{$')
    
    for line in lines:
        match = zero_address_pattern.search(line)
        if match:
            # Capture the variable name (e.g., account in account.equals)
            var_name = match.group(1)
            # Modify the line to add .getAddress() before .equals and remove the extra parentheses
            modified_line = line.replace(f"if(({var_name}.equals", f"if({var_name}.getAddress().equals")
            updated_lines.append(modified_line)
            
        else:
            updated_lines.append(line)
    
    return updated_lines

if __name__ == "__main__":
    memory_before = measure_peak_memory()
    start_final_assembly_time = time.time()
    solidity_to_java = SolidityToJava(".\\sample_codes\\", "0")
    java_code = solidity_to_java.get_java_code()  # Get the Java code generated
    print("Solidity Code is:")
    print(solidity_to_java.get_solidity_code())
    print("Java Code is:")
    
    default_java_code = """
    public class Account {
    private String address;
    private float balance;

    public Account(String address, float balance) {
        this.address = address;
        this.balance = balance;
    }

    public String getAddress() {
        return address;
    }

    public void setAddress(String address) {
        this.address = address;
    }

    public float getBalance() {
        return balance;
    }

    public void setBalance(float balance) {
        this.balance = balance;
    }

    @Override
    public String toString() {
        return "Address: " + address + ", Balance: " + balance;
    }

    public boolean approximate(float amount) {
        Account senderAccount = accounts[0];
        Account receiverAccount = accounts[1];

        float sender_balance = senderAccount.getBalance();
        float receiver_balance = receiverAccount.getBalance();

        System.out.println("Sender balance: " + sender_balance);
        System.out.println("Receiver balance: " + receiver_balance);

        if (amount > sender_balance) {
            System.out.println("Insufficient balance in sender's account");
            return false;
        } else {
            receiver_balance += amount;
            sender_balance -= amount;

            System.out.println("Transaction successful");
            System.out.println("Final sender balance: " + sender_balance);
            System.out.println("Final receiver balance: " + receiver_balance);

            return true;
        }
    }

    public boolean send(float amount) {
        return approximate(amount);
    }

    public boolean transfer(float amount) {
        boolean result = approximate(amount);
        if (!result) {
            System.out.println("Exception on transfer");
        }
        return result;
    }

    private static Account[] accounts = new Account[10];

    public static void main(String[] args) {
        accounts[0] = new Account("0x123456789abcdef0123456789abcdef0123456789", 1000.0f);
        accounts[1] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 2500.0f);
        accounts[2] = new Account("0x9876543210abcdef0123456789abcdef01234567", 150.0f);
        accounts[3] = new Account("0xfedcba9876543210abcdef0123456789abcdef012", 3000.0f);
        accounts[4] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 500.0f);
        accounts[5] = new Account("0x0123456789abcdef0123456789abcdef01234567", 1200.0f);
        accounts[6] = new Account("0xfedcba9876543210abcdef0123456789abcdef012", 750.0f);
        accounts[7] = new Account("0x123456789abcdef0123456789abcdef0123456789", 2000.0f);
        accounts[8] = new Account("0x9876543210abcdef0123456789abcdef01234567", 1800.0f);
        accounts[9] = new Account("0xabcdef0123456789abcdef0123456789abcdef012", 900.0f);

        Account accountInstance = new Account("", 0.0f);

        boolean sendStatus = accountInstance.send(500.0f);
        System.out.println("Send status: " + sendStatus);

        boolean transferStatus = accountInstance.transfer(700.0f);
        System.out.println("Transfer status: " + transferStatus);
    }
"""
    default_java_lines = """import java.math.BigInteger;
import java.util.HashMap;
import java.util.Map;

public class GlobalVariables {
    public static EthereumAddress msg_sender = "0x1234567890abcdef1234567890abcdef12345678";
}
"""
    
    print(solidity_to_java.get_java_code())
    output_string = solidity_to_java.get_java_code()
    output_string = default_java_lines + output_string
    output_file_path = "sol_to_java_output.txt"
    
    with open(output_file_path, "w") as output_file:
        output_file.write(output_string)
    
    with open(output_file_path, "r") as output_file:
        lines = output_file.readlines()
    
    # Extract the main contract class name
    contract_class_name = solidity_to_java.extract_contract_class_name(java_code)
    if contract_class_name:
        print(f"Extracted contract class name: {contract_class_name}")
    else:
        print("Could not extract contract class name.")
    
    # Step 2: Replace msg_sender with GlobalVariables.msg_sender
    lines = replace_msg_sender_with_global(lines)
    
    # Handle mapping declarations and assignments
    lines, hashmaps = handle_mapping_declarations_and_assignments_enhanced(lines)

    # Handle return statements separately
    lines = handle_mapping_return_statements_enhanced(lines)
    
    # Handle comparison statements within round brackets
    lines = handle_comparisons_in_round_brackets(lines)
    
    # Handle function calls with double mapping variables inside the arguments
    lines = handle_function_calls_with_double_mapping(lines)
    
    # Ensure a new line before class declarations when a line ends with '}'
    lines = ensure_newline_before_class_declaration(lines)
    
    # Write the output to the file after ensuring newline before class declaration
    with open(output_file_path, "w") as output_file:
        output_file.writelines(lines)

    # Reopen the updated file for further processing
    with open(output_file_path, "r") as output_file:
        lines = output_file.readlines()

    
    # Fix missing constructor names using stored class names
    lines = fix_missing_constructor_names(lines)
    
    
    # Enhanced Logic: Add `;` at the end of lines that do not end with `{`, `}`, or `;`
    # and make sure the line is not empty
    def add_semicolon_to_lines(lines):
        for index, line in enumerate(lines):
            stripped_line = line.strip()
            # Check if the line is not empty and doesn't end with `{`, `}`, or `;`
            if stripped_line and not stripped_line.endswith(('{', '}', ';')):
                lines[index] = line.rstrip() + ';\n'
        return lines

    # Run the new logic after all other function calls
    lines = add_semicolon_to_lines(lines)

    # Modify get statements in the Java code
    lines = modify_get_statements(lines) 
    
    with open(output_file_path, "w") as output_file:
        output_file.writelines(lines)
        
        
    # Enhanced logic for handling the new transformation after all the other steps
    with open(output_file_path, "r") as output_file:
        lines = output_file.readlines()

    # Modify 'return 0;' to 'return BigInteger.ZERO;' for functions returning BigInteger
    lines = modify_big_integer_return_statements_and_comparisons(lines)
    
    # Step 2: Apply double negation removal and fix comparisons
    lines = remove_double_negations_and_fix_comparisons(lines)

    # Write the modified lines back to the output file
    with open(output_file_path, "w") as output_file:
        output_file.writelines(lines)
        
    # Read the generated Java code
    with open(output_file_path, "r") as output_file:
        lines = output_file.readlines()
    
    # Correct the function signatures using the new function
    corrected_lines = correct_function_signatures_and_initializations(lines)
    
    # Write the corrected Java code back to the file
    with open(output_file_path, "w") as output_file:
        output_file.writelines(corrected_lines)

    # Apply `getAddress()` to zero address comparisons, open output file, parse, apply updates, write back
    with open(output_file_path, "r") as output_file:
        final_lines = output_file.readlines()

    final_updated_lines = add_get_address_to_zero_address_comparisons(final_lines)

    with open(output_file_path, "w") as output_file:
        output_file.writelines(final_updated_lines)
    
        
    # Extract the directory from output_file_path and generate SolidityUint.java in the same directory
    directory_path = os.path.dirname(output_file_path)
    solidity_to_java.generate_solidity_uint_class(directory_path)
    solidity_to_java.generate_ethereum_address_class(directory_path)
    solidity_to_java.generate_solidity_bytes_class(directory_path)
    solidity_to_java.generate_solidity_fallback_class(directory_path)
    solidity_to_java.generate_blockchain_simulator_class(directory_path)
    solidity_to_java.generate_transaction_context_class(directory_path)
    
    # Append the `Main` class to the file using the extracted contract name
    if contract_class_name:
        solidity_to_java.append_main_class_with_fallback(output_file_path, contract_class_name)
    else:
        print("Skipping Main class generation due to missing contract class name.")
    
    end_final_assembly_time = time.time()
    final_assembly_duration = end_final_assembly_time - start_final_assembly_time
    
    print(f"Final Assembly took {final_assembly_duration:.2f} seconds.")
    
    report_memory_usage(memory_before)  # Report memory usage after the translation process
