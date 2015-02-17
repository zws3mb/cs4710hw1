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
        print 'Refining:'+instring
        for i in range(0,len(instring)):
            if instring[i] =='(':
                subtree=self.refine(instring[i+1:],nodestack)
                nodestack.append(subtree)
                break
            if instring[i] ==')':
                pass
            elif instring[i]=='!':
                if len(nodestack)>0:
                    ctree=nodestack.pop()
                    if ctree.left ==None:
                        ctree.left=node(None,self.refine(instring[i+1:],nodestack),'!')
                    elif ctree.right==None:
                        ctree.right=node(None,self.refine(instring[i+1:],nodestack),'!')
                else:
                    ctree=node(None,self.refine(instring[i+1:],nodestack),'!')
                nodestack.append(ctree)
                break
            elif instring[i] == '&':
                subtree=node(nodestack.pop(),self.refine(instring[i+1:],nodestack),'&')
                nodestack.append(subtree)
                break
            elif instring[i] == '|':
                subtree=node(nodestack.pop(),self.refine(instring[i+1:],nodestack),'|')
                nodestack.append(subtree)
                break
            else:
                if len(nodestack) >0:
                    ctree=nodestack.pop()
                    if ctree.left == None:
                        ctree.left=instring[i]
                    elif ctree.right==None:
                        ctree.right=instring[i]
                else:
                    ctree=node(None,None,instring[i])
                nodestack.append(ctree)
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
                args.insert(0,self.refine(word,[]))
                print args
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