__author__ = 'Zachary'
class node:
    def __init__(self,left,right,value):
        self.left=left
        self.right=right
        self.value=value
    def __str__(self):
        return str(self.left)+'-'+'*'+str(self.value).upper()+'*'+'-'+str(self.right)
        #return str(self.value)+'\r'+str(self.left)+'\t'+str(self.right)
    __repr__=__str__
class Trash:
    def refine(instring):
        leftstack=[]
        rightstack=[]
        lsub=None
        rsub=None
        tempstring=instring
        while '(' in tempstring:
            leftstack.append(tempstring.find('('))
            tempstring=tempstring[tempstring.find('(')+1:]
        tempstring=instring
        while ')' in tempstring:
            rightstack.append(tempstring.find(')'))
            tempstring=tempstring[tempstring.find(')')+1:]
        #Parentheses
        lrem=''
        rrem=''
        while len(leftstack)>0 and len(rightstack) >0:

            print instring[max(leftstack)+1:min(rightstack)]
            if not rsub:
                lsub=self.refine(instring[max(leftstack)+1:min(rightstack)]) #remove parens
                lrem=instring[:max(leftstack)]
                rrem=instring[min(rightstack)+1:]
            elif not lsub:
                rsub=self.refine(instring[max(leftstack)+1:min(rightstack)]) #remove parens
                lrem=instring[:max(leftstack)]
                rrem=instring[min(rightstack)+1:]
            leftstack.remove(max(leftstack))
            rightstack.remove(min(rightstack))

        if '(' not in instring or ')' not in instring:
            if '&' in instring:
                return node(self.refine(instring[:instring.find('&')]),self.refine(instring[instring.find('&')+1:]),'&')
            if '|' in instring:
                return node(self.refine(instring[:instring.find('|')]),self.refine(instring[instring.find('|')+1:]),'|')
        # if '(' in instring and ')' not in instring:
        #     instring=instring[instring.find('(')+1:]
        # if ')' in instring and '(' not in instring:
        #     instring=instring[:instring.find(')')]
            return node(lsub,rsub,instring)
        return node(lsub,rsub,instring)



    instring='('+instring+')'
        stack=[]
        temptree=node(None,None,None)
        stack.append(temptree)
        ctree = temptree
        for i in instring:
            if i == '(':
                ctree.left=node(None,None,'')
                stack.append(ctree)
                ctree = ctree.left
            elif i not in ['&', '|', ')','(']:
                ctree.value=i
                parent = stack.pop()
                ctree = parent
            elif i in ['&', '|', '!']:
                ctree.value=i
                ctree.right=node(None,None,'')
                stack.append(ctree)
                ctree = ctree.right
            elif i == ')':
                ctree = stack.pop()
            else:
                raise ValueError
        return temptree