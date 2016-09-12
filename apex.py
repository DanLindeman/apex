import pygame
import PyParticles
import time
from pygame.locals import *
pygame.mixer.init()

zero_point_sound_effect = pygame.mixer.Sound('zero.wav')
two_point_sound_effect = pygame.mixer.Sound('two.wav')
ten_point_sound_effect = pygame.mixer.Sound('ten.wav')
pygame.mixer.music.load('Shanty.wav')
pygame.mixer.music.play(-1)


def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

def calculate_score(x, y):
    """Calculates the users score by comparing peak time to user guess"""
    raw = abs(x - y)
    if raw < 0.1:
        ten_point_sound_effect.play()
        return 10
    if 0.1 < raw < 0.25:
        two_point_sound_effect.play()
        return 2
    else:
        zero_point_sound_effect.play()
        return 0

if __name__ == '__main__':
    pygame.font.init()
    pygame.display.set_caption('Apex')
    (width, height) = (400, 400)
    screen = pygame.display.set_mode((width, height))
    env = PyParticles.Environment((width, height))
    env.addParticles(x=200, y=150, size=10, speed=4, angle=0)

    running = True
    start, now, user_guess, score, loops = 0, 0, 0, 0, 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif (event.type == pygame.MOUSEBUTTONDOWN) or (event.type == pygame.KEYDOWN):
                if (event.type == pygame.MOUSEBUTTONDOWN) or (event.key == pygame.K_SPACE):
                    user_guess = float(truncate(time.time() - start, 2))
        env.update()
        font = pygame.font.Font(None, 36)
        text = font.render("Score", 1, (0, 0, 0))
        #  textpos = text.get_rect(centerx=width/2)

        screen.fill(env.colour)
        screen.blit(text, (100, 100))

        for p in env.particles:
            if height < p.y + 2*p.size:
                if loops < 4:
                    p.colour = (0, 0, 255)
                if 4 < loops < 7:
                    p.colour = (175, 0, 255)
                if 7 < loops < 10:
                    p.colour = (255, 0, 0)
                #  The bottom of the balls journey
                loops += 1
                start = time.time()
                if loops > 10:
                    running = False
            if p.speed == 0.0:
                now = time.time()
                diff = float(truncate(abs(now - start), 2))
                score += calculate_score(diff, user_guess)
                diff = 0
                user_guess = 0
                print("Score: {0}".format(score))

            pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)), p.size, p.thickness)
        pygame.display.flip()
