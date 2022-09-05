#各サイトのページ数の集計

import re
import csv
from pathlib import Path
from lxml import html
import os
import MeCab
import pandas as pd
import ast
import datetime as dt

def main(list_sitename,input_name):
  
  dir = make_derectory()
  
  for i in range(len(input_name)):
    input_file_name = input_name[i]
    column_sitename = []
    column_pagenum = []
    #精査前の各サイトの全ページ
    if input_file_name == 'correspondence_list':
      for j in range(len(list_sitename)):
        site_name = list_sitename[j]
        
        # if site_name == 'batapara.compp':
        #   df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_'+site_name+'_正規.csv',header=None)
        #   column_sitename.append(site_name)
        #   column_pagenum.append(len(df))        
        #else:
        df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_'+site_name+'.csv',header=None)
        column_sitename.append(site_name)
        column_pagenum.append(len(df))
      
      df_output = pd.DataFrame({'サイト名':column_sitename,'総ページ数':column_pagenum})
      df_output.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/all_page_num.csv',sep=',',index=None) 
      df_output.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/all_page_num.xlsx') 
    
      #精査後の各サイトの全ページ
    elif input_file_name == 'removed_correspondence_list':
      for j in range(len(list_sitename)):
        site_name = list_sitename[j]
        
        # if site_name == 'batapara.compp':
        #   df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_'+site_name+'_正規.csv',header=None)
        #   column_sitename.append(site_name)
        #   column_pagenum.append(len(df))        
        #else:
        input_dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data_removed/'
        #input_dir2 = 'removed_0511/'
        input_dir2 = 'removed_0526/'
        df = pd.read_csv(input_dir + input_dir2+'removed_correspondence_list_'+site_name+'.csv',header=None)
        column_sitename.append(site_name)
        column_pagenum.append(len(df))
      
      
      df_output = pd.DataFrame({'サイト名':column_sitename,'総ページ数':column_pagenum})
      df_output.to_csv(dir + '/removed_all_page_num.csv',sep=',',index=None) 
      df_output.to_excel(dir +'/removed_all_page_num.xlsx') 
    

#プログラム実行日のフォルダを作る
def make_derectory():
  dt_now = dt.datetime.now()
 
  #フォルダ名用にyyyymmddの文字列を取得する
  mmdd = dt_now.strftime('%m%d')
 
  #作成するフォルダ名を定義する
  directory_name = u'Aggregation_' + mmdd
 
  #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
  #current_directory = os.path.dirname(os.path.abspath(__file__))
 
  #作成のために確認するフォルダパスを作成する
  create_directory =  '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/' + directory_name
 
  #対象フォルダが存在しない場合
  if(not (os.path.exists(create_directory))):
 
    #フォルダを作成
    os.mkdir(create_directory)
  
  return create_directory

        
if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','tau.doshisha.ac.jp','ufcpp.net','univ-juken.com',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp',
                    'www.momoyama-usagi.com','www.sci.hokudai.ac.jp','yorikuwa.com']
    
    
    input_name = ['correspondence_list','removed_correspondence_list']
    # df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_yorikuwa.com.csv',header=None)
    # filename = df[0]
    # fileurl = df[1]
    # print(filename.head(50))
    # print(fileurl.head(50))

    main(list_sitename,input_name)
