__author__ = 'Zachary'

class brain:

    def __init__(self):
        self.whyexp=''
        self.var_map={}
        self.known_table={}
        self.working_mem=[]
        self.order_q=[]
        self.order_v_q=[]
        self.orig_rule_exp=[]
        self.op_dict={'&':'and','|':'or','!':'not'}
        self.thought=''
        self.subconscious=[]
        self.currentop=None
        self.varMemory = []

    def teach(self,instring):
        self.currentop='Teach'
        if '=' in instring and instring[2] !='true' and instring[2] !='false':
            if instring[0] not in self.known_table:
                #print "This is new to me"
                self.var_map[instring[0]]=instring[2]
                self.known_table[instring[0]]=False
                self.order_q.append(instring[0])
                return ''
                #return 'Assignment'+str(instring)

            else:
                return "Error: Variable " + str(instring[0]) + " already declared."
        elif '=' in instring:

            if instring[0] not in self.known_table:
                return "Error: Variable " + str(instring[0]) + " must be declared first before given value."

            self.known_table[instring[0]]=eval(instring[2].capitalize())

            if(eval(instring[2].capitalize()) and instring[0] not in self.order_v_q):
                self.order_v_q.append(instring[0])
            elif instring[0] in self.order_v_q:
                self.order_v_q.remove(instring[0])
        else:
            if '->' in instring and instring[2] in self.known_table:
                self.working_mem.append((instring[0],instring[2]))
                return ''
                #return 'Rule'+str(instring)
            else:
                return ''
                #return "Error.  One variable in this is undeclared."
        return ''
        #return 'Teach branch'+str(instring)

    def lister(self,instring):
        self.currentop='List'
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
        self.currentop='Learn'
        change=True
        while change:
            change=False
            for item in self.working_mem:
                prop1, prop2 = item
                if prop1 in self.known_table:
                    if self.known_table[prop1] and not self.known_table[prop2]:
                        #print "This is the one"
                        #print str(prop2)+' is now True.'
                        change=True
                        self.known_table[prop2] = True
                        #print(self.known_table[prop2])
                        self.order_v_q.append(prop2)
                # elif prop2 in self.known_table:
                #     if not self.known_table[prop2]:
                #         print str(prop1)+'is now False.'
                #         self.known_table[prop1]=False
                elif eval(self.evaluate_tree(prop1,'Learn')) and (not self.known_table[prop2]):
                    #print str(prop2)+' is now True.'
                    self.known_table[prop2] = True
                    self.order_v_q.append(prop2)

                    change=True
                else:
                    # do stuff
                    pass
        return self.lister('dummy')



    def query(self,instring):
        self.currentop='Query'
        current=instring[0]
        self.evaluate_tree(current,'Query')
        #print str(self.thought)+'=>'
        print self.thought
        return 'I THINK: '+str(eval(self.thought))
    def get_rule_string(self,exp):
        for i in range(0,len(self.working_mem)):
            if exp == self.working_mem[i][0]:
                return self.instring_to_english(str(self.orig_rule_exp[i]))
        return 'Error in Rulefind'

    def backchain(self,instr):

        for p1,p2 in self.working_mem:
            if instr == p2:

                tobeval=[]
                self.bevaluate_tree(p1,tobeval)
                outcome= eval(''.join(tobeval))
                if outcome and instr not in self.varMemory:
                    self.subconscious.append('BECAUSE '+self.get_rule_string(p1)+", ")
                elif instr not in self.varMemory:
                    self.varMemory.append(instr)
                    self.subconscious.append('BECAUSE IT IS NOT TRUE THAT '+self.get_rule_string(p1))+ ", " #('+self.get_rule_string(p1)+'->'+self.var_map[p2]+')')
                return outcome
        return 'NORULE'
    def bevaluate_tree(self,ptree,tobeval):
        current=ptree
        #print 'Back Evaluating:'+str(ptree)
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
        #print 'Converting: '+instr
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
            # self.subconscious.append('\n')
            if instr in self.op_dict:
                #self.subconscious.append(self.op_dict[instr].upper()+' ')
                return self.op_dict[instr]
            elif instr in self.known_table:
                if self.currentop=='Query':
                    if self.known_table[instr]:
                        self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+') \n')
                        return self.known_table[instr]
                    else:
                        val=self.backchain(instr)
                        if val == "NORULE":
                            return self.known_table[instr]
                        if val:
                            self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+')')
                        else:
                            self.subconscious.append('I CANNOT PROVE ('+self.var_map[instr]+')')
                        return val
                elif self.currentop=='Why':
                    val=self.backchain(instr)
                    #print str(instr)
                    if val=='NORULE':
                        if self.known_table[instr] and instr not in self.varMemory:
                            self.varMemory.append(instr)
                            #print "instr: " + str(instr) + " added to var mem"
                            self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+') \n')
                        elif instr not in self.varMemory:
                            self.varMemory.append(instr)
                            #print "instr: " + str(instr) + " added to var mem"
                            self.subconscious.append('I CANNOT PROVE ('+self.var_map[instr]+') \n')
                        return self.known_table[instr]
                    elif val and instr not in self.varMemory:
                        self.varMemory.append(instr)
                        self.subconscious.append('I KNOW THAT ('+self.var_map[instr]+') \n')
                    elif instr not in self.varMemory:
                        self.varMemory.append(instr)
                        self.subconscious.append('I CANNOT PROVE ('+self.var_map[instr]+') \n')
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
        #print 'Evaluating:'+str(ptree)
        if isinstance(current,basestring):
            self.gather(str(self.convert(current,exp)))
        else:
            self.inorder(ptree,exp)

        return self.thought

    def instring_to_english(self,instring):
        out='('
        for v in instring:
            if v in self.var_map:
                out+=self.var_map[v]
            elif v == '!':
                out+=' NOT '
            elif v == '&':
                out+=' AND '
            elif v == '|':
                out+=' OR '
            else:
                out+=v
        out+=')'
        #print out
        return out
    def why(self,instring):
        self.currentop='Why'
        self.subconscious=[]
        tobeval=[]
        self.bevaluate_tree(instring[0],tobeval)

        output=eval(''.join(tobeval))
        if output:
            if len(self.subconscious)>1:
                self.subconscious.append('\nTHUS I KNOW THAT '+self.instring_to_english(self.whyexp)+'\n')
            self.subconscious.insert(0,str(output)+'\n')
        else:
            if len(self.subconscious)>1:
                self.subconscious.append('\nTHUS I KNOW IT IS NOT TRUE THAT '+self.instring_to_english(self.whyexp)+'\n')
            self.subconscious.insert(0,str(output)+'\n')
        reversed=[i for i in self.subconscious[::-1]]
        #print self.subconscious
        self.varMemory = []
        return ''.join(self.subconscious)

    def clear(self,instring):
        self.currentop='Clear'
        try:
            arg=instring[0]
            if arg.upper() == 'YES':
                self.var_map={}
                self.known_table={}
                self.working_mem=[]
                self.order_q=[]
                self.order_v_q=[]
                self.orig_rule_exp=[]
                self.op_dict={'&':'and','|':'or','!':'not'}
                self.thought=''
                return 'Done'
            return 'Not cleared.'
        except:
            pass

