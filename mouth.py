__author__ = 'Zachary'
from brain import brain
class node:
    def __init__(self,left,right,value):
        self.left=left
        self.right=right
        self.value=value
    def __str__(self):
        return str(self.left)+'-'+'*'+str(self.value).upper()+'*'+'-'+str(self.right)
        #return str(self.value)+'\r'+str(self.left)+'\t'+str(self.right)
    __repr__=__str__
class Parser:
    def __init__(self,brain):
        self.commands={'Teach':brain.teach,'List':brain.lister,'Learn':brain.learn,'Query':brain.query,'Why':brain.why,'Clear':brain.clear}
        self.brain=brain

    def refine(self,instring,nodestack):
        #print 'Refining:'+instring
        i=nodestack[0][0]
        while i < nodestack[0][1]:
            if instring[i] =='(':
                nodestack[0]=(i+1,len(instring))
                subtree=self.refine(instring,nodestack)
                nodestack.append(subtree)

            elif instring[i] ==')':
                go, to=nodestack[0]
                nodestack[0]=(i+1,to)
                return nodestack.pop()
            elif instring[i]=='!':
                # if len(nodestack)>0:
                #     ctree=nodestack.pop()
                #     if ctree.left ==None:
                #         ctree.left=node(None,self.refine(instring[i+1:],nodestack),'!')
                #     elif ctree.right==None:
                #         ctree.right=node(None,self.refine(instring[i+1:],nodestack),'!')
                # else:
                ctree=node(None,None,'!')
                nodestack.append(ctree)

                if instring[i+1]=='(' or instring[i+1]=='!':
                    nodestack[0]=(i+1,len(instring))
                    nodestack[len(nodestack)-1].right=self.refine(instring,nodestack)
                else:

                    nodestack[len(nodestack)-1].right=node(None,None,instring[i+1])
                    nodestack[0]=(i+2,len(instring))

                return nodestack.pop()
            elif instring[i] == '&':
                subtree=node(nodestack.pop(),None,'&')
                nodestack.append(subtree)
                nodestack[0]=(i+1,len(instring))
                nodestack[len(nodestack)-1].right=self.refine(instring,nodestack)

            elif instring[i] == '|':
                subtree=node(nodestack.pop(),None,'|')
                nodestack.append(subtree)
                nodestack[0]=(i+1,len(instring))
                nodestack[len(nodestack)-1].right=self.refine(instring,nodestack)

            else:
                # if len(nodestack) >1:
                #     ctree=nodestack.pop()
                #     if ctree.left == None:
                #         ctree.left=node(None,None,instring[i])
                #     elif ctree.right==None:
                #         ctree.right=node(None,None,instring[i])
                # else:
                #nodestack[0]=(0,len(instring))
                ctree=node(None,None,instring[i])
                nodestack.append(ctree)
                nodestack[0]=(i+1,len(instring))
            i=nodestack[0][0]
        return nodestack.pop()

    def parse(self,instring):
        args=list()
        expressions=instring.split('\"')
        rest=''

        if '\"' in instring:
            args.append(instring[instring.find('\"'):instring.rfind('\"')+1])
            rest=instring[:instring.find('\"')-1]
        else:
            rest=instring

        words=rest.split(' ')
        if '->' in words:
            self.brain.orig_rule_exp.append(words[words.index('->')-1])
        command=words[0].lower().capitalize()
        for word in reversed(words[1:len(words)]):
            if command=='Why':
                brain.whyexp=word
            if '&' in word or '|' in word or '!' in word:
                self.parenin=0
                args.insert(0,self.refine(word,[(0,len(word)-1)]))
                #print args
            elif '(' in word and ')' in word:
                args.insert(0,word[word.rfind('(')+1:word.find(')')])
            else:
                args.insert(0,word)
        return self.direct(command,args)


    def direct(self,command,args):
        try:
            return self.commands[command](args)
        except KeyError:
            print 'Invalid command'

brain=brain()
parser=Parser(brain)

x=None
x=raw_input()
while(x):
    print parser.parse(x)
    x=raw_input()