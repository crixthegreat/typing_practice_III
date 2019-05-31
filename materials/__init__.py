#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/28 17:03:36
import os
import data.Const as Const
import pyglet
import cocos
import random
from cocos.audio.pygame.mixer import Sound
from cocos.audio.pygame import mixer

"""materials define all the images, labels, sprites
and also define the methods handling them
"""
class Audio(Sound):
    """The standard class for Audio
    """
    def __ini__(self, file_name):
        super(Audio, self).__init__(file_name)



def time_format(t):
    _ = '{:>2}:{:>2}'.format(str(int(t // 60)), str(int(t % 60))) 
    return _


def gen_anime_sprite(img, grid_x, grid_y, delay, loop, pos_x, pos_y):

    _image = pyglet.image.load(img)
    _anime = pyglet.image.ImageGrid(_image, grid_x, grid_y)
    _seq = pyglet.image.Animation.from_image_sequence(_anime, delay, loop)
    return cocos.sprite.Sprite(_seq, position=(pos_x, pos_y))


def show_alpha(_str, pos_x=100, pos_y=400):
    """The KEY method of this game
    to display a string 
    """

    if len(_str) > Const.MAX_LEN:
        _str = _str[:Const.MAX_LEN]
    #print('show alpha:', _str)

    for _ in range(Const.MAX_LEN):
        sprites['alpha_str' + str(_)].position = 0, 0

    for _ in range(len(_str)):
        if _str[_] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
            _str_index = ord(_str[_])
            if _str_index >= 97:
                _str_index -= 97
            else:
                _str_index -= 38
        else:
            _str_index = 26

        sprites['alpha_str' + str(_)].visible = True
        sprites['alpha_str' + str(_)].image = alpha_image[_str_index]
        sprites['alpha_str' + str(_)].position = pos_x + _ * 50, pos_y
        sprites['alpha_str' + str(_)].scale = random.randrange(8, 20) / 10
        sprites['alpha_str' + str(_)].rotation = random.randrange(-30, 30)

mixer.init()
cocos.director.director.init(width=800, height=600, caption=Const.GAME_TITLE)

bg_file = os.path.abspath(Const.BACKGROUND_IMG_FILE)
bg_img=pyglet.image.load(bg_file) 

#load the alphabet to alpha_image
alpha_image = []
alpha_image=pyglet.image.ImageGrid(pyglet.image.load('./pic/alpha.png'), 2, 27)


images = {'alpha_image':alpha_image, 'bg_img':bg_img}

labels = {}
for _ in range(5):
    #print('normal', _)
    labels['highscore_label' + str(_)] = cocos.text.Label('',font_size=16, \
            font_name='Verdana', 
            bold=False, 
            color=Const.DEFAULT_COLOR, x=200, y=110 - (_ * 25))

for _ in range(5):
    #print('hard', _)
    labels['highscore_label' + str(_ + 5)] = cocos.text.Label('',font_size=16, \
            font_name='Verdana', 
            bold=False, 
            color=Const.DEFAULT_COLOR, 
            x=430, y=110 - (_ * 25))


sprites = {'alpha_str' + str(_):cocos.sprite.Sprite(alpha_image[_], position=(0, 0)) for _ in range(Const.MAX_LEN)}


import materials.menu
import materials.main_scr

