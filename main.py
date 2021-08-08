
import pygame as pg
import random
from settings import *
from sprite import *

class Game():
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH,HEIGHT))
        pg.display.set_caption("Jumpy")
        self.clock=pg.time.Clock()

        self.running=True
        self.font_name=pg.font.match_font(FONT_NAME)
    
    def startScreen(self):
        self.screen.fill(BG)
        self.draw_text(TITLE,40,RED,WIDTH/2,HEIGHT/4)
        self.draw_text("Arrows to move,Space to jump",22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to play",22,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    waiting=False
                    self.running=False
                if event.type==pg.KEYUP:
                    waiting=False

    def new(self):
        self.score=0
        self.all_sprites=pg.sprite.Group()
        self.plateform=pg.sprite.Group()
        self.player=Players(self)

        self.all_sprites.add(self.player)
        for plate in P_LIST:
            p=Plateforms(*plate)
            self.plateform.add(p)
            self.all_sprites.add(p)
        self.run()

    def run(self):
        #gameloop
        self.playing=True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
            

    def events(self):
        for event in pg.event.get():
            if event.type==pg.QUIT:
                if self.playing:
                    self.playing=False
                self.running=False
            if event.type==pg.KEYDOWN:
                if event.key==pg.K_SPACE:
                    self.player.jump()
            
        
    def update(self):
        self.all_sprites.update()
        #stop only if falling
        if self.player.vel.y>0:
            hits=pg.sprite.spritecollide(self.player,self.plateform,False)
            if hits:
                self.player.pos.y=hits[0].rect.top
                self.player.vel.y=0
        #scrolling down
        if self.player.rect.top<=HEIGHT/4:
            self.player.pos.y+=abs(self.player.vel.y)
            for plat in self.plateform:
                plat.rect.y+=abs(self.player.vel.y)
                if plat.rect.top>=HEIGHT:
                    plat.kill()
                    self.score+=10
        #GAMEoVER
        if self.player.rect.bottom>HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y-=max(self.player.vel.y,10)
                if sprite.rect.bottom<0:
                    sprite.kill()
            if len(self.plateform)==0:
                self.playing=False
        #spawning new ones
        while len(self.plateform)<6:
            width=random.randrange(50,100)
            
            p=Plateforms(random.randrange(0,WIDTH-width),random.randrange(-75,-30)
                        ,width,20)
            self.plateform.add(p)
            self.all_sprites.add(p)

            

    def draw(self):
        self.screen.fill(BG)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score),22,WHITE,WIDTH/2,50)
    #at theend of drawing everything
        pg.display.flip()

    def draw_text(self,text,size,color,x,y):
        font=pg.font.Font(self.font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        text_rect.midtop=(x,y)
        self.screen.blit(text_surface,text_rect)
        

    def gameOver(self):
        if not self.running:
            return
        self.screen.fill(BG)
        self.draw_text("GAME OVER",40,RED,WIDTH/2,HEIGHT/4)
        self.draw_text("Score: "+str(self.score),22,WHITE,WIDTH/2,HEIGHT/2)
        self.draw_text("Press a key to play again",22,WHITE,WIDTH/2,HEIGHT*3/4)
        pg.display.flip()
        self.wait_for_key()


g=Game()
g.startScreen()
while g.running:
    
    g.new()
    
    g.gameOver()

pg.quit()

    
