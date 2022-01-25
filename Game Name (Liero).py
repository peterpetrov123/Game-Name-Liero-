"""
 Show how to fire bullets.
 
 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
 
 Explanation video: http://youtu.be/PpdJjaiLX6A
"""
import pygame
import random
import sys
import math

PI = 3.141592653589793238
 
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
BLUE  = (0, 0, 255)
 
# --- Classes
class Crosshair(pygame.sprite.Sprite):
    def __init__(self,crosshair_img):
        super().__init__()
        self.image = pygame.image.load(crosshair_img)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = 100

    def update(self):
        pos = pygame.mouse.get_pos()
 
        # Make the player x-axis position equal to the mouse x-axis position
        self.rect.x = pos[0]-25
        self.rect.y = pos[1]-25
 
class Mud_blob(pygame.sprite.Sprite):
    """ This class represents the block. """
    def __init__(self, dirt_img):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.image.load(dirt_img)
        self.rect = self.image.get_rect()
 
class Player(pygame.sprite.Sprite):
    """ This class represents the Player. """
 
    def __init__(self):
        """ Set up the player on creation. """
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([20, 20])
        self.image.fill(RED)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Update the player's position. """
        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()
 
        # Make the player x-axis position equal to the mouse x-axis position
        self.rect.x = pos[0]
 
class Ammo(pygame.sprite.Sprite):
    """ This class represents the bullet . """
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.image = pygame.Surface([4, 10])
        self.image.fill(BLACK)
 
        self.rect = self.image.get_rect()
 
    def update(self):
        """ Move the bullet. """
        self.rect.y -= 1


 
# --- Create the window
 
# Initialize Pygame
pygame.init()
 
# Set the height and width of the screen
screen_width = 1200
screen_height = 600
screen = pygame.display.set_mode([screen_width, screen_height])

#Load Images
background_img = pygame.image.load("bg5.jpg")
#crosshair_img = pygame.image.load("paternus1.png")

 
# --- Sprite lists
 
# This is a list of every sprite. All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()
 
# List of each block in the game
mud_blob_list = pygame.sprite.Group()
 
# List of each bullet
ammo_list = pygame.sprite.Group()
 
# --- Create the sprites

tempX = -20
tempY = -20

x_lenght_of_display = 0
y_width_of_display = 0
for x in range(60):
    for y in range(30):
        # This represents a block
        mud_blob = Mud_blob("clay_small.jpg")
        
        # Move block by 20 each iteration in x direction
        mud_blob.rect.x = x * 20
        # Move block by 20 each iteration in y direction
        mud_blob.rect.y = y * 20
        
        # Add the block to the list of objects
        mud_blob_list.add(mud_blob)
        all_sprites_list.add(mud_blob)

class Tunneler(pygame.sprite.Sprite):
    """ This class represents the tunneler. """
    def __init__(self, size, speed, direction, remaining_length):
        # Call the parent class (Sprite) constructor
        super().__init__()
 
        self.initial_remaining_length = remaining_length
        self.remaining_length = remaining_length
        self.speed = speed
        self.direction = math.radians(direction)
        # self.image = pygame.image.load(dirt_img)
        # self.rect = self.image.get_rect()

        self.image = pygame.Surface([size, size])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        pygame.draw.circle(self.image, (0,0,0), (200,200), 5)
        # screen.blit(surf1, (0,0))

    def calculate_new_xy(self, old_xy,speed,angle_in_radians):
        new_x = old_xy[0] + (speed*math.cos(angle_in_radians))
        new_y = old_xy[1] + (speed*math.sin(angle_in_radians))
        return new_x, new_y
        
    def update(self):
        """ Move the tunneler. """
        #self.direction = random.uniform(0, 2 * PI)
        #self.direction = PI
        #print(self.rect.center)
        #self.rect.center = self.calculate_new_xy(self.rect, self.speed, self.direction)
        #print(self.rect.center)
        if self.remaining_length != 0:
            self.remaining_length -= self.speed
            self.rect.center = self.calculate_new_xy(self.rect.center, self.speed, self.direction)
        else:
            self.remaining_length = self.initial_remaining_length
            self.direction = random.uniform(0, 2 * PI)
        # pass
        # self.rect.y += 1

tunneler = Tunneler(20, 25, 45, 200)
all_sprites_list.add(tunneler)


# Create a red player block
player = Player()
all_sprites_list.add(player)

crosshair = Crosshair("paternus1.png")
all_sprites_list.add(crosshair)
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
score = 0
player.rect.y = 370
 
# -------- Main Program Loop -----------
while not done:
    # --- Event Processing
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
 
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Fire a bullet if the user clicks the mouse button
            ammo = Ammo()
            # Set the bullet so it is where the player is
            ammo.rect.x = player.rect.x
            ammo.rect.y = player.rect.y
            # Add the bullet to the lists
            all_sprites_list.add(ammo)
            ammo_list.add(ammo)
 
    # --- Game logic
 
    # Call the update() method on all the sprites
    all_sprites_list.update()
 
    # Calculate mechanics for each bullet
    for ammo in ammo_list:
 
        # See if it hit a block
        ammo_hit_list = pygame.sprite.spritecollide(ammo, mud_blob_list, True)

 
        # For each block hit, remove the bullet and add to the score
        for mud_blob in ammo_hit_list:
            ammo_list.remove(ammo)
            all_sprites_list.remove(ammo)
            score += 1
            print(score)
 
        # Remove the bullet if it flies up off the screen
        if ammo.rect.y < -10:
            ammo_list.remove(ammo)
            all_sprites_list.remove(ammo)
 
    tunneler_hit_list = pygame.sprite.spritecollide(tunneler, mud_blob_list, True)
    # for tunneler in block_hit_list:
    #     all_sprites_list.remove(tunneler)

    # --- Draw a frame
 
    # Clear the screen
    screen.fill((214, 114, 196))
    screen.blit(background_img,((0,0)))
 
    # Draw all the spites
    all_sprites_list.draw(screen)
 
    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
pygame.quit()
