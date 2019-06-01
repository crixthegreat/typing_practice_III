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

images = {}

"""
time_label & best_time_label : as the name says
"""
labels = dict(time_label=cocos.text.Label('00:00', 
    font_size=16,font_name='Verdana', 
    bold=False,color=Const.DEFAULT_COLOR, x=165, y=15), 
    best_time_label=cocos.text.Label('99:59', 
        font_size=16,font_name='Verdana', 
        bold=False,color=Const.DEFAULT_COLOR, x=555, y=15))

sprites = {}

bg_music = materials.Audio(Const.BG_MUSIC_FILE)
highscore_music = materials.Audio(Const.HIGHSCORE_MUSIC_FILE)

def show(level):
    """to display menu screen
    """
    # generate a string to be practiced
    _str = []
    if level == 'Normal':
        #print('Normal game started')
        for _ in range(Const.MAX_LEN):
            _str.append(chr(random.randint(97, 122))) 
        random.shuffle(_str)
        _str = ''.join(_str)
    elif level == 'Hard':
        #print('Hard game started')
        for _ in range(26):
            _str.append(chr(97 + _))
            _str.append(chr(65 + _))
        random.shuffle(_str)
        _str = _str[:Const.MAX_LEN]
        _str = ''.join(_str)
    else:
        print('unknown game level')
        sys.exit()
    #print('the _str is:', _str)
    materials.show_alpha(_str, 100, 400)
    materials.main_scr.labels['time_label'].element.text = ' 0: 0'
    materials.menu.bg_music.stop()
    materials.main_scr.highscore_music.stop()
    bg_music.play(-1)
    return _str
    
