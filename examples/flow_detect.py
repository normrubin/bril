'''
flow_detect.py

Program that analyzes the functions within a bril program and counts the number
of loops it detects, what functions are called, and if recursion is present.

Usage: "bril2json < *.bril | python flow_detect.py"
'''

import sys
import json


def read_json():
    json_data = 0
    try:
        json_data = json.load(sys.stdin)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        exit(1)
    return json_data


def commalist(li):
    if len(li) == 0:
        return ""
    if len(li) == 1:
        return li[0]
    str = ""
    for i in range(len(li) - 1):
        str = str + li[i] + ", "
    return str + li[len(li) - 1]


def argstats(foo):
    s = {}
    if 'args' in foo:
        for a in foo['args']:
            str = ""
            if 'ptr' in a['type']:
                str = f"{a['type']['ptr']} ptr"
            else:
                str = a['type']
            if str not in s:
                s[str] = []
            s[str].append(a['name'])
    return s


def enumops(foo):
    x = {}
    x['labels'] = {}
    x['ops'] = {}
    ins = foo['instrs']
    opnum = 0
    for i in range(len(ins)):
        curr = ins[i]
        if 'op' in curr:
            x['ops'][opnum] = curr
            opnum = opnum + 1
        elif 'label' in curr:
            opnum = opnum + 1
            x['labels'][curr['label']] = opnum
        else:
            print("unknown instruction type?")
    return x


def findloops(bar):
    baz = bar['labels']
    loops = []
    for k, v in bar['ops'].items():
        if 'jmp' in v['op'] or 'br' in v['op']:
            for label in v['labels']:
                if baz[label] < k:
                    to_add = True
                    for entry in loops:
                        if label in entry:
                            to_add = False
                    if to_add:
                        loops.append((label, baz[label], k, v))
    return loops


def findrecursion(bar, name):
    recurses = []
    for k, v in bar['ops'].items():
        if 'call' in v['op']:
            if name in v['funcs']:
                recurses.append((k, v))
    return recurses


def findcalls(bar):
    calls = []
    for k, v in bar['ops'].items():
        if 'call' in v['op']:
            calls.append((k, v))
    return calls


def printfuncstats(funcs):
    for foo in funcs:
        if 'name' in foo:
            print(f"{foo['name']}:")
        else:
            print("anonymous block:")

        if 'args' in foo:
            print("\targs:")
            for ty in argstats(foo).items():
                print(f"\t\t{ty[0]}: {commalist(ty[1])}")

        ops = enumops(foo)
        loops = findloops(ops)
        if len(loops) > 0:
            print(f"\tnum potential loops: {len(loops)}")

        calls = findcalls(ops)
        if len(calls) > 0:
            print(f"\tfunction calls: {len(calls)}")
            for c in calls:
                print(f"\t\t{c[1]['funcs'][0]}({commalist(c[1]['args'])})")

        if 'name' in foo:
            recur = findrecursion(ops, foo['name'])
        if len(recur) > 0:
            print("\trecursion present")

        print()


if __name__ == '__main__':
    j = read_json()
    funcs = j['functions']
    printfuncstats(funcs)
