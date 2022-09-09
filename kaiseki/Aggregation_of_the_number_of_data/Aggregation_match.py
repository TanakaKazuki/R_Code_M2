#テキストとのマッチ結果から、各節ごとのマッチページ数を集計

#


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
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+ text_name +'_'+ ver +'.csv')
  #節番号のリスト
  setu_name = df['setu_num'].tolist()
  print(setu_name)
  
  #出力データフレームのカラム名
  columns_name = ['節番号']
  columns_name.extend(list_sitename) 
  print(columns_name)
  
  #各カラムのデータ
  column_num = []
  setu_name_str = [str(n) for n in setu_name]
  column_num.append(setu_name_str) #節番号
                              #各節番号、各サイトのマッチページ数（2次元）
  
  #フィルタリング前後
  for i in range(len(input_name)):
    #自動マッチング結果の集計
    #全サイト
    match_num = []
    for j in range(len(list_sitename)):
      match_setu_num = []
      site_name = list_sitename[j]
      
      #各節
      for k in range(len(setu_name)):
        dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/text_match/'
        df_match = pd.read_csv(dir+'/'+text_name+'/'+ver+'/'+input_name[i]+'_'+site_name+'_'+limit+'_'+ver+'.csv')
        #df_setu_match = df_match[df_match['節番号']==setu_name[k]]
        if setu_name[k] in df_match.values:
          # print(setu_name[k])
          # print(df_match['節番号'].value_counts()[setu_name[k]])
          match_setu_num.append(df_match['節番号'].value_counts()[setu_name[k]])
        else:
          # print(setu_name[k])
          # print(0)
          match_setu_num.append(0)
      print(match_setu_num)
      column_num.append(match_setu_num)
    
    df = pd.DataFrame(column_num)
    df = df.T
    df.columns = columns_name
    print(df)
    
    
    
    dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/Aggregation_'+ver
    df.to_csv(dir + '/' + 'Aggregation_match_'+input_name[i]+'_'+ver+'_'+limit+'.csv',index=None) 
    df.to_excel(dir + '/' + 'Aggregation_match_'+input_name[i]+'_'+ver+'_'+limit+'.xlsx') 
    
####0527追加##########
  #手動マッチング結果の集計
  #全サイト
  #tau_doshisha,hokudaiは手動マッチなしのため飛ばす
  
  text_name = input_name[0]
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+ text_name +'_'+ ver +'.csv')
  #節番号のリスト
  setu_name = df['setu_num'].tolist()
  print(setu_name)
  
  #出力データフレームのカラム名
  columns_name = ['節番号']
  columns_name.extend(list_sitename) 
  print(columns_name)
  
  #各カラムのデータ
  column_num = []
  setu_name_str = [str(n) for n in setu_name]
  column_num.append(setu_name_str) #節番号
                              #各節番号、各サイトのマッチページ数（2次元）
  
  skip_sitename = ['tau.doshisha.ac.jp','www.sci.hokudai.ac.jp']
  
  match_num = []
  for j in range(len(list_sitename)):
    match_setu_num = []
    site_name = list_sitename[j]
    #tau_doshisha,hokudaiは手動マッチなしのため飛ばす
    if site_name not in skip_sitename:
      #各節
      for k in range(len(setu_name)):
        
        ver2 = '0819'
        
        dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/hand_match'
        df_match = pd.read_csv(dir+'/'+ver2+'/'+'handmatch_'+input_name[i]+'_'+site_name+'.csv')
        #df_setu_match = df_match[df_match['節番号']==setu_name[k]]
        if setu_name[k] in df_match[df_match['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==1].values:
          # print(setu_name[k])
          # print(df_match['節番号'].value_counts()[setu_name[k]])
          #match_setu_num.append(df_match['節番号'].value_counts()[setu_name[k]])
          print(site_name)
          match_setu_num.append(df_match[df_match['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==1]['節番号'].value_counts()[setu_name[k]])
        else:
          # print(setu_name[k])
          # print(0)
          match_setu_num.append(0)
      print(match_setu_num)
      column_num.append(match_setu_num)
    
    #skipサイトは-を代入しておく
    else:
      for k in range(len(setu_name)):
        match_setu_num.append('-')
      column_num.append(match_setu_num)
      
  
  df = pd.DataFrame(column_num)
  df = df.T
  df.columns = columns_name
  print(df)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/Aggregation_'+ver
  df.to_csv(dir + '/' + 'Aggregation_handmatch_'+input_name[i]+'_'+ver+'.csv',index=None) 
  df.to_excel(dir + '/' + 'Aggregation_handmatch_'+input_name[i]+'_'+ver+'.xlsx') 
      
        
if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','tau.doshisha.ac.jp','ufcpp.net','univ-juken.com',
                    'univ-study.net','www.geisya.or.jp',
                    'www.momoyama-usagi.com','www.sci.hokudai.ac.jp','yorikuwa.com']
    
    
    #input_name = ['kosen_biseki1']
    input_name = ['bibunsekibungaku']
    
    ver = '0819'
    limit = '2'

    main(list_sitename,input_name,ver,limit)