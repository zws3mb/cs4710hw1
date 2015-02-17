__author__ = 'Zachary'
class listtrack(list):
    state=0
    def __init__(self):
        self.step=[]
        self.phrase={0:'I KNOW THAT ',1:'BECAUSE',2:'I THUS KNOW THAT',3:'I KNOW IT IS NOT TRUE THAT',4:'BECAUSE IT IS NOT TRUE THAT',5:'THUS I CANNOT PROVE THAT'}
        super(listtrack,self).__init__()
    def append(self, p_object):
        self.step.append(self.phrase[listtrack.state]+'('+p_object+')')
        super(listtrack,self).append(p_object)
    def __iadd__(self, other):
        self.step.append(self.phrase[listtrack.state]+'('+other+')')
        super(listtrack,self).__iadd__(other)

class brain:

    def __init__(self):
        self.var_map={}
        self.known_table={}
        self.working_mem=[]
        self.order_q=[]
        self.order_v_q=[]
        self.orig_rule_exp=[]
        self.op_dict={'&':'and','|':'or','!':'not'}
        self.thought=''
        self.subconscious=[]
    def teach(self,instring):
        if '=' in instring and instring[2] !='True' and instring[2] !='False':
            self.var_map[instring[0]]=instring[2]
            self.known_table[instring[0]]=False
            self.order_q.append(instring[0])
            return 'Assignment'+str(instring)
        elif '=' in instring:
            self.known_table[instring[0]]=eval(instring[2])
            self.order_v_q.append(instring[0])
        else:
            if '->' in instring:
                self.working_mem.append((instring[0],instring[2]))
                return 'Rule'+str(instring)
        return 'Teach branch'+str(instring)
    def lister(self,instring):
        outstring='Variables:\n'
        for v in self.order_q:
            outstring+='\t'+v+' = '+self.var_map[v]+'\n'
        outstring+='\nFacts:\n'
        for v in self.order_v_q:
            outstring+='\t'+v+'\n'
        outstring+='\nRules:'+'\n'
        for i in range(0,len(self.working_mem)):
            outstring+='\t'+str(self.orig_rule_exp[i])+' -> '+self.working_mem[i][1]+'\n'
        #print outstring
        return outstring
    def learn(self,instring):
        change=True
        while change:
            change=False
            for item in self.working_mem:
                prop1, prop2 = item
                if prop1 in self.known_table:
                    if self.known_table[prop1] and not self.known_table[prop2]:
                        print str(prop2)+' is now True.'
                        change=True
                        self.known_table[prop2]=True
                        self.order_v_q.append(prop2)
                # elif prop2 in self.known_table:
                #     if not self.known_table[prop2]:
                #         print str(prop1)+'is now False.'
                #         self.known_table[prop1]=False
                elif eval(self.evaluate_tree(prop1,'Learn')) and not self.known_table[prop2]:
                    print str(prop2)+' is now True.'
                    change=True
                else:
                    # do stuff
                    pass
        return self.lister('dummy')



    def query(self,instring):
        current=instring[0]
        self.evaluate_tree(current,'Query')
        print str(self.thought)+'=>'
        return 'I THINK:'+str(eval(self.thought))
    def get_rule_string(self,exp):
        for i in range(0,len(self.working_mem)):
            if exp == self.working_mem[i][1]:
                return str(self.orig_rule_exp[i])+' -> '+self.working_mem[i][1]+'\n'
        return 'Error in Rulefind'

    def backchain(self,instr):

        for p1,p2 in self.working_mem:
            if instr == p2:

                tobeval=[]
                self.bevaluate_tree(p1,tobeval)
                outcome= eval(''.join(tobeval))
                if outcome:
                    self.subconscious.append('BECAUSE ')
                else:
                    self.subconscious.append('BECAUSE IT IS NOT TRUE THAT ')#('+self.get_rule_string(p1)+'->'+self.var_map[p2]+')')
                return outcome
        return False
    def bevaluate_tree(self,ptree,tobeval):
        current=ptree
        print 'Evaluating:'+str(ptree)
        #self.subconscious.append(self.get_rule_string(ptree))
        if isinstance(current,basestring):
            self.back_thought(str(self.convert(current,'Query')),tobeval)
        else:
            self.inorder_back(ptree,tobeval)

    def back_thought(self,val,tobeval):
        tobeval+=val
    def inorder_back(self,node,tobeval):
        if node is not None:
            self.back_thought('(',tobeval)
            self.inorder_back(node.left, tobeval)
            self.back_thought(str(self.convert(node.value,'Query')),tobeval)
            self.inorder_back(node.right, tobeval)
            self.back_thought(')',tobeval)

    def convert(self,instr,flag):
        if flag =='Learn':
            if instr in self.op_dict:
                return self.op_dict[instr]
            elif instr in self.known_table:
                return self.known_table[instr]
            # elif instr in self.var_map:
            #     return self.var_map[instr]
            elif instr in self.working_mem:
                return self.working_mem[instr]
        elif flag=='Query':
            self.subconscious.append('\n')
            if instr in self.op_dict:
                return self.op_dict[instr]
            elif instr in self.known_table:
                if self.known_table[instr]:
                    self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+')')
                    return self.known_table[instr]
                else:
                    val=self.backchain(instr)
                    if val:
                        self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+')')
                    else:
                        self.subconscious.append('I CANNOT PROVE ('+self.var_map[instr]+')')
                    return val
            # elif instr in self.var_map:
            #     return self.var_map[instr]
            # elif instr in self.working_mem:
            #     return self.working_mem[instr]
    def gather(self,val):
        self.thought+=' '+val
    def inorder(self,node,exp):
        if node is not None:
            self.gather('(')
            self.inorder(node.left, exp)
            self.gather(str(self.convert(node.value,exp)))
            self.inorder(node.right, exp)
            self.gather(')')

    def evaluate_tree(self,ptree,exp):
        self.thought=''
        current=ptree
        print 'Evaluating:'+str(ptree)
        if isinstance(current,basestring):
            self.gather(str(self.convert(current,exp)))
        else:
            self.inorder(ptree,exp)

        return self.thought


    def why(self,instring):
        self.subconscious=[]
        tobeval=[]
        self.bevaluate_tree(instring[0],tobeval)

        output=eval(''.join(tobeval))
        if output:
            self.subconscious.append('I KNOW THAT ')
            self.subconscious.append(str(output))
        else:
            self.subconscious.append('I KNOW IT IS NOT TRUE THAT')
            self.subconscious.append(str(output))
        reversed=[i for i in self.subconscious[::-1]]
        #print self.subconscious

        return ''.join(reversed)
    def clear(self,instring):
        if instring == 'Yes':
            self.var_map={}
            self.known_table={}
            self.working_mem=[]
            self.order_q=[]
            self.order_v_q=[]
            self.orig_rule_exp=[]
            self.op_dict={'&':'and','|':'or','!':'not'}
            self.thought=''
