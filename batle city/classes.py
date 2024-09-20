import pygame
from settings import * 
from abc import ABC , abstractmethod
from random import randint
pygame.init()



mw = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

class TXT (): 
    def __init__(self,x,y,text,font_size) :
        self.font = pygame.font.Font("Bully.otf",int(font_size))
        self.x = x 
        self.y = y
        self.text = text
        self.txt = self.font.render(str(self.text),1, WHITE, None)
        self.filename = "txt" 
        
    def draw(self): 
        self.txt = self.font.render(str(self.text),1, WHITE, None)
        mw.blit(self.txt ,(self.x,self.y))

class Sprite(ABC,pygame.sprite.Sprite):
    def __init__(self, filename, x, y, w,h):
        super().__init__()
        self.filename = filename
        self.w=w
        self.h=h
        self.image = pygame.Surface.convert(pygame.transform.scale(pygame.image.load(self.filename), (self.w, self.h)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def collidepoint (self , x ,y):
        return self.rect.collidepoint(x,y)  
      
    def draw(self): 
        self.image = pygame.transform.scale(pygame.image.load(self.filename), (self.w, self.h))
        mw.blit(self.image, (self.rect.x, self.rect.y))

    @abstractmethod
    def update (self):
        pass

class Picture(Sprite):
    def update(self):
        self.draw()

class Tank (ABC):
    def __init__(self, filename, x, y, w, h, color):
        super().__init__(filename, x, y, w, h)
        self.speed = TILE/10
        self.pivot = "up"
        self.color = color
        self.bullets = pygame.sprite.Group()
        self.shotting = True
        self.count_frames = 0   
        self.xp = 1

    @abstractmethod
    def shot(self):
        pass
    
    def update(self,blocks,tanks):
        self.update_bulets(blocks,tanks)
        if self.xp > 0 :
            self.filename = "img/"+self.color+"_tank_"+self.pivot+".png"                
            self.count_frames -= 1
            if self.xp <=0 :
                self.kill
            self.movement()
            self.shot()
            self.draw()
       

    def update_bulets(self,blocks,tanks):
        for bullet in self.bullets:
            bullet.draw()
            bullet.update()
            if bullet.rect.x > WIDTH or bullet.rect.x < 0 or bullet.rect.y > HEIGHT or bullet.rect.y < 0 :
                self.bullets.remove(bullet)
            
            for block in blocks :
                if pygame.sprite.collide_rect(bullet,block):
                    self.bullets.remove(bullet)
             
            for tank in tanks:
                if tank != self and pygame.sprite.collide_rect(bullet,tank) :
                    if  (isinstance(self,Enemy) and isinstance(tank,Player)) or (isinstance(self,Player) and isinstance(tank,Enemy)):
                        tank.xp -=1
                        self.bullets.remove(bullet)
                        if tank.xp <=0 and isinstance(tank,Enemy):
                            self.murder +=1


    @abstractmethod
    def movement(self):
        pass
            
class Bullet(Sprite):
    def __init__(self, filename, x, y, w, h ,pivot):
        super().__init__(filename, x, y, w, h)
        self.pivot = pivot
        self.speed = TILE//6

    def update(self):
        if self.pivot == "up":
            self.rect.y -= self.speed 
        elif self.pivot == "down":
            self.rect.y += self.speed 
        elif self.pivot == "left":
            self.rect.x -= self.speed 
        elif self.pivot == "right":
            self.rect.x += self.speed

class Player (Tank,Sprite):
    def __init__(self, filename, x, y, w, h, color):
        super().__init__(filename, x, y, w, h, color)
        self.murder = 0

    def movement(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_w]  :
            self.rect.y-=self.speed
            self.pivot = "up"
        elif keys[pygame.K_s]  :
            self.rect.y+=self.speed
            self.pivot = "down"
        elif keys[pygame.K_a]:
            self.rect.x-=self.speed
            self.pivot = "left"
        elif keys[pygame.K_d]:
            self.rect.x +=self.speed
            self.pivot = "right"    

    def shot(self):
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE] and self.count_frames <= 0 :
            self.bullets.add(Bullet("img/bulletr.png",self.rect.centerx-TILE//8,self.rect.centery-TILE//8,TILE//4,TILE//4,self.pivot))
            self.count_frames = 20

    def draw(self):
        if self.xp > 0 :
            super().draw() 
    
class Enemy(Tank,Sprite):
    def __init__(self, filename, x, y, w, h, color):
        super().__init__(filename, x, y, w, h, color)
        self.pivots = ["up","down","left","right"]
        self.change_pivot()
        speed = randint(TILE//10,TILE//7)
        self.speed = speed
    
    def movement(self):
        if self.pivot == "up"  :
            self.rect.y-=self.speed    
        elif self.pivot == "down"  :
            self.rect.y+=self.speed    
        elif self.pivot == "left":
            self.rect.x-=self.speed    
        elif self.pivot == "right":
            self.rect.x +=self.speed

    def change_pivot(self):
        self.pivot = self.pivots[randint(0,len(self.pivots)-1)]

    def shot(self):
        if  self.count_frames <= 0 :
            self.bullets.add(Bullet("img/bulletr.png",self.rect.centerx-TILE//8,self.rect.centery-TILE//8,TILE//4,TILE//4,self.pivot))
            self.count_frames = 80

    

class Block(Sprite):
    def update(self,tanks):
        for tank in tanks :
            if pygame.sprite.collide_rect(self,tank):
                if tank.pivot == "up":
                    tank.rect.y += tank.speed 
                elif tank.pivot == "down":
                    tank.rect.y -= tank.speed 
                elif tank.pivot == "left":
                    tank.rect.x += tank.speed 
                elif tank.pivot == "right":
                    tank.rect.x -= tank.speed
                if isinstance(tank,Enemy):
                    try:
                        tank.change_pivot()
                    except:
                        pass




