# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#   Created by: Asher Andargachew                                             #
#                                                                             #
#   Created on: Aug 10th, 2021                                                #
#                                                                             #
#   Description: Matrix code rain from the Matrix movie intro.                #
#                                                                             #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

import pygame
import os
import random

# get screen information
pygame.init()
screenInfo = pygame.display.Info()
WIDTH, HEIGHT = screenInfo.current_w, screenInfo.current_h

# initialize frames
#pygame.time.init()
frameCount = pygame.time.get_ticks()


# initialize screen
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("M4TR1X.exe")
motionBlur = pygame.Surface((WIDTH, HEIGHT))
motionBlur.set_alpha(100)


# initialize font
#pygame.font.init()
FONTSIZE = int((WIDTH+HEIGHT)/100)
FONT = pygame.font.Font(os.path.join('Assets','Fonts/arial-unicode-ms.ttf'), FONTSIZE)

# colors
GREEN = pygame.Color(0, 179, 21) # RGB
LIGHTGREEN = pygame.Color(125,250,140)
BLACK = (0, 0, 0)
BGCOLOR = BLACK

# audio
morpheus = pygame.mixer.Sound(os.path.join('Assets', 'Audio/morpheus.mp3'))

# frames per second
FPS = 60
# frame control
clock = pygame.time.Clock()

print(HEIGHT)
# Katakana class
class Katakana:
    # default properties
    def __init__(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(-HEIGHT, -HEIGHT/4)
        self.TXTSIZE = FONTSIZE
        self.fallSpeed = random.randrange(int(0.0015*HEIGHT), int(0.00601*HEIGHT))
        self.value = str(chr(0x30A0 + random.randrange(0,96)))
        self.switchSpeed = random.randint(2, 20)
        self.rowLength = random.randint(5, 12)
        self.row = [""]*self.rowLength
        self.color = (0,0,0)

    # set characetr value
    def rain(self):
        # create a row for each katakana character falling
        frameCount = pygame.time.get_ticks()
        for x in range(self.rowLength):
            if not int(frameCount) % self.switchSpeed:
                self.value = str(chr(0x30A0 + random.randrange(0,96)))
                self.row[x] = self.value
        self.show()

    # show each character
    def show(self):
        for chr in self.row:
            index = self.row.index(chr)
            if index == len(self.row)-1:
                LIGHTGREEN.hsva = (127, 30, 100, 100)
                self.color = LIGHTGREEN
            else:
                # brightness of characters 
                brightness = self.reMap(index, 5, 0, 70, 0)
                GREEN.hsva = (127, 100, brightness, 100) # HSBA
                self.color = GREEN

            text = FONT.render(chr.encode("utf-8").decode("utf-8"), 1, self.color)
            WIN.blit(text, (self.x - self.TXTSIZE, self.y-(index*-self.TXTSIZE)))
        self.update()
    
    # update character movement
    def update(self):
        # when character is below screen
        if self.y > HEIGHT:
            self.y = -HEIGHT/3

        # increase the fall of the character
        self.y += self.fallSpeed
    
    # remap brightness values (not my function)
    def reMap(self, value, maxInput, minInput, maxOutput, minOutput):
        value = maxInput if value > maxInput else value
        value = minInput if value < minInput else value

        inputSpan = maxInput - minInput
        outputSpan = maxOutput - minOutput

        scaledThrust = float(value - minInput) / float(inputSpan)

        return minOutput + (scaledThrust * outputSpan)

# draw window
def draw(streams):
    #WIN.fill(BGCOLOR)
    WIN.blit(motionBlur,(0,0))

    for stream in streams:
        stream.rain()

    # update screen
    pygame.display.flip()


# main window
def main():
    # for sound
    playing = False

    # create list of character streams
    streams = []
    katakana_limit = int((WIDTH/FONTSIZE)*2.1)
    for _ in range(katakana_limit):
        stream = Katakana()
        streams.append(stream)

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                # when space bar is pushed
                if event.key == pygame.K_SPACE and playing == False:
                    morpheus.play()
                    playing = True
                elif event.key == pygame.K_SPACE and playing == True:
                    morpheus.stop()
                    playing = False

        # display final result
        draw(streams)

    pygame.quit()

if __name__ == "__main__":
    main()