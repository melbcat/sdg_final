import os
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
        def print_info():
            print self.acts[self.eip - 1]
            print "eax: " + str(self.eax)
            print "ebx: " + str(self.ebx)
            print "ecx: " + str(self.ecx)
            print "edx: " + str(self.edx)
            print "esi: " + str(self.esi)
            print "edi: " + str(self.edi)
            print "eip: " + str(self.eip)
            print "zflag: " + str(self.zflag)
            raw_input()
            os.system("clear")
            
        self.eip += 1
        if self.eip > len(self.acts):
            self.is_legal = False
        else:
            self.execute(self.acts[self.eip - 1])

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
            return
        elif re.search("cmp", act):
            dest = re.search("(e[abcd]x|e[sd]i|[\d]+)", act).group()
            src = re.search(", *(e[abcd]x|e[sd]i|[\d]+)", act).group().split(" ")[1]

            # eval
            dest = "self." + dest if is_reg(dest) else dest
            src = "self." + src if is_reg(src) else src
            exec "self.zflag = {} == {}".format(dest, src) in dict(locals())
        
    def is_running(self):
        return self.esi > 0 and self.is_legal
 
