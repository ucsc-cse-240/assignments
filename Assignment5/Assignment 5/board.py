import random
import pygame
import helper
from typing import List


class BoardEnv:
    """
    This class defines the board environment.
    It initializes the board and has several functions to get useful information
    about the current board state.
    Keeps track of the board and the snake.
    """

    def __init__(self,
                snake_head_x: int,
                snake_head_y: int,
                food_x: int,
                food_y: int
            ):
        """
        This is the constructor, it initializes game variables including the current
        snake location and food location.
        The show variable is used to keep track of when we should draw it on screen or not.
        """
        self.game = Snake(snake_head_x, snake_head_y, food_x, food_y)
        self.show = False

    #   All comments starting with a "*" are just calling functions in the Snake class which do the same.

    def get_actions(self):
        """ * Returns all possible actions the snake can make """
        return self.game.get_actions()

    def reset(self):
        """ * Resets the game state """
        return self.game.reset()

    def get_points(self):
        """ * Returns the current points during the current game state """
        return self.game.get_points()

    def get_state(self):
        """ * Returns the current state of the game """
        return self.game.get_state()

    def step(self, action: int):
        """ * Given an action, does the action and returns the next state """
        state, points, dead = self.game.step(action)
        if self.show:
            self.draw(state, points, dead)
        return state, points, dead

    def draw(self, state: List, points: int, dead: bool):
        """
        Helper function to draw the different parts of the snake game.
        Uses the pygame module to easily draw the board, snake, and food.
        """
        snake_head_x, snake_head_y, snake_body, food_x, food_y = state
        self.display.fill(helper.BLUE)
        pygame.draw.rect(self.display, helper.BLACK,
                [
                    helper.GRID_SIZE,
                    helper.GRID_SIZE,
                    helper.DISPLAY_SIZE - helper.GRID_SIZE * 2,
                    helper.DISPLAY_SIZE - helper.GRID_SIZE * 2
                ])

        # draw snake head
        pygame.draw.rect(
                    self.display,
                    helper.GREEN,
                    [
                        snake_head_x,
                        snake_head_y,
                        helper.GRID_SIZE,
                        helper.GRID_SIZE
                    ],
                    3
                )
        # draw snake body
        for seg in snake_body:
            pygame.draw.rect(
                self.display,
                helper.GREEN,
                [
                    seg[0],
                    seg[1],
                    helper.GRID_SIZE,
                    helper.GRID_SIZE,
                ],
                1
            )
        # draw food
        pygame.draw.rect(
                    self.display,
                    helper.RED,
                    [
                        food_x,
                        food_y,
                        helper.GRID_SIZE,
                        helper.GRID_SIZE
                    ]
                )

        text_surface = self.font.render("Points: " + str(points), True, helper.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = ((280),(25))
        self.display.blit(text_surface, text_rect)
        pygame.display.flip()
        if dead:
            # slow clock if dead
            self.clock.tick(1)
        else:
            self.clock.tick(5)

        return


    def display(self):
        """
        Main function to display the game.
        Uses the pygame module to draw everything and calls the draw() helper function.
        Also keeps track of time since the beginning of the game.
        """
        pygame.init()
        pygame.display.set_caption('CSE 240 Assignment 5')
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font(pygame.font.get_default_font(), 15)
        self.display = pygame.display.set_mode((helper.DISPLAY_SIZE, helper.DISPLAY_SIZE), pygame.HWSURFACE)
        self.draw(self.game.get_state(), self.game.get_points(), False)
        self.show = True


class Snake:
    """
    Class to keep track of the snake.
    Most of these functions are called by the BoardEnv class.
    """

    def __init__(self,
                snake_head_x: int,
                snake_head_y: int,
                food_x: int,
                food_y: int
            ):
        """ Constructor used to initialize the Snake and food at some positions passed to it. """
        self.init_snake_head_x = snake_head_x
        self.init_snake_head_y = snake_head_y
        self.init_food_x = food_x
        self.init_food_y = food_y
        self.starve_steps = 8*(helper.DISPLAY_SIZE//helper.GRID_SIZE)**2
        self.reset()

    def reset(self):
        """ Reset the game state to the initial one """
        self.points = 0
        self.steps = 0
        self.snake_head_x = self.init_snake_head_x
        self.snake_head_y = self.init_snake_head_y
        self.snake_body = []
        self.food_x = self.init_food_x
        self.food_y = self.init_food_y

    def get_points(self):
        """ Return the current points """
        return self.points

    def get_actions(self):
        """ Return the actions that the snake can make \n
            0 -> up, 1 -> down, 2 -> left, 3 -> right
        """
        return [helper.UP, helper.DOWN, helper.LEFT, helper.RIGHT]

    def get_state(self):
        """ Returns the current positions and how long the snake is """
        return [
            self.snake_head_x,
            self.snake_head_y,
            self.snake_body,
            self.food_x,
            self.food_y
        ]

    def move(self, action: int):
        """
        Makes the move depending on the action passed to it.
        It also handles the case where the snake eats food and new food needs to be generated.
        It also decides if the snake is dead based on hitting walls,
        itself or runs out of max turns and returns true if this is the case.
        """
        self.steps += 1

        delta_x = delta_y = 0
        if action == 0:
            delta_y = -1 * helper.GRID_SIZE
        elif action == 1:
            delta_y = helper.GRID_SIZE
        elif action == 2:
            delta_x = -1 * helper.GRID_SIZE
        elif action == 3:
            delta_x = helper.GRID_SIZE

        old_body_head = None
        if len(self.snake_body) == 1:
            old_body_head = self.snake_body[0]
        self.snake_body.append((self.snake_head_x, self.snake_head_y))
        self.snake_head_x += delta_x
        self.snake_head_y += delta_y

        if len(self.snake_body) > self.points:
            del(self.snake_body[0])

        self.handle_eatfood()

        #   Case where it moves into itself when body length greater than 1
        if len(self.snake_body) >= 1:
            for seg in self.snake_body:
                if self.snake_head_x == seg[0] and self.snake_head_y == seg[1]:
                    return True

        #   Case when it moves into itslef when body lenght is 1
        if len(self.snake_body) == 1:
            if old_body_head == (self.snake_head_x, self.snake_head_y):
                return True

        #   dead on hitting wall
        if (self.snake_head_x < helper.GRID_SIZE or self.snake_head_y < helper.GRID_SIZE or
            self.snake_head_x + helper.GRID_SIZE > helper.DISPLAY_SIZE-helper.GRID_SIZE or self.snake_head_y + helper.GRID_SIZE > helper.DISPLAY_SIZE-helper.GRID_SIZE):
            return True

        #   Starvation case
        if self.steps > self.starve_steps:
            return True

        return False

    def step(self, action: int):
        """
        Do a step, given an action.
        Returns the next state, points, and if it is dead.
        """
        is_dead = self.move(action)
        return self.get_state(), self.get_points(), is_dead

    def handle_eatfood(self):
        """
        Increments the total points if the snake ate the food
        and creates another food for the snake.
        """
        if (self.snake_head_x == self.food_x) and (self.snake_head_y == self.food_y):
            self.random_food()
            self.points += 1
            self.steps = 0

    def random_food(self):
        """
        Creates food at a random location and makes sure it isn't
        at a location the snake is already at.
        """
        max_x = (helper.DISPLAY_SIZE - helper.WALL_SIZE - helper.GRID_SIZE)
        max_y = (helper.DISPLAY_SIZE - helper.WALL_SIZE - helper.GRID_SIZE)

        self.food_x = random.randint(helper.WALL_SIZE, max_x)//helper.GRID_SIZE * helper.GRID_SIZE
        self.food_y = random.randint(helper.WALL_SIZE, max_y)//helper.GRID_SIZE * helper.GRID_SIZE

        while self.check_food_on_snake():
            self.food_x = random.randint(helper.WALL_SIZE, max_x)//helper.GRID_SIZE * helper.GRID_SIZE
            self.food_y = random.randint(helper.WALL_SIZE, max_y)//helper.GRID_SIZE * helper.GRID_SIZE

    def check_food_on_snake(self):
        """ Helper function that checks if the newly created food is on the snake. """
        if self.food_x == self.snake_head_x and self.food_y == self.snake_head_y:
            return True
        for seg in self.snake_body:
            if self.food_x == seg[0] and self.food_y == seg[1]:
                return True
        return False
