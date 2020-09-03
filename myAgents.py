# File: myAgents.py
# Purpose: Agent for Pacman to avoid ghosts
# Pair Programmer 1: John Robinson, 2020-09-01
# Pair Programmer 2: Jonathan Nguyen, 2020-09-01

from pacman import Directions
from game import Agent, Actions
from pacmanAgents import LeftTurnAgent

class TimidAgent(Agent):
    """
    A simple agent for PacMan
    """

    def __init__(self):
        super().__init__()  # Call parent constructor

    def inDanger(self, pacman, ghost, dist=3):
        """inDanger(pacman, ghost) - Is the pacman in danger
        For better or worse, our definition of danger is when the pacman and
        the specified ghost are:
           in the same row or column,
           the ghost is not scared,
           and the agents are <= dist units away from one another

        If the pacman is not in danger, we return Directions.STOP
        If the pacman is in danger, we return the direction to the ghost
        """
        pacPos = pacman.getPosition()
        ghostPos = ghost.getPosition()
        
        rowLoc = pacPos[0]-ghostPos[0] # pacman left(-) or right(+) of ghost
        rowDist = abs(rowLoc)
        colLoc = pacPos[1]-ghostPos[1] # pacman below(-) or above(+) ghost
        colDist = abs(colLoc)
        if not ghost.isScared():
            # check if in same row or column
            if rowDist == 0 or colDist == 0:
                if rowDist == 0: # Pacman in same column as ghost
                    if colDist <= dist:
                        if colLoc < 0: # Pacman is below ghost
                            return Directions.NORTH
                        return Directions.SOUTH # Pacman is above ghost
                else: # Pacman in same row as ghost
                    if rowDist <= dist:
                        if rowLoc < 0: # Pacman to left of ghost
                            return Directions.EAST
                        return Directions.WEST # Pacman to right of ghost
        return Directions.STOP        
    
    def getAction(self, state):
        """
        state - GameState

        Chooses a set of actions to take based on whether Pacman is in danger from ghosts 
        If any ghosts, perform evasive actions
        If two ghosts, perform evasive actions from the first ghost 
        If Pacman is not in danger, revert to LeftTurnAgent
        Note: legal and agentState taken from LeftTurnAgent code
        """
        
        # List of directions the agent can choose from
        legal = state.getLegalPacmanActions()

        # Get the agent's state from the game state and find agent heading
        agentState = state.getPacmanState()
        ghostStates = state.getGhostStates()
                
        # Check danger from each ghost
        for i in range(len(ghostStates)):
            evadeDirection = self.inDanger(agentState, ghostStates[i])
            if evadeDirection is not Directions.STOP: # Pacman is in danger  
               # perform evasive maneuvers
                if Directions.REVERSE[evadeDirection] in legal:
                    action = Directions.REVERSE[evadeDirection] # reverse direction from ghost 
                elif Directions.LEFT[evadeDirection] in legal:
                    action = Directions.LEFT[evadeDirection] # turn left
                elif Directions.RIGHT[evadeDirection] in legal:
                    action = Directions.RIGHT[evadeDirection] # turn right
                elif evadeDirection in legal:
                    action = evadeDirection # go forward
                else: # no legal moves
                    action = Directions.STOP 
                return action
        action = LeftTurnAgent.getAction(self, state) # Pacman not in danger       
        return action

