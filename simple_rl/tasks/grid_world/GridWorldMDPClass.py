''' GridWorldMDPClass.py: Contains the GridWorldMDP class. '''

# Python imports.
import random

# Other imports.
from ...mdp.MDPClass import MDP
from GridWorldStateClass import GridWorldState

class GridWorldMDP(MDP):
    ''' Class for a Grid World MDP '''

    # Static constants.
    ACTIONS = ["up", "down", "left", "right"]

    def __init__(self, width=5, height=3, init_loc=(1,1), goal_locs=[(5,3)], is_goal_terminal=True):
        '''
        Args:
            height (int)
            width (int)
            init_loc (tuple: (int, int))
            goal_locs (list of tuples: [(int, int)...])
        '''
        MDP.__init__(self, GridWorldMDP.ACTIONS, self._transition_func, self._reward_func, init_state=GridWorldState(init_loc[0], init_loc[1]))
        if type(goal_locs) is not list:
            print "Error: argument @goal_locs needs to be a list of locations. For example: [(3,3), (4,3)]."
            quit()
        for g in goal_locs:
            if g[0] > width or g[0] > height:
                print "Error: goal provided is off the map."
                print "\tGridWorld dimensions: (" + str(width) + "," + str(height) + ")"
                print "\tProblematic Goal:", g
        self.width = width
        self.height = height
        self.init_loc = init_loc
        self.goal_locs = goal_locs
        self.cur_state = GridWorldState(init_loc[0], init_loc[1])
        self.is_goal_terminal = is_goal_terminal

    def _reward_func(self, state, action):
        '''
        Args:
            state (State)
            action (str)

        Returns
            (float)
        '''
        _error_check(state, action)

        if self._is_goal_state_action(state, action):
            return 1.0
        else:
            return 0

    def _is_goal_state_action(self, state, action):
        '''
        Args:
            state (State)
            action (str)

        Returns:
            (bool): True iff the state-action pair send the agent to the goal state.
        '''
        if (state.x, state.y) in self.goal_locs and self.is_goal_terminal:
            return False

        if action == "left" and (state.x - 1, state.y) in self.goal_locs:
            return True
        elif action == "right" and (state.x + 1, state.y) in self.goal_locs:
            return True
        elif action == "down" and (state.x, state.y - 1) in self.goal_locs:
            return True
        elif action == "up" and (state.x, state.y + 1) in self.goal_locs:
            return True
        else:
            return False

    def _transition_func(self, state, action):
        '''
        Args:
            state (State)
            action (str)

        Returns
            (State)
        '''
        _error_check(state, action)

        if state.is_terminal():
            return state

        if action == "up" and state.y < self.height:
            next_state = GridWorldState(state.x, state.y + 1)
        elif action == "down" and state.y > 1:
            next_state = GridWorldState(state.x, state.y - 1)
        elif action == "right" and state.x < self.width:
            next_state = GridWorldState(state.x + 1, state.y)
        elif action == "left" and state.x > 1:
            next_state = GridWorldState(state.x - 1, state.y)
        else:
            next_state = GridWorldState(state.x, state.y)

        if self.is_goal_terminal and (next_state.x, next_state.y) in self.goal_locs:
            next_state.set_terminal(True)

        return next_state

    def __str__(self):
        if not self.is_goal_terminal:
            return "gridworld-no-term"
        return "gridworld_h-" + str(self.height) + "_w-" + str(self.width)

    def get_goal_locs(self):
        return self.goal_locs

    def visualize_agent(self, agent):
        from ...utils.mdp_visualizer import visualize_agent
        from grid_visualizer import _draw_state
        visualize_agent(self, agent, _draw_state)
        raw_input("Press anything to quit ")
        quit()


def _error_check(state, action):
    '''
    Args:
        state (State)
        action (str)

    Summary:
        Checks to make sure the received state and action are of the right type.
    '''

    if action not in GridWorldMDP.ACTIONS:
        print "Error: the action provided (" + str(action) + ") was invalid."
        quit()

    if not isinstance(state, GridWorldState):
        print "Error: the given state (" + str(state) + ") was not of the correct class."
        quit()


def main():
    grid_world = GridWorldMDP(5, 10, (1, 1), (6, 7))

    grid_world.visualize()

if __name__ == "__main__":
    main()
