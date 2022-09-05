#各サイトの全ページデータcorrespondence_listのURLを基に不要なデータを削除



from email.contentmanager import raw_data_manager
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
    if input_file_name == 'correspondence_list':
      
      #除去ページのURLを取得
      df_remove_page = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/Removal_Key/removal_key.csv',encoding="shift jis")
      #各サイトの全ページから除去ページを除去
      for j in range(len(list_sitename)):
        site_name = list_sitename[j]
        
        df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/correspondence_list_'+site_name+'.csv',header=None)
        
        #df内のURLを順に見ていき、removal_key.csvに該当するURLを除去
        # kaiseki ramenhuhu,ufcpp hokudai見れないから無理　tau見れないから無理
        # senkei ai-trend ramenhuhu
        #         mathwords規則ないから無理
        #         risalc 　規則ないから無理
        #         tau見れないから無理
        
        #df_copyから除去していき、reset_index
        df_copy = df.copy()
        print(site_name)
        print('df')
        print(len(df))
        #df_remove_page中のsite_nameの除去URLのリスト
        list_remove_page_URL = df_remove_page[df_remove_page['サイト名'] == site_name]['キー'].tolist()
        #print(list_remove_page_URL)
        #dfの各URLから不要なものを除去（ramenhuhu,ufcppに関しては、逆に必要なもののみ取得）
        
        #remenhuhu.com
        if site_name == 'ramenhuhu.com':
          list_match_page_URL = 'https://ramenhuhu.com/math'
          for k in range(len(df)):
            URL_str = df[1][k]
            if list_match_page_URL not in URL_str:
              df_copy = df_copy[df_copy[1]!= URL_str]
        
        elif site_name == 'ai-trend.jp':
          list_match_page_URL = ['https://ai-trend.jp/basic-study/linear-algebra','https://ai-trend.jp/basic-study/math-analysis']
          for k in range(len(df)):
            tag = df[0][k] 
            URL_str = df[1][k]
            #URL_strがist_match_page_URLの文字列を含むか否か
            tf = any(word in URL_str for word in list_match_page_URL )
            #print(tf)
            if tf == False:
              df_copy = df_copy[df_copy[1]!= URL_str]
          
        #その他のサイト  
        else:
          for k in range(len(df)):
            tag = df[0][k] 
            URL_str = df[1][k]
            for l in range(len(list_remove_page_URL)):
              if list_remove_page_URL[l] in URL_str:
                df_copy = df_copy[df_copy[1]!= URL_str]
                break
        print('df_copy')  
        print(len(df_copy))
        
  #0621追加############
        re_removed(dir,site_name,df_copy)
  ######################
        
    
#URLリストから除去済みのデータからさらに除外
def re_removed(dir,site_name,df_copy):
  
  df_copy =df_copy.reset_index()
  
  
  if  site_name == 'fromhimuka.com':
    df_copy_copy = df_copy.copy()
    list_remove_page_URL = 'math/'
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      if list_remove_page_URL in URL_str:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
    
    df_copy_copy = df_copy_copy.drop(columns='index')
    
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 

  elif site_name =='hooktail.sub.jp':
    df_copy_copy = df_copy.copy()
    #文字列を含むか
    list_remove_page_URL = ['analytic/','astronomy/','vectoranalysis/','physFormula/']
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      #URL_strがist_match_page_URLの文字列を含むか否か
      tf = any(word in URL_str for word  in list_remove_page_URL )
      #print(tf)
      if tf == True:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
    
  
    #URLの末尾が/かどうか
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      #URLの末尾を正規表現で確認
      pattern =  re.compile(r'/$')
      if bool(pattern.search(URL_str)):
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
    
    df_copy_copy = df_copy_copy.drop(columns='index')
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
        
  
  elif site_name =='w3e.kanazawa-it.ac.jp':
    df_copy_copy = df_copy.copy()
    list_remove_page_URL = 'index.html'
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      if list_remove_page_URL  in URL_str:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
    
    df_copy_copy = df_copy_copy.drop(columns='index')
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
    
  elif site_name == 'www.geisya.or.jp':
    df_copy_copy = df_copy.copy()
    #文字列を含むか
    list_remove_page_URL = ['maxima','mobile']
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      #URL_strがist_match_page_URLの文字列を含むか否か
      tf = any(word in URL_str for word in list_remove_page_URL )
      #print(tf)
      if tf == True:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
    
    df_copy_copy = df_copy_copy.drop(columns='index')
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
    
  elif site_name == 'www.momoyama-usagi.com':
    df_copy_copy = df_copy.copy()
    #文字列を含むか(math/2bを削除し、math-2bを残したい)
    list_remove_page_URL = ['math/','info/','2019/']
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      #URL_strがist_match_page_URLの文字列を含むか否か
      tf = any(word in URL_str for word in list_remove_page_URL )
      #print(tf)
      if tf == True:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
     
    df_copy_copy = df_copy_copy.drop(columns='index')   
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
    
  elif site_name == 'yorikuwa.com':
    df_copy_copy = df_copy.copy()
    list_remove_page_URL = '/2/'
    for k in range(len(df_copy)):
      URL_str = df_copy[1][k]
      if list_remove_page_URL in URL_str:
        df_copy_copy = df_copy_copy[df_copy_copy[1]!= URL_str]
        
    df_copy_copy = df_copy_copy.drop(columns='index')    
    df_copy_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
    
  
  
  
  else:
    df_copy = df_copy.drop(columns='index')
    df_copy.to_csv(dir +'/removed_correspondence_list_'+site_name+'.csv',sep=',',header=False,index=None) 
    df_copy.to_excel(dir +'/removed_correspondence_list_'+site_name+'.xlsx') 
    



#プログラム実行日のフォルダを作る
def make_derectory():
  dt_now = dt.datetime.now()
 
  #フォルダ名用にyyyymmddの文字列を取得する
  mmdd = dt_now.strftime('%m%d')
 
  #作成するフォルダ名を定義する
  directory_name = u'removed_' + mmdd
 
  #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
  #current_directory = os.path.dirname(os.path.abspath(__file__))
 
  #作成のために確認するフォルダパスを作成する
  create_directory =  '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data_removed/' + directory_name
 
  #対象フォルダが存在しない場合
  if(not (os.path.exists(create_directory))):
 
    #フォルダを作成
    os.mkdir(create_directory)
  
  return create_directory


if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    
    list_sitename = ['ai-trend.jp','atarimae.biz','jfor.net','k-san.link',
                 'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net',
                 'math-juken.com','math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
                 'ramenhuhu.com','risalc.info','takun-physics.net',
                 'tau.doshisha.ac.jp','univ-study.net','w3e.kanazawa-it.ac.jp',
                 'www.geisya.or.jp','www.headboost.jp','www.momoyama-usagi']
    
    input_name = ['correspondence_list']
    
    main(list_sitename,input_name)
  