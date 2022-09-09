#手動マッチにおいて、
#マッチページ件数と、マッチページ数を調べる

import re
import csv
from pathlib import Path
from lxml import html
import os
import pandas as pd
import ast
import datetime as dt

from scipy.fft import skip_backend



def main(list_sitename,input_name,ver,limit):
  text_name = input_name[0]
  for i in range(len(list_sitename)):
    dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/hand_match'
    df = pd.read_csv( dir +'/' +ver+ '/' + 'handmatch_'+text_name+'_'+ list_sitename[i] +'.csv')
    
    
    print(list_sitename[i])
    #各サイトのマッチ件数
    print('マッチ件数')
    print(df[df['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==1]['マッチページURL'].count())
    
    
    #各サイトのマッチページ数
    print('マッチページ数')
    print(df[df['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==1]['マッチページURL'].nunique())
    
    
    #各サイトのマッチ件数（非対応）
    print('マッチ件数（非対応）')
    print(df[df['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==2]['マッチページURL'].count())
    
    #各サイトのマッチページ数（非対応）
    print('マッチページ数（非対応）')
    print(df[df['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==2]['マッチページURL'].nunique())


if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','ufcpp.net','univ-juken.com',
                    'univ-study.net','www.geisya.or.jp',
                    'www.momoyama-usagi.com','yorikuwa.com']
    
    
    #input_name = ['kosen_biseki1']
    input_name = ['bibunsekibungaku']
    
    ver = '0819'
    limit = '1'

    main(list_sitename,input_name,ver,limit)