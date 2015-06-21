#!/usr/bin/python

import sys
import argparse
import re
from ASMBattle import ASMBattle

s = ASMBattle()
e = ASMBattle()

def check_fmt(act):
    pat = "^ *("
    # legal instructions
    for ins in ["mov", "int", "cmp", "jmp", "je", "ja", "jne"]:
        pat += ins + "|"
    pat = pat[:-1]
    pat += ") +(e[abcd]x|e[sd]i|0x80|[\d]+)($| *, *(e[abcd]x|e[sd]i|[\d]+)$)"
    return re.search(pat, act)

def check_logic(act):
    if re.search("^ *mov*?", act):
        return re.search("^ *mov +e[abcd]x*?", act)
    elif re.search("^ *(jmp|je|ja|jne)", act):
        return re.search("^ *(jmp|je|ja|jne) +[\d]+ *$", act)
    elif re.search("^ *int*?", act):
        return re.search(" *int +0x80 *$", act)
    elif re.search("^ *cmp*?", act):
        return True 
    else:
        return False

def parse_actions(acts):
    for act in acts:
        if not check_fmt(act) or not check_logic(act):
            print "Instruction \"{}\" illegal".format(act)
            return False
        
    return True

def start_game():
    s.eip = 1
    e.eip = 1

    while True:
        if not s.is_running() or not e.is_running():
            return
            
        print s.acts[s.eip - 1],
        print e.acts[s.eip - 1]
        if "int" not in s.acts[s.eip - 1]:
            s.ni()
        if "int" not in e.acts[e.eip - 1]:
            e.ni()

        s.action(e)
        e.action(s)
    

def main():
    parser = argparse.ArgumentParser(description='ASM battle')
    parser.add_argument("-e", "--enemy", help="Enemy's actions.", default="enemy")
    parser.add_argument("-s", "--self", help="Your's actions.", default="self")
    args = parser.parse_args()


    self_acts = open(args.self, "r").read().strip().split("\n")
    enemy_acts = open(args.enemy, "r").read().strip().split("\n")
    
    if parse_actions(self_acts):
        s.set_actions(self_acts)
        s.is_legal = True
    if parse_actions(enemy_acts):
        e.set_actions(enemy_acts)
        e.is_legal = True

    start_game()
    
    # judge winner
    if s.is_legal and e.is_legal:
        if s.esi == 0 and e.esi == 0:
            winner = 2
        else:
            winner = 0 if s.esi > 0 else 1
    else:
        if not s.is_legal and not e.is_legal:
            winner = 2
        else:
            winner = 0 if s.is_legal else 1

    print winner
        
main()
