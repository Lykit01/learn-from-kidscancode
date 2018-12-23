# -*- coding:utf-8 -*-
#!/usr/bin/env python
import pygame as pg
vec=pg.math.Vector2
#game options
TITLE='Tilemap Demo'
SIZE=WIDTH,HEIGHT=1024,768
FPS=60
FONT_NAME='arial'
HS_FILE='highscore.txt'
SPRITESHEET='spritesheet_jumper.png'

TILESIZE=64
GRIDWIDTH=WIDTH/TILESIZE
GRIDHEIGHT=HEIGHT/TILESIZE

WALL_IMG='tile_42.png'


#player property
PLAYER_HEALTH=100
PLAYER_SPEED=250
PLAYER_ROT_SPEED=250
PLAYER_IMG='manBlue_pistol.png'
PLAYER_HIT_RECT=pg.Rect(0,0,35,35)
BARREL_OFFSET=vec(30,10)

#Gun settings
WEAPONS={}
WEAPONS['pistol']={'bullet_speed':500,'bullet_lifetime':1000,
            'rate':300,'kickback':200,'spread':5,'damage':10,
                  'bullet_size':'lg','bullet_count':1}
WEAPONS['shotgun']={'bullet_speed':400,'bullet_lifetime':500,
            'rate':1000,'kickback':300,'spread':20,'damage':5,
                  'bullet_size':'sm','bullet_count':12}
BULLET_IMG='bullet.png'

#Mob settings
MOB_HEALTH=100
MOB_DAMAGE=10
MOB_IMG='zoimbie1_hold.png'
MOB_SPEEDS=[150,100,200,250]
MOB_HIT_RECT=pg.Rect(0,0,30,30)
MOB_KNOCKBACK=20
AVOID_RADIUS=50
DETECT_RADIUS=400



#Effects
MUZZLE_FLASHES=['whitePuff15.png','whitePuff16.png',
                'whitePuff17.png','whitePuff18.png']
FLASH_DURATION=40
SPLAT='splat green.png'
DAMAGE_ALPHA=[i for i in range(0,255,25)]

#Layers
WALL_LAYER=1
ITEM_LAYER=1
PLAYER_LAYER=2
BULLET_LAYER=3
MOB_LAYER=2
EFFECTS_LAYER=4

#items
ITEM_IMAGES={'health':'health.png','shotgun':'obj_shotgun.png'}
HEALTH_PACK_AMOUNT=20
BOB_RANGE=20
BOB_SPEED=0.5

#colors
WHITE=(255,255,255)
BLACK=(0,0,0)
RED=(255,0,0)
GREEN=(0,255,0)
BLUE=(0,0,255)
YELLOW=(255,255,0)
LIGHTBLUE=(0,155,155)
DARKGREY=(40,40,40)
LIGHTGREY=(100,100,100)
CYAN=(0,255,255)
BROWN=(106,55,5)
BGCOLOR=BROWN

#sounds
BG_MUSIC='espionage.ogg'
PLAYER_HIT_SOUNDS=['pain/8.wav','pain/9.wav',
                   'pain/10.wav','pain/11.wav']
ZOMBIE_MOAN_SOUNDS=['brains2.wav','brains3.wav','zombie-roar-1.wav',
        'zombie-roar-2.wav','zombie-roar-3.wav','zombie-roar-5.wav',
        'zombie-roar-6.wav','zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS=['splat-15.wav']
WEAPON_SOUNDS={'pistol':['pistol.wav'],'shotgun':['shotgun.wav']}
WEAPON_SOUNDS_GUN=['sfx_weapon_singleshot2.wav']
EFFECTS_SOUNDS={'level_start':'level_start.wav',
                'health_up':'health_pack.wav',
                'gun_pickup':'gun_pickup.wav'}