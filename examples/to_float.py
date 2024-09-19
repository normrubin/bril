import json
import sys

int_to_float_op_mapping = {
    "add": "fadd",
    "sub": "fsub",
    "mul": "fmul",
    "div": "fdiv",
    "eq": "feq",
    "lt": "flt",
    "gt": "fgt",
    "le": "fle",
    "ge": "fge",
}


def ints_to_floats_in_function(func):
    # Change the args to float
    if 'args' in func:
        for arg in func['args']:
            if arg['type'] == 'int':
                arg['type'] = 'float'
    for instr in func['instrs']:
        # Instructions that have a int dest need to be changed to float
        if 'dest' in instr:
            if instr['type'] == 'int':
                instr['type'] = 'float'
        if 'op' in instr and instr['op'] in int_to_float_op_mapping:
            instr['op'] = int_to_float_op_mapping[instr['op']]


def ints_to_floats(bril_program):
    """
    Scans the json of a BRIL program, and changes every value type of int to float, and the
    instructions operating on the values to their float variants
    """
    for func in bril_program['functions']:
        ints_to_floats_in_function(func)
    return bril_program


if __name__ == '__main__':
    print(json.dumps(ints_to_floats(json.load(sys.stdin)), indent=2, sort_keys=True))
