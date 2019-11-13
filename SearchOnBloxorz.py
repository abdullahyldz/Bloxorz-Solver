from enum import Enum
from copy import deepcopy
import sys
def printmap(agent):
    for j in range(len(myMap)):
        for i in range(len(myMap[j])):

            if j in agent.yvalue and i in agent.xvalue:
                print("s", end=' ')
            else:
                print(myMap[j][i], end=' ')

        print()

class Orientation(Enum):
    SINGLE = 1
    HORIZONTAL = 2
    VERTICAL = 3

class Direction(Enum):
    LEFT = 1
    UP = 2
    RIGHT = 3
    DOWN = 4
class Agent:
    def __init__(self,startupx,startupy):
        self.orientation=Orientation.SINGLE
        self.xvalue=[startupx]
        self.yvalue=[startupy]
        self.cost=0
        self.path=""
        self.depth=0

    def printagentinfo(self):
        print("Agent orientation: "+str(self.orientation))
        print("Agent x values: "+ str(self.xvalue))
        print("Agent y values: "+ str(self.yvalue))
        print("Agent cost so far: "+ str(self.cost))
        print("Agent path so far: "+ str(self.path))
def moveagent(agent:Agent, direction:Direction):
    if (agent.orientation == Orientation.SINGLE):
        tmpx=agent.xvalue[0]
        tmpy=agent.yvalue[0]
        if(direction==Direction.RIGHT):
            agent.xvalue=[tmpx+1,tmpx+2]
            agent.orientation=Orientation.HORIZONTAL
        elif(direction==Direction.LEFT):
            agent.xvalue = [tmpx - 1,tmpx-2]
            agent.orientation=Orientation.HORIZONTAL

        elif(direction==Direction.UP):
            agent.yvalue = [tmpy - 1,tmpy-2]
            agent.orientation=Orientation.VERTICAL

        elif(direction==Direction.DOWN):
            agent.yvalue = [tmpy + 1,tmpy + 2]
            agent.orientation=Orientation.VERTICAL
    else: # not single
        if(agent.orientation==Orientation.HORIZONTAL):
            [tmpx1,tmpx2] = agent.xvalue
            tmpy = [agent.yvalue[0]]

            if (direction==Direction.DOWN):
                agent.yvalue=[c+1 for c in tmpy]

            elif (direction == Direction.UP):
                agent.yvalue=[c-1 for c in tmpy]

            elif (direction == Direction.LEFT):
                agent.xvalue = [tmpx1-1]
                agent.orientation=Orientation.SINGLE

            elif (direction == Direction.RIGHT):
                agent.xvalue = [tmpx2+1]
                agent.orientation = Orientation.SINGLE

        else: ## VERTICAL
            [tmpy1, tmpy2] = agent.yvalue
            tmpx = [agent.xvalue[0]]

            if (direction == Direction.RIGHT):
                agent.xvalue=[c+1 for c in tmpx]

            elif (direction == Direction.LEFT):
                agent.xvalue=[c-1 for c in tmpx]

            elif (direction == Direction.UP):
                agent.yvalue=[tmpy1-1]
                agent.orientation = Orientation.SINGLE

            elif (direction == Direction.DOWN):
                agent.yvalue=[tmpy2+1]
                agent.orientation = Orientation.SINGLE
    agent.xvalue.sort()
    agent.yvalue.sort()
    return agent
def isoktomove(agent:Agent, direction: Direction):
    if (agent.orientation == Orientation.SINGLE):
        if (direction == Direction.LEFT):
            if (agent.xvalue[0]-2>=0 and myMap[agent.yvalue[0]][agent.xvalue[0]-2]!='h' and myMap[agent.yvalue[0]][agent.xvalue[0]-1]!='h'):
                return True
        elif(direction==Direction.RIGHT):
            if (agent.xvalue[0]+2<xlimit and myMap[agent.yvalue[0]][agent.xvalue[0]+1]!='h' and myMap[agent.yvalue[0]][agent.xvalue[0]+2]!='h') :
                return True
        elif (direction == Direction.UP):
            if (agent.yvalue[0] - 2 >=0 and myMap[agent.yvalue[0]-1][agent.xvalue[0]]!='h' and myMap[agent.yvalue[0]-2][agent.xvalue[0]]!='h'):
                return True
        elif (direction == Direction.DOWN):
            if (agent.yvalue[0] + 2 < ylimit and myMap[agent.yvalue[0]+1][agent.xvalue[0]]!='h' and myMap[agent.yvalue[0]+2][agent.xvalue[0]]!='h'):
                return True

    elif(agent.orientation==Orientation.HORIZONTAL):
        if (direction == Direction.LEFT):
            if (agent.xvalue[0]-1>=0) and myMap[agent.yvalue[0]][agent.xvalue[0]-1]!='h':
                return True
        elif(direction==Direction.RIGHT):
            if (agent.xvalue[1]+1<xlimit and myMap[agent.yvalue[0]][agent.xvalue[1]+1]!='h'):
                return True
        elif (direction == Direction.UP):
            if (agent.yvalue[0] - 1 >= 0 and myMap[agent.yvalue[0]-1][agent.xvalue[0]]!='h' and myMap[agent.yvalue[0]-1][agent.xvalue[1]]!='h'):
                return True
        elif (direction == Direction.DOWN):
            if (agent.yvalue[0] + 1 < ylimit and myMap[agent.yvalue[0]+1][agent.xvalue[0]]!='h' and myMap[agent.yvalue[0]+1][agent.xvalue[1]]!='h'):
                return True

    elif (agent.orientation == Orientation.VERTICAL):
        if (direction == Direction.LEFT):
            if (agent.xvalue[0]-1>=0) and myMap[agent.yvalue[0]][agent.xvalue[0]-1]!='h' and myMap[agent.yvalue[1]][agent.xvalue[0]-1]!='h':
                return True
        elif(direction==Direction.RIGHT):
            if (agent.xvalue[0]+1<xlimit and myMap[agent.yvalue[0]][agent.xvalue[0]+1]!='h' and myMap[agent.yvalue[1]][agent.xvalue[0]+1]!='h'):
                return True
        elif (direction == Direction.UP):
            if (agent.yvalue[0] - 1 >= 0 and myMap[agent.yvalue[0]-1][agent.xvalue[0]]!='h' ):
                return True
        elif (direction == Direction.DOWN):
            if (agent.yvalue[1] + 1 < ylimit and myMap[agent.yvalue[1]+1][agent.xvalue[0]]!='h'):
                return True
    return False
def calculate_cost(agent:Agent, direction:Direction):
    if Orientation.VERTICAL == agent.orientation and (direction==Direction.DOWN or direction==Direction.UP) :
        return 3
    elif Orientation.HORIZONTAL == agent.orientation and (direction==Direction.RIGHT or direction==Direction.LEFT) :
        return 3
    else:
        return 1
def euclidean_distance(x,y):
    return (x-GOALX)**2+(y-GOALY)**2
def doesAgentTouchGoal(agent):
    if((GOALX in agent.xvalue) and (GOALY in agent.yvalue)):
        return True
    return False
def isGoalAchieved(agent):
    if((GOALX in agent.xvalue) and (GOALY in agent.yvalue) and (agent.orientation==Orientation.SINGLE)):
        return True
    return False
def greedy_estimate(agnt:Agent):
    agent=deepcopy(agnt)
    cst=0
    while(not doesAgentTouchGoal(agent)):
        dir=get_direction(agent)
        cst+=calculate_cost(agent,dir)
        agent=moveagent(agent,dir)
    return cst

def get_direction(agent):
    ax=agent.xvalue[0]
    ay=agent.yvalue[0]
    if(agent.orientation==Orientation.SINGLE):
        if(GOALX<ax):
            return Direction.LEFT
        elif(GOALY<ay):
            return Direction.UP
        elif(GOALX>ax):
            return Direction.RIGHT
        return Direction.DOWN
    elif(agent.orientation==Orientation.VERTICAL):
        if(GOALX<ax):
            return Direction.LEFT
        elif(GOALX>ax):
            return Direction.RIGHT
        elif(GOALY<ay):
            return Direction.UP
        return Direction.DOWN
    else:
        if (GOALY < ay):
            return Direction.UP
        elif (GOALY > ay):
            return Direction.DOWN
        elif (GOALX < ax):
            return Direction.LEFT
        return Direction.RIGHT


filename = sys.argv[1]
f = open(filename, "r")
tmp = f.readline()
tmpparse = tmp.split(" ")
xlimit = int(tmpparse[0]) #xlimit==2
ylimit = int(tmpparse[1]) #ylimit==3
myMap=[[0 for x in range(xlimit)] for y in range(ylimit)]

a=Agent(-1,-1)
GOALX=-1
GOALY=-1
#READ INPUT
for j in range(ylimit):
    temporary = f.readline().replace(' ', 'h').replace('\n', '')
    temporary=temporary.ljust(xlimit,'h')
    for i in range(xlimit):
        if(temporary[i]=='s'):
            a.xvalue=[i]
            a.yvalue=[j]
            myMap[j][i] = 'o'
        elif(temporary[i]=='g'):
            GOALX=i
            GOALY=j
            myMap[j][i] = temporary[i]
        else:
            myMap[j][i] = temporary[i]
f.close()

def DFS():
    agent = a
    max_depth=0
    TRAVERSED = []
    STACK = [agent]
    cost = 0
    while STACK:
        cur_agent = STACK.pop()
        tmp = (cur_agent.xvalue, cur_agent.yvalue)
        if (tmp not in TRAVERSED):
            TRAVERSED.append(tmp)
        else:
            continue
        directions = [Direction.DOWN, Direction.RIGHT, Direction.UP, Direction.LEFT]
        for dire in directions:
            if(isoktomove(cur_agent,dire)):
                new_agent=moveagent(deepcopy(cur_agent), dire)
                new_agent.cost=new_agent.cost+calculate_cost(cur_agent,dire)
                new_agent.path+=dire.name[0]
                new_agent.depth=cur_agent.depth+1
                max_depth=max(max_depth,new_agent.depth)
                if(isGoalAchieved(new_agent)):
                    return new_agent,TRAVERSED,max_depth
                if((new_agent.xvalue,new_agent.yvalue) not in TRAVERSED):
                    STACK.append(new_agent)

def BFS():
    agent = a
    max_depth = 0
    TRAVERSED = []
    STACK = [agent]
    cost = 0
    while STACK:
        cur_agent = STACK.pop(0)
        tmp=(cur_agent.xvalue, cur_agent.yvalue)
        if(tmp not in TRAVERSED):
            TRAVERSED.append(tmp)
        else:
            continue
        directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
        for dire in directions:
            if(isoktomove(cur_agent,dire)):
                new_agent=moveagent(deepcopy(cur_agent), dire)
                new_agent.cost=new_agent.cost+calculate_cost(cur_agent,dire)
                new_agent.path+=dire.name[0]
                new_agent.depth=cur_agent.depth+1
                max_depth=max(max_depth,new_agent.depth)
                if(isGoalAchieved(new_agent)):
                    return new_agent,TRAVERSED,max_depth
                if((new_agent.xvalue,new_agent.yvalue) not in TRAVERSED):
                    STACK.append(new_agent)


def UCS():
    agent = a
    max_depth=0
    TRAVERSED = []
    STACK = [agent]

    while STACK:
        cur_agent = STACK.pop(0)
        tmp = (cur_agent.xvalue, cur_agent.yvalue)
        if (tmp not in TRAVERSED):
            TRAVERSED.append(tmp)
        else:
            continue
        directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
        for dire in directions:
            if(isoktomove(cur_agent,dire)):
                new_agent=moveagent(deepcopy(cur_agent), dire)
                new_agent.cost=new_agent.cost+calculate_cost(cur_agent,dire)
                new_agent.path+=dire.name[0]
                new_agent.depth=cur_agent.depth+1
                max_depth=max(max_depth,new_agent.depth)
                if(isGoalAchieved(new_agent)):
                    return new_agent,TRAVERSED,max_depth
                if((new_agent.xvalue,new_agent.yvalue) not in TRAVERSED):
                    STACK.append(new_agent)
                    STACK=sorted(STACK,key=lambda x : x.cost)


def GREEDYSEARCH():
    agent = a
    max_depth=0
    TRAVERSED = []
    STACK = [(0,agent)]
    while STACK:
        cur_agent = STACK.pop(0)[1]
        tmp = (cur_agent.xvalue, cur_agent.yvalue)
        if (tmp not in TRAVERSED):
            TRAVERSED.append(tmp)
        else:
            continue
        directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
        for dire in directions:
            if(isoktomove(cur_agent,dire)):
                new_agent=moveagent(deepcopy(cur_agent), dire)
                new_agent.cost=new_agent.cost+calculate_cost(cur_agent,dire)
                new_agent.path+=dire.name[0]
                new_agent.depth=cur_agent.depth+1
                max_depth=max(max_depth,new_agent.depth)
                if(isGoalAchieved(new_agent)):
                    return new_agent,TRAVERSED,max_depth
                if((new_agent.xvalue,new_agent.yvalue) not in TRAVERSED):
                    estimate_cost=greedy_estimate(new_agent)
                    STACK.append((estimate_cost,new_agent))
                    STACK=sorted(STACK,key=lambda x : x[0])


def ASTARSEARCH():
    agent = a
    max_depth=0
    TRAVERSED = []
    STACK = [(0,agent)]
    while STACK:
        cur_agent = STACK.pop(0)[1]
        tmp = (cur_agent.xvalue, cur_agent.yvalue)
        if (tmp not in TRAVERSED):
            TRAVERSED.append(tmp)
        else:
            continue
        directions = [Direction.LEFT, Direction.UP, Direction.RIGHT, Direction.DOWN]
        for dire in directions:
            if(isoktomove(cur_agent,dire)):
                new_agent=moveagent(deepcopy(cur_agent), dire)
                new_agent.cost=new_agent.cost+calculate_cost(cur_agent,dire)
                new_agent.path+=dire.name[0]
                new_agent.depth=cur_agent.depth+1
                max_depth=max(max_depth,new_agent.depth)
                if(isGoalAchieved(new_agent)):
                    return new_agent,TRAVERSED,max_depth
                if((new_agent.xvalue,new_agent.yvalue) not in TRAVERSED):
                    estimate_cost=greedy_estimate(new_agent)
                    STACK.append((estimate_cost+new_agent.cost,new_agent))
                    STACK=sorted(STACK,key=lambda x : x[0])


alg = sys.argv[2]
if (alg == "dfs"):
    agent, traversed, maxdepth = DFS()
elif (alg == "bfs"):
    agent, traversed, maxdepth = BFS()
elif (alg == "ucs"):
    agent, traversed, maxdepth = UCS()
elif (alg == "as"):
    agent, traversed, maxdepth = ASTARSEARCH()
elif (alg == "gs"):
    agent, traversed, maxdepth = GREEDYSEARCH()

print(str(agent.cost)+" "+ str(len(traversed))+ " "+ str(maxdepth)+ " "+ str(agent.depth)+ "\n" + agent.path)