__author__ = 'Zachary'
from brain import brain

class Parser:
    def __init__(self,brain):
        self.commands={'Teach':brain.teach,'List':brain.lister,'Learn':brain.learn,'Query':brain.query,'Why':brain.why}
    def refine(self,instring):
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