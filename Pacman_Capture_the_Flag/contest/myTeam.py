# myTeam.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

trashNode =[]
powered = False
powerTime = 40

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def __init__(self, gameState):
    CaptureAgent.__init__(self, gameState)
    self.foodHeld = 0
    self.legal_y = []
    self.midx =0
    self.mostlikely = [None]*4
    self.scareTime = 0
    self.scared = False

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    '''
    Your initialization code goes here, if you need any.
    '''

    # Get game space
    self.x, self.y = gameState.getWalls().asList()[-1]
    self.walls = list(gameState.getWalls())

    global agents
    agents = [util.Counter()] * gameState.getNumAgents()

    for i, val in enumerate(agents):
      if i in self.getOpponents(gameState):
        agents[i][gameState.getInitialAgentPosition(i)] = 1.0

    if self.red:
      initial_x = -1
    else:
      initial_x = 1
    # Get positions except walls
    self.avaliablePos = []
    for pos in gameState.getWalls().asList(False):
      if pos[1] > 1:
        self.avaliablePos.append(pos)

    self.midx = self.x/2 + initial_x
    self.legal_y = []
    for i in range(self.y):
      if not self.walls[self.midx][i]:
        self.legal_y.append(i)

    self.upper, self.lower = self.getIniDefendPos(gameState)

  def getIniDefendPos(self,gameState):

      #list contains current capsules and food
      defFood = self.getFoodYouAreDefending(gameState).asList()
      capsules = self.getCapsulesYouAreDefending(gameState)
      defFood.extend(capsules)
      defFoodDist = util.Counter()
      defend_posList = []
      #for each food and capsules in the list, find the cloest one to midx, return its x-value
      for node in defFood:
          minFoodDis = 99999
          for i in self.legal_y:
              dis = self.getMazeDistance(node, (self.midx,i))
              if dis<minFoodDis:
                  minFoodDis = dis
          defFoodDist[node] = minFoodDis
      minDist = defFoodDist.sortedKeys()[-1]

      #along this x-value, find the choke points on this x-value, record a 1/4 and 3/4 position in the choke
      for i in range(self.y):
        if not self.walls[minDist[0]][i]:
          #only record the y-value
          defend_posList.append(i)
      upper = len(defend_posList)/4
      below = 3*len(defend_posList)/4
      defPosDist = []
      #find the cloest distance to midx for each position (the list only contains y-value)
      for y in defend_posList:
          minDisToCen = 99999
          #every avaliable position on midx, already calculated in the registerInitialState()
          for i in self.legal_y:
              dis = self.getMazeDistance((minDist[0],y), (self.midx,i))
              if dis<minDisToCen:
                  minDisToCen = dis
          defPosDist.append((y,minDisToCen))

      #sort the candidate by their distance to center
      sortByDistance = sorted(defPosDist, key=lambda tup:tup[1])
      firstSet = []
      firstSet.append(sortByDistance[0][0])
      secStart = 0
      for i in range(1,len(sortByDistance)):
        if sortByDistance[i][1] == sortByDistance[0][1]:
          firstSet.append(sortByDistance[i][0])
        else:
          secStart = i
          break
      secondSet = []
      secondSet.append(sortByDistance[secStart][0])
      for i in range(secStart+1,len(sortByDistance)):
        if sortByDistance[i][1] == sortByDistance[secStart][1]:
          secondSet.append(sortByDistance[i][0])
        else:
          break
      upper_y_f = 99
      upper_y_s = 99
      lower_y_f = 99
      lower_y_s = 99
      upper_Loc = None
      lower_Loc = None
      for i in range(len(firstSet)):
        disUp = abs(firstSet[i]-defend_posList[upper])
        disLo = abs(firstSet[i]-defend_posList[below])
        if disUp<upper_y_f:
            upper_y_f = disUp
            canUpF = firstSet[i]
        if disLo<lower_y_f:
            lower_y_f = disLo
            canLoF = firstSet[i]
      for i in range(len(secondSet)):
        disUp = abs(secondSet[i]-defend_posList[upper])
        disLo = abs(secondSet[i]-defend_posList[below])
        if disUp<upper_y_s:
            upper_y_s = disUp
            canUpS = secondSet[i]
        if disLo<lower_y_s:
            lower_y_s = disLo
            canLoS = secondSet[i]
      if upper_y_f < upper_y_s:
          upper_Loc = (minDist[0], canUpF)
      else:
          upper_Loc = (minDist[0], canUpS)
      if lower_y_f < lower_y_s:
          lower_Loc = (minDist[0], canLoF)
      else:
          lower_Loc = (minDist[0], canLoS)
      return (upper_Loc,lower_Loc)

  def isPacman(self, gameState):
    state = gameState.getAgentState(self.index)
    return state.isPacman

  def getDefFoodPos(self,gameState):
      defFood = self.getFoodYouAreDefending(gameState).asList()

      defFoodDist = util.Counter()
      defend_posList = []
      for node in defFood:
          minFoodDis = 99999
          for i in self.legal_y:
              dis = self.getMazeDistance(node, (self.midx,i))
              if dis<minFoodDis:
                  minFoodDis = dis
          defFoodDist[node] = minFoodDis
      minDist = defFoodDist.sortedKeys()[-1]
      val = defFoodDist[minDist]
      for node in defFoodDist:
          if defFoodDist[node]==val:
              defend_posList.append(node)

      if len(defend_posList)>1:
          self.defend_pos = defend_posList[len(defend_posList)/2]
      else:
          self.defend_pos = defend_posList[0]
      return self.defend_pos

  def chooseAction(self, gameState):

    """
    The following codes are for the classical planning. But the methods don't work well, so we choose the heuristic algoritms.
    """
    # bestAction = 'Stop'
    # self.generatePDDLproblem()
    # self.runPlanner()
    # (newx,newy) = self.parseSolution()

    # for a in actions:
    #   succ = self.getSuccessor(gameState, a)

    #   """
    #   SELECT FIRST ACTION OF THE PLAN
    #   """
    #   if succ.getAgentPosition( self.index ) == (newx, newy):
    #     bestAction = a
    #     print self.index, bestAction, self.getCurrentObservation().getAgentPosition( self.index ) ,(newx,newy) 
    opponents = self.getOpponents(gameState)
    # noisyD = gameState.getAgentDistances()
    # Get this agent's current position
    myPos = gameState.getAgentPosition(self.index)

    global powered
    print(str(powered)+ str("**************"))
    global powerTime
    print(str(powerTime) + str("@@@@@@@@@@@"))
    global powered
    if powered:
        global powerTime
        powerTime -= 2
    for agent in opponents:
        self.update(gameState, agent)
    for agent in opponents:
        agents[agent].normalize()
        self.mostlikely[agent] = self.getMaxProbPos(gameState,agent)

    self.computePosVal(gameState)

    actions = gameState.getLegalActions(self.index)

    values = [self.evaluate(gameState, a) for a in actions]

    maxValue = max(values)

    bestActions = [a for a, v in zip(actions, values) if v == maxValue]
    print(str("+++++++++++  ")+str("AGENT ")+str(self.index)+str("  ++++++++++++"))
    pos = gameState.getAgentPosition(self.index)
    print(str("At  ")+str(pos)+"  choose to "+str(bestActions))
    print("\n")
    action = random.choice(bestActions)

    return action

  def getSuccessor(self, gameState, action):
      """
      Finds the next successor which is a grid position (location tuple).
      """
      successor = gameState.generateSuccessor(self.index, action)
      pos = successor.getAgentState(self.index).getPosition()
      if pos != nearestPoint(pos):
        # Only half a grid position was covered
        return successor.generateSuccessor(self.index, action)
      else:
        return successor

  def getDefFeatures(self, gameState, action):
      """
      Returns a counter of features for the state
      """
      features = util.Counter()

      successor = self.getSuccessor(gameState, action)
      myState = successor.getAgentState(self.index)
      mypos = myState.getPosition()

      enemyPos = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      invaders = [a for a in enemyPos if a.isPacman and a.getPosition()!=None]

      if len(invaders)>0:
        dis = [self.getMazeDistance(mypos,a.getPosition()) for a in invaders]
        if min(dis)!=0:
          features['hunt'] = 1.0/min(dis)
          print(str("+++++++++++  hunt Scores  ++++++++++++"))
          print(str(features['hunt'])+"    "+str(action))
        else:
          features['hunt'] = 100
          print(str("+++++++++++  hunt Scores  ++++++++++++"))
          print(str(features['hunt'])+"    "+str(action))
      else:
        if self.index==2:
            otherAgentIndex = 0
        elif self.index ==3:
            otherAgentIndex = 1
        if self.index==2 or self.index==3:
          if gameState.getAgentState(otherAgentIndex).isPacman:
              toCenter = self.getMazeDistance(mypos,self.getDefFoodPos(gameState))
          else:
              toCenter = self.getMazeDistance(mypos,self.lower)
        else:
          toCenter = self.getDisToCenter(mypos, gameState, 2)
        if toCenter!=0:
          features['disToDef'] = 1.0/toCenter
        print(str("+++++++++++  disToDef  ++++++++++++"))
        print(str(features['disToDef'])+"    "+str(action))
        if toCenter<2:
            for agent in self.getOpponents(gameState):
              can = self.mostlikely[agent]
              enemyDist = self.getMazeDistance(mypos, can)
            print(str("===========  candidate enemy ======="))
            print(str(can))
            if enemyDist!=0:
              features['hover'] = 0.8/enemyDist
              print(str("+++++++++++  Hover Scores  ++++++++++++"))
              print(str(10*features['hover'])+"      "+str(action))

      if successor.getAgentState(self.index).scaredTimer > 0:
        enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
        pacmen = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() != None]
        if len(invaders) > 0:
          minDist = min([self.getMazeDistance(mypos,a.getPosition()) for a in invaders])
        else:
          closetPacman = self.defend(successor)
          minDist = self.getMazeDistance(mypos, closetPacman)
        if minDist < successor.getAgentState(self.index).scaredTimer and minDist!=0:
          features['scared'] = minDist
        elif minDist!=0:
          features['scared'] = 1.0/minDist

      if(action == Directions.STOP):
        features['stop'] = -1.0
        print(str("+++++++++++    stop    ++++++++++++"))
        print(str((-1))+"    "+str(action))

      return features

  def transform(self, gameState):
      myState = gameState.getAgentState(self.index)
      mypos = myState.getPosition()
      enemySta = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      opponents = [a.getPosition() for a in enemySta if ((not a.isPacman) and (a.getPosition()!=None))]

      if len(opponents) == 2:
        mind = 9999
        for pos in opponents:
          dis = util.manhattanDistance(mypos,pos)
          if dis<mind:
            mind = dis
        if mind>5:
          return True
      else:
        return False

  def evaluate(self, gameState, action):
      """
      Computes a linear combination of features and feature weights
      """
      enemies = [gameState.getAgentState(i) for i in self.getOpponents(gameState)]
      pacmen = [enemy for enemy in enemies if enemy.isPacman and enemy.getPosition() != None]
      mypos = gameState.getAgentPosition(self.index)
      closestEnemy = None
      partner = 0
      if self.index==0:
          partner = 2
      elif self.index == 1:
          partner = 3
      partnerPos = gameState.getAgentPosition(partner)

      if self.index == 0 or self.index ==1:
          if self.getScore(gameState)<=0:
              features = self.getAttFeatures(gameState,action)
          else:
              features = self.getDefFeatures(gameState,action)
          if len(pacmen)>0:
              mind=999
              for pos in pacmen:
                  dis = util.manhattanDistance(mypos,pos.getPosition())
                  if dis<mind:
                      mind = dis
                      closestEnemy = pos.getPosition()
              if self.isPacman(gameState):
                if dis>5:
                  features = self.getAttFeatures(gameState,action)
                else:
                  features = self.getDefFeatures(gameState,action)
              else:
                  if self.getMazeDistance(partnerPos,closestEnemy)< dis:
                      features = self.getAttFeatures(gameState,action)
                  else:
                      features = self.getDefFeatures(gameState,action)
      else:
          if not self.transform(gameState):
            features = self.getDefFeatures(gameState,action)
          else:
            features = self.getAttFeatures(gameState,action)
      weights = self.getWeights(gameState, action)

      print(str("+++++++++++  FEATURESSCORES  ++++++++++++"))
      print(str(features))
      print(str(features * weights)+"    "+str(action))
      return features * weights

  def getWeights(self, gameState, action):
    """
    Normally, weights do not depend on the gamestate.  They can be either
    a counter or a dictionary.
    """
    return {'foodDistance': 1, 'run':1, 'backHome': 1,'huntGhost': 1,
        'hunt': 1,'capsules': 1, 'stop': 1, 'disToDef':1, 'scared':1,
        'deadEnd': 1, 'hover': 1, 'detour':1, 'toUpper':1}

  def computePosVal(self, gameState):
    for agent, pVal in enumerate(agents):
      if agent in self.getOpponents(gameState):
          new_values = util.Counter()
          pos = gameState.getAgentPosition(agent)
          if pos != None:
            new_values[pos] = 1.0
          else:
            for p in pVal:
              if p in self.avaliablePos and pVal[p] > 0:
                x, y = p
                directions = [(x+1, y), (x-1, y), (x,y), (x, y+1), (y, y-1)]
                actions = [direct for direct in directions if direct in self.avaliablePos]
                candidatePosDis = util.Counter()
                for act in actions:
                    candidatePosDis[act] = 1
                for x, y in candidatePosDis:
                          new_values[x, y] += pVal[p] * candidatePosDis[x, y]
            if len(new_values) == 0:
                preValue = self.getPreviousObservation()
                if preValue != None and preValue.getAgentPosition(agent) != None:
                    new_values[preValue.getInitialAgentPosition(agent)] = 1.0
                else:
                    for p in self.avaliablePos:
                        new_values[p] = 1.0
          agents[agent] = new_values

  def get3DeadEnd(self,position, previous):
      if position == previous:
          return False
      depth = 1
      x,y = position
      print(str("##################"))
      print(str(position))
      path = [previous]
      print(str(path))
      clear = []
      block = 0
      if self.walls[x+1][y]:
          block +=1
      elif ((x+1,y) not in path) and ((x+1,y) not in [item[0] for item in clear]):
          clear.append(((x+1,y),depth))
      if self.walls[x-1][y]:
          block +=1
      elif ((x-1,y) not in path) and ((x-1,y) not in [item[0] for item in clear]):
          clear.append(((x-1,y),depth))
      if self.walls[x][y+1]:
          block +=1
      elif ((x,y+1) not in path) and ((x,y+1) not in [item[0] for item in clear]):
          clear.append(((x,y+1),depth))
      if self.walls[x][y-1]:
          block +=1
      elif ((x,y-1) not in path) and ((x,y-1) not in [item[0] for item in clear]):
          clear.append(((x,y-1),depth))
      if block>2:
        return True
      else:
          while len(clear) > 0:
            print(clear)
            path.append(position)
            pos = clear.pop()
            path.append(pos[0])
            print(str("++++++++++++++++++++     POP        +++++++++++++++="))
            print(clear)
            depth = pos[1]
            depth += 1
            x,y = pos[0]
            block = 0
            if self.walls[x+1][y]:
              block +=1
            elif ((x+1,y) not in path) and ((x+1,y) not in [item[0] for item in clear]) and (depth != 4):
              clear.append(((x+1,y),depth))
              print(clear)
            if self.walls[x-1][y]:
              block +=1
            elif ((x-1,y) not in path) and ((x-1,y) not in [item[0] for item in clear]) and (depth != 4):
              clear.append(((x-1,y),depth))
              print(clear)
            if self.walls[x][y+1]:
              block +=1
            elif ((x,y+1) not in path) and ((x,y+1) not in [item[0] for item in clear]) and (depth != 4):
              clear.append(((x,y+1),depth))
              print(clear)
            if self.walls[x][y-1]:
              block +=1
            elif ((x,y-1) not in path) and ((x,y-1) not in [item[0] for item in clear]) and (depth != 4):
              clear.append(((x,y-1),depth))
              print(clear)
            if block>2:
              print("***********************************************************")
              continue
            else:
              if depth > 3:
                return False
      if len(clear)==0:
          return True

  def candidatePos(self, gameState, agent):
    currPos = gameState.getAgentPosition(self.index)
    posValue = util.Counter()
    noisyDis = gameState.getAgentDistances()
    for point in self.avaliablePos:
      trueDis = self.getMazeDistance(point, currPos)
      posValue[point] += gameState.getDistanceProb(trueDis, noisyDis[agent])
    return posValue

  def update(self, gameState, agent):
    posValue = self.candidatePos(gameState, agent)
    for p in self.avaliablePos:
      agents[agent][p] *= posValue[p]

  def getMaxProbPos(self, gameState, agent):
    predictedState = agents[agent]
    pointSet =[]
    pointProList = sorted(predictedState.items(), key=lambda item:item[1], reverse=True)
    maxPro = pointProList[0][1]
    for point, possibility in pointProList:
        if possibility==maxPro:
            pointSet.append(point)
    point = random.choice(pointSet)
    return point

  def defend(self, gameState):
    myPos = gameState.getAgentPosition(self.index)
    closestEnemy = None
    minDistance = 9999999999999
    for agent in self.getOpponents(gameState):
      enemyPos = gameState.getAgentPosition(agent)
      if enemyPos is None:
        enemyPos = self.mostlikely[agent]
    print(str("closestPacman"))
    print(str(enemyPos))
    return enemyPos

  def getDisToCenter(self,position, gameState, indent):
    minCenterDist = 9999
    if self.red:
        midx = gameState.data.layout.width/2 - indent
    else:
        midx = gameState.data.layout.width/2 + (indent-1)

    for i in range(gameState.data.layout.height):
      if (midx, i) in self.avaliablePos:
        centerDist = self.getMazeDistance(position, (midx, i))
        if centerDist < minCenterDist:
          minCenterDist = centerDist
          y_axis = i
    distToCenter = self.getMazeDistance(position, (midx,y_axis))
    return distToCenter

  def getAttFeatures(self, gameState, action):
    """
    Returns a counter of features for the state
    """
    print(str("1"))
    print(self.getPreviousObservation)
    print(str("2"))
    print(self.getCurrentObservation)


    enemyState = self.getOpponents(gameState)
    successor = self.getSuccessor(gameState, action)
    currPos = successor.getAgentPosition(self.index)
    capsules = self.getCapsules(gameState)
    if currPos in self.getFood(gameState).asList():
      self.foodHeld += 1

    if not self.isPacman(gameState):
      self.foodHeld=0

    features = util.Counter()
    # attFood gets all the food position from current gameState
    attFood = self.getFood(gameState).asList()
    # nextStateFood gets all the food position if we make the move
    nextStateFood = self.getFood(successor).asList()
    # if two is not equals, means we eat one if we performed the action, time to clean the trashNode
    # and find the next possible food trash
    if len(attFood) != len(nextStateFood):
      global trashNode
      trashNode = []

    # a food dictionary base on attFood and its distance between selfAgent
    attFoodList = util.Counter()
    for node in attFood:
      distance = self.getMazeDistance(node, successor.getAgentPosition(self.index))
      #assign value to key
      attFoodList[node] = distance
    # check whether the food in trash is in the food dictionary, remove if true
    if len(trashNode)>0:
        for food in attFoodList.keys():
            if food in trashNode:
                del attFoodList[food]    #a new food dictionary without the trashNode

    # find the cloest food in the food dictionary
    minDisFood = attFoodList.sortedKeys()[-1]
    val = attFoodList[minDisFood]
    foodValue = val
    # get all visible enemy position
    enemyPosition = []
    for enemy in enemyState:
      position = gameState.getAgentPosition(enemy)
      if position != None:
        enemyPosition.append(position)

    # 1 or 2 enemy on site!!!
    minDisFood2 = None
    val2 = 0
    if len(enemyPosition) > 0:
        # the cloest enemy distance to the cloest food
      distanceDiff = min([self.getMazeDistance(pos, minDisFood) for pos in enemyPosition])
      # enemy at position closer to the food than us and the distance is less than 3
      # which means it is very close to the food, thus the food does not have much value
      if distanceDiff <= val and distanceDiff <= 3:
        global trashNode
        for node in trashNode:
            #the distance of cloest enemy with food in trashNode
          dis = min([self.getMazeDistance(pos, node) for pos in enemyPosition])
          if dis > 4:
            trashNode.remove(node)  # release the node that away from enemy in site (d > 5)
        trashNode.append(minDisFood)
        del attFoodList[minDisFood]

      minDisFood2 = attFoodList.sortedKeys()[-1]
      val2 = attFoodList[minDisFood]
    else:
      posEnemy = []
      for enemy in enemyState:
        posEnemy.append(self.mostlikely[enemy])
      global trashNode
      for node in trashNode:
        dis = min([self.getMazeDistance(pos, node) for pos in posEnemy])
        if dis > 4:
          trashNode.remove(node)

    if foodValue!=0:
      features['foodDistance'] = 2.0/foodValue
    else:
      features['foodDistance'] = 10
    print(str("+++++++++++  foodDistance  ++++++++++++"))
    print(str(features['foodDistance'])+"    "+str(action))

    if len(trashNode) > 0:
      min1 = 99999999
      for node in trashNode:
        dist1 = self.getMazeDistance(currPos, node)
        print(dist1)
        if dist1 < min1:
          min1 = dist1
      if min1!=0:
        features['detour'] = 1.0/min1
      else:
        features['detour'] = 0
      print(str("~~~~~~~~~ detour score ~~~~~~~"))
      print(str(features['detour'])+"    "+str(action))
      if val2!=0:
        features['foodDistance'] = 2.0/val2
      else:
        features['foodDistance'] = 10

    enemyPos = []
    runMode = False
    for enemy in self.getOpponents(gameState):
      pos = gameState.getAgentPosition(enemy)
      if pos != None:
        enemyPos.append((enemy, pos))
    minEneDist = 9999

    if len(enemyPos) > 0:
      for enemy, pos in enemyPos:
        dist = self.getMazeDistance(pos, currPos)
        if dist < minEneDist:
          minEneDist = dist
      if currPos == gameState.getInitialAgentPosition(self.index):
        runMode = True
      global powered
      distToCenter = self.getDisToCenter(currPos, gameState, 1)
      if (not powered) and (self.isPacman(gameState)):
        print(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"))
        if minEneDist <= 5 and (minEneDist!=1) and (minEneDist!=0):
          features['run'] = minEneDist
          features['foodValue'] = 0
        elif minEneDist == 1 or minEneDist == 0 or runMode:
          features['run'] = -10000
          print(str("+++++++++++    run !!!    ++++++++++++"))
          print(str(features['run'])+"    "+str(action))
        if (distToCenter!=0):
          features['backHome'] = 10.0/distToCenter
        else:
          features['backHome'] = 100
          print(str("llllllllllllllllllllllllllll"))

    if len(enemyPos)>0 and self.get3DeadEnd(currPos,gameState.getAgentPosition(self.index)) and min([self.getMazeDistance(i[1],currPos) for i in enemyPos])<4:
      features['deadEnd'] = -10000
      print(str("+++++++++++    deadEnd    ++++++++++++"))
      print(str((-10000))+"    "+str(action))

    if(action == Directions.STOP):
      features['stop'] = -1000.0
      print(str("+++++++++++    stop    ++++++++++++"))
      print(str((-1000))+"    "+str(action))

    if len(capsules)>0:
      capsuleDis = min([self.getMazeDistance(currPos,capPos) for capPos in capsules])
      if features['run']>0:
        if capsuleDis!=0:
          features['capsules'] = 1.0/capsuleDis
        else:
          features['capsules'] = 1000
          global powered
          powered = True
          global powerTime
          powerTime = 20
          print(str(powerTime)+ str("```````````"))
          print(str(powered)+str("&&&&&&&&&&&&&"))
        # features['detour'] = 0
        print(str("+++++++++++  capsulesDistance  ++++++++++++"))
        print(str(features['capsules'])+"    "+str(action))

    global powerTime
    print(str(powerTime) + str("```````````"))
    print(str(powered)+str("&&&&&&&&&&&&&"))

    if powered == True:
      features['deadEnd'] = 0
      features['detour'] = 0
      features['backHome'] = 0
      if foodValue!=0:
        features['foodDistance'] = 10.0/foodValue
      else:
        features['foodDistance'] = 100
      features['run'] = 0
      min3=999
      for i in enemyState:
        enePos = gameState.getAgentPosition(i)
        if enePos != None:
          min2 = self.getMazeDistance(currPos, gameState.getAgentPosition(i))
          if min2 < min3:
            min3 = min2
      if min3==0:
          features['huntGhost'] = 100.0
      if powerTime <4:
        global powered
        powered = False
        print(str("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^"))
        if len(enemyPos)>0 and self.get3DeadEnd(currPos,gameState.getAgentPosition(self.index)) and min([self.getMazeDistance(i[1],currPos) for i in enemyPos])<4:
          features['deadEnd'] = 1
          print(str("+++++++++++    deadEnd    ++++++++++++"))
          print(str((-100000))+"    "+str(action))
        if foodValue!=0:
          features['foodDistance'] = 1.0/foodValue
        else:
          features['foodDistance'] = 10
        features['run'] = minEneDist

    if self.isPacman(gameState):
      distToCenter = self.getDisToCenter(currPos, gameState, 1)
      if (foodValue<=2 and enemyPos == []) or powered:
        pass
      elif (distToCenter!=0):
        features['backHome'] = 1.0/(distToCenter+0.3333*self.foodHeld)
      elif (not self.isPacman(successor) and (currPos != gameState.getInitialAgentPosition(self.index))):
        features['backHome'] = 10
      print(str("+++++++++++    backHome    ++++++++++++"))
      print(str((features['backHome']))+"    "+str(action))

    if not self.isPacman(gameState) and len(enemyPos)==0:
        distToUpper = self.getMazeDistance(currPos,self.upper)
        if distToUpper!=0:
          features['toUpper'] = 1.0/distToUpper
          features['foodDistance']=0
        else:
          features['toUpper'] = 0
          if foodValue!=0:
            features['foodDistance'] = 1.0/foodValue
          else:
            features['foodDistance'] = 10
    return features

  def createPDDLobjects(self, gameState):
    result = ''
    layout = gameState.data.layout
    for i in range(0,layout.width):
      for j in range(0,layout.height):
        result = result + "loc" + "-" + str(i) + "-" + str(j)

    result = result + " - position"
    """
    FILL THE CODE TO GENERATE PDDL OBJECTS
    """
    return result

  def createPDDLfluents(self, gameState):
    fluents = ''

    """
    FILL THE CODE TO GENERATE PDDL PREDICATES
    """
    pos = gameState.getAgentPosition(self.index)
    fluents = fluents + "\t(pacmanAt " + "loc" + "-" + str(pos[0]) + "-" + str(pos[1]) + ")\n"

    walls = gameState.getWalls()
    wallsList = walls.asList()

    for i in range(0,walls.width):
      for j in range(0,walls.height):
        # Check the position is a wall
        currPos = "loc" + "-" + str(i) + "-" + str(j)
        if (i,j) not in wallsList:
          # If it is not a wall, check each of its neightbours,
          # and add them to the adjacency list if they are free
          # Check left
          if (i - 1 >= 0) and ((i - 1,j) not in wallsList):
            fluents = fluents + "\t(adjacent " + currPos + " " + "loc" + "-" + str(i - 1) + "-" + str(j) + ")\n"
          # Check right
          if (i + 1 < walls.width) and ((i + 1,j) not in wallsList):
            fluents = fluents + "\t(adjacent " + currPos + " " + "loc" + "-" + str(i + 1) + "-" + str(j) + ")\n"
          # Check up
          if (j + 1 >= 0) and ((i,j + 1) not in wallsList):
            fluents = fluents + "\t(adjacent " + currPos + " " + "loc" + "-" + str(i) + "-" + str(j + 1) + ")\n"
          # Check down
          if (j - 1 >= 0) and ((i,j - 1) not in wallsList):
            fluents = fluents + "\t(adjacent " + currPos + " " + "loc" + "-" + str(i) + "-" + str(j - 1) + ")\n"

    food = self.getFood(gameState).asList()
    for x,y in food:
      fluents = fluents + "\t(foodAt " + "loc" + "-" + str(x) + "-" + str(y) + ")\n"

    return fluents


  def getHomePoint(self, gameState):
    minCenterDist = 9999999999
    avaliablePos = []
    homeArea = []
    for pos in gameState.getWalls().asList(False):
      if pos[1] > 1:
        avaliablePos.append(pos)

    if self.red:
      x = gameState.data.layout.width/2 - 1
    else:
      x = gameState.data.layout.width/2

    for i in range(gameState.data.layout.height):
      if (x, i) in avaliablePos:
        centerDist = self.getMazeDistance(gameState.getAgentPosition(self.index), (x, i))
        if centerDist < minCenterDist:
          minCenterDist = centerDist
          y_axis = i
          homePoint = (x, i)

    return homePoint


  def createPDDLgoal(self, gameState):
    goals = ''

    state = gameState.getAgentState(self.index)
    food = self.getFood(gameState).asList()

    if len(food) == 0 or state.numCarrying >= 3:
      pos = self.getHomePoint(gameState)
      goals = goals + "\t(homeAt " + "loc" + "-" + str(pos[0]) + "-" + str(pos[1]) + ")\n"      
    else:
      for x,y in food:
        goals = goals + "\t(not (foodAt " + "loc" + "-" + str(x) + "-" + str(y) + "))\n"
    
    enemies = []
    for i in self.getOpponents(gameState):
      if gameState.getAgentPosition(i) != None:
          enemies.append(gameState.getAgentPosition(i))
    for enemy in enemies:
      golas = goals + "\t(not (ghostAt " + "loc" + "-" + str(enemy[0]) + "-" + str(enemy[1]) + "))\n"
    """
    FILL THE CODE TO GENERATE PDDL GOAL
    """
    return goals

  def generatePDDLproblem(self):
    """convierte un escenario en un problema de strips"""
    cd = os.path.dirname(os.path.abspath(__file__))
    f = open("%s/problem%d.pddl"%(cd,self.index),"w");
    lines = list();
    lines.append("(define (problem paman-01)\n");
    lines.append("   (:domain pacman)\n");
    lines.append("   (:objects \n");
    lines.append( self.createPDDLobjects(gameState) + "\n");
    lines.append(")\n");
    lines.append("   (:init \n");
    lines.append("   ;primero objetos \n");
    lines.append( self.createPDDLfluents(gameState) + "\n");

    lines.append(")\n");
    lines.append("   (:goal \n");
    lines.append("   ( and  \n");
    lines.append( self.createPDDLgoal(gameState) + "\n");
    lines.append("   ))\n");
    lines.append(")\n");
       
    f.writelines(lines);
    f.close();


  def generatePDDLdomain(self): 
    """convierte un escenario en un problema de strips"""
    cd = os.path.dirname(os.path.abspath(__file__))
    f = open("%s/domin%d.pddl"%(cd,self.index),"w");
    lines = list();
    lines.append("(define (domain pacman)\n");
    lines.append("   (:requirements :typing :conditional-effects)\n");
    lines.append("   (:types        position)\n");
    lines.append("   (:predicates (pacmanAt ?x - position)\n");
    lines.append("   (            (foodAt ?x - position)\n");
    lines.append("   (            (pelletAt ?x - position)\n");
    lines.append("   (            (ghostAt ?x - position)\n");
    lines.append("   (            (adjacent ?x ?y - position)\n");
    lines.append("   (            (powered)\n");
    lines.append(")\n");

    lines.append("   (:action move\n");
    lines.append("       :parameters (?from ?to - position)\n");
    lines.append("       :precondition (and (pacmanAt ?from)\n");
    lines.append("                          (adjacent ?from ?to)\n");
    lines.append("                      )\n");
    lines.append("       :effect (and (pacmanAt ?to)\n");
    lines.append("                    (not (pacmanAt ?from))\n");
    lines.append("                    (not (foodAt ?to))\n");
    lines.append("                    (not (pelletAt ?to))\n");
    lines.append("                    (when (powered) (not (ghostAt ?to))\n");
    lines.append("                )\n");
    lines.append("    )\n");
    lines.append(")\n");

    f.writelines(lines);
    f.close();


  def runPlanner( self ):
    cd = os.path.dirname(os.path.abspath(__file__))
    os.system("%s/%s/ff  -o %s/domain%d.pddl -f %s/problem%d.pddl > %s/solution%d.txt"
                %(cd,bin_path,cd,self.index,cd,self.index,cd,self.index) );

  def parseSolution( self ):
    cd = os.path.dirname(os.path.abspath(__file__))
    f = open("%s/solution%d.txt"%(cd,self.index),"r");
    lines = f.readlines();
    f.close();
    
    for line in lines:
      pos_exec = line.find("0: "); #First action in solution file
      if pos_exec != -1: 
        command = line[pos_exec:];
        command_splitted = command.split(' ')

        x = int(command_splitted[3].split('_')[1])
        y = int(command_splitted[3].split('_')[2])

        return (x,y)

      #
      # Empty Plan, Use STOP action, return current Position
      #
      if line.find("ff: goal can be simplified to TRUE. The empty plan solves it") != -1:
        return  self.getCurrentObservation().getAgentPosition( self.index )

