__author__ = 'Zachary'
from brain import brain
class node:
    def __init__(self,left,right,value):
        self.left=left
        self.right=right
        self.value=value
class Parser:
    def __init__(self,brain):
        self.commands={'Teach':brain.teach,'List':brain.lister,'Learn':brain.learn,'Query':brain.query,'Why':brain.why}
    def refine(self,instring):
        leftstack=[]
        rightstack=[]
        while '(' in instring:
            leftstack.append(instring.find('('))
        while ')' in instring:
            rightstack.append(instring.find(')'))
        while(len(rightstack)>0):
            minitree=self.refine(instring[max(leftstack):min(rightstack)+1])

        return instring

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
        command=words[0]
        for word in reversed(words[1:len(words)]):
            if '&' in word or '|' in word or '!' in word:
                args.insert(0,self.refine(word))
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