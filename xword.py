# Justin Parker
# AI project - final submission
import json
import re
import string
import random
import time
import sys

def show():
    data=[["  " for x in range(width)] for x in range(height)]
    
    for word in horizontalWords:
        for letter in range(word[2]):
            data[word[0]].pop(word[1]+letter)
            data[word[0]].insert(word[1]+letter,"[]")
            
    for word in verticalWords:
        for letter in range(word[2]):
            data[word[0]+letter].pop(word[1])
            data[word[0]+letter].insert(word[1],"[]")
    
    for word in words:
        if word[0]=='h':
            x=horizontalWords[word[1]][0]
            y=horizontalWords[word[1]][1]
            for num,letter in enumerate(word[2]):
                data[x].pop(y+num)
                data[x].insert(y+num,letter.upper()+' ')
        if word[0]=='v':
            x=verticalWords[word[1]][0]
            y=verticalWords[word[1]][1]
            for num,letter in enumerate(word[2]):
                data[x+num].pop(y)
                data[x+num].insert(y,letter.upper()+' ')
        
            
    
    print '  ',
    for i in range(width):
        if i+1<10:
            print i+1, '',
        else:
            print i+1,
    print
    for i in range(height):
        if i+1 < 10:
            print '',i+1,
        else:
            print i+1,
        for col in data[i]:
            print col,
        print

def interpretGrid(rows):
    words = []
    for num,row in enumerate(rows):
        nextWordIndex = row.find('L')
        while nextWordIndex != -1:
            try:
                nextWordEnd = row.index('X',nextWordIndex)
    
            except ValueError:
                nextWordEnd = len(row)
            length = nextWordEnd-nextWordIndex
            if length>1:
                words.append([num,nextWordIndex,length])
            nextWordIndex = row.find('L',nextWordEnd)
    return words
        
def rowsToCols(rows):
    cols = []
    for i in range(len(rows[0])):
        cols.append("")
    for row in rows:
        for col,char in enumerate(row):
            cols[col] += char
    return cols
    
def findConstraints(pointer):
    ori,index=pointer[0],pointer[1]
    constraints=[]
    if ori=='h':
        constraints.append(horizontalWords[index][2])
        for lap in overlap:
            if lap[0]==index:
                hpos=lap[1]
                vind=lap[2]
                vpos=lap[3]
                for word in words:
                    if word[0]=='v' and word[1]==vind:
                        constraints.append([hpos,word[2][vpos]])
                        break
    elif ori=='v':
        constraints.append(verticalWords[index][2])
        for lap in overlap:
            if lap[2]==index:
                hind=lap[0]
                hpos=lap[1]
                vpos=lap[3]
                for word in words:
                    if word[0]=='h' and word[1]==hind:
                        constraints.append([vpos,word[2][hpos]])
                        break
    return constraints

def match(cols,it=0):
    it=0
    if cols[0]==1:
        return True
    reg = []
    for i in range(cols[0]):
        reg.append('\w')
    length=cols.pop(0)
    for item in cols:
        reg[item[0]]=item[1]
    while it < len(dict[length]):   
        rand = random.randrange(0,len(dict[length]))
        word = re.match(''.join(reg),dict[length][rand],re.U|re.I)
        if word:
            return [word.group(0),rand]
        it += 1
    return False            

def solve(init=0,offset=False):
    myOrder = order[:]
    delOrder=[]
    delWords={}
    while len(myOrder)>0:
        if offset:
            prev=words.pop()
            thing=match(findConstraints(myOrder[0]),prev[3]+1)
            offset=False
        elif not vars().has_key('new'):
            new=True
            thing=match(findConstraints(myOrder[0]),init)        
        else:
            if delWords.has_key((myOrder[0][0],myOrder[0][1])):
                thing=match(findConstraints(myOrder[0]),delWords[(myOrder[0][0],myOrder[0][1])]+1)
            else:
                thing=match(findConstraints(myOrder[0]))
        if thing==False:
            pointer=0
            const=myOrder[pointer]
            while thing==False:
                try:
                    move = words.pop()
                except IndexError:
                    continue
                delWords[(move[0],move[1])]=move[3]
                for tup in delOrder:
                    if tup[0]==move[0] and tup[1]==move[1]:
                        myOrder.append(tup)
                        break
                    if delWords.has_key((myOrder[0][0],myOrder[0][1])):
                        thing=match(findConstraints(myOrder[0]),delWords[(myOrder[0][0],myOrder[0][1])]+1)
                    else:
                        thing=match(findConstraints(myOrder[0]))
            words.append([myOrder[pointer][0],myOrder[pointer][1],thing[0],thing[1]])
            delOrder.append(myOrder.pop(pointer))
            if disp:
                show()
            continue
        words.append([myOrder[0][0],myOrder[0][1],thing[0],thing[1]])
        delOrder.append(myOrder.pop(0))
        if disp:
            show()
        
    
    

dict = []
f = open('words2.json')
dict = json.load(f)
print 'Dictionary Loaded.'
while True:
    read = False
    while read==False:
        fname = raw_input('Grid file to open? ')
        try:
            file = open(fname, 'r')
            rows = file.read().splitlines()
            file.close()
            width = int(rows[0].split(" ")[0])
            height = int(rows[0].split(" ")[1])
            del rows[0]
        except IOError:
            print 'File read unsuccessful.'
            continue
        else:
            read = True
            
    horizontalWords = interpretGrid(rows)
    cols = rowsToCols(rows)
    verticalWords = interpretGrid(cols)
    for elem in verticalWords:
        elem[0],elem[1]=elem[1],elem[0]
    
    overlap = []
    for hindex,htuple in enumerate(horizontalWords):
        for hpos in range(htuple[2]):
            for vindex,vtuple in enumerate(verticalWords):
                for vpos in range(vtuple[2]):
                    if htuple[0]==vtuple[0]+vpos and htuple[1]+hpos==vtuple[1]:
                            overlap.append([hindex,hpos,vindex,vpos])
    
    words=[]
    show()
    if raw_input("Type 'm' for manual mode; press ENTER for automatic.\n").lower()=='m':
        while len(words)<len(horizontalWords)+len(verticalWords):
            r=0
            while not 0<r<=height:
                print 'Row ( 1 to', height,')?',
                try:
                    r=int(raw_input(''))
                except ValueError:
                    r=0
            c=0
            while not 0<c<=width:
                print 'Column ( 1 to', width,')?',
                try:
                    c=int(raw_input(''))
                except ValueError:
                    r=0
            o=''
            while o.lower()!='h' and o.lower()!='v':
                o=raw_input("'h' or 'v'? ")
            if o=='h':
                found=False
                for ind,w in enumerate(horizontalWords):
                    if w[0]==r-1 and w[1]==c-1:
                        l=w[2]
                        ii=ind
                        found=True
                        break
                if not found:
                    print 'No horizontal word at that position.'
                    continue
            else:
                found = False
                for ind,w in enumerate(verticalWords):
                    if w[0]==r-1 and w[1]==c-1:
                        l=w[2]
                        ii=ind
                        found=True
                        break
                if not found:
                    print 'No vertical word at that position.'
                    continue
            w=''
            while len(w)!=l:
                print 'Word (', l, 'characters ) ?',
                cc=findConstraints([o,ii])
                cc.pop(0)
                w=raw_input('')
                conflict=False
                for tt in cc:
                    if w[tt[0]]!=tt[1]:
                        print 'Word conflicts with a placed word.'
                        conflict=True
                        break
                if len(w)>l and not conflict:
                    print 'Too long.'
                if len(w)<l and not conflict:
                    print 'Too short.'
            if conflict:
                continue
            words.append([o,ii,w])
            show()
        print 'Grid Complete!'
        print 'Words:\n---------\n',
        for wo in words:
            print wo[2]
    else:
        read = False
        while read==False:
            fname2 = raw_input('File to write solutions to? ')
            try:
                file = open(fname2, 'w')
            except IOError:
                print 'File open unsuccessful.'
                continue
            else:
                read = True
        disp=False
        if fname in ['3.txt', '11.txt', '12.txt', '13.txt', '14.txt']:
            if raw_input('Based on my testing for this file, a solution is unlikely. Pressing ENTER will allow \
            partial solutions to be displayed, "n" will not display anything. An infinite loop will still occur.')=='':
                disp=True
        sols=0
        t=0
        order = []
        order1 = []
        order2 = []
        for i in range(len(horizontalWords)):
            order1.append(['h',i])
        for i in range(len(verticalWords)):
            order2.append(['v',i])
        order = []
        while True:
            try:
                order.append(order1.pop(0))
                order.append(order2.pop(0))
            except IndexError:
                break
        if len(order1)>0:
            order.extend(order1)
        if len(order2)>0:
            order.extend(order2)
        for init in range(100):
            sols=sols+1
            print 'Solution', sols
            temp=time.time()
            solve()
            t+=time.time()-temp
            sys.stdout = file
            print 'Solution', sols
            show()
            sys.stdout=sys.__stdout__
            file.flush()
            show()
            if t>30:
                break
        print t
        sys.stdout = file
        print t
        sys.stdout=sys.__stdout__
        file.close()
    if raw_input("'y' to exit; Press ENTER to choose another grid.\n").lower()=='y':
        break
                    