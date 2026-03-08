import pygame
from sys import exit
from random import randint, choice

class Chickie(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        chickie_bounce_1 = pygame.image.load('graphics/bounce1.png').convert_alpha()
        chickie_bounce_2 = pygame.image.load('graphics/bounce2.png').convert_alpha()
        self.chickie_bounce = [chickie_bounce_1, chickie_bounce_2]
        self.chickie_index = 0
        self.chickie_jump = pygame.image.load('graphics/jump.png').convert_alpha()

        self.image = self.chickie_bounce[self.chickie_index]
        self.rect = self.image.get_rect(midbottom = (80, 301))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.5)

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 301:
            self.gravity = -22
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1.2
        self.rect.y += self.gravity
        if self.rect.bottom >= 301:
            self.rect.bottom = 301

    def animation_state(self):
        if self.rect.bottom < 301:
            self.image = self.chickie_jump
        else:
            self.chickie_index += 0.05
            if self.chickie_index >= len(self.chickie_bounce):
                self.chickie_index = 0
            self.image = self.chickie_bounce[int(self.chickie_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Badicecream(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        icecream_bad = pygame.image.load('graphics/icecream_bad.png').convert_alpha()
        self.image = icecream_bad
        y_pos = choice([210, 305])

        self.rect = self.image.get_rect(midbottom = (choice([randint(800, 850), randint(1000,1050)]), y_pos))

    def update(self):
        self.rect.x -= movement_speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

class Goodicecream(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        icecream_good = pygame.image.load('graphics/icecream_good.png').convert_alpha()
        self.image = icecream_good
        y_pos = choice([210, 305])

        self.rect = self.image.get_rect(midbottom = (choice([randint(900, 950), randint(1100,1150)]), y_pos))

    def update(self):
        self.rect.x -= movement_speed
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()


pygame.init()
screen = pygame.display.set_mode((800,400))
clock = pygame.time.Clock()

global movement_speed, points, current_time, start_time
current_time = pygame.time.get_ticks()
start_time = pygame.time.get_ticks()
movement_speed = 5
points = 0
game_active = False
text_font = pygame.font.Font('font/Comfortaa-Regular.ttf', 40)
over_font = pygame.font.Font('font/Comfortaa-Bold.ttf', 50)
light_font = pygame.font.Font('font/Comfortaa-Light.ttf', 30)

def score():
    global points, movement_speed
    if pygame.sprite.spritecollide(chickie.sprite, good_icecream, False):
        points += 1
    if points % 10 == 0 and points != 0:
        if movement_speed <= 10:
            movement_speed += 0.0025
        else:
            movement_speed = 10
    score_text = text_font.render("Score: " + str(points), True, '#fedc79')
    score_rect = score_text.get_rect(center = (400, 50))
    screen.blit(score_text, score_rect)
    return points

def collision():
    if pygame.sprite.spritecollide(chickie.sprite, bad_icecream, False):
        splat_sound = pygame.mixer.Sound('audio/splat.mp3')
        splat_sound.play()
        bad_icecream.empty()
        good_icecream.empty()
        return False
    elif pygame.sprite.spritecollide(chickie.sprite, good_icecream, True):
        point_sound = pygame.mixer.Sound('audio/pop.mp3')
        point_sound.play()
        return True
    else: return True

# Title and Icon
pygame.display.set_caption('Chickie Run')
icon = pygame.image.load('graphics/bounce1.png')
pygame.display.set_icon(icon)

# Groups
chickie = pygame.sprite.GroupSingle()
chickie.add(Chickie())

bad_icecream = pygame.sprite.Group()
good_icecream = pygame.sprite.Group()


# Timer
ice_cream_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ice_cream_timer, 1600)

# Background
sky_surf = pygame.image.load('graphics/sky.png').convert()
ground_surf = pygame.image.load('graphics/ground.png').convert()

bg_music = pygame.mixer.Sound('audio/background.mp3')
bg_music.play(loops = -1)

icecream_good = pygame.image.load('graphics/icecream.png').convert_alpha()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == ice_cream_timer:
                choice([good_icecream.add(Goodicecream()), bad_icecream.add(Badicecream())]) 
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = 0
                points = 0
                movement_speed = 5


    if game_active:
        # Background
        screen.blit(sky_surf, (0,0))
        screen.blit(ground_surf, (0, 300))

        bad_icecream.draw(screen)
        bad_icecream.update()

        good_icecream.draw(screen)
        good_icecream.update()

        chickie.draw(screen)
        chickie.update()

        score()

        game_active = collision()

    else:
        screen.blit(sky_surf, (0, 0))
        screen.blit(ground_surf, (0, 300))
        over_text = over_font.render('GAME OVER', False, '#f8ad1f')
        over_text_rect = over_text.get_rect(center = (400, 100))

        score_message = text_font.render('Score: ' + str(points), False, '#f2c32e')
        score_message_rect = score_message.get_rect(center = (400, 175))

        title = pygame.image.load('graphics/title.png')
        title_rect = title.get_rect(center = (400, 100))

        start_text = text_font.render('Press SPACE to start', False, '#f2c32e')
        start_text_rect = start_text.get_rect(center = (400, 250))

        instructions_text_1 = light_font.render('Collect ', False,'#f8ad1f')
        instruction_text_1_rect = instructions_text_1.get_rect(topleft = (310, 140))
        instructions_text_2 = light_font.render('Avoid ', False, '#f8ad1f')
        instruction_text_2_rect = instructions_text_2.get_rect(topleft=(310, 180))

        if current_time - start_time == 0:
            screen.blit(title, title_rect)
            screen.blit(start_text, start_text_rect)
            screen.blit(pygame.image.load('graphics/icecream_good.png'), (450, 140))
            screen.blit(pygame.image.load('graphics/icecream_bad.png'), (450, 180))
            screen.blit(instructions_text_1, instruction_text_1_rect)
            screen.blit(instructions_text_2, instruction_text_2_rect)
        else:
            screen.blit(over_text, over_text_rect)
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
