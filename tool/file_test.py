#python code env
#-*-coding:utf-8-*-
#Code by Crix @ crixthegreat@gmail.com
#https://github.com/crixthegreat/
#codetime: 2019/5/5 10:54:41

import data.Const as Const
import json

def init_file():

    data = [(1000, 'crix'), (380, 'crix'), (200, 'jenny'), 
            (230, 'crix'), (170, 'jenny'), 
            (3000, 'crix'), (1500, 'judy'), (700, 'jenny'),
            (80, 'crix'),(99, 'jenny')
            ]
    data_normal = sorted(data[0:5])
    data_hard = sorted(data[5:])

    data = data_normal + data_hard

    with open(Const.HIGHSCORE_FILE, 'w') as _file:
        try:
            json.dump(data, _file)
        except:
            print('write file failed')


if __name__ == '__main__':
    init_file()

