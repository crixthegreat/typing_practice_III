#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/29 11:22:10

import sys
import os
import json
import cocos
from cocos.scene import Scene
from cocos.layer import Layer, ScrollingManager, ScrollableLayer
from cocos.director import director
from cocos.sprite import Sprite
from cocos.text import Label
import data.Const as Const
import pyglet
import materials 
import random
import data.highscore as highscore
import tool.file_test as file_test
from cocos.scenes import FadeTransition, FlipY3DTransition

"""Typing practice 3
It has the very same game mechanism of typing practice 2
I learned to use module package in the ty3, so the code get clear and clean significally
The game has:
    ty3.py -- main program
        /data
            __init__.py
            Const.py -- stores the game CONSTs
            highscore.py -- handler the highscore
            highscore.tp -- the highscore data file
        /materials
            __init__.py -- defines the labels, sprites, imgs to be used globally
            /background
                (not used in this game)
            /main_scr
                __init__.py -- defines the labels, sprites, imgs to be used in main game screen
            /menu
                __init__.py -- defines the labels, sprites, imgs to be used in menu layer
        /tool
            file_test.py -- to initialise the high score record file
        /pic
            alpha.png -- the alphabet image file
            bg.png -- the backgroud image file (800 x 600)
            start.png -- the 'start' image file
"""




class Game(object):
    """main game class
    """
    def __init__(self, level='Normal', player_name=Const.PLAYER_NAME):
        # The game has two level: 'Normal' and 'Hard'
        self.level = level
        self.time_passed = 0
        # The game has 3 status: STARTED, END, HIGHSCORE
        self.game_status = 'END'
        # prac_str is the random strings to be practiced
        self.prac_str = ''
        self.player_name = player_name
        # name_input_text is used to store the input text in 'HIGHSCORE' game mode
        self.name_input_text = ''


    def show_highscore(self, level):
        """display the highscore
        """
        _data = highscore.get_highscore()
        for _ in range(10):
            materials.labels['highscore_label' + str(_)].element.text = '{:>10}'.format(_data[_][1]) + materials.time_format(_data[_][0])


    def show_best_time(self, level):
        _best = 9999
        _data = highscore.get_highscore()
        #print (_data[0], _data[1], self.player_name)
        if level == 'Normal':
            for _ in _data[0:5]:
                if _[1] == self.player_name:
                    _best = _[0]
                    break
        elif level == 'Hard':
            for _ in _data[5:]:
                if _[1] == self.player_name:
                    _best = _[0]
                    break
        #print(_best)
        if _best == 9999:
            materials.main_scr.labels['best_time_label'].element.text = 'Your Best: N/A'
        else:
            materials.main_scr.labels['best_time_label'].element.text = 'Your Best: ' + materials.time_format(_best)
    

    
    def show_menu(self):
        materials.menu.show()
        materials.menu.labels['player_name_label'].element.text = self.player_name

    def show_game(self):
        """show the game screen and initial the game
        """
        self.prac_str = materials.main_scr.show(self.level)
        self.time_passed = 0
        self.game_status = 'STARTED'
        self.show_best_time(self.level)

    def show_highscore_name(self, _str):
        """display the name input by the player in HIGHSCORE game mode
        """
        _str = _str[:6]
        for _ in range(14, Const.MAX_LEN):
            materials.sprites['alpha_str' + str(_)].visible = False
        for _ in range(len(_str)):
            _str_index = ord(_str[_])
            if _str_index >= 97:
                _str_index -= 97
            else:
                _str_index -= 38
            materials.sprites['alpha_str' + str(_ + 14)].visible = True
            materials.sprites['alpha_str' + str(_ + 14)].image = materials.alpha_image[_str_index]
            materials.sprites['alpha_str' + str(_ + 14)].position = 100 + _ * 50, 300



class Menu_Screen(Layer):
    """The menu layer class, where the player starts the game 
    and change the game level
    """
    is_event_handler = True


    def __init__(self, game):

        super(Menu_Screen, self).__init__()
        
        self.game = game
        self.keys_pressed = set()

        self.image = materials.images['bg_img']

        for _, _label in materials.labels.items():
            self.add(_label)
        for _, _label in materials.menu.labels.items():
            self.add(_label)
        materials.menu.labels['level_label'].element.text = self.game.level
        materials.menu.labels['player_name_label'].element.text = self.game.player_name

        for _, _sprite in materials.sprites.items():
            self.add(_sprite)
        for _, _sprite in materials.menu.sprites.items():
            self.add(_sprite)

        materials.menu.sprites['t2_sprite'].scale = 1.5

        self.game.show_menu()
        self.game.show_highscore(self.game.level)


    def on_key_press(self, key, modifiers):
        
        self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        
        if 'ENTER' in key_names:
            #Start the game
            self.keys_pressed.clear()
            self.game.show_game()
            #self.game.show_highscore()
            director.replace(Scene(game_screen))
        # use the LEFT or RIGHT to change the game level
        elif 'LEFT' in key_names:
            if self.game.level != 'Normal':
                self.game.level = 'Normal'
                materials.menu.labels['level_label'].element.text = self.game.level
        elif 'RIGHT' in key_names:
            if self.game.level != 'Hard':
                self.game.level = 'Hard'
                materials.menu.labels['level_label'].element.text = self.game.level
        elif 'F12' in key_names:
            file_test.init_file()
            self.game.show_highscore(self.game.level)



    def on_key_release(self, key, modifiers):
        # release the key_pressed set
        # be careful that the layer changing when key is be pressed (but not released)
        if len(self.keys_pressed) > 0 and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    def draw(self):
        self.image.blit(0, 0)
    


class Main_Screen(ScrollableLayer):
    """The main game screen
    do a lot of key events
    """
    is_event_handler = True

    def __init__(self, game):

        super(Main_Screen, self).__init__()
        self.game = game
        self.keys_pressed = set()
        #self.image = materials.images['bg_img']
        self.tx = 1600
        self.ty = 1600
        self._move_dir = 0
        self._moved_time = 0
    
        #for _, _label in materials.labels.items():
        #    self.add(_label)
        for _, _label in materials.main_scr.labels.items():
            self.add(_label)
        for _, _sprite in materials.sprites.items():
            self.add(_sprite)
        # use the time interval event to calculate the time used
        self.schedule_interval(self.refresh_time, 0.1)


    def refresh_time(self, dt):
        # the 'dt' means the time passed after the last event occured
        if self.game.game_status == 'STARTED':
            self.game.time_passed += dt
            #print (self.game.time_passed)
            if int(self.game.time_passed * 10) % 100 == 0:
                self._move_dir = random.randrange(8)
            if self._move_dir == 0:
                self.ty -= 5
            elif self._move_dir == 1:
                self.ty -= 5
                self.tx += 5
            elif self._move_dir == 2:
                self.tx += 5
            elif self._move_dir == 3:
                self.tx += 5
                self.ty += 5
            elif self._move_dir == 4:
                self.ty += 5
            elif self._move_dir == 5:
                self.ty += 5
                self.tx -= 5
            elif self._move_dir == 6:
                self.tx -= 5
            elif self._move_dir == 7:
                self.ty -= 5
                self.tx -= 5
            else:
                print('wrong move dir')
                sys.exit()
          
            if self.tx < 0:
                self.tx = 0
            if self.ty < 0:
                self.ty =0
            if self.tx > 7200:
                self.tx = 7200
            if self.ty > 7400:
                self.ty = 7400


            materials.main_scr.labels['time_label'].element.text = 'Your time: ' + materials.time_format(self.game.time_passed) 
            #print(self.tx, self.ty)
            map_layer.set_view(self.tx, self.ty, 800, 600) 

    def on_key_press(self, key, modifiers):
        # use '_str' to judge whether the alphabet key is pressed, 
        # can also use the '.isalpha' method
        _str = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        # use a set(keys_pressed) to store all the keys pressed
        if key != 983547510784:
            self.keys_pressed.add(key)
        key_names = [pyglet.window.key.symbol_string(k) for k in self.keys_pressed]
        if 'SPACE' in key_names:
            # return to the menu(title) screen
            self.keys_pressed.clear()
            self.game.show_menu()
            self.game.show_highscore(self.game.level)
            director.replace(FlipY3DTransition(Scene(my_menu)))
        elif self.game.game_status == 'STARTED':
            _input_text = ''
            # handler the lower_case and upper_case input (with 'SHIFT' key)
            if len(key_names) > 1 and ('LSHIFT' in key_names) and (key_names[1] in _str or key_names[0] in _str):
                if key_names[0] in _str:
                    _input_text = key_names[0]
                else:
                    _input_text = key_names[1]
            elif len(key_names) == 1 and (key_names[0] in _str):
                _input_text = key_names[0].lower()
            # use the 'prac_str' to judge the input key
            if len(self.game.prac_str) > 0:
                # input the right key(char)
                if _input_text == self.game.prac_str[0]:
                    materials.sprites['alpha_str' + str(Const.MAX_LEN - len(self.game.prac_str))].image = materials.alpha_image[26]
                    # the leftmost char disappears
                    self.game.prac_str = self.game.prac_str[1:]
                    if len(self.game.prac_str) > 10:
                        # if the string is more than 10 chars long, the strings move left
                        for _ in range(Const.MAX_LEN):
                            _pos_x, _pos_y = materials.sprites['alpha_str' + str(_)].position
                            if _pos_x - 50 >= 0:
                                materials.sprites['alpha_str' + str(_)].position = _pos_x - 50, _pos_y
                            # or stay still
                            else:
                                materials.sprites['alpha_str' + str(_)].position = 0, _pos_y
                    elif len(self.game.prac_str) == 0:
                        # typing complete
                        # if the time is in top5
                        if self.game.time_passed <= highscore.top_highscore(self.game.level):
                            materials.show_alpha('HIGHSCORE NAME')
                            # now game changes into HIGHSCORE mode
                            self.game.name_input_text = self.game.player_name
                            self.game.game_status = 'HIGHSCORE'
                            self.game.show_highscore_name(self.game.player_name)
                            materials.main_scr.bg_music.stop()
                            materials.main_scr.highscore_music.play(-1)
                        # or just continue
                        else:
                            materials.show_alpha('continue')
                            self.game.game_status = 'END'
                else:
                    # wrong typing
                    action = cocos.actions.RotateBy(15, 0.03) + cocos.actions.RotateBy(-15, 0.03)
                    materials.sprites['alpha_str' + str(Const.MAX_LEN - len(self.game.prac_str))].do(action)
        # <<highscore mode>>
        # do key events when the game is in 'highscore' mode
        elif self.game.game_status == 'HIGHSCORE':
            if 'ENTER' in key_names:
                # confirm the name when get high score
                highscore.write_highscore(self.game.level, self.game.player_name, self.game.time_passed)
                materials.show_alpha('continue')
                self.game.show_best_time(self.game.level)
                self.game.game_status = 'END'
            # use BACKSPACE or DELETE key to delete chars
            elif 'BACKSPACE' in key_names or 'DELETE' in key_names:
                if len(self.game.name_input_text) > 0:
                    self.game.name_input_text = self.game.name_input_text[:len(self.game.name_input_text) - 1]
                    self.game.player_name = self.game.name_input_text
                    self.game.show_highscore_name(self.game.player_name)
            # input upper case chars (with SHIFT key)
            elif len(key_names) > 1 and ('LSHIFT' in key_names) and (key_names[1] in _str or key_names[0] in _str) and len(self.game.name_input_text) < 6:
                if key_names[0] in _str:
                    self.game.name_input_text += key_names[0]
                else:
                    self.game.name_input_text += key_names[1]
                self.game.player_name = self.game.name_input_text
                self.show_highscore_name(self.game.player_name)
            # input lower case chars
            elif len(key_names) == 1 and (key_names[0] in _str) and len(self.game.name_input_text) < 6:
                self.game.name_input_text += key_names[0].lower()
                self.game.player_name = self.game.name_input_text
                self.game.show_highscore_name(self.game.player_name)
        # play the game again
        elif self.game.game_status == 'END':
            if 'ENTER' in key_names:
                self.keys_pressed.clear()
                self.game.show_game()


    def on_key_release(self, key, modifiers):
        #print('main key:', self.keys_pressed)
        if len(self.keys_pressed) > 0 and key in self.keys_pressed:
            self.keys_pressed.remove(key)

    #def draw(self):
     #   self.image.blit(0, 0)



if __name__ == '__main__':

    # change the working dir to the exe temp dir for the pyinstaller 
    if getattr(sys, 'frozen', False):
        os.chdir(sys._MEIPASS)

    my_game =Game()
    game_screen = ScrollingManager()
    map_layer = cocos.tiles.load('./data/map.tmx')['start']
    my_main = Main_Screen(my_game)
    my_menu = Menu_Screen(my_game)

    game_screen.add(map_layer)
    game_screen.add(my_main)
    
    main_scene =Scene(my_menu)
    #print ('game initialised')
    cocos.director.director.run(main_scene)

    #print('game end')

