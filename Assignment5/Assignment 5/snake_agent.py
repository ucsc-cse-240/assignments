import numpy as np
import helper
import random


class SnakeAgent:
    """
        This class has all the functions and variables necessary to implement the snake game.
        We will be using Q-learning to do this.
    """

    def __init__(self, actions, Ne, LPC, gamma):
        """
        This is the constructor for the SnakeAgent class.
        It initializes the actions that can be made,
        Ne - a parameter helpful to perform exploration before deciding the next action,
        LPC - a parameter helpful in calculating the learning rate (lr),
        gamma - a parameter helpful in calculating the next move, in other words,
            gamma is used to balance immediate and future rewards,
        Q - the Q-table used in Q-learning,
        N - the next state used to explore possible moves and decide the best one before
            updating the Q-table.
        """
        self.actions = actions
        self.Ne = Ne
        self.LPC = LPC
        self.gamma = gamma
        self.reset()

        # Create the Q and N Table to work with
        self.Q = helper.initialize_q_as_zeros()
        self.N = helper.initialize_q_as_zeros()


    def set_train(self):
        """ Sets the program into training mode."""
        self._train = True

    def set_eval(self):
        """ Sets the program into testing mode. """
        self._train = False

    def save_model(self):
        """ Save the q-table after training """
        helper.save(self.Q)

    def load_model(self):
        """ Calls the helper function to load the q-table when testing """
        self.Q = helper.load()

    def reset(self):
        """ Resets the game state """
        self.points = 0
        self.s = None
        self.a = None

    #   THIS IS FUNCTION YOU NEED TO WRITE
    def helper_func(self, state):
        """
        Function Helper: It gets the current state, and based on the
        current snake head location, body, and food location,
        determines which move(s) it can make by also using the
        board variables to see if it's near a wall or if the
        moves it can make lead it into the snake body, and so on.
        This can return a list of variables that help you keep track of
        conditions mentioned above.
        """
        print("IN helper_func")
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE


    def compute_reward(self, points, dead):
        """ Computing the reward, need not be changed. """
        if dead:
            return -1
        elif points > self.points:
            return 1
        else:
            return -0.1

    #   THIS IS FUNCTION YOU NEED TO WRITE
    def agent_action(self, state, points, dead):
        """
            This is the reinforcement learning agent.
            Use the helper_func you need to write above to
            decide which move is the best move that the snake needs to make
            using the compute_reward function defined above.
            This function also keeps track of the fact that we are in
            training state or testing state so that it can decide if it needs
            to update the Q variable. It can use the N variable to test outcomes
            of possible moves it can make.
            The LPC variable can be used to determine the learning rate (lr), but if
            you're stuck on how to do this, just use a learning rate of 0.7 first,
            get your code to work then work on this.
            Gamma is another useful parameter to determine the learning rate.
            Based on the lr, reward, and gamma values you can update the Q-table.
            If you're not in training mode, use the Q-table loaded (already done)
            to make moves based on that.
            The only thing this function should return is the best action to take
            i.e., (0 or 1 or 2 or 3) respectively.
            The parameters defined should be enough. If you want to describe more elaborate
            states as mentioned in helper_func, use the state variable to contain all that.
        """
        print("IN AGENT_ACTION")
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE
        # YOUR CODE HERE

        #UNCOMMENT THIS TO RETURN THE REQUIRED ACTION.
        #return action
