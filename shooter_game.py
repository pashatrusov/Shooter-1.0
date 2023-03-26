#Создай собственный Шутер!

from pygame import *
from random import randint
win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"),(win_width,win_height))
score = 0
lost = 0

speed = 3
game = True
clock = time.Clock()
FPS = 80

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font2 = font.SysFont("Arial", 36)
win = font2.render('YOU WIN!', True,(255,215,0))
lose = font2.render('YOU LOSE!', True,(180,0,0))
img_bulet = "puly.png"
class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y,size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
           self.rect.x = randint(40,win_height - 30 )
           self.rect.y = 0
           lost = lost + 1 

class Bulet(GameSprite):
      def update(self):
          self.rect.y += self.speed
          if self.rect.y == 0:
              self.kill()


class Player(GameSprite):
    def update(self):
        keys=key.get_pressed()
        if keys[K_LEFT] and self.rect.x > -20:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
        bulet = Bulet(img_bulet,self.rect.centerx,self.rect.top,20,40,-15)
        bulets.add(bulet)

player = Player('raketa.png',200,390,100,100,10)


monsters = sprite. Group()
for i in range(1 ,10):
    monster=Enemy('asteroid.png',randint(10,680), -40,95,95, randint(3,5))
    monsters.add(monster)
finish = False

bulets = sprite. Group()

musors = sprite. Group()
for i in range(1 ,4):
    musor=Enemy('musor.png',randint(10,680), -40,90,90, randint(4,5))
    musors.add(musor)
finish = False


while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                #fire_sound.play()
                player.fire()
    if not finish:        
        window.blit(background,(0,0))

        musors.draw(window)
        player.update()
        monsters.update()   
        player.reset()

        musors.update()      
        monsters.draw(window)   
        bulets.draw (window)
        bulets.update()
        text=font2.render("Счет:" + str(score), 1, (255,0,255)) 
        window.blit(text,(10,20))
        text_lose = font2.render("Пропущено:" + str(lost), 1, (255,0,255))
        window.blit(text_lose,(10,50))
        
        collides = sprite.groupcollide(monsters,bulets,True,True)
        for c in collides:
            score = score + 1
            monster = Enemy('asteroid.png',randint(10,690), -40,95,95, randint (3,5))
            monsters.add(monster)

        if sprite.spritecollide(player,monsters,False) or lost >=15 or sprite.spritecollide(player,musors,False):
            finish = True
            window.blit(lose,(300, 200))

        if score >= 51:
            finish = True
            window.blit(win,(300, 200))

        if finish == True:
            mixer.music.stop()

        display.update() 

    time.delay(50)