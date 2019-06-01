#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
import os
import data.Const as Const
import pyglet
import cocos
import materials
import random


images = {'t2_anime':[materials.alpha_image[26], materials.alpha_image[53]]}

labels = dict(player_name_label=cocos.text.Label('N/A', 
    font_size=16,font_name='Verdana', 
    bold=False,color=Const.DEFAULT_COLOR, x=165, y=205),
    level_label=cocos.text.Label('', font_size=20,
        font_name='Verdana', bold=True,
        color=Const.HIGHLIGHT_COLOR, x=355, y=240))


t2_seq = pyglet.image.Animation.from_image_sequence(images['t2_anime'], 0.5, True)

sprites = {'start_sprite':materials.gen_anime_sprite('./pic/start.png', 2, 1, 0.5, True, 400, 280),
        't2_sprite':cocos.sprite.Sprite(t2_seq, position=(650, 400))}

bg_music = materials.Audio(Const.TITLE_MUSIC_FILE)

def show():
    materials.show_alpha('typingpractice', 100, 450)
    for _ in range(6):
        materials.sprites['alpha_str' + str(_)].position = 280 + _ * 50, 500
        materials.sprites['alpha_str' + str(_)].scale = random.randrange(8, 20) / 10
        materials.sprites['alpha_str' + str(_)].rotation = random.randrange(-30, 30)
    for _ in range(8):
        materials.sprites['alpha_str' + str(_ + 6)].position = 230 + _ * 50, 400 
        materials.sprites['alpha_str' + str(_ + 6)].scale = random.randrange(8, 20) / 10
        materials.sprites['alpha_str' + str(_ + 6)].rotation = random.randrange(-30, 30)
    materials.main_scr.bg_music.stop()
    materials.main_scr.highscore_music.stop()
    bg_music.play(-1)

