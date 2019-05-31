#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/30 15:07:46

### to handle the high scores

import os
import data.Const as Const
import json

def get_highscore():
    """load the record file and return _data
    """
    #print(os.path.abspath(Const.HIGHSCORE_FILE))
    with open(Const.HIGHSCORE_FILE) as _file:
        try:
            _data = json.load(_file)
        except:
            print('open file failed')
        return _data


def top_highscore(level):
    """return the fifth high score from the record file
        used to judge TOP5 or not
    """
    with open(Const.HIGHSCORE_FILE) as _file:
        try:
            _data = json.load(_file)
        except:
            print('open file failed')
        data_normal = sorted(_data[0:5])
        data_hard = sorted(_data[5:])
        if level == 'Normal':
            return data_normal[4][0]
        elif level == 'Hard':
            return data_hard[4][0]
        else:
            print('wrong game level')


def write_highscore(level, name, highscore):
    """write the name and highscore into the record file
    """
    with open(Const.HIGHSCORE_FILE) as _file:
        try:
            _data = json.load(_file)
        except:
            print('open file failed')
        data_normal = sorted(_data[0:5])
        data_hard = sorted(_data[5:])
        if level == 'Normal':
            _ = data_normal
        elif level == 'Hard':
            _ = data_hard
        else:
            print('wrong game level')
        #trim the name below 10 chars
        _ += [[int(highscore), name[:10]]]
        # _  sorted
        _ = sorted(_)
        # _ trimed into 5 items)
        _ = _[:5]
        # combine the Normal top5 and the Hard top5
        if level == 'Normal':
            _data = _ + data_hard
        elif level == 'Hard':
            _data = data_normal + _
    with open(Const.HIGHSCORE_FILE, 'w') as _file:
        try:
            json.dump(_data, _file)
        except:
            print('write file failed')

