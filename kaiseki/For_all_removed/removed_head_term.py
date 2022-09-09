#ページ見出し、タイトルから 
# all_vocab_kaisekiあるいは、senkei_1500_new内の用語を抽出
from cgitb import text
from distutils import text_file
import site
from turtle import title
import math
import pandas as pd
import numpy as np
import re
import csv
from pathlib import Path
from lxml import html
import os
import datetime as dt
import itertools
import shutil
def main(list_sitename,yogo_filename,ver,list_text_filename):
    """メイン関数"""
    #保存ディレクトリの生成
    make_derectory(list_sitename,ver)
    
    #用語集合の追記用ファイルの生成
    shutil.copy('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'.csv','/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'_'+ver+'.csv')
    
    #用語集合の読み込み　リスト化
    df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'_'+ver+'.csv')
    yogo_list = df[df['select'] != '×']['yogo'].tolist()
    #print(yogo_list)
    
    #テキストごとに出力
    for i in range(len(list_text_filename)):
      #テキスト名
      text_filename = list_text_filename[i]
      #テキスト内出現用語の読み込み　リスト化
      df_text = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+text_filename)
      text_yogo_list = []
      for setu in range(len(df_text['term'])):
        setu_term = df_text['term'][setu].split('/')
        text_yogo_list.append(setu_term)
      text_yogo_list = list(itertools.chain.from_iterable(text_yogo_list))
      text_yogo_list = list(set(text_yogo_list))
      #print(text_yogo_list)
      
      #テキストでしか出現しない用語を、1500語のcsvに追加
      #もし、テキストでしか出現しない用語があれば
      if len(list((set(text_yogo_list) ^ set(yogo_list)) & set(text_yogo_list))) > 0:
        yogo_list = add_term_csv(text_yogo_list,yogo_filename,ver)
      
      
      #テキストでしか出現しない用語がないかチェック
      #出力されなければ良い
      print('##########注意#############')
      print('用語集合に含まれないテキスト中用語')
      print(list((set(text_yogo_list) ^ set(yogo_list)) & set(text_yogo_list)))
      print('用語集合に含まれないテキスト中用語数')
      print(len(list((set(text_yogo_list) ^ set(yogo_list)) & set(text_yogo_list))))
      
      #サイトごとに
      for j in range(len(list_sitename)):
        site_name = list_sitename[j]
        dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data_removed/removed_0526/removed_correspondence_list_'
        df_html_data = pd.read_csv(dir+site_name+'.csv',header=None)
        id_list = df_html_data[0].tolist()
        
        column_id = []
        column_URL = []
        column_title = []
        column_title_head_term = []
        column_title_head_term_len = []
        column_title_term = []
        column_title_term_len = []
        column_head = []
        column_head_num = []
        column_head_term = []
        column_head_term_len = []
        
        
        #除去後の各ページを見ていく
        for k in range(len(id_list)):
          id = id_list[k]
          dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/head_data/'
          df_head_data = pd.read_csv(dir+site_name+'_'+'0526'+'/removed_head_'+id+'.csv')
          
          column_id.append(id)
          URL_index = df_html_data[df_html_data[0]==id][1]
          URL_str = URL_index.reset_index()[1][0] 
          column_URL.append(URL_str)
          
          
          
          #各ページの各タグテキストから、用語集合中の用語を抽出
          
          page_head_yogo = []
          page_head = []
          page_title_yogo = []
          
          if len(df_head_data['URL'])>0 and df_head_data['URL'][0] == 'title':
            title_ = df_head_data.query('URL == ["title"]')['タグ名'][0]
            checked_yogo = term_check(title_,yogo_list)
            page_title_yogo = checked_yogo
            column_title.append(title_ )
            column_title_term.append(checked_yogo)
            column_title_term_len.append(len(checked_yogo))
            
          else:
            title_ = ''
            column_title.append(title_ )
            column_title_term.append('')
            column_title_term_len.append(0)
            
            
          for l in range(len(df_head_data['URL'])):
            sentence = df_head_data['タグテキスト'][l]
            checked_yogo = term_check(sentence,yogo_list)
            page_head_yogo.append(checked_yogo)
            page_head.append(sentence)
           
              
            # if df_head_data['URL'][l]== 'title':
            #   sentence =  df_head_data['タグ名'][l]
            #   checked_yogo = term_check(sentence,yogo_list)
            #   page_title_yogo = checked_yogo
              
            #   column_title.append(sentence)
            #   column_title_term.append(checked_yogo)
            #   column_title_term_len.append(len(checked_yogo))
              
            # else:
            #   sentence = df_head_data['タグテキスト'][l]
            #   checked_yogo = term_check(sentence,yogo_list)
            #   page_head_yogo.append(checked_yogo)
            #   page_head.append(sentence)
          
          page_head_yogo = list(itertools.chain.from_iterable(page_head_yogo))
          #text_yogo_list = list(itertools.chain.from_iterable(text_yogo_list))
          page_yogo = list(set(page_title_yogo + page_head_yogo))
          column_title_head_term.append(page_yogo)
          column_title_head_term_len.append(len(page_yogo))
          column_head.append(page_head)
          column_head_num.append(len(page_head))
          column_head_term.append(page_head_yogo)
          column_head_term_len.append(len(page_head_yogo))
      
        df_output = pd.DataFrame({'id':column_id,'URL':column_URL,'タイトル':column_title,'タイトル・見出し出現用語':column_title_head_term,'タイトル・見出し出現用語数':column_title_head_term_len,'タイトル内単語':column_title_term,'タイトル内単語数':column_title_term_len,'見出し文':column_head,'見出し文数':column_head_num,'見出し内単語':column_head_term,'見出し内単語数':column_head_term_len})
        dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/head_data_site/'
        df_output.to_csv(dir+ver+'/removed_'+site_name+'_header_term.csv',sep=',')   
        df_output.to_excel(dir+ver+'/removed_'+site_name+'_header_term.xlsx')
  
    return

#用語集合に含まれないテキスト内出現用語を、用語集合に加えcsvファイルで出力
from csv import writer
def add_term_csv(text_yogo_list,yogo_filename,ver):
  
  #用語集合の読み込み　リスト化
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'_'+ver+'.csv')
  print(df)
  yogo_list = df[df['select'] != '×']['yogo'].tolist()
  only_text_yogo = list((set(text_yogo_list) ^ set(yogo_list)) & set(text_yogo_list))
  for i in range(len(only_text_yogo)):
    yogo = only_text_yogo[i]
    #df_append = pd.DataFrame([yogo,text_filename])
    #df = df.append(df_append)
    
    list_data = [yogo,yogo_filename]
    print(list_data)
  
    with open('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'_'+ver+'.csv', 'a', newline='') as f_object:  
      # Pass the CSV  file object to the writer() function
      #writer_object = writer(f_object)
      writer_object = csv.writer(f_object)
      # Result - a writer object
      # Pass the data in the list as an argument into the writerow() function
      writer_object.writerow(list_data)  
      # Close the file object
      f_object.close()
  
  
  
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/yogo/kaiseki/'+yogo_filename+'_'+ver+'.csv')
  
  # #テキストにしか出現しない用語追加verの用語集合に更新
  yogo_list = df[df['select'] != '×']['yogo'].tolist()
  
  
  
  
  
  return yogo_list
  

#文中から文集合中の用語を抽出する
def term_check(sentence,yogo_list):
  checked_yogo = []
  for term in range(len(yogo_list)):
    if pd.isnull(sentence) == False:
      if yogo_list[term] in sentence:
        checked_yogo.append(yogo_list[term])
  
  return checked_yogo
        
      
#プログラム実行日のフォルダを作る
def make_derectory(list_sitename,ver):
  dt_now = dt.datetime.now()
 
  #作成するフォルダ名を定義する
  #for i in range(len(list_sitename)):
    
    #directory_name = list_sitename[i]+'_'+ ver
    #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
  directory_name = ver
    #作成のために確認するフォルダパスを作成する
  create_directory =  '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/head_data_site/' + directory_name
    
    #対象フォルダが存在しない場合
  if(not (os.path.exists(create_directory))):
    
        #フォルダを作成
      os.mkdir(create_directory)
    
    

if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #path
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','tau.doshisha.ac.jp','ufcpp.net','univ-juken.com',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp',
                    'www.momoyama-usagi.com','www.sci.hokudai.ac.jp','yorikuwa.com']
    
    yogo_filename = 'all_vocab_kaiseki_tanaka'
    
    
    ver = '0819'
    
    #text_filename = ['kosen_biseki1_'+ver+'.csv']
    text_filename = ['bibunsekibungaku_'+ver+'.csv']


    main(list_sitename,yogo_filename,ver,text_filename)

