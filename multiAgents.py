# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import math

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        currPos = currentGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        currFood = currentGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        currGhostStates = currentGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        newFoodDistance = 0.0
        newGhostDistance = 0.0
        currFoodDistance = 0.0
        currGhostDistance = 0.0

        #Check if the next move will secure a food pellet
        if (successorGameState.getNumFood() < currentGameState.getNumFood()):
            currFoodDistance -= 2
        
        #Evaluate current state of affairs in terms of food
        x = 0
        while (x < currFood.width):
            y = 0
            while (y < currFood.height):
                if (currFood[x][y]):
                    currFoodDistance += (1.0/((manhattanDistance(currPos, (x,y)))))
                y += 1
            x += 1

        #Evaluate future state of affairs in terms of food
        x = 0    
        while (x < newFood.width):
            y = 0
            while (y < newFood.height):
                if (newFood[x][y]):
                    newFoodDistance += (1.0/((manhattanDistance(newPos, (x,y)))))
                y += 1
            x += 1

        #Evaluate future risk of ghosts
        for ghost in newGhostStates:
            if (manhattanDistance(newPos, ghost.getPosition()) != 0):
                newGhostDistance += (5/math.pow(manhattanDistance(newPos, ghost.getPosition()),2))

        #Evaluate current risk of ghosts
        for ghost in currGhostStates:
            if (manhattanDistance(newPos, ghost.getPosition()) != 0):
                currGhostDistance += (5/math.pow(manhattanDistance(currPos, ghost.getPosition()),2))

        #Return how much better the future state of affairs is in terms of food
        #plus the added ghost risk of that future 
        return (newFoodDistance - currFoodDistance) + (currGhostDistance - newGhostDistance)

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"

        return self.miniMax(gameState, 0, self.depth)[1]


    def miniMax (self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)


        if (len(gameState.getLegalActions()) == 0 or depth == 0):
            return (self.evaluationFunction(gameState), None)

        #agentIndex == 0 is pacman and is the MAXIMIZING function
        if (agentIndex == 0):
            # a list where the first element is the cost and the second is the name of the move
            bestMove = [-99999, None]
            for action in legalActions:
                successor = self.miniMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth)
                if (successor[0] > bestMove[0]):
                    bestMove[0] = successor[0]
                    bestMove[1] = action
            return bestMove

        #every other agent value is a ghost and is the MINIMIZING function
        else:
            bestMove = [99999, None]
            for action in legalActions:
                #if the next call is going to end the ghostPhase we decrement depth
                if ((agentIndex + 1) % gameState.getNumAgents()) == 0:
                    successor = self.miniMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth - 1)
                #else the next call is going to continue the ghost phase and the depth remains the same
                else:
                    successor = self.miniMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth)
                if (successor[0] < bestMove[0]):
                    bestMove[0] = successor[0]
                    bestMove[1] = action
            return bestMove

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.alphaBetaMax(gameState, 0, self.depth, -99999, 99999)[1]

    def alphaBetaMax (self, gameState, agentIndex, depth, alpha, beta):
        legalActions = gameState.getLegalActions(agentIndex)


        if (len(gameState.getLegalActions()) == 0 or depth == 0):
            return (self.evaluationFunction(gameState), None)

        #agentIndex == 0 is pacman and is the MAXIMIZING function
        if (agentIndex == 0):
            # a list where the first element is the cost and the second is the name of the move
            bestMove = [-99999, None]
            for action in legalActions:
                successor = self.alphaBetaMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth, alpha, beta)
                if (successor[0] > bestMove[0]):
                    bestMove[0] = successor[0]
                    bestMove[1] = action
                if (bestMove[0] > beta):
                    return bestMove
                if (bestMove[0] > alpha):
                    alpha = bestMove[0]
            return bestMove

        #every other agent value is a ghost and is the MINIMIZING function
        else:
            bestMove = [99999, None]
            for action in legalActions:
                #if the next call is going to end the ghostPhase we decrement depth
                if ((agentIndex + 1) % gameState.getNumAgents()) == 0:
                    successor = self.alphaBetaMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth - 1, alpha, beta)
                #else the next call is going to continue the ghost phase and the depth remains the same
                else:
                    successor = self.alphaBetaMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth, alpha, beta)
                if (successor[0] < bestMove[0]):
                    bestMove[0] = successor[0]
                    bestMove[1] = action
                if (bestMove[0] < alpha):
                    return bestMove
                if (bestMove[0] < beta):
                    beta = bestMove[0]
            return bestMove

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.expectiMax(gameState, 0, self.depth)[1]

    def expectiMax (self, gameState, agentIndex, depth):
        legalActions = gameState.getLegalActions(agentIndex)


        if (len(gameState.getLegalActions()) == 0 or depth == 0):
            return (self.evaluationFunction(gameState), None)

        #agentIndex == 0 is pacman and is the MAXIMIZING function
        if (agentIndex == 0):
            # a list where the first element is the cost and the second is the name of the move
            bestMove = [-99999, None]
            for action in legalActions:
                successor = self.expectiMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth)
                if (successor[0] > bestMove[0]):
                    bestMove[0] = successor[0]
                    bestMove[1] = action
            return bestMove

        #every other agent value is a ghost and is the RANDOMIZING function
        else:
            bestMove = [0.0, None]
            for action in legalActions:
                #if the next call is going to end the ghostPhase we decrement depth
                if ((agentIndex + 1) % gameState.getNumAgents()) == 0:
                    successor = self.expectiMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth - 1)
                #else the next call is going to continue the ghost phase and the depth remains the same
                else:
                    successor = self.expectiMax(gameState.generateSuccessor(agentIndex, action), ((agentIndex + 1) % gameState.getNumAgents()), depth)
                bestMove[0] += ((successor[0])/len(gameState.getLegalActions(agentIndex)))
            return bestMove

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Useful information you can extract from currentGameState (pacman.py)
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()
    currGhostStates = currentGameState.getGhostStates()
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]
    currCapsules = currentGameState.getCapsules()

    currFoodDistance = 0.0
    currGhostDistance = 0.0
    currCapsuleDistance = 0.0
    numFood = 0
    numCapsule = 0
    numGhost = 0
    
    #Evaluate current state of affairs in terms of food
    x = 0
    while (x < currFood.width):
        y = 0
        while (y < currFood.height):
            if (currFood[x][y]):
                currFoodDistance += (3.0/((manhattanDistance(currPos, (x,y)))))
                numFood +=1
            y += 1
        x += 1

    #Evaluate current state of affairs in terms of capsules

    for CapsulePos in currCapsules:
        x,y = CapsulePos
        if (x):
            currCapsuleDistance += (1.0/((manhattanDistance(currPos, (x,y)))))
            numCapsule +=1

    #Evaluate current risk of ghosts
    for ghost in currGhostStates:
        if (manhattanDistance(currPos, ghost.getPosition()) != 0):
            currGhostDistance += (5.0/math.pow(manhattanDistance(currPos, ghost.getPosition()),2))
            numGhost +=1

    # If ghosts are scared, have pacman chase the ghosts, but run away when they stop being scared
    for time in currScaredTimes:
        if (time > 0):
            if (manhattanDistance(currPos, ghost.getPosition()) == 0):
                currGhostDistance = 50
            return (15*currFoodDistance + 50*int(time)*currGhostDistance - numFood - 20*numGhost)
        
        
    #Return the distance from food plus the risk of ghosts
    return (currCapsuleDistance + currFoodDistance + 20*currGhostDistance - 6*numFood - numCapsule)

      # Things to change: Make pacman chase the ghost while it's scared, make pacman go after foods

# Abbreviation
better = betterEvaluationFunction





