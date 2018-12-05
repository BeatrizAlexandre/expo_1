# -- coding: utf-8 --
"""
Created on Tue May 29 11:04:40 2018

@author: Beatriz
"""
#========= IMPORTANDO BIBLIOTECAS======
import pygame
from pygame.locals import *
from random import randrange
from random import randint
import cv2
import numpy as np
import pygame.locals

#======== DEFININDO FUNÇÕES====

def text_objects(text, font):
    textSurface = font.render('Fit Ninja', True, pink)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',115)
    TextSurf, TextRect = text_objects('Fit Ninja', largeText)
    TextRect.center = ((400),(100))
    gameDisplay.blit(TextSurf, TextRect)
 
    pygame.display.update()
    relogio.tick(15)
  
# ======== OPEN CV ========
lowerBound = np.array([20,100,20]) #amarelo
upperBound = np.array([80,255,255]) #amarelo
cam = cv2.VideoCapture(0)

def open_cv():
    
    ret, img = cam.read()
    img = cv2.resize(img, (800, 600))    
    imgHSV = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(imgHSV,lowerBound,upperBound)
    # Find the largest contour and extract it
    # https://stackoverflow.com/questions/39044886/finding-largest-blob-in-image
    _, contours, _ = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE )

    maxContour = 0
    maxContourData = None
    for contour in contours:
        contourSize = cv2.contourArea(contour)
        if contourSize > maxContour:
            maxContour = contourSize
            maxContourData = contour
    if maxContourData is not None and maxContour > 400:
        x,y,w,h=cv2.boundingRect(maxContourData)
        x = 800 - x 
        ponto_x = (x + (w/2))
        ponto_y = (y + (h/2))
    else:
        ponto_x = None
        ponto_y = None
        
#    cv2.imshow('mask',mask)
#    cv2.imshow('cam',img)
#    cv2.waitKey(10)
    
    return ponto_x, ponto_y


#======== CLASSES========
#Botão
class Button(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()

    def setCords(self,x,y):
        self.rect.topleft = x,y

    def pressed(self,mouse):
        if mouse[0] > self.rect.topleft[0] and \
            mouse[1] > self.rect.topleft[1] and \
            mouse[0] < self.rect.bottomright[0] and \
            mouse[1] < self.rect.bottomright[1]:
            return True
        else:
            return False
#Comida
class InfoComida:
    FAST_FOOD = 0
    FIT = 1    
    def __init__(self, tipo, imagem, recompensa):
        self.tipo = tipo
        self.imagem = imagem
        self.recompensa = recompensa
    def move(self, x, y):
        self.rect.x = x - 10
        self.rect.y = y - 10
      
class Comida(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y, vel_x, vel_y, recompensa):
        pygame.sprite.Sprite.__init__(self)
        self.recompensa = recompensa
        self.vx = vel_x
        self.vy = vel_y
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
    def update(self):
        self.rect.y += self.vy

#Mouse
class Mouse(pygame.sprite.Sprite):
    def __init__(self, arquivo_imagem, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(arquivo_imagem)
        self.rect = self.image.get_rect()
        self.rect.x = pos_x
        self.rect.y = pos_y
        
    def move(self, x, y):
        self.rect.x = x - 10
        self.rect.y = y - 10

#======= DICIONARIO DE COMIDAS ========
comidas = {
    'abacaxi': InfoComida(InfoComida.FIT, 'abacaxi.png', -5),
    'agua': InfoComida(InfoComida.FIT, 'agua.png', -5),
    'morango': InfoComida(InfoComida.FIT, 'morango.png', -10),
    'pessego': InfoComida(InfoComida.FIT, 'pessego.png', -10),
    'pizza': InfoComida(InfoComida.FAST_FOOD, 'pizza.png', 5),
    'burger': InfoComida(InfoComida.FAST_FOOD, 'burger.png', 10),
    'bacon': InfoComida(InfoComida.FAST_FOOD, 'bacon.png', 15)
}

# ========= LISTA DE COMIDAS =========
lista_comidas = [
    'abacaxi', 'agua', 'morango', 'pessego', 'pizza', 'burger', 'bacon'
]


#====== TELA INICIAL =====        
pygame.init()
tela = pygame.display.set_mode((800, 600), 0, 32)

gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Fit Ninja')
fundo_inicial = pygame.image.load("fundo.jpg").convert()

relogio = pygame.time.Clock()

# ======= CORES DAS LETRAS =====
black = (0,0,0)
white = (255,255,255)
pink = (255,110,246)

# ============= BOTÕES DO JOGO  ========
config = Button('config.png')
config.setCords(100,400)

button = Button('button.png')
button.setCords(275,200)

music = Button ('music.png')
music.setCords(100,400)

replay = Button('replay.png')
replay.setCords(300,300)

sound = Button('sound.png')
sound.setCords(500,400)

# ========= FUNDO ========
fundo_inicial = pygame.image.load("fundo.jpg").convert()

largeText = pygame.font.Font('freesansbold.ttf',115)
TextSurf, TextRect = text_objects('Fit Ninja', largeText)
TextRect.center = ((400),(100))
fundo_inicial.blit(TextSurf, TextRect)
gameDisplay.blit(fundo_inicial, (0,0))
gameDisplay.blit(button.image, button.rect.topleft)
gameDisplay.blit(config.image, config.rect.topleft)
pygame.display.update()

bolinha = Mouse("bolinha.png", 0, 0)

fast_food_group = pygame.sprite.Group()
comida_fit_group = pygame.sprite.Group()

# ========= CAINDO COMIDAS ========
ultima_pos_y = 0
for i in range(randint(1,1100)):
    c = lista_comidas[randrange(0,len(lista_comidas))]
    
    pos_x = randrange(0,600,130)
    pos_y = ultima_pos_y - randrange(200)
    ultima_pos_y = pos_y
    rango = Comida(comidas[c].imagem, pos_x, pos_y, 3, randrange(8,10),
               comidas[c].recompensa)
    tipo_rango = comidas[c].tipo
    if tipo_rango == InfoComida.FAST_FOOD:
        fast_food_group.add(rango)
    elif tipo_rango == InfoComida.FIT:
        comida_fit_group.add(rango)

# === SEGUNDA PARTE: LÓGICA DO JOGO ===

relogio = pygame.time.Clock()

#===== MUSICA ============
pygame.mixer.music.load('getdown.mp3')
# Link da musica
# https://www.youtube.com/watch?v=91LPvNmw04s

#======= SOM ==========
som = pygame.mixer.Sound('som.wav')


fundo = pygame.image.load("fundo.jpg").convert()

#Pontos
pontos = 0
font = pygame.font.SysFont("arial", 55)

#Vidas
vidas = 5
fonte = pygame.font.SysFont("arial", 55)

#Recorde
recorde = 0
fon= pygame.font.SysFont("arial", 55)

# ========= IMAGENS =======
right = pygame.image.load('right.png')
abacaxi = pygame.image.load('abacaxi.png')
agua = pygame.image.load('agua.png')
morango = pygame.image.load('morango.png')
pessego = pygame.image.load('pessego.png')
wrong = pygame.image.load('wrong.png')
pizza = pygame.image.load('pizza.png')
burger = pygame.image.load('burger.png')
bacon = pygame.image.load('bacon.png')

#============ TELAS =============
estado = 0            

while estado != -1:
    
    relogio.tick(120)
    
    if estado == 0:  # Esperando começar o jogo.
        for event in pygame.event.get():
            if event.type == QUIT:
                estado = -1

            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button.pressed(mouse_pos):
                    pygame.mixer.music.play(loops=-1,start=0.0)
                    estado = 3  
                elif config.pressed(mouse_pos):
                     gameDisplay.blit(fundo, (0,0))
                     estado = 2
        pygame.display.update()

              
    elif estado == 1:  # Jogo começa.
        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                estado = -1
        mouse_position = open_cv()
        if mouse_position[0] == None:
            bolinha.move(400,300)
        else:
            bolinha.move(mouse_position[0], mouse_position[1])
            
        #destruindo comidas
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_SPACE]:
            fast_food_killed = pygame.sprite.spritecollide(bolinha, fast_food_group, True)
            comida_fit_killed = pygame.sprite.spritecollide(bolinha, comida_fit_group, True)

            #GANHA PONTOS SE ACERTAR FAST FOOD
            for comida in fast_food_killed:
                som.play(1)
                pontos += comida.recompensa
                                
            #PERDE VIDAS SE ACERTAR COMIDA FIT
            for comida in comida_fit_killed:  
                pontos += comida.recompensa
                vidas -= 1
            if vidas <= 0:
                estado = 7  # TELA GAME OVER.

    
        fast_food_group.update()
        comida_fit_group.update()
        
        #VERIFICANDO SE TODAS AS COMIDAS CAIRAM, SE SIM ACONTECE GAME OVER
        tem_comida = False
        for c in fast_food_group:
            if c.rect.y < 600:
                tem_comida = True
        for c in comida_fit_group:
            if c.rect.y < 600:
                tem_comida = True

        if not tem_comida:
            estado = 7
        
        tela.blit(fundo, (0, 0))
        
        
        #MOSTRA OS PONTOS NA TELA
        texto = font.render("Pontos: {0}". format(pontos), True, (0, 1, 0))
        tela.blit(texto, (580 - texto.get_width() // 5, 120 - texto.get_height() // 1))
        
        #MOSTRA AS VIDAS NA TELA
        texto = font.render("Vidas: {0}". format(vidas), True, (0, 1, 0))
        tela.blit(texto, (230 - texto.get_width() // 1, 120 - texto.get_height() // 1))
        
        fast_food_group.draw(tela)
        comida_fit_group.draw(tela)
        tela.blit(bolinha.image, (bolinha.rect.x, bolinha.rect.y))
        
        pygame.display.update()
 

#=========== CONFIGURACOES ===============      
    elif estado == 2: 
        
        gameDisplay.blit(button.image, button.rect.topleft)
        gameDisplay.blit(music.image, music.rect.topleft)
        gameDisplay.blit(sound.image, sound.rect.topleft)
        
        for event in pygame.event.get():
            if event.type == QUIT:
                estado = -1
                
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if music.pressed(mouse_pos):
                    pygame.mixer.quit()
                    estado = 2

                elif sound.pressed(mouse_pos):
                    pygame.mixer.quit()
                    estado = 2
                
                elif button.pressed(mouse_pos):
                    estado = 1
                    
                
        pygame.display.update()
            
#========== INSTRUÇÕES =================
    #O que NÃO acertar        
    elif estado == 3:
        gameDisplay.blit(fundo, (0,0))
        gameDisplay.blit(wrong, (225,100))
        gameDisplay.blit(agua, (50,300))
        gameDisplay.blit(abacaxi, (250,170))
        gameDisplay.blit(morango, (450,300))
        gameDisplay.blit(pessego, (650,300))
        texto = font.render("Não clique (espaço) nas comidas fit!", True, pink)
        tela.blit(texto, (45,400))     
        text = font.render("Aperte enter", True, pink)
        tela.blit (text, (250, 500))
        pygame.display.update()        
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                estado = -1
            elif events.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_RETURN]:
                    estado = 4        
    #O que acertar
    elif estado == 4:
        gameDisplay.blit(fundo, (0,0))
        gameDisplay.blit(right, (225,50))
        gameDisplay.blit(pizza, (75,250))
        gameDisplay.blit(burger, (300,270))
        gameDisplay.blit(bacon, (525,250))
        texto = font.render("Clique (espaço) nos fast foods!", True, pink)
        tela.blit(texto, (101,400))
        text = font.render("Aperte enter", True, pink)
        tela.blit (text, (250, 500))
        pygame.display.update()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                estado = -1
            elif events.type == pygame.KEYDOWN:
                pressed_keys = pygame.key.get_pressed()
                if pressed_keys[K_RETURN]:
                    estado = 1
        
# ================ GAME OVER =========       
    elif estado == 7:  
        tela.blit(fundo, (0, 0))
        Fonte= pygame.font.SysFont("freesansbold.ttf", 115)
        Fonte2= pygame.font.SysFont("freesansbold.ttf", 40)
        txt = Fonte.render("GAME OVER", True, (0, 1, 0))
        txt2 = Fonte2.render("REPLAY", True, (0, 0.2, 0))
        tela.blit(txt, (650 - txt.get_width() // 1, 200 - txt.get_height() // 1))
        pygame.mixer.music.stop()

        tem_recorde = False

        if pontos > recorde:
            tem_recorde = True
            recorde = pontos

        while estado == 7:
            tela.blit(fundo, (0, 0))
            Fonte= pygame.font.SysFont("freesansbold.ttf", 115)
            txt = Fonte.render("GAME OVER", True, (0, 1, 0))
            tela.blit(txt, (650 - txt.get_width() // 1, 200 - txt.get_height() // 1))
            gameDisplay.blit(replay.image, replay.rect.topleft)
            tela.blit(txt2, (827 - txt.get_width() // 1, 455 - txt.get_height() // 1))
            
            # Link dos escritos: https://nerdparadise.com/programming/pygame/part5
            # Modificado
            if tem_recorde:
                texto = font.render("Novo Recorde: {0}". format(recorde), True, (0, 1, 0))
                tela.blit(texto, (550 - texto.get_width() // 1, 250 - texto.get_height() // 1))
            
            else:
                texto = font.render("Pontos: {0}". format(pontos), True, (0, 1, 0))
                tela.blit(texto, (500 - texto.get_width() // 1, 250 - texto.get_height() // 1))
            
            for event in pygame.event.get():
                if event.type == QUIT:
                    estado = -1
                    
                elif event.type == MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if replay.pressed(mouse_pos):
                        pygame.mixer.music.play(loops=-1,start=0.0)
                        estado = 1
                        vidas = 5
                        pontos = 0
   
            pygame.display.update()
        

pygame.display.quit()
pygame.mixer.quit()
pygame.quit()


# ============ Links ===============

# Para entender melhor o Pygame
#http://www.dainf.ct.utfpr.edu.br/petcoce/wp-content/uploads/2013/09/document.pdf
#http://www.dsc.ufcg.edu.br/~pet/atividades/minicurso_pygame/MiniCursoPygame.pdf

# Para diminuir as imagens
# https://www.iloveimg.com/resize-image

# Para baixar as imagens PNG
# https://designermaodevaca.com/post/pngall

# Para colocar musica e som no jogo
# https://nerdparadise.com/programming/pygame/part3

# Para converter o som
# https://www.youtube.com/watch?v=91LPvNmw04s