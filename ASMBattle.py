import os
import re

class ASMBattle:
    """
    eax = status
    ebx = attribute
    ecx = nothing
    edx = nothing
    esi = HP
    sdi = opponent's HP
    """

    def __init__(self):
        self.eax = 0
        self.ebx = 0
        self.ecx = 0
        self.edx = 0
        self.esi = 10
        self.edi = 10
        self.eip = 0
        self.zflag = False
        self.cflag = False
        self.is_legal = False 

    def set_actions(self, acts):
        self.acts = acts

    def print_info(self):
        os.system("clear")
        print "eax: " + str(self.eax)
        print "ebx: " + str(self.ebx)
        print "ecx: " + str(self.ecx)
        print "edx: " + str(self.edx)
        print "esi: " + str(self.esi)
        print "edi: " + str(self.edi)
        print "eip: " + str(self.eip)
        print "zflag: " + str(self.zflag)
        print "cflag: " + str(self.cflag)
        raw_input()
            
    def ni(self, o):
        if self.eax == 2:
            self.esi -= 1
            o.edi = self.esi
        self.execute(self.acts[self.eip - 1], o)
        
        self.eip += 1
        if self.eip > len(self.acts):
            self.is_legal = False

    def execute(self, act, o):
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
            if re.search("jmp", act) \
                or (re.search("je", act) and self.zflag) \
                or (re.search("jne", act) and not self.zflag) \
                or (re.search("ja", act) and self.cflag):
                self.eip = int(dest) - 1

        elif re.search("cmp", act):
            dest = re.search("(e[abcd]x|e[sd]i|[\d]+)", act).group()
            src = re.search(", *(e[abcd]x|e[sd]i|[\d]+)", act).group().split(" ")[1]

            # eval
            dest = "self." + dest if is_reg(dest) else dest
            src = "self." + src if is_reg(src) else src
            exec "self.zflag = {} == {}".format(dest, src) in dict(locals())
            exec "self.cflag = {} > {}".format(dest, src) in dict(locals())

        elif re.search("int", act):
            if self.eax == 1:
                if self.ebx == 0 or self.ebx > 3:
                    if o.ebx == 0 or o.ebx > 3:
                        # NO vs NO
                        o.esi -= 3
                    else:
                        # NO vs any
                        o.esi -= 1
                else:
                    if o.ebx == 0 or o.ebx > 3:
                        # any vs NO
                        o.esi -= 3
                    elif self.ebx == o.ebx % 3 + 1:
                        # suppress
                        o.esi -= 3
                    elif self.ebx == o.ebx:
                        o.esi -= 2
                    else:
                        # suppressed
                        o.esi -= 1
                        
                self.edi = o.esi
            elif self.eax == 2:
                self.esi += 1
                o.edi = self.esi
            else:
                o.ebx = 0

    def is_running(self):
        return self.esi > 0 and self.is_legal
 
