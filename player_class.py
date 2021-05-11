import pygame
class Player:
    def __init__(self, posx, posy, width, height, limit_bullets, bullet_vel):
        self.health=10
        self.hit_box = pygame.Rect(posx, posy, width, height)
        self.bullets=[]
        self.limit_bullets=limit_bullets
        self.bullet_vel=bullet_vel

    def handle_health(self, event, player_hit):
        if event.type == player_hit:
            self.health-=1  

    def create_bullets(self, event, key_pressed, player_width=0):
        if event.key == key_pressed and len(self.bullets) < self.limit_bullets + 1:
            bullet = pygame.Rect(self.hit_box.x + player_width, self.hit_box.y + self.hit_box.height//2, 10, 5)
            self.bullets.append(bullet)       

    def handle_bullets_impact(self, other, obstacles, red_hit, blue_hit, width):
        for bullet in self.bullets:
            bullet.x +=self.bullet_vel
            if other.hit_box.colliderect(bullet):
                pygame.event.post(pygame.event.Event(blue_hit))
                self.bullets.remove(bullet)
            if bullet.x > width:
                self.bullets.remove(bullet)
            for obstacle in obstacles.obstacles:
                if obstacle.colliderect(bullet):
                    obstacles.obstacles.remove(obstacle)
                    self.bullets.remove(bullet)        
        
        for bullet in other.bullets:
            bullet.x -=other.bullet_vel
            if  self.hit_box.colliderect(bullet):
                pygame.event.post(pygame.event.Event(red_hit))
                other.bullets.remove(bullet)
            if bullet.x < 0:
                other.bullets.remove(bullet)    
            for obstacle in obstacles.obstacles:
                if obstacle.colliderect(bullet):
                    obstacles.obstacles.remove(obstacle)
                    other.bullets.remove(bullet)            