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

    def findClosestFood(self, gameState):
        #takes a location tuple and returns the closest food it as a tuple
        #WARNING:   ONLY CLOSEST +/- 1 SPACE. DOES NOT CONSISTENTLY BREAK TIES.
        #           this should not effect evaluation significantly
        closestFood = None
        foodGrid = gameState.getFood()
        foodGridList = gameState.getFood().asList()
        pacmanPosition = gameState.getPacmanPosition()
        j = pacmanPosition[0]
        k = pacmanPosition[0]
        i = pacmanPosition[1]
        l = pacmanPosition[1]

        while True:
            x = 0
            while (j + x <= k):
                y = 0
                while (l + y <= i):
                    if (foodGrid[(j + x)][(l + y)]):
                        print('found closest food @:', j+x, l+y)
                        return (j + x, l + y)
                    y += 1
                x += 1
            if (j - 1 >= 0):
                j -= 1
            if (k + 1 < len(foodGridList)):
                k += 1
            if (l - 1 >= 0):
                j -= 1
            if (i + 1 < len(foodGrid[0])):
                i += 1
        return closestFood

    def ghostDistanceEvaluation(self, gameState):     
        ghostStates = gameState.getGhostStates()
        totalGhostValue = 0
        for ghostState in ghostStates:
            dist = int(manhattanDistance(ghostState.getPosition(), gameState.getPacmanPosition()))
            if (dist == 0):
                totalGhostValue += -5
            else:
                totalGhostValue += -((1/dist)^2)
        return totalGhostValue

    def foodDistanceEvaluation(self, gameState):
        closestFood = self.findClosestFood(gameState)
        print("pacmanPosition =", gameState.getPacmanPosition())
        print("closestFood =", closestFood)
        print ('foodDistanceEvaluation about to return:', manhattanDistance(gameState.getPacmanPosition(), closestFood))
        return manhattanDistance(gameState.getPacmanPosition(), closestFood)



        """
        OLD FOOD DISTANCE EVAL FUNCTION. TOO SLOW TO RUN REAL TIME
        foodStates = gameState.getFood()
        pacmanPosition = gameState.getPacmanPosition()
        totalFoodValue = 0
        foodGrid = gameState.getFood().asList()
        i = 0
        while i < len(foodGrid):
            j = 0
            while j < len(foodGrid[0]):
                if (foodGrid[i][j]):
                totalFoodValue += manhattanDistance((i, j), pacmanPosition)
                j += 1
            i += 1
            #print(foodState)
            #totalFoodValue += int(manhattanDistance(foodState, gameState.getPacmanPosition()))
            #print("totalFoodValue found to be ",totalFoodValue)
        return totalFoodValue
        """
        return totalFoodValue


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
        #print("len", len(successorGameState.getFood().asList()))

        "*** YOUR CODE HERE ***"
        newFoodDistance = 0.0
        newGhostDistance = 0.0
        currFoodDistance = 0.0
        currGhostDistance = 0.0
        if (successorGameState.getNumFood() < currentGameState.getNumFood()):
            currFoodDistance += 2
        
        x = 0
        while (x < currFood.width):
            y = 0
            while (y < currFood.height):
                #print("about to use", x , y)
                if (currFood[x][y]):
                    currFoodDistance += (1/((manhattanDistance(currPos, (x,y)))))
                y += 1
            x += 1

        while (x < newFood.width):
            y = 0
            while (y < newFood.height):
                #print("about to use", x , y)
                if (newFood[x][y]):
                    print("seen value is", (1/((manhattanDistance(currPos, (x,y))))))
                    newFoodDistance += (1/((manhattanDistance(newPos, (x,y)))))
                y += 1
            x += 1

        for ghost in newGhostStates:
            if (manhattanDistance(newPos, ghost.getPosition()) != 0):
                newGhostDistance += (1/manhattanDistance(newPos, ghost.getPosition()))

        for ghost in currGhostStates:
            if (manhattanDistance(newPos, ghost.getPosition()) != 0):
                newGhostDistance += (1/math.pow(manhattanDistance(newPos, ghost.getPosition()),111))

        print("3 distances are:")
        print("newFoodDistance", newFoodDistance)
        print("currFoodDistance", currFoodDistance)
        print("newGhostDistance", newGhostDistance)
        return (currFoodDistance - newFoodDistance) - newGhostDistance

        """
        utility = 0
        currentGhostDistance = 0
        currentGhostValue = 0
        newGhostDistance = 0
        #print("for successor func returns:", self.ghostDistanceEvaluation(successorGameState))
        #print("for current func returns:", self.ghostDistanceEvaluation(currentGameState))
        #print("diff =", self.ghostDistanceEvaluation(successorGameState) - self.ghostDistanceEvaluation(currentGameState))
        #print("while diff for food =", self.foodDistanceEvaluation(successorGameState) - self.foodDistanceEvaluation(currentGameState))
        ghostDelta = (self.ghostDistanceEvaluation(successorGameState) - self.ghostDistanceEvaluation(currentGameState))
        foodDelta = self.foodDistanceEvaluation(successorGameState)
        print('foodDelta is :', foodDelta)
        if (foodDelta > 0):
            return (1/foodDelta)
        return (10)
        
        return foodDistance - ghostDistance
        """



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
        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

