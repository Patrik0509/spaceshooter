from pygame import *
from random import randint,random
 
score = 0 
lost = 0 
life = 3
color = (86,222,55)
#класс-родитель для спрайтов
class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
 
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
 
 
#класс-наследник для спрайта-игрока (управляется стрелками)
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < win_width - 40:
            self.rect.x += self.speed


    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 10, self.rect.top, 16, 32, 10)
        bullets.add(bullet)
 
 
#класс-наследник для спрайта-врага
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost += 1

 

#класс-наследник для пуль
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -32:
            self.kill()


#класс-наследник для астероидов
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.y = -50
            self.rect.x = randint(80, win_width - 80)


 
#Игровая сцена:
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
 
#Персонажи игры:
player = Player('rocket.png', 330, win_height - 70, 40,50,10)
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy('ufo.png',randint(80, win_width - 80), - 100,80,50, random() * randint(2,5))
    monsters.add(monster)

bullets = sprite.Group()

# # Астероиды
asteroids = sprite.Group()
for i in range(1, 4):
    asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -50, 50, 50, (random() + random()) * randint(1, 4))
    asteroids.add(asteroid)






#paratmerbl cblkna
game = True
finish = False
clock = time.Clock()
 
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

fire_sound = mixer.Sound('fire.ogg')

#shriftbl
font.init()
font1 = font.SysFont('Arial', 70)
win_text = font1.render('ВЫ ПОБЕДИЛИ',True, (255,255,255))
lose_text = font1.render('ВЫ ПРОИГРАЛИ',True, (255,0,0))

font2 = font.SysFont('Arial',36)


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
 
    if finish != True:
 
        window.blit(background,(0, 0))
        player.update()
        asteroids.update()
        monsters.update()
        monsters.draw(window)
        bullets.update()
        player.reset()
        asteroids.draw(window)
        bullets.draw(window)

        text_score = font2.render('СЧЁТ:' + str(score),True,(255,255,255))
        window.blit(text_score,(10,20))
        
        text_lost = font2.render('ПРОПУЩЕНО:' + str(lost),True,(255,255,255))
        window.blit(text_lost,(10,50))

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png',randint(80, win_width - 80), - 50,80,50, random() * randint(2,5))
            monsters.add(monster)


        if life == 2:
            color = (222,208,55)
        elif life == 1:
            color = (224,63,63)

        text_life = font2.render(str(life),True,color)
        window.blit(text_life,(650,20))

        if sprite.spritecollide(player,monsters,True):
            life -= 1
            monster = Enemy('ufo.png',randint(80, win_width - 80), - 50,80,50, random() * randint(2,5))
            monsters.add(monster)


        if sprite.spritecollide(player,asteroids,True):
            life -= 1

            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -50, 50, 50, (random() + random()) * randint(1, 4))
            asteroids.add(asteroid)


        sprite.groupcollide(bullets,asteroids,True,False )

        if life < 1 or lost >= 5:
            finish = True
            window.blit(lose_text, 150,250)

        
        if score >= 10:
            finish = True
            window.blit(win_text,200,200) 

        display.update()

    else:
        finish = False
        score = 0
        life = 3
        lost = 0

        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1, 6):
            monster = Enemy('ufo.png', randint(80, win_width - 80), -100, 80, 50, (random() + random()) * randint(1, 6))
            monsters.add(monster)

        for i in range(1, 4):
            asteroid = Asteroid('asteroid.png', randint(80, win_width - 80), -50, 50, 50, (random() + random()) * randint(1, 4))
            asteroids.add(asteroid)



    clock.tick(60)



