import random
import pygame

class Obstacles:
    def __init__(self, limit_obstacles, width, height, velocity, left_limit, right_limit, height_limit):
       self.obstacles=[] 
       self.limit_obstacles= limit_obstacles
       self.width=width
       self.height=height
       self.velocity=velocity
       self.left_limit= left_limit
       self.right_limit = right_limit
       self.height_limit = height_limit

    def create_obstacles(self, event, obstacle_event):
       if len(self.obstacles) < self.limit_obstacles + 1 and event.type == obstacle_event:
            x, y = self.possicion_random_generator() 
            obstacle = pygame.Rect(x, y, self.width, self.height)
            self.obstacles.append(obstacle)    

    def possicion_random_generator(self):
        x = random.randrange(self.left_limit, self.right_limit - self.width)
        y = self.height_limit-20
        return x, y  

    def handle_obstacles_movement(self):
        for obstacle in self.obstacles:
            obstacle.y-=self.velocity
            if obstacle.y < 0:
                self.obstacles.remove(obstacle)          