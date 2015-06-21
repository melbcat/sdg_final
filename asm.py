import sys
import argparse
import re

class ASMBattle:
    """
    eax = action
    ebx = attribute
    ecx = nothing
    edx = nothing
    esi = HP
    sdi = opponent's HP
    zflag = condition jump
    """

    def __init__(self):
        self.eax = 0
        self.ebx = 0
        self.ecx = 0
        self.edx = 0
        self.esi = 100
        self.edi = 100
        self.eip = 0
        self.zflag = False
        self.is_legal = False 

    def set_actions(self, acts):
        self.acts = acts

    def ni(self):
        self.eip += 1
        if self.eip > len(self.acts):
            self.is_legal = False
        else:
            e.execute(self.acts[self.eip - 1])

    def execute(self, act):
        def is_reg(arg):
            return re.search("(e[abcd]x|e[sd]i)", arg)
            
        if re.search("mov", act):
            dest = re.search("e[abcd]x", act).group()
            src = re.search(", *(e[abcd]x|e[sd]i|[\d]+)", act).group().split(" ")[1]

            # eval
            dest = "self." + dest
            src = "self." + src if is_reg(src) else src
            exec "{} = {}".format(dest, src) in dict(locals())

        elif re.search("(jmp|je|ja|jne)", act):
            dest = re.search("[\d]+", act).group()
            if re.search("jmp", act) or self.zflag == True:
                self.eip = int(dest) - 1
        elif re.search("int", act):
            print
        elif re.search("cmp", act):
            dest = re.search("(e[abcd]x|e[sd]i|[\d]+)", act).group()
            src = re.search(", *(e[abcd]x|e[sd]i|[\d]+)", act).group().split(" ")[1]

            # eval
            dest = "self." + dest if is_reg(dest) else dest
            src = "self." + src if is_reg(src) else src
            exec "self.zflag = {} == {}".format(dest, src) in dict(locals())
            
        return
        
    def is_running(self):
        return self.esi > 0 and self.is_legal
        
        
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
    while True:
        if not s.is_running():
            return 0 
        if not e.is_running():
            return 1 
            
        s.ni()
        e.ni()
    

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

        
main()
