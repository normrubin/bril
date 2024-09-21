import json
import sys

def myFunction():
    functions = []
    function_calls = {}
    prog = json.load(sys.stdin)
    
    for func in prog['functions']:
        functions.append(func['name'])
        function_calls[func['name']] = 0  # Initialize with zero calls
    
    for func in prog['functions']:
        for instr in func['instrs']:
            if instr.get('op') == 'call':
                called_func = instr['funcs'][0]
                if called_func not in function_calls:
                    function_calls[called_func] = 0  # Initialize if not present
                function_calls[called_func] += 1
    
    print("Number of Functions: ", len(functions))
    print("------------------------")
    
    print("Function Call Counts:")
    
    max_func_name_length = max(len(func) for func in function_calls.keys())
    for func, count in function_calls.items():
        print(f"{func.ljust(max_func_name_length)}: {count}")

if __name__ == '__main__':
    myFunction()
