# V4
#pedro
import pygame
import random
from pygame.locals import *

#define fps
clock = pygame.time.Clock()
fps = 30


width = 600
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

#define variaveis
linhas = 5
colunas = 5


#define cores
vermelho = (255, 0, 0)
verde = (0, 255, 0)


#carrega imagem
bg = pygame.image.load('espaco.jpg')
bg = pygame.transform.scale(bg, (width,height))

def draw_bg():
    screen.blit(bg, (0, 0))


#create spaceships class
class Nave(pygame.sprite.Sprite):
    def _init_(self, x, y, vida):
        pygame.sprite.Sprite._init_(self)
        self.image = pygame.image.load('nave.png')
        self.image = pygame.transform.scale(self.image, (60, 60)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.vida_inicial = vida
        self.vida_restante = vida
        self.ultimo_tiro = pygame.time.get_ticks()


    def update(self):
        #velocidade de movimento
        velocidade = 8
        #cooldown
        cooldown = 500 #milisegundos
        
        
        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right <width:
            self.rect.x += velocidade


        #record current time
        time_now = pygame.time.get_ticks()
        #shoot
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:
            balas = Tiros(self.rect.centerx, self.rect.top)
            tiro_grupo.add(balas)
            self.last_shot = time_now


        #draw health bar
        pygame.draw.rect(screen, vermelho, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, verde, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 15))



#create spaceships class
class Tiros(pygame.sprite.Sprite):
    def _init_(self, x, y):
        pygame.sprite.Sprite._init_(self)
        self.image = pygame.image.load('tiro.png')
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()

#cria Aliens
class Aliens(pygame.sprite.Sprite):
    def _init_(self, x, y):
        pygame.sprite.Sprite._init_(self)
        self.image = pygame.image.load('img/alien' + str(random.radiant(1,5))+'.png')
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.contador_movimento = 0
        self.direcao_movimento = 1 
    
    def update(self):
        self.rect.x += self.direcao_movimento
        self.contador_movimento += 1
        if abs(self.contador_movimento) > 75:
            self.direcao_movimento *= -1
            self.contador_movimento *= self.direcao_movimento


#cria grupo de sprites
nave_grupo = pygame.sprite.Group()
tiro_grupo = pygame.sprite.Group()
alien_grupo = pygame.sprite.Group()

def cria_aliens():
    #gera aliens
    for linha in range(linhas):
        for item in range(colunas):
            alien = Aliens(100+item*100, 100 + linhas*70)
            alien_grupo.add(alien)
cria_aliens()




#cria jogador
nave = Nave(int(width / 2), height - 100, 3)
nave_grupo.add(nave)



run = True
while run:

    clock.tick(fps)

    #draw background
    draw_bg()

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    
    #update spaceship
    nave.update()

    
    #update sprite groups
    tiro_grupo.update()
    alien_grupo.update()
    #draw sprite groups
    nave_grupo.draw(screen)
    tiro_grupo.draw(screen)
    alien_grupo.draw(screen)

    pygame.display.update()

pygame.quit()