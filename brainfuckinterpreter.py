class BracketsError(Exception):
    '''
    Errortype signaling a syntaxerror in the sourcecode regarding bracketplacement
    errortype is either 0 or 1, indexes is the list of brackets that caused the error
    errortype==0 : closing bracket without corresponding opening bracket
    errortype==1 : opening bracket without corresponding closing bracket
    '''
    
    def __init__(self, errortype, indexes):
        self.errortype=errortype
        self.indexes=indexes

def execute(filename, outputmode=0):
    '''
    takes a filename as argument, filters out comments and evaluates the code using the given outputmode
    outputmode==0: celldata is interpreted as ascii code for printing
    outputmode==1: celldata is interpreted as an integer for printing
    '''
    file = open(filename, 'r')
    code=cleanup(file.read())

    try:
        evaluate(code, outputmode)
    except BracketsError as b_err:
        if b_err.errortype==0:
            print('SyntaxError: closing bracket not opened at index: ' + str(b_err.indexes[0]))
        else:
            print('SyntaxError: opened bracket(s) not closed at index(es):' + str(b_err.indexes))
    except IndexError:
        print('ArrayIndexOutOfBoundsException')
    except ValueError:
        print('Input was not a number')
    
    file.close()

def evaluate(code, outputmode):
    '''
    runs the given code using the given outputmode as explained above
    '''
    try:
        bracketdict = buildbracketdictionary(code)
    except BracketsError as b_err:
        raise b_err
    
    data=[0]
    datapointer=0
    codepointer=0

    while codepointer < len(code):
        c = code[codepointer]
        
        if c=='<':
            datapointer-=1
            
        elif c=='>':
            datapointer+=1
            if datapointer >=len(data):
                data.append(0)
                
        elif c=='+':
            data[datapointer]+=1

        elif c=='-':
            data[datapointer]-=1

        elif c=='.':
            if outputmode==0:
                print(chr(data[datapointer]), end='')
            else:
                print(data[datapointer])

        elif c==',':
            data[datapointer]=int(input())

        elif c=='[' and data[datapointer]==0:
            codepointer = bracketdict[codepointer]
            
        elif c==']' and data[datapointer]!=0:
            codepointer = bracketdict[codepointer]

        codepointer+=1

def buildbracketdictionary(code):
    '''
    forms the brackets into corresponding pairs and returns as a dictionary
    '''
    dictionary={}
    stack=[]
    for i in range(len(code)):
        c=code[i]
        if c=='[':
            stack.append(i)
        if c==']':
            try:
                j=stack.pop()
                dictionary[i]=j
                dictionary[j]=i
            except IndexError:
                raise BracketsError(0, [i])
    if stack:
        raise BracketsError(1, stack)
    
    return dictionary
    

def cleanup(source):
    '''
    removes any symbols that are not interpretable (such as comments) from the sourcecode
    '''
    return [c for c in source if c in '<>+-.,[]']

