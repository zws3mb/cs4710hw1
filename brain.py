__author__ = 'Zachary'

class brain:
    def __init__(self):
        self.var_map={}
        self.known_table={}
        self.working_mem=[]
        self.stack = []
        self.order_q=[]
        self.op_dict={'&':'and','|':'or','!':'not'}
        self.thought=''
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


    def back_chain(self, value):

        self.thought = ""
        for x in self.working_mem:

            str(x)

            if x[1] == value:

                print str(x[0]) + " is an expression with consequence " + str(value)

                self.evaluate_tree(x[0])
                print self.thought
                if(eval(self.thought)):
                    self.thought = ""
                    return True
                else:
                    print "No dice on this expression as is, let's query this expression though"
                    self.thought = ""
                    return self.query_call(x[0])


    def query_call(self,instring):

                #Reset thought
        self.thought=''
        current=instring[0]
        print str(instring)

        stack=[]


        lookthrough = (str(instring[0]).split("-"))

        print str(lookthrough)
        #Look through each node
        for x in lookthrough:

            #If it's not a Expression or None
            if x != "None" and x != "*&*" and x != "*!*" and x != "*|*":


                if(self.known_table[x]!=None):

                    if(self.known_table[x]==False):

                        print "We are going to backchain to find: " + str(x)


                        boolean = self.back_chain(x)

                        if(boolean):

                            print "We have succesfully found something that fucks up our notion of what to do with " + str(x)
                            #update everything
                            temporary = [str(x), "=", "True"]
                            self.stack.append(x)
                            self.teach(temporary)
                            return True

        return False





    def query(self,instring):
        current=instring[0]

        self.query_call(instring)
        self.thought = ""
        self.evaluate_tree(current)

        for x in self.stack:
            temporary = [str(x), "=", "False"]

            self.teach(temporary)


        return 'I THINK:'+str(eval(self.thought))
    def convert(self,instr):
        if instr in self.op_dict:
            return self.op_dict[instr]
        elif instr in self.known_table:
            return self.known_table[instr]
        elif instr in self.var_map:
            return self.var_map[instr]
        elif instr in self.working_mem:
            return self.working_mem[instr]
    def gather(self,val):
        self.thought+=' '+val
    def inorder(self,node,exp):
        if node is not None:
            self.gather('(')
            self.inorder(node.left, exp)
            self.gather(str(self.convert(node.value)))
            self.inorder(node.right, exp)
            self.gather(')')
    def evaluate_tree(self,ptree):
        exp=''
        current=ptree
        stack=[]
        if isinstance(current,basestring):
            self.gather(str(self.convert(current)))
        else:
            self.inorder(ptree,exp)
        #
        # while(current.value!=None):
        #
        #     # stack.append(current)
        #     if current.left !=None:
        #         stack.append(current.left)
        #         #print current.left
        #     exp+=' '+str(self.convert(current.value))
        #     if current.right !=None:
        #         stack.append(current.right)
        #         #print current.right
        #     if len(stack)>0:
        #         current=stack.pop()
        #     else:
        #         break
        print self.thought

    def why(self,instring):
        return instring
    def express(self,instring):
        return instring
