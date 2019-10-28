import numpy as np
import os.path
import ai
from comp_exec import Game
import pygame

class Player():
    def __init__(self):
        self.w1_name = "weights_one_js.txt"
        self.w2_name = "weights_two_js.txt"

        self.input_size = 4400
        self.hidden_layer_size = 200

        self.weights_one = []
        self.weights_two = []

        if os.path.exists(self.w1_name) and os.path.exists(self.w2_name):
            self.loadWeights()

    def loadWeights(self):
        self.weights_one = np.loadtxt(self.w1_name)
        self.weights_two = np.loadtxt(self.w2_name)
    def screenProcess(self, np_array):
        np_array = np_array[100:]
        np_array = np_array[::8, ::8, 0].flatten()
        #print(np.shape(np_array))
        np_array[np_array == 255] = 1
        np_array[np_array != 1] = 0
        return np_array
    def getAction(self, info):
        ########################
        # Input Paramter "info":
        # See environment file - info is an array containing: [the rgb array of a frame
        # of the screen, a two-element array representing the coordinates of paddleA (left paddle)
        # (so info[1][0] is the x coordinate of paddleA and info[1][1] is the y coordinate),
        # the two-element array representing the coordinates of paddleB, a two-element array
        # representing the coordinates of the ball, the reward obtained from the previous action
        # from the last screen, boolean indicating whether game is done]
        #print(info[0])
        input_layer = self.screenProcess(np.array(info[0]))
        #print(sum(input_layer))
        
        hidden_unactivated = np.dot(self.weights_one, input_layer)
        hidden = self.relu(hidden_unactivated)
        output_unactivated = np.dot(self.weights_two, hidden)
        #print(output_unactivated)
        output = self.sigmoid(output_unactivated)
        #print("unactivated: %.6f\noutput: %.6f" % (output_unactivated, output))
        return 10 if output >= .5 else -10
        # The number returned from this function determines how "violently" the paddle
        # is moved up. So 10 will move up and -10 will move down
    def playFullGame(self):
        game = Game(ai.getAction, self.getAction, False)
        game.reset()
        pygame.init()
        pygame.display.set_caption("Pong Competition")

        while not game.done:
            game.step()
        pygame.quit()
            

    #@np.vectorize
    def sigmoid(self, x):
        return 1.0/(1+np.exp(-1*x))

    def relu(self, vector):
        vector[vector < 0] = 0
        return vector
