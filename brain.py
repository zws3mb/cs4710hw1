__author__ = 'Zachary'
class brain:
    def __init__(self):
        self.var_map={}
        self.known_table={}
        self.working_mem=[]
        self.order_q=[]
    def teach(self,instring):
        if '=' in instring and instring[2] !='True' and instring[2] !='False':
            self.var_map[instring[0]]=instring[2]
            self.known_table[instring[0]]=False
            self.order_q.append(instring[0])
            return 'Assignment'+str(instring)
        elif '=' in instring:
            self.known_table[instring[0]]=eval(instring[2])
        else:
            if '->' in instring:
                self.working_mem.append((instring[0],instring[2]))
                return 'Rule'+str(instring)
        return 'Teach branch'+str(instring)
    def lister(self,instring):
        return str(self.var_map)+' '+str(self.known_table)
    def learn(self,instring):
        for item in self.working_mem:
            prop1, prop2 = item
            if prop1 in self.known_table:
                if self.known_table[prop1]:
                    self.known_table[prop2]=True
            else:
                # do stuff
                pass
        return instring
    def query(self,instring):
        return instring
    def why(self,instring):
        return instring
    def express(self,instring):
        return instring