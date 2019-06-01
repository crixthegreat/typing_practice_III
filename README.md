# typing_practice_III

### It has the very same game mechanism of typing practice 2

### I learned to use module package in the ty3, so the code get clear and clean significally
------
### what's new in ty3
- title screen background fix
- added scrollable background in main game
- we have music now!
------
### The code structure:

    ty3.py -- main program
        /data
            __init__.py
            Const.py -- stores the game CONSTs
            highscore.py -- handling the highscore
            highscore.tp -- the highscore data file
            map.tmx -- the background tile map (with the layer 'start')
            map_tile.png -- the cell image of the tile map of the background
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
        /music
            title.ogg -- the title music
            main.ogg -- the main game music
            highscore -- the highscore mode music
