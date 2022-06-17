import pygame
import random

#initialize the pygame
pygame.init()



#game window (display surface)

GAME_FOLDER = 'C:/Users/shris/PycharmProjects/pythonProject/money_heist/'
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 700
display_surface = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))

#set caption
pygame.display.set_caption("Money Heist")


background_image = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'background_image.webp'), (WINDOW_WIDTH,WINDOW_HEIGHT))
background_image2 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + "BACKGROUND2.jpg"), (WINDOW_WIDTH,WINDOW_HEIGHT))


#game actors
car = pygame.transform.scale(pygame.image.load(GAME_FOLDER + 'car.png'), (150,100))
car_rect = car.get_rect()
car_rect.right= WINDOW_WIDTH
car_rect.centery = WINDOW_HEIGHT//2
car_velocity = 8

coins = []
for i in range(6):
    coins.append(pygame.transform.scale( pygame.image.load(GAME_FOLDER + 'coin/' + str(i)+ '.png'), (32,32)))
coin_index = 0
coin_rect = coins[coin_index].get_rect()
coin_rect.left = 0
coin_rect.top = 400
coin_velocity = 5

#LOADING SOUNDS
pickup = pygame.mixer.Sound(GAME_FOLDER + 'pickup.wav')
pickup.set_volume(0.5)
background_music = pygame.mixer.music.load(GAME_FOLDER + 'background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)


#OTHER ASSETS
barrier = pygame.transform.scale(pygame.image.load(GAME_FOLDER + "barrier.webp"), (30,30))
barrier_rect = barrier.get_rect()

barrier2 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + "barrier2.webp"), (30,30))
barrier2_rect = barrier2.get_rect()

li= [barrier, barrier2]



car2 =pygame.transform.scale(pygame.image.load(GAME_FOLDER + "car2.png"), (180,90))
car2_rect = car2.get_rect()
car2_rect.left = 0
car2_rect.centery = WINDOW_HEIGHT//2 - WINDOW_HEIGHT//4



car3 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + "car3.png"), (180,180))
car3_rect = car3.get_rect()
car3_rect.left = car2_rect.left - 1000
car3_rect.centery = WINDOW_HEIGHT//2 + WINDOW_HEIGHT//4

car4 =pygame.transform.scale(pygame.image.load(GAME_FOLDER + "car4.png"), (180,150))
car4_rect = car4.get_rect()
car4_rect.left = car3_rect.left - 900
car4_rect.centery = WINDOW_HEIGHT//2 + WINDOW_HEIGHT//4

car5 = pygame.transform.scale(pygame.image.load(GAME_FOLDER + "car5.png"), (180,100))
car5_rect = car3.get_rect()
car5_rect.left = car4_rect.right - 1000
car5_rect.centery = WINDOW_HEIGHT//2 - WINDOW_HEIGHT//4



#load the font and colors
big_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 40)
small_game_font = pygame.font.Font(GAME_FOLDER + 'font1.ttf', 20)
BLACK = pygame.Color(0, 0, 0)
RED = pygame.Color(255, 0, 0)
WHITE = pygame.Color(255, 255, 255)



title = big_game_font.render('Money Heist', True, BLACK)
title_rect = title.get_rect()
title_rect.centerx = WINDOW_WIDTH//2
title_rect.top = 0

player_score = 0
player_lives = 3
score = small_game_font.render('Score: '+ str(player_score), True, WHITE)
score_rect = score.get_rect()
score_rect.left = 50
score_rect.top = 10


lives = small_game_font.render('Lives: ' + str(player_lives), True, WHITE)
lives_rect = lives.get_rect()
lives_rect.right = WINDOW_WIDTH - 50
lives_rect.top = 10


game_over_text = big_game_font.render('GAME OVER !', True, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.centery = WINDOW_HEIGHT//2
game_over_rect.centerx = WINDOW_WIDTH//2

FPS = 60
clock = pygame.time.Clock()
running = True
game_status = 1
#main game loop
while running:
    #listen to the events (user actions)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False

    if game_status == 1:

        #apply the background
        display_surface.blit(background_image, (0,0))



        #know the keys pressed
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and car_rect.top > 100:
            car_rect.top -= car_velocity
        elif keys[pygame.K_DOWN] and car_rect.bottom < WINDOW_HEIGHT :
            car_rect.top += car_velocity
        elif keys[pygame.K_LEFT] and car_rect.left >0:
            car_rect.left -= car_velocity
        elif keys[pygame.K_RIGHT] and car_rect.right <  WINDOW_WIDTH:
            car_rect.left += car_velocity

        #update the coin position
        coin_rect.right+= coin_velocity
        car2_rect.right += coin_velocity
        car3_rect.right += coin_velocity
        car4_rect.right += coin_velocity
        car5_rect.right += coin_velocity


        if car5_rect.left > WINDOW_WIDTH:
            car2_rect.right = 0
            car3_rect.left = car2_rect.left - 700
            car4_rect.left = car3_rect.left - 500
            car5_rect.left = car4_rect.right - 800

        #check whether dragon ate it
        if coin_rect.colliderect(car_rect):
            pickup.play()
            coin_velocity += 0.5
            coin_rect.left = -150
            coin_rect.top = random.randint(100, WINDOW_HEIGHT - coin_rect.height)
            player_score += 1
            score = small_game_font.render('Score: ' + str(player_score), True, WHITE)

        #check for loss
        if car_rect.colliderect(car2_rect) or car_rect.colliderect(car3_rect) or car_rect.colliderect(car4_rect) or car_rect.colliderect(car5_rect):
            car_rect.right = WINDOW_WIDTH
            car_rect.centery = WINDOW_HEIGHT // 2

            coin_rect.left = -150
            coin_rect.top = random.randint(100, WINDOW_HEIGHT- coin_rect.height)
            coin_velocity -=1
            player_lives -=1
            if player_lives > 1:
                lives = small_game_font.render('Lives: ' + str(player_lives), True, WHITE)
            elif player_lives == 1:
                lives = small_game_font.render('Lives: ' + str(player_lives), True, RED)
            elif player_lives == 0:
                game_status = 2
                pygame.mixer.music.stop()

        #draw the actors
        display_surface.blit(car, car_rect)
        display_surface.blit(coins[int(coin_index)], coin_rect)
        coin_index = (coin_index +0.2) % 6
        display_surface.blit(car2,car2_rect)
        display_surface.blit(car3,car3_rect)
        display_surface.blit(car4,car4_rect)
        display_surface.blit(car5,car5_rect)

        display_surface.blit(title, title_rect)
        display_surface.blit(score, score_rect)
        display_surface.blit(lives, lives_rect)


    if game_status == 2:
        display_surface.blit(background_image2, (0,0))
        display_surface.blit(game_over_text, game_over_rect)

    # refesh the window
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()