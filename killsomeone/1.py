import random
import math

WHITE="white"
BLACK="black"

PERSONNUMBER=10
class chess():
    def __init__(self,color,num):
        self.color=color
        self.num=num
        self.trust=[]
    
    def GetColor(self):return self.color
    def GetNum(self):return self.num
    def GetTrust(self):return self.trust
    def AddTrust(self,someone):self.trust.append(someone)
    def RemoveTrust(self,someone):
        if someone not in self.GetTrust():
            pass
        else:
            self.trust.remove(someone)
    def ChangeColor(self,color):self.color=color
    def GetCColor(self):
        if self.GetColor()==WHITE:
            return "\033[1;42m%s\033[0m"%("white")
        elif self.GetColor()==BLACK:
            return "\033[1;47m%s\033[0m"%("black")

def InitChess(Chess):
    num=PERSONNUMBER
    Chess=[chess(WHITE,i) for i in range(num-1)]
    Chess.append(chess(BLACK,num-1))
    random.shuffle(Chess)
    return Chess

def PrintChess(Chess):
    n=0
    for i in Chess:
        print("%d: (%s , %s)"%(n,i.GetCColor(),i.GetNum()),end='  ')
        n+=1
    print()
    #print("\n长度是 "+str(len(Chess)))

def GetVote(Chess):
    Vote=[0 for i in range(len(Chess))]
    for i in range(len(Chess)):
        while True:
            vote=random.randint(0,len(Chess)-1)
            if vote!=i and Chess[vote].GetNum() not in Chess[i].GetTrust():break  
            elif len(Chess[i].GetTrust())==len(Chess)-1:
                raise ZeroDivisionError
        Vote[vote]+=1
    return Vote

def RemoveChess(Chess,Vote):
    maxvote=Vote[0]
    for i in Vote:
        if(i>maxvote):
            maxvote=i
    pos=[i for i in range(len(Vote)) if Vote[i]==maxvote]
    for elem in pos[::-1]:
        for i in Chess:
            i.RemoveTrust(Chess[elem].GetNum())
        print(str(Chess[elem].GetNum())+" who is "+Chess[elem].GetCColor()+" is kicked out")
        del Chess[elem]
    return Chess

def CheckWin(Chess):
    for elem in Chess:
        if elem.GetColor()==BLACK:
            return False
    return True

def CheckLose(Chess):
    for elem in Chess:
        if elem.GetColor()==WHITE:
            return False
    return True

def TurnBlack(Chess):
    lazy=[]
    for i in range(len(Chess)):
        if Chess[i].GetColor() ==BLACK and i not in lazy:
            who=-1
            while True:
                who=random.randint(0,len(Chess)-1)
                if who!=i and Chess[who].GetNum() not in Chess[i].GetTrust():break
                elif len(Chess[i].GetTrust())==len(Chess)-1:
                    raise ZeroDivisionError
            Chess[who].ChangeColor(BLACK)
            print(str(Chess[i].GetNum())+" who trusts "+str(Chess[i].GetTrust())+" let "+str(Chess[who].GetNum())+" turn \033[1;41mBLACK\033[0m")
            Chess[i].AddTrust(Chess[who].GetNum())
            Chess[who].AddTrust(Chess[i].GetNum())
            lazy.append(who)
    return Chess
def main():
    round=0
    Chess=[]
    Chess=InitChess(Chess)
    while True:
        print("\033[1;31m第%d轮\033[0m"%round)  
        PrintChess(Chess)
        Vote=GetVote(Chess)
        #print(Vote)
        #print(sum(Vote))
        Chess=RemoveChess(Chess,Vote)
        #PrintChess(Chess)
        if Chess!=[] and CheckWin(Chess):
            print("你获胜了")
            print(end='\t')
            PrintChess(Chess)
            break
        elif Chess==[] or CheckLose(Chess):
            print("你失败了")
            if Chess==[]:
                print("无人生还")
            else:
                print(end='\t')
                PrintChess(Chess)
            break
        else:
            pass
        Chess=TurnBlack(Chess)
        if CheckLose(Chess):
            print("你失败了")
            break
        round+=1
try:
    main()
except ZeroDivisionError:
    print("while True出错")