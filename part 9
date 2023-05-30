#V6

import pygame
import random
from pygame import mixer 
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

#define fps
clock = pygame.time.Clock()
fps = 60


width = 600
height = 800

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Space Invaders')

#define fonts

font30 = pygame.font.SysFont('Constantia, 30')
font40 = pygame.font.SysFont('Constantia, 40')

explosao_fx = pygame.mixer.Sound("img/explosao.wav")
explosao_fx.set_volume(0.25)

explosao2_fx = pygame.mixer.Sound("img/explosao2.wav")
explosao2_fx.set_volume(0.25) 

laser_fx = pygame.mixer.Sound("img/laser.wav")
laser_fx.set_volume(0.25) 


#define variaveis
linhas = 5
colunas = 5
alien_cooldown = 1000
ultimo_tiro_alien = pygame.time.get_ticks()
countdown = 3
ultimo_count = pygame.time.get_ticks
game_over = 0  


#define cores
vermelho = (255, 0, 0)
verde = (0, 255, 0)
white = (255, 255, 255)


#carrega imagem
bg = pygame.image.load('espaco.jpg')
bg = pygame.transform.scale(bg, (width,height))

def draw_bg():
    screen.blit(bg, (0, 0))


#define function for creating text

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))




#create spaceships class
class Nave(pygame.sprite.Sprite):
    def init(self, x, y, vida):
        pygame.sprite.Sprite.init(self)
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
        game_over = 0  
        
        
        #get key press
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= velocidade
        if key[pygame.K_RIGHT] and self.rect.right <width:
            self.rect.x += velocidade


        #record current time
        tempo_0 = pygame.time.get_ticks()
        #atira
        if key[pygame.K_SPACE] and tempo_0 - self.last_shot > cooldown:
            laser_fx.play()
            balas = Tiros(self.rect.centerx, self.rect.top)
            tiro_grupo.add(balas)
            self.last_shot = tempo_0


        #mascara
        self.mascara = pygame.mask.from_surface(self.image)

        #barra de vida
        pygame.draw.rect(screen, vermelho, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.vida_restante > 0:
            pygame.draw.rect(screen, verde, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.vida_restante / self.vida_inicial)), 15))
        elif self.vida_restante <= 0:
            explosao = Explosao(self.rect.centerx,self.rect.centery, 3)
            explosao_grupo.add(explosao)
            self.kill()
            game_over = -1
        return game_over 


#create spaceships class
class Tiros(pygame.sprite.Sprite):
    def init(self, x, y):
        pygame.sprite.Sprite.init(self)
        self.image = pygame.image.load('donut.jpeg')
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    
    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_grupo, True):
            self.kill()
            explosao = Explosao(self.rect.centerx,self.rect.centery, 2)
            explosao_grupo.add(explosao)

#cria Aliens
class Aliens(pygame.sprite.Sprite):
    def init(self, x, y):
        pygame.sprite.Sprite.init(self)
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



#cria tiro dos aliens
class Alien_Tiros(pygame.sprite.Sprite):
    def init(self, x, y):
        pygame.sprite.Sprite.init(self)
        self.image = pygame.image.load('tiro_dos_aliens.png')
        self.image = pygame.transform.scale(self.image, (40, 40)) 
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]

    
    def update(self):
        self.rect.y += 2
        if self.rect.top > height:
            self.kill()
        if pygame.sprite.spritecollide(self, nave_grupo, False, pygame.sprite.collide_mask ):
            self.kill()
            explosao2_fx.play() 
            #dano na nave
            nave.vida_restante -= 1
            explosao_fx.play()
            explosao = Explosao(self.rect.centerx,self.rect.centery, 1)
            explosao_grupo.add(explosao)

#cria classe de Explosoes  
class Explosao(pygame.sprite.Sprite):
    def init(self, x, y, tamanho):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1,6):
            img = pygame.image.load(f"img/exp{num}.png")
            if tamanho == 1:
                img = pygame.transform.scale(img, (20,20))
            if tamanho == 2:
                img = pygame.transform.scale(img, (40,40))
            if tamanho == 3:
                img = pygame.transform.scale(img, (160,160))
            #adiciona a imagem na lista
            self.images.append(img)
        self.index = 0 
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.counter = 0
    
    def update(self):
        explosion_speed = 3
        #atualiza a animacao da explosao
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # se a animacao estiver completa, apaga a explosao 
        if self.index >= len(self.images) -1 and self.counter >= explosion_speed:
            self.kill()


#cria grupo de sprites
nave_grupo = pygame.sprite.Group()
tiro_grupo = pygame.sprite.Group()
alien_grupo = pygame.sprite.Group()
tiro_alien_grupo = pygame.sprite.Group()
explosao_grupo = pygame.sprite.Group()


def cria_aliens():
    #gera aliens
    for linha in range(linhas):
        for item in range(colunas):
            alien = Aliens(100+item*100, 100 + linha*70)
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

    if countdown == 0:
        #tiros aliens
        tempo_0 = pygame.time.get_ticks()
        if tempo_0 - ultimo_tiro_alien > alien_cooldown and len(tiro_alien_grupo) < 7 and len(alien_grupo) > 0:
            ataque_alien = random.choice(alien_grupo.sprites())
            tiro_alien = Alien_Tiros(ataque_alien.rect.centerx, ataque_alien.rect.bottom)
            tiro_alien_grupo.add(tiro_alien)
            ultimo_tiro_alien = tempo_0

        #checa se todos os aliens morreram
        if len(alien_grupo) == 0:
            game_over = 1
        
        if game_over == 0:
 
            #update spaceship
            game_over = nave.update()

            #update sprite groups
            tiro_grupo.update()
            alien_grupo.update()
            tiro_alien_grupo.update()
        else:
            if game_over == -1:
                draw_text("GAME OVER!", font40, white, int(width/ 2 - 100), int(height / 2 + 50))
            if game_over == 1:
                draw_text("YOU WIN!", font40, white, int(width/ 2 - 100), int(height / 2 + 50))

    if countdown > 0: 
        draw_text("GET READY!", font40, white, int(width/ 2 - 100), int(height / 2 + 50))
        draw_text(str(countdown) , font40, white, int(width/ 2 - 10), int(height / 2 + 100 ))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer
    
    #update explosion group 
    explosao_grupo.update()
    
    #draw sprite groups
    nave_grupo.draw(screen)
    tiro_grupo.draw(screen)
    alien_grupo.draw(screen)
    tiro_alien_grupo.draw(screen)
    explosao_grupo.draw(screen)

    #event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()