import pygame
import random
import math
from pygame import mixer

pygame.init()

#==========================
# COLOURS
white = (255,255,255)
black = (0,0,0)
red = (200,0,0)
br_red = (200,0,0)
green = (0,200,0)
br_green = (0,200,0)
blue = (0,0,255)
yellow = (255,255,0)

#========================
bullet_state = "ready"
# ==========================
#screen variables
screen_width = 800 
screen_height = 600 
window = pygame.display.set_mode((screen_width,screen_height))
# ===================================

# background music
mixer.music.load("w.mp3")
mixer.music.play(-1)

# =====================================
#icon and title
icon = pygame.image.load("XOD.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("XODUKU")
# ============================================

# IMAGES
## player image
player_image = pygame.image.load("heroship.png")
## enemy image
enemy_image = pygame.image.load("enemyship.png")
## bullets images
bulletp = pygame.image.load("player_bullets.png")
bullete = pygame.image.load("new_enemy.png")
# chicken
chicken = pygame.image.load("chicken.png")
#pubg
pubg = pygame.image.load("pubg.png")
explosion = pygame.image.load("explosion.png")
# ============================================
# FONTS
fontl = pygame.font.Font("freesansbold.ttf",64)
fonts = pygame.font.Font("freesansbold.ttf",32)
fontvs = pygame.font.Font("freesansbold.ttf",20)
# ===============================================

# ================================================
# LEVELS
level_background = [pygame.image.load("level_1.jpg"),pygame.image.load("level_2.jpg"),pygame.image.load("level_3.jpg")]
level_text = ["LEVEL-1","LEVEL-2","LEVEL-3"]
# ==================================================



# ====================================================
# USED FOR WRITING ON SCREEN
def screen_text(text,colour,x,y,font_type):
    show = font_type.render(text,True,colour)
    window.blit(show,(x,y))
# ================================================

# ===========================================
# USED FOR PUTTING IMAGES ON SCREEN
def screen_image(image,x,y):
    window.blit(image,(x,y))
# =============================================    

# ============================================
# WELCOME BACKGROUND
welcome_back= pygame.image.load("welcome_screen.png")
# END BACKGROUND
end_screen_img = pygame.image.load("end_screen.png")
# PAUSE BUTTON
pause_img = pygame.image.load("pause.png")
# ============================================

# ====================================
# GAME OVER
def show_game():
    exitgame = False
    while not exitgame:
        screen_text("GAME OVER",white,200,100,fontl)
        button1("MENU",green,290,200,180,70,welcome)
        button1("RESTART",green,290,280,180,70,gameloop)
        button1("QUIT",green,290,360,180,70,quit_game)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                exitgame = True
        pygame.display.update()
    pygame.quit()
    quit()
# ======================================
def explosion_img(x,y):
    for i in range(50):
        screen_image(explosion,x,y)
        pygame.display.update()

#===========================
## PLAYERS BULLET
def fire_bullet(bx,by):
    global bullet_state
    bullet_state = "fire"
    window.blit(bulletp,(bx+15,by+10))
## ENEMY'S BULLET
def fire_bullet_e(bx,by):
    window.blit(bullete,(bx+15,by+10))
# ===================================

# =============================================
# CHECKING FOR COLLISION
def iscollision(bulletsx1,bulletsy1,enemyx,enemyy):
    distance1 = math.sqrt(math.pow(bulletsx1-enemyx,2)+math.pow(bulletsy1-enemyy,2))
    if(distance1<25):
        return True
    return False
# ================================================

# ==================================================
## UPDATING SCORE AND LEVEL
def level_updater(score1,score2,level_curr):
    if(score1 == 10 and score2 < 10):
        level_curr = level_curr + 1 
        score1 = 0
        score2 = 0
        return level_curr,score1,score2
    return level_curr,score1,score2
# ====================================================
def enemy_coll(level,enemy_x,enemy_y,enemyxchange
    ,bullet_x,bullet_y,bullet_y_e,player_x,player_y,score_value1,
        score_value2,move):
    for i in range(level+1):
        screen_image(enemy_image,enemy_x[i],enemy_y[i])
        enemy_x[i] = enemy_x[i] + enemyxchange[i]
        fire_bullet_e(enemy_x[i],bullet_y_e[i])
        bullet_y_e[i] = bullet_y_e[i] + 5.5
        ## out of bound control for enemy
        if(enemy_x[i]>=745):
            enemyxchange[i] = -3
            enemy_y[i] = enemy_y[i] + 20
        elif enemy_x[i]<=0:
            enemyxchange[i] = 3
            enemy_y[i] = enemy_y[i] + 20
        ## types of game over
        elif enemy_y[i]>455 or score_value2==10:
            move ="n"
            show_game()
        ## out of state for the enemy bullet
        if(bullet_y_e[i]>=600):
            bullet_y_e[i] = enemy_y[i]
            # COLLISION
        ## BETWEEN ENEMY AND  PLAYER BULLET
        if(iscollision(bullet_x,bullet_y,enemy_x[i],enemy_y[i])):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            explosion_img(enemy_x[i],enemy_y[i])
            score_value1 = score_value1 + 1
            bullet_y = 480
            bullet_state = "ready"
            enemy_x[i] = random.randint(70,730)
            enemy_y[i] = random.randint(70,200)
        ## BETWEEN PLAYER AND ENEMY BULLET
        if(iscollision(enemy_x[i],bullet_y_e[i],player_x,player_y)):
            explosion_sound = mixer.Sound("explosion.wav")
            explosion_sound.play()
            explosion_img(player_x,player_y)
            score_value2 = score_value2 + 1
            bullet_y_e[i] = enemy_y[i]
            player_x = random.randint(70,730)
            player_y = 530
    return player_x,player_y,score_value1,score_value2,move
# ================================================

#==============================================
def out_state_player_bullet(player_x,
        bullet_y,bullet_state):
           ## OUT OF STATE:PLAYER
        if(player_x<=5):
            player_x = 5
        elif player_x>=735:
            player_x = 735

        ## OUT OF STATE:PLAYERS BULLET
        if(bullet_y<=0):
            bullet_y = 520
            bullet_state = "ready"
        return player_x,bullet_y,bullet_state

#============================================
def pause_button(x,y):
    mouse_pos = pygame.mouse.get_pos()
    if( x+32>mouse_pos[0]>x and y+32>mouse_pos[1]>y):
        click = pygame.mouse.get_pressed()
        if(click[0] == 1):
            exitgame = False
            while not exitgame:
                screen_text("PAUSED",white,250,100,fontl)
                if(button1("RESUME",green,290,200,180,70)):
                    exitgame = True
                button1("RESTART",green,290,280,180,70,gameloop)
                button1("MENU",green,290,360,180,70,welcome)
                button1("QUIT",green,290,440,180,70,quit_game)
                for event in pygame.event.get():
                    if(event.type == pygame.QUIT):
                        pygame.quit()
                        quit()
                pygame.display.update()
            # pygame.quit()
            # quit()
              

#===============================================
## END SCREEN
def end_screen():
    exitgame = False
    while not exitgame:
        screen_image(end_screen_img,0,0)
        screen_image(chicken,260,200)
        screen_text(f"{name.upper()} SAVED",blue,230,50,fontl)
        screen_text("THE EARTH",blue,180,120,fontl)
        button1("MENU",green,20,480,155,70,welcome)
        button1("QUIT",green,600,480,155,70,quit_game)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                exitgame = True
        pygame.display.update()
    pygame.quit()
    quit()
#==========================


# ===============================
## GAMELOOP
def gameloop():
    enemy_x = []
    enemy_y = []
    enemyxchange = []
    bullet_y_e = []
    exitgame = False
    level = 0
    ## INITIAL SCORES
    score_value1 = 0
    score_value2 = 0
    ## PLAYER
    player_x = 310
    player_y = 530
    playerxchange = 0
    ## ENEMY
    for i in range(3):
        enemy_x.append(random.randint(70,730))
        enemy_y.append(random.randint(70,200))
        enemyxchange.append(3) 
        bullet_y_e.append(enemy_y[i])
    ## BULLET FOR PLAYER
    bullet_x = 0
    bullet_y = 520
    global bullet_state
    # MOVEMENT
    move = "y"
    while not  exitgame:
        # BACKGROUND IMAGE
        screen_image(level_background[level],0,0)
        ## PLAYER SHIP
        screen_image(player_image,player_x,player_y)      
        # LEVEL TEXT
        screen_text(level_text[level],yellow,340,10,fonts)
        # LINE
        pygame.draw.line(window,white,(0,500),(800,500))
        # PAUSE BUTTON
        screen_image(pause_img,300,10)
        pause_button(300,10)

        # SCORES
        screen_text(f"P_SCORE:{score_value1}",white,10,10,fontvs)
        screen_text(f"E_SCORE:{score_value2}",white,670,10,fontvs)

        # EVENT CONTROLS
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                exitgame =  True
            if(event.type == pygame.KEYDOWN):
                if(event.key == pygame.K_RIGHT):
                    playerxchange = 5
                if(event.key == pygame.K_LEFT):
                    playerxchange = -5
                if(event.key == pygame.K_UP):
                    if(bullet_state == "ready"):
                        bullet_sound = mixer.Sound("laser.wav")
                        bullet_sound.play()
                        bullet_x = player_x
                        fire_bullet(bullet_x,bullet_y)
            if(event.type == pygame.KEYUP):
                if(event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT):
                    playerxchange = 0

        if(move == "y"):
            player_x = player_x + playerxchange
            # ENEMY AND COLLISION CONTROLLER
            player_x,player_y,score_value1,score_value2,move=enemy_coll(level,enemy_x,enemy_y,
                enemyxchange,bullet_x,bullet_y,
                bullet_y_e,player_x,player_y,score_value1,
            score_value2,move)
        # OUT OF STATE:PLAYER AND HIS BULLET
        player_x,bullet_y,bullet_state=out_state_player_bullet(player_x,
        bullet_y,bullet_state)
     
        if(bullet_state == "fire"):
            fire_bullet(bullet_x,bullet_y)
            bullet_y = bullet_y - 5.5
            
        ## WINNING -> END SCREEN
        if(level == 2 and score_value1 == 10):
            end_screen()    

        ## LEVEL UPDATER
        level,score_value1,score_value2 = level_updater(score_value1,score_value2,level)
        pygame.display.update()

    pygame.quit()
    quit()
# =========================================
def quit_game():
    pygame.quit()
    quit()

def button1(text,colour,x,y,w,h,action=None):
    mouse_pos = pygame.mouse.get_pos()
    pygame.draw.rect(window,colour,(x,y,w,h))
    screen_text(text,black,x+20,y+20,fonts)
    if x+w>mouse_pos[0]>x and y+h>mouse_pos[1]>y:
        click = pygame.mouse.get_pressed()
        pygame.draw.rect(window,yellow,(x,y,w,h))
        screen_text(text,black,x+20,y+20,fonts)
        if(click[0] == 1):
            if(action != None):
                action()
            else:
                return True

def info():
    run = True
    while run:
        window.fill(white)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                pygame.quit()
                quit()
        screen_image(chicken,500,350)
        screen_text("HOW TO GO ABOUT?",blue,100,5,fontl)
        screen_text("1.THERE ARE 3 LEVELS",green,30,80,fontvs)
        screen_text("2.KILL ENEMY SPACESHIPS AND STOP THEM FROM ENTERING YOUR PLANET.",
        green,30,120,fontvs)
        screen_text("2.1 STOP THEM BEFORE THEY CROSS THE LINE.",green,30,160,fontvs)
        screen_text("3.KILL 10 ENEMIES TO REACH NEXT LEVEL.",green,30,200,fontvs)
        screen_text("4.YOUR SHIP CAN SUSTAIN 10 MISSILE DAMAGE FOR EACH LEVEL.",green,30,240,fontvs)
        screen_text(">.SUIT UP AND SAVE YOUR PLANET.",red,30,300,fonts)
        if(button1("BACK",red,10,500,130,50)):
            break
        pygame.display.update()


# ==========================================
# WELCOME SCREEN FUNCTION
def welcome():
    exitgame = False
    while not exitgame:
        screen_image(welcome_back,0,0)
        screen_image(pubg,480,170)
        screen_text("XODUKU",black,250,70,fontl)
        screen_text("WELCOMES YOU",black,140,120,fontl)
        screen_text("ENEMY",black,310,220,fonts)
        screen_text("PLAYER",black,310,350,fonts)
        ## enemyship
        screen_image(enemy_image,200,200)
        ## playership
        screen_image(player_image,200,330)
        # BUTTONS
        button1("PLAY",green,140,450,120,80,gameloop)
        button1("?",blue,10,10,65,65,info)
        button1("QUIT",red,540,450,120,80,quit_game)
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                exitgame = True
        pygame.display.update()
    pygame.quit()
    quit()
# ===============================================


## STARTING FROM HERE
name = input("Enter your Name:")
welcome()
pygame.quit()
quit()
