import random # For generating random numbers
import sys # We will use sys.exit to exit the program
import pygame
from pygame.locals import * # Basic pygame imports

# Global Variables for the game
FPS = 32
SCREENWIDTH = 800
SCREENHEIGHT = 600
SCREEN = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
GROUNDY= SCREENHEIGHT*0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
BACKGROUND1 = 'sprites/background1.jpg'
BACKGROUND2 = 'sprites/background2.jpg'
BACKGROUND3='sprites/backgroun3.jpg'
PIPE = 'sprites/pipe.png'
WELCOME='sprites/welcome.jpg'
GAMEOVER='sprites/gameover.jpg'

current_background='background1'

PLAYER_OPTIONS = [
    {'image': 'sprites/fish.png', 'name': 'NEMO'},
    {'image': 'sprites/fish 2.png', 'name': 'DORY'},
    {'image': 'sprites/whale.png', 'name': 'WHALE'}
]

# ... (existing code remains the same)

selected_player = 0  # Index of the selected player
PLAYER = PLAYER_OPTIONS[selected_player]['image']  # Initial player image


def welcomeWindow():
    """
    Shows welcome window allowing player to select character
    """
    welcome_bg = pygame.image.load(WELCOME).convert()
    select_text = pygame.font.Font(None, 50).render("Select Your Character", True, (0,0,139))
    select_rect = select_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 4))

    game_title_font = pygame.font.Font(None, 80)
    game_title_text = game_title_font.render("FLUTTERING FISH", True, (0, 0, 139))
    game_title_rect = game_title_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 8))

    player_rects = []
    player_images = [pygame.image.load(player['image']).convert_alpha() for player in PLAYER_OPTIONS]
    player_names = [player['name'] for player in PLAYER_OPTIONS]

    for i, player_image in enumerate(player_images):
        player_rects.append(player_image.get_rect(center=((i + 1) * SCREENWIDTH // 4, SCREENHEIGHT // 2)))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                for i, player_rect in enumerate(player_rects):
                    if player_rect.collidepoint(event.pos):
                        global selected_player
                        selected_player = i
                        global PLAYER
                        PLAYER = PLAYER_OPTIONS[selected_player]['image']  # Update player image
                        return

        SCREEN.blit(welcome_bg, (0, 0))
        SCREEN.blit(select_text, select_rect)
        SCREEN.blit(game_title_text, game_title_rect)
        for i, player_image in enumerate(player_images):
            SCREEN.blit(player_image, player_rects[i])
            text = pygame.font.Font(None, 30).render(player_names[i], True, (0, 0, 139))
            text_rect = text.get_rect(center=((i + 1) * SCREENWIDTH // 4, SCREENHEIGHT // 1.5))
            SCREEN.blit(text, text_rect)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)


def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENWIDTH/2)
    

    # Create 2 pipes for blitting on the screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()

    # my List of upper pipes
    upperPipes = [
        {'x': SCREENWIDTH, 'y':newPipe1[0]['y']},
        {'x': SCREENWIDTH+(SCREENWIDTH/2), 'y':newPipe2[0]['y']},
    ]
    # my List of lower pipes
    lowerPipes = [
        {'x': SCREENWIDTH, 'y':newPipe1[1]['y']},
        {'x': SCREENWIDTH+(SCREENWIDTH/2), 'y':newPipe2[1]['y']},
    ]

    pipeVelX = -5 

    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1

    playerFlapAccv = -8 # velocity while flapping
    playerFlapped = False # It is true only when the bird is flapping

    


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playery > 0:
                    playerVelY = playerFlapAccv
                    playerFlapped = True
                    GAME_SOUNDS['flap'].play()
                   


        crashTest = isCollide(playerx, playery, upperPipes, lowerPipes)
         # This function will return true if the player is crashed
        if crashTest:
            gameOver(score)    
            return     

        #check for score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2
            if pipeMidPos<= playerMidPos < pipeMidPos+4:
                score +=1
                print(f"Your score is {score}")
                GAME_SOUNDS['point'].play()

        
       
            

                


        if playerVelY <playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY

        if playerFlapped:
            playerFlapped = False            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        # move pipes to the left
        for upperPipe , lowerPipe in zip(upperPipes, lowerPipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is about to cross the leftmost part of the screen
        if 0<upperPipes[0]['x']<10:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        # Lets blit our sprites now
        SCREEN.blit(GAME_SPRITES['background1'], (0, 0))
        for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        
        player_image = pygame.image.load(PLAYER).convert_alpha()
        SCREEN.blit(player_image, (playerx, playery))

        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        Xoffset = (SCREENWIDTH - width)/2

        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
            Xoffset += GAME_SPRITES['numbers'][digit].get_width()



        if score>=5:
            current_background='background2' 
            SCREEN.blit(GAME_SPRITES[current_background], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))
            
            player_image = pygame.image.load(PLAYER).convert_alpha()
            SCREEN.blit(player_image, (playerx, playery))

            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()





        if score>=10:
            current_background='background3' 
            SCREEN.blit(GAME_SPRITES[current_background], (0, 0))
            for upperPipe, lowerPipe in zip(upperPipes, lowerPipes):
                SCREEN.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
                SCREEN.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        
            
            player_image = pygame.image.load(PLAYER).convert_alpha()
            SCREEN.blit(player_image, (playerx, playery))
            
            myDigits = [int(x) for x in list(str(score))]
            width = 0
            for digit in myDigits:
                width += GAME_SPRITES['numbers'][digit].get_width()
            Xoffset = (SCREENWIDTH - width)/2

            for digit in myDigits:
                SCREEN.blit(GAME_SPRITES['numbers'][digit], (Xoffset, SCREENHEIGHT*0.12))
                Xoffset += GAME_SPRITES['numbers'][digit].get_width()


                
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def isCollide(playerx, playery, upperPipes, lowerPipes):
    if playery> GROUNDY - 25  or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight + pipe['y'] and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True

    for pipe in lowerPipes:
        if (playery + GAME_SPRITES['player'].get_height() > pipe['y']) and abs(playerx - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True

    return False

def getRandomPipe():
    """
    Generate positions of two pipes(one bottom straight and one top rotated ) for blitting on the screen
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0, int(SCREENHEIGHT- 1.2 *offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 + offset
    pipe = [
        {'x': pipeX, 'y': -y1}, #upper Pipe
        {'x': pipeX, 'y': y2} #lower Pipe
    ]
    return pipe

def gameOver(score):
    game_over_bg = pygame.image.load(GAMEOVER).convert()

    # Display game over text
    game_over_text = pygame.font.Font(None, 50).render("GAME OVER", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 4))

    # Display score
    score_text = pygame.font.Font(None, 50).render(f"YOUR SCORE IS {score}", True, (255, 255, 255))
    score_rect = score_text.get_rect(center=(SCREENWIDTH // 2, SCREENHEIGHT // 2))

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                return  # Return to welcome window upon spacebar press

        SCREEN.blit(game_over_bg, (0, 0))
        SCREEN.blit(game_over_text, game_over_rect)
        SCREEN.blit(score_text, score_rect)

        pygame.display.update()
        pygame.time.Clock().tick(FPS)







if __name__ == "__main__":
    # This will be the main point from where our game will start
    pygame.init() # Initialize all pygame's modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption('FLUTTERING FISH')
    GAME_SPRITES['numbers'] = ( 
        pygame.image.load('sprites/0.png').convert_alpha(),
        pygame.image.load('sprites/1.png').convert_alpha(),
        pygame.image.load('sprites/2.png').convert_alpha(),
        pygame.image.load('sprites/3.png').convert_alpha(),
        pygame.image.load('sprites/4.png').convert_alpha(),
        pygame.image.load('sprites/5.png').convert_alpha(),
        pygame.image.load('sprites/6.png').convert_alpha(),
        pygame.image.load('sprites/7.png').convert_alpha(),
        pygame.image.load('sprites/8.png').convert_alpha(),
        pygame.image.load('sprites/9.png').convert_alpha(),
    )


   
    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load( PIPE).convert_alpha(), 180), 
    pygame.image.load(PIPE).convert_alpha()
    )

  

    GAME_SPRITES['background1'] = pygame.image.load(BACKGROUND1).convert()
    GAME_SPRITES['background2'] = pygame.image.load(BACKGROUND2).convert()
    GAME_SPRITES['background3'] =  pygame.image.load(BACKGROUND3).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

    GAME_SOUNDS['die'] = pygame.mixer.Sound('sounds/game-over-arcade-6435.mp3')
    GAME_SOUNDS['hit'] = pygame.mixer.Sound('sounds/Wooden Bat Hits Baseball Run.mp3')
    GAME_SOUNDS['point'] = pygame.mixer.Sound('sounds/collectcoin-6075.mp3')
    GAME_SOUNDS['swoosh'] = pygame.mixer.Sound('sounds/Punch Swoosh Series.mp3')
    GAME_SOUNDS['flap'] = pygame.mixer.Sound('sounds/wing-flap-1-6434.mp3')    

    

    while True:
        welcomeWindow() # Shows welcome screen to the user until he presses a button
        mainGame()