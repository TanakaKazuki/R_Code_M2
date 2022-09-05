#人手対応を取ったhandmatch/..の各節対応ページの出現用語と、
#テキストの各節の出現用語を比較

#handmatchの結果に対して、その節のテキスト内出現用語、そのページの出現用語、そのページでのみの出現用語、その節で人手マッチする用語
#を追加するイメージ



import re
import csv
from pathlib import Path
from lxml import html
import os
import MeCab
import pandas as pd
import ast
import datetime as dt

def main(list_sitename,input_name,ver,ver2,limit):
  text_name = input_name[0]
  #テキストデータ
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+ text_name +'_'+ ver +'.csv')
  #節番号のリスト
  setu_name = df['setu_num'].tolist()
  #print(setu_name)
  
  for i in range(len(list_sitename)):
    #その節のテキスト内出現用語用カラム
    column_text_yogo = []
    #ページ内出現用語用カラム
    column_page_yogo = []
    
    #そのページでのみ出現する用語用カラム
    column_page_only_yogo = []
    
    #そのページで出現するテキスト内出現用語用カラム
    column_page_text_yogo = []
    
    
  
    #人手マッチの結果
    df_handmatch = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/hand_match/senkei/'+ver2+'/handmatch_'+text_name+'_'+list_sitename[i]+'.csv')
    #全ページデータ
    df_page_data = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/For_all_removed/head_data_site/'+ver+'/removed_'+list_sitename[i]+'_header_term.csv')
  
    for j in range(len(df_handmatch['節番号'])):
      column_text_yogo.append(df['term_list'][df['setu_num']==df_handmatch['節番号'][j]].reset_index()['term_list'][0])

  
      page_URL = df_handmatch['マッチページURL'][j]
      #print(page_URL)
      column_page_yogo.append(df_page_data['タイトル・見出し出現用語'][df_page_data['URL']==page_URL].reset_index()['タイトル・見出し出現用語'][0])
      
      column_page_only_yogo.append(list(set(eval(df_page_data['タイトル・見出し出現用語'][df_page_data['URL']==page_URL].reset_index()['タイトル・見出し出現用語'][0]))-set(eval(df['term_list'][df['setu_num']==df_handmatch['節番号'][j]].reset_index()['term_list'][0]))))
      
      column_page_text_yogo.append(list(set(eval(df_page_data['タイトル・見出し出現用語'][df_page_data['URL']==page_URL].reset_index()['タイトル・見出し出現用語'][0]))&set(eval(df['term_list'][df['setu_num']==df_handmatch['節番号'][j]].reset_index()['term_list'][0]))))
    
    
    
    df_handmatch['テキスト内出現用語']= column_text_yogo
    df_handmatch['ページ内出現用語(ページ単位）'] = column_page_yogo
    df_handmatch['ページでのみ出現する用語（ページ単位）'] = column_page_only_yogo
    df_handmatch['ページで出現するテキスト内出現用語（ページ単位）'] = column_page_text_yogo
    
    
    #各節ごと
    #ページ内出現用語(節単位）
    column_all_setu_yogo = []
    #ページでのみ出現用語（節単位）
    column_all_page_only_yogo = []
    #ページで出現するテキスト内出現用語（節単位）
    column_all_page_text_yogo = []
    
    for j in range(len(df_handmatch['節番号'])):
      class_groupby = df_handmatch.groupby("節番号")
      class_groupby_setu = class_groupby.get_group(df_handmatch['節番号'][j]).reset_index()
      #print(class_groupby_setu)
      all_yogo = []
      all_only_yogo = []
      all_page_text_yogo = []
      for k in range(len(class_groupby_setu['節番号'])):
        all_yogo.extend(eval(class_groupby_setu['ページ内出現用語(ページ単位）'][k]))
        all_only_yogo.extend(class_groupby_setu['ページでのみ出現する用語（ページ単位）'][k])
        all_page_text_yogo.extend(class_groupby_setu['ページで出現するテキスト内出現用語（ページ単位）'][k])
      all_yogo = list(set(all_yogo))
      column_all_setu_yogo.append(all_yogo)
      
      all_only_yogo = list(set(all_only_yogo))
      column_all_page_only_yogo.append(all_only_yogo)
      
      all_page_text_yogo = list(set(all_page_text_yogo))
      column_all_page_text_yogo.append(all_page_text_yogo)
      
    
    df_handmatch['ページ内出現用語(節単位）'] = column_all_setu_yogo
    df_handmatch['ページでのみ出現する用語（節単位）'] = column_all_page_only_yogo
    df_handmatch['ページで出現するテキスト内出現用語（節単位）'] = column_all_page_text_yogo
    
    df_handmatch.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/yogo_bunpu/yogobunpu_'+list_sitename[i]+'.csv',sep=',',index=None)
    df_handmatch.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/yogo_bunpu/yogobunpu_'+list_sitename[i]+'.xlsx') 
  
  


if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #20サイト
    list_sitename = ['ai-trend.jp','atarimae.biz','jfor.net','k-san.link',
              'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net',
              'math-juken.com','math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
              'ramenhuhu.com','risalc.info','takun-physics.net',
              'univ-study.net',
              'www.geisya.or.jp','www.headboost.jp','www.momoyama-usagi']

    input_name = ['senkeidaisugaku']
    #教科書データのver
    ver = '0621'
    #人手マッチデータのver
    ver2 = '0715'
    limit = '1'


    main(list_sitename,input_name,ver,ver2,limit)
