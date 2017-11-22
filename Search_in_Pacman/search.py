# search.py
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    # First, build the Stack data constructure; Second, get the PacMan's start
    # position;Then initialize the action and push them into Stack.
    fringe = util.Stack()
    start = problem.getStartState()
    action = []
    node = (start, action)
    fringe.push(node)

    visited = []
    state, action = fringe.pop()
    # If the node is not visited, do DFS algorithm recursively.
    if state not in visited:
        visited.append(state)
        dfsExplore(problem, fringe, state, action, visited)

    # Once find the goal just pop last node which contains the goal state and
    # the path to it.
    goal, action = fringe.pop()
    return action

    util.raiseNotDefined()


def dfsExplore(problem, fringe, node, action, visited):

    if problem.isGoalState(node):
        return True

    # For the node which is not visited, keep doing the DFS algorithm for each
    # successor until find the goal.
    successors = problem.getSuccessors(node)
    for nextState, direction, cost in successors:
        if nextState not in visited:
            visited.append(nextState)
            nextMove = action + [direction]
            nextNode = (nextState, nextMove)
            fringe.push(nextNode)
            if dfsExplore(problem, fringe, nextState, nextMove, visited):
                return True
    return False


def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # First, build the Queue data constructure. Then put the start position and
    # action into Queue.
    fringe = util.Queue()
    start = problem.getStartState()

    node = (start, [])
    fringe.push(node)

    visited = [start]
    # Every time dequeue a node, it must be tested whether it is a goal or not.
    # If true, stop the algorithm and return the path. If not, get this node's
    # successors and keep looking.
    while not fringe.isEmpty():
        state, action = fringe.pop()

        if problem.isGoalState(state):
            return action

        successors = problem.getSuccessors(state)
        for nextState, direction, cost in successors:
            if nextState not in visited:
                visited.append(nextState)
                nextMove = action + [direction]
                nextNode = (nextState, nextMove)
                fringe.push(nextNode)

    return []

    util.raiseNotDefined()


def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    # Build the PriorityQueue data constructure
    fringe = util.PriorityQueue()
    start = problem.getStartState()

    node = (start, [], 0)
    fringe.push(node, 0)

    visited = []
    while not fringe.isEmpty():
        # Always pop the node with the least total cost.
        state, action, cost = fringe.pop()

        if state in visited:
            continue

        visited.append(state)

        if problem.isGoalState(state):
            return action

        successors = problem.getSuccessors(state)
        for nextState, direction, cost in successors:
            if nextState not in visited:
                nextMove = action + [direction]
                # Priority is the accumulated cost of path.
                priority = problem.getCostOfActions(nextMove)
                nextNode = (nextState, nextMove, priority)
                # Rebulid the whole PriorityQueue according to the priority.
                fringe.update(nextNode, priority)

    return []

    util.raiseNotDefined()


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    fringe = util.PriorityQueue()
    start = problem.getStartState()

    node = (start, [], 0)
    fringe.push(node, 0 + heuristic(start, problem))

    closedSet = []
    while not fringe.isEmpty():
        state, action, cost = fringe.pop()

        if state in closedSet:
            continue

        closedSet.append(state)

        if problem.isGoalState(state):
            return action

        successors = problem.getSuccessors(state)
        for nextState, direction, cost in successors:
            if nextState not in closedSet:
                nextMove = action + [direction]
                # Priority is the accumulated cost of path and heuristic.
                priority = problem.getCostOfActions(nextMove) + heuristic(nextState, problem)
                nextNode = (nextState, nextMove, priority)
                fringe.update(nextNode, priority)

    return []

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
