# -*- coding:utf-8 -*-
#!/usr/bin/env python
#Jumpy!(a platform game)original author:http://patreon.com/kidscancode
#Art from https://www.kenney.nl/
#Happy Tune by http://opengameart.org/users/syncopika
#Yippee by http://opengameart.org/users/snabisch

import pygame as pg
import random,sys
from settings import *
from sprites import *
from tilemap import *
from os import path

#HUD fucntions
def draw_player_health(surf,x,y,pct):
    if pct<0:
        pct=0
    BAR_LENGTH=100
    BAR_HEIGHT=20
    fill=pct*BAR_LENGTH
    outline_rect=pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect=pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct>0.6:col=GREEN
    elif pct>0.3:col=YELLOW
    else:col=RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE ,outline_rect,2)


class Game:
    def __init__(self):
        global pg
        pg.mixer.pre_init(44100,-16,1,2048)
        pg.init()
        self.screen = pg.display.set_mode(SIZE)
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500,100)
        self.running=True
        self.font_name=pg.font.match_font(FONT_NAME)
        self.load_data()

    def load_data(self):
        game_folder=path.dirname(__file__)
        img_folder=path.join(game_folder,'img')
        self.title_font=path.join(img_folder,'ZOMBIE.TTF')
        self.hud_font = path.join(img_folder, 'Impacted2.0.TTF')
        self.dim_screen=pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))

        self.map_folder = path.join(game_folder, 'maps')
        snd_folder = path.join(game_folder, 'snd')
        music_folder = path.join(game_folder, 'music')
        self.player_img=pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.bullet_img={}

        self.bullet_img['org'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img['lg'] = pg.transform.scale(self.bullet_img['org'], (25, 25))
        self.bullet_img['sm'] = pg.transform.scale(self.bullet_img['org'], (10,10))

        self.mob_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.wall_img=pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.splat=pg.image.load(path.join(img_folder,SPLAT)).convert_alpha()
        self.splat=pg.transform.scale(self.splat,(64,64))
        self.gun_flashes=[]
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())
        self.item_images={}
        for item in ITEM_IMAGES:
            self.item_images[item]=pg.image.load(path.join(img_folder,ITEM_IMAGES[item]))

        #sound loading
        pg.mixer.music.load(path.join(music_folder,BG_MUSIC))
        self.effects_sounds={}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type]=pg.mixer.Sound(path.join(snd_folder,EFFECTS_SOUNDS[type]))
        self.weapon_sounds={}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon]=[]
            for snd in WEAPON_SOUNDS[weapon]:
                s=pg.mixer.Sound(path.join(snd_folder,snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)
        self.zombie_moan_sounds=[]
        for snd in ZOMBIE_MOAN_SOUNDS:
            s=pg.mixer.Sound(path.join(snd_folder,snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            self.player_hit_sounds.append(s)
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            self.zombie_hit_sounds.append(s)

    def new(self):
        #restart the game
        self.score=0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls=pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TileMap(path.join(self.map_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        #for row,tiles in enumerate(self.map.data):
        #    for col,tile in enumerate(tiles):
        #        if tile=='1':
        #            Wall(self,col,row)
        #        if tile=='P':
        #            self.player=Player(self,col,row)
        #        if tile=='M':
        #            Mob(self,col,row)
        for tile_obejct in self.map.tmxdata.objects:
            obj_center=vec(tile_obejct.x+tile_obejct.width/2,
                           tile_obejct.y+tile_obejct.height)
            if tile_obejct.name=='player':
                self.player=Player(self,obj_center.x,obj_center.y)
            if tile_obejct.name == 'wall':
                Obstacle(self, tile_obejct.x, tile_obejct.y,
                         tile_obejct.width, tile_obejct.height)
            if tile_obejct.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_obejct.name in ITEM_IMAGES.keys():
                Item(self,obj_center,tile_obejct.name)

        self.camera=Camera(self.map.width,self.map.height)
        self.draw_debug=False
        self.pause=False
        self.effects_sounds['level_start'].play()

    def run(self):
        #game loop
        self.playing=True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt=self.clock.tick(FPS)/1000
            self.events()
            if not self.pause:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        #game loop update
        self.all_sprites.update()
        self.camera.update(self.player)

        if len(self.mobs)==0:
            self.playing=False
        #player hit items
        hits=pg.sprite.spritecollide(self.player,self.items,False)
        for hit in hits:
            if hit.type=='health' and self.player.health<PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
            if hit.type=='shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon='shotgun'


        #mobs hit player
        hits=pg.sprite.spritecollide(self.player,self.mobs,False,collide_hit_rect)
        for hit in hits:
            if random()<0.7:
                choice(self.player_hit_sounds).play()
            self.player.health-=MOB_DAMAGE
            hit.vel=vec(0,0)
            if self.player.health<=0:
                self.playing=False
        if hits:
            self.player.hit()
            self.player.pos+=vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)
        #bullets hit mobs
        hits=pg.sprite.groupcollide(self.mobs,self.bullets,False,True)
        for mob in hits:#hits is a dict,hit is dict[mob]=[b1,b2,b3],that means hits[hit]=[b1,b2,b3]
            for bullet in hits[mob]:
                mob.health-=bullet.damage
            mob.vel=vec(0,0)

    def events(self):
        #game loop events
        for event in pg.event.get():
            if event.type==pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key==pg.K_ESCAPE:
                    self.quit()
                if event.key==pg.K_h:
                    self.draw_debug=not self.draw_debug
                if event.key==pg.K_p:
                    self.pause=not self.pause

    def draw_grid(self):
        for x in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(x,0),(x,HEIGHT))
        for y in range(0,WIDTH,TILESIZE):
            pg.draw.line(self.screen,LIGHTGREY,(0,y),(WIDTH,y))

    def draw(self):
        pg.display.set_caption('{:.2f}'.format(self.clock.get_fps()))
        #game loop draw
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))
        #self.draw_grid()
        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image,self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen,CYAN,self.camera.apply_rect(sprite.hit_rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect),1)
        # after drawing everything,flip the display
        #pg.draw.rect(self.screen,WHITE,self.player.hit_rect,2)
        #HUD functions
        self.draw_text('Zombies:%d'%len(self.mobs),
                self.hud_font,30,WHITE,WIDTH-10,10,align='ne')
        draw_player_health(self.screen,10,10,
                           self.player.health/PLAYER_HEALTH)
        if self.pause:
            self.screen.blit(self.dim_screen,(0,0))
            self.draw_text('PAUSED',self.title_font,105,RED,WIDTH/2,HEIGHT/2,align='center')
        pg.display.flip()

    def show_start_screen(self):
        #start screen
        self.screen.fill(BGCOLOR)
        self.draw_text(TITLE,self.title_font,100,WHITE,WIDTH//2,HEIGHT//4,align='center')
        self.draw_text('Arrows to move,Space to jump',self.hud_font,50,WHITE,WIDTH//2,HEIGHT//2,align='center')
        self.draw_text('Press a key to play',self.title_font,40,WHITE,WIDTH//2,HEIGHT*3//4,align='center')
        #self.draw_text('High Score:%d'%self.highscore, self.title_font,22, WHITE, WIDTH // 2, 15)
        self.draw_text('@Original Author:Patreon,Practice:Hue' ,self.hud_font, 20, WHITE, WIDTH // 2, HEIGHT-40,align='center')
        pg.display.flip()
        self.wait_for_key()

    def show_go_screen(self):
        #game over
        if not self.running:
            return
        #pg.mixer.music.load(path.join('snd', 'Yippee.ogg'))
        #pg.mixer.music.play(loops=-1)
        self.screen.fill(BGCOLOR)
        self.draw_text('GAME OVER',self.title_font, 100, RED, WIDTH // 2, HEIGHT // 4,align='center')
        self.draw_text('Score %d'%self.score,self.hud_font,50, WHITE, WIDTH // 2, HEIGHT // 2,align='center')
        self.draw_text('Press a key to play again',self.title_font,40, WHITE, WIDTH // 2, HEIGHT * 3 // 4,align='center')
        self.draw_text('@Original Author:Patreon,Practice:Hue',self.hud_font,20, WHITE, WIDTH // 2, HEIGHT - 40,align='center')
        #if self.score>self.highscore:
        #    self.highscore=self.score
        #    self.draw_text('NEW HIGH SCORE!',22,WHITE,WIDTH//2,HEIGHT//2+40)
        #    with open(path.join(self.dir,HS_FILE),'w') as f:
        #        f.write(str(self.highscore))
        #else:
        #    self.draw_text('High Score:%d' % self.highscore, 22, WHITE, WIDTH // 2, HEIGHT//2+40)
        pg.display.flip()
        self.wait_for_key()
        #pg.mixer.music.fadeout(500)

    def wait_for_key(self):
        pg.event.wait()#重新载入事件队列。没有这一句的话，上一局游戏中未执行的按键也会触发重新开始游戏
        waiting=True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type==pg.QUIT:
                    Waiting=False
                    self.quit()
                if event.type==pg.KEYUP:
                    waiting=False

    def draw_text(self,text,font_name,size,color,x,y,align='nw'):
        font=pg.font.Font(font_name,size)
        text_surface=font.render(text,True,color)
        text_rect=text_surface.get_rect()
        if align=='nw':
            text_rect.topleft=(x,y)
        if align=='ne':
            text_rect.topright=(x,y)
        if align=='sw':
            text_rect.bottomleft=(x,y)
        if align=='se':
            text_rect.bottomright=(x,y)
        if align=='n':
            text_rect.midtop=(x,y)
        if align=='s':
            text_rect.midbottom=(x,y)
        if align=='e':
            text_rect.midright=(x,y)
        if align=='w':
            text_rect.midleft=(x,y)
        if align=='center':
            text_rect.center=(x,y)
        self.screen.blit(text_surface,text_rect)

g=Game()
g.show_start_screen()
while g.running:
    g.new()
    g.run()
    g.show_go_screen()

pg.quit()