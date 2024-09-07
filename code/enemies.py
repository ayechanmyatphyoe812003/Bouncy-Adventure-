import pygame.sprite

from settings import *
from random import choice
from timer import Timer


class Tooth(pygame.sprite.Sprite): # Defines the Tooth class, which inherits from Pygame's Sprite class
    def __init__(self, pos, frames, groups, collision_sprites):
        super().__init__(groups) # Calls the initializer of the parent Sprite class and adds the Tooth instance to the specified groups
        self.frames, self.frame_index = frames, 0 # Initializes the frames for the tooth animation and sets the current frame index to 0
        self.image = self.frames[self.frame_index] # Sets the initial image for the tooth from the frames
        self.rect = self.image.get_rect(topleft=pos) # Creates a rectangle for the tooth's position based on the initial image
        self.z = Z_LAYERS['main'] # Sets the z-layer for the tooth (used for rendering order)

        self.direction = choice((-1, 1)) # Randomly sets the initial direction of the tooth (left or right)
        self.collision_rects = [sprite.rect for sprite in collision_sprites] # Creates a list of rectangles for collision detection
        self.speed = 200

        self.hit_timer = Timer(250) # control how often the tooth can reverse direction

    def reverse(self):
        # print('tooth')
        if not self.hit_timer.active: # Checks if the hit timer is not active
            self.direction *= -1 # Reverses the direction of the tooth
            self.hit_timer.activate() # Activates the hit timer to prevent immediate subsequent reversals

    def update(self, dt):
        self.hit_timer.update()

        # animate
        self.frame_index += ANIMATION_SPEED * dt # Increments the frame index based on the animation speed and delta time
        self.image = self.frames[int(self.frame_index % len(self.frames))] # Updates the tooth's image to the current frame
        self.image = pygame.transform.flip(self.image, True, False) if self.direction < 0 else self.image
        # Flips the image if the tooth is moving left

        # move
        self.rect.x += self.direction * self.speed * dt
        # Moves the tooth based on its direction and speed

        # reverse direction
        floor_rect_right = pygame.Rect(self.rect.bottomright, (1, 1))
        floor_rect_left = pygame.Rect(self.rect.bottomleft, (-1, 1))
        wall_rect = pygame.Rect(self.rect.topleft + vector(-1, 0), (self.rect.width + 2, 1))
        # Defines rectangles for collision detection on the right and left floor edges and wall

        if floor_rect_right.collidelist(self.collision_rects) < 0 and self.direction > 0 or \
                floor_rect_left.collidelist(self.collision_rects) < 0 and self.direction < 0 or \
                wall_rect.collidelist(self.collision_rects) != -1:
            self.direction *= -1


class Shell(pygame.sprite.Sprite):
    def __init__(self, pos, frames, groups, reverse, player, create_pearl):
        super().__init__(groups)

        if reverse:
            self.frames = {}
            for key, surfs in frames.items():
                self.frames[key] = [pygame.transform.flip(surf, True, False) for surf in surfs]
            self.bullet_direction = -1
        else:
            self.frames = frames
            self.bullet_direction = 1

        self.frame_index = 0
        self.state = 'idle'
        self.image = self.frames[self.state][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.old_rect = self.rect.copy()
        self.z = Z_LAYERS['main']
        self.player = player
        self.shoot_timer = Timer(3000)
        self.has_fired = False
        self.create_pearl = create_pearl

    def state_management(self):
        player_pos, shell_pos = vector(self.player.hitbox_rect.center), vector(self.rect.center)
        player_near = shell_pos.distance_to(player_pos) < 500
        player_front = shell_pos.x < player_pos.x if self.bullet_direction > 0 else shell_pos.x > player_pos.x
        player_level = abs(shell_pos.y - player_pos.y) < 30

        if player_near and player_front and player_level and not self.shoot_timer.active:
            self.state = 'fire'
            self.frame_index = 0
            self.shoot_timer.activate()

    # Defines the update method, called every frame to update the shell's state
    def update(self, dt):
        self.shoot_timer.update()
        self.state_management()

        # animation / attack
        self.frame_index += ANIMATION_SPEED * dt
        if self.frame_index < len(self.frames[self.state]):
            self.image = self.frames[self.state][int(self.frame_index)]

            # fire
            if self.state == 'fire' and int(self.frame_index) == 3 and not self.has_fired:
                self.create_pearl(self.rect.center, self.bullet_direction)
                self.has_fired = True

        else:
            self.frame_index = 0
            if self.state == 'fire':
                self.state = 'idle'
                self.has_fired = False


class Pearl(pygame.sprite.Sprite):
    def __init__(self, pos, groups, surf, direction, speed):
        self.pearl = True
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(center=pos + vector(50 * direction, 0))
        self.direction = direction
        self.speed = speed
        self.z = Z_LAYERS['main']
        self.timers = {'lifetime': Timer(5000), 'reverse': Timer(250)}
        self.timers['lifetime'].activate()

    def reverse(self):
        if not self.timers['reverse'].active:
            self.direction *= -1
            self.timers['reverse'].activate()

    def update(self, dt):
        for timer in self.timers.values():
            timer.update()

        self.rect.x += self.direction * self.speed * dt
        if not self.timers['lifetime'].active:
            self.kill()
