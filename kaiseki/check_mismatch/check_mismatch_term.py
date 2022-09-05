#textbook/..のテキスト内出現用語と
#eval/eval_handmatch_kosen_biseki1_....csv　手動マッチングの各節自動マッチ状況＋マッチ用語
#をもとに、
#テキスト内出現用語の内、実際のマッチに結びついていないものを調査

#main()
  #全サイトで
  #・正しいマッチ結果でのマッチ語で出現した用語
  #・正しいマッチ結果での1用語のみのマッチ語で出現した用語


  #各サイトで
  #・正しいマッチ結果でのマッチ語で出現した用語
  #・正しいマッチ結果での1用語のみのマッチ語で出現した用語

#count_match()
  #1用語のみでマッチしている場合の
  #誤マッチを発生させることが多い用語と正マッチを発生させることが多い用語

from cgitb import text
import re
import csv
from pathlib import Path

import os
from typing import Counter
import pandas as pd
import ast
import datetime as dt
import collections


def main(list_sitename,input_name,ver,limit):
  text_name = input_name[0]
  #テキスト内出現用語
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+ text_name +'_'+ ver +'.csv')
  #csv化によりリストが文字列になっているためリストに変換
  df['term_list']=[ast.literal_eval(d) for d in df['term_list']]
  textbook_term_list = []
  for i in range(len(df['term_list'])):
    textbook_term_list.extend(df['term_list'][i])
  #テキスト内出現用語の重複削除
  textbook_term_list = list(set(textbook_term_list)) 
  
  
  #手動マッチングのうち、自動マッチングできているページのマッチ用語
  for j in range(len(input_name)):
    text_name = input_name[j]
    
    #全サイトの正解マッチのいずれかでマッチした用語
    match_allsite_term_list = []
    #全サイトの正解マッチのいずれかで、1用語のみでマッチした用語
    match_allsite_a_term_list = []
    
    
    #各サイトの
    for k in range(len(list_sitename)):
      #１サイト中の正解マッチでマッチした用語
      match_site_term_list = []
      #１サイト中の正解マッチで1用語のみでマッチした用語
      match_site_a_term_list = []
      
      
      sitename = list_sitename[k]
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/eval'
      df_match = pd.read_csv(dir+'/'+ver+'/'+'eval_handmatch_'+text_name+'_'+sitename+'_'+limit+'.csv')
      
      for l in range(len(df_match['マッチ用語'])):
        if df_match['自動マッチ結果'][l] == '○':
          
          df_match['マッチ用語'][l] = eval(df_match['マッチ用語'][l])   
          match_allsite_term_list.extend(df_match['マッチ用語'][l])
          match_site_term_list.extend(df_match['マッチ用語'][l])
          
          #1用語のみでマッチしているか
          if len(df_match['マッチ用語'][l]) == 1:
            match_allsite_a_term_list.extend(df_match['マッチ用語'][l])
            match_site_a_term_list.extend(df_match['マッチ用語'][l])
          
      match_site_term_list = list(set(match_site_term_list))
      match_site_a_term_list = list(set(match_site_a_term_list))
      
      
      print('サイト名')
      print(sitename)
      print('このサイトで正しくマッチしたページでマッチした用語')        
      print(match_site_term_list)
      print('このサイトで正しくマッチしたページで1用語のみでマッチした用語')
      print(match_site_a_term_list)
      
      
      
      
      
      
      
      
    match_allsite_term_list = list(set(match_allsite_term_list))
    match_allsite_a_term_list = list(set(match_allsite_a_term_list))
    
    print('全サイトのどこかで正しくマッチしたページでマッチした用語')
    print(match_allsite_term_list)
    print('全サイトのどこかで正しくマッチしたページで1用語のみでマッチした用語')
    print(match_allsite_a_term_list)
    
    #全サイトを通して、一度も正しいマッチ結果のマッチ用語として出現しなかった語
    mismatch_term_list = [i for i in textbook_term_list if i not in match_allsite_term_list]
    print('一度も正しいマッチ結果に寄与しなかった用語')
    print(mismatch_term_list)
    
    #全サイトを通して、一度も正しいマッチ結果のマッチ用語(1用語のみ)として出現しなかった語
    mismatch_term_list = [i for i in textbook_term_list if i not in match_allsite_a_term_list]
    print('一度も正しいマッチ結果に、1文字のみで寄与しなかった用語')
    print(mismatch_term_list)
    
  
  count_match(list_sitename,input_name,ver,limit)


#1用語のみでマッチしている場合の
#正しいマッチ回数と誤マッチ回数を調査
#（目的）
  #１用語でのみマッチの誤マッチが多い
  #しかし、閾値＝２にするとカバー率が下がる
  #１用語のみのマッチで通すべき、弾くべき用語を調査する
def count_match(list_sitename,input_name,ver,limit):
  for i in range(len(input_name)):
    text_name = input_name[i]
    
    #以下のリストの各用語の出現回数を調べる
      #正マッチ（１語のみでの）用語リスト
    match_term_list = []
      #誤マッチ（１語のみでの）用語リスト
    mismatch_term_list = []
    
    
    
    
    for j in range(len(list_sitename)):
      #以下のリストの各用語の出現回数を調べる
      #正マッチ（１語のみでの）用語リスト
      match_term_list_site = []
      #誤マッチ（１語のみでの）用語リスト
      mismatch_term_list_site = []
      
      
      
      sitename = list_sitename[j]
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/eval'
      df_handmatch = pd.read_csv(dir+'/'+ver+'/'+'eval_handmatch_'+text_name+'_'+sitename+'_'+limit+'.csv')
      
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/text_match/'+text_name
      df_match = pd.read_csv(dir+'/'+ver+'/'+text_name+'_'+sitename+'_'+limit+'_'+ver+'.csv')
      #csv化によりリストが文字列になっているためリストに変換
      df_match['マッチ用語']=[ast.literal_eval(d) for d in df_match['マッチ用語']]
      
      
      #自動マッチ結果を上から見ていき、hand_match結果にあるページならmatch_term_list、そうでないならmismatch_term_listにマッチ用語を追加
      for k in range(len(df_match['節番号'])):
        #手動マッチ結果の中に、該当節番号があり、かつ、該当URLがあり、マッチ用語数=1なら
        if df_match['節番号'][k] in df_handmatch.values:
          if df_match['マッチページURL'][k] in df_handmatch[df_handmatch['節番号']==df_match['節番号'][k]].values:
            if len(df_match['マッチ用語'][k]) ==1:
              match_term_list.extend(df_match['マッチ用語'][k])
              match_term_list_site.extend(df_match['マッチ用語'][k])
          else:
            if len(df_match['マッチ用語'][k]) ==1:
              mismatch_term_list.extend(df_match['マッチ用語'][k])
              mismatch_term_list_site.extend(df_match['マッチ用語'][k])
        else:
          if len(df_match['マッチ用語'][k]) ==1:
            mismatch_term_list.extend(df_match['マッチ用語'][k])
            mismatch_term_list_site.extend(df_match['マッチ用語'][k])
      
      #各サイトでの
      #１用語のみで正マッチ・誤マッチした用語とその回数を出力
      counter_match = Counter(match_term_list_site)
      counter_match = counter_match.most_common()
      #print(counter_match)
      print(func_list_tuple(counter_match))
      a,b = func_list_tuple(counter_match)
      df = pd.DataFrame((zip(a, b)), columns = ['1用語のみで正マッチした語', '正マッチ回数'])
      print(df)
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/check_mismatch'
      df.to_csv(dir + '/' + ver + '/'+ sitename +'_match_a_term.csv',sep=',',index=None) 
      df.to_excel(dir + '/' + ver + '/'+ sitename+ '_match_a_term.xlsx') 
      
      counter_mismatch = Counter(mismatch_term_list_site)
      counter_mismatch = counter_mismatch.most_common()
      #print(counter_mimatch)
      print(func_list_tuple(counter_mismatch))
      c,d = func_list_tuple(counter_mismatch)
      df = pd.DataFrame((zip(c, d)), columns = ['1用語のみで誤マッチした語', '誤マッチ回数'])
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/check_mismatch'
      df.to_csv(dir + '/' + ver + '/'+ sitename + '_mismatch_a_term.csv',sep=',',index=None) 
      df.to_excel(dir + '/' + ver + '/'+ sitename + '_mismatch_a_term.xlsx') 
      
    
    #全サイトでの
    #１用語のみで正マッチ・誤マッチした用語とその回数を出力
    print('match_term_list')
    # print(match_term_list)
    c_match = collections.Counter(match_term_list)
    print(c_match)
    counter_match = Counter(match_term_list)
    counter_match = counter_match.most_common()
    #print(counter_match)
    print(func_list_tuple(counter_match))
    a,b = func_list_tuple(counter_match)
    df = pd.DataFrame((zip(a, b)), columns = ['1用語のみで正マッチした語', '正マッチ回数'])
    print(df)
    dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/check_mismatch'
    df.to_csv(dir + '/' + ver + '/'+ 'all_site_match_a_term.csv',sep=',',index=None) 
    df.to_excel(dir + '/' + ver + '/'+ 'all_site_match_a_term.xlsx') 
    
    print('mismatch_term_list')
    #print(mismatch_term_list)
    c_mismatch = collections.Counter(mismatch_term_list)
    print(c_mismatch)
    counter_mismatch = Counter(mismatch_term_list)
    counter_mismatch = counter_mismatch.most_common()
    #print(counter_mimatch)
    print(func_list_tuple(counter_mismatch))
    c,d = func_list_tuple(counter_mismatch)
    df = pd.DataFrame((zip(c, d)), columns = ['1用語のみで誤マッチした語', '誤マッチ回数'])
    dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/check_mismatch'
    df.to_csv(dir + '/' + ver + '/'+ 'all_site_mismatch_a_term.csv',sep=',',index=None) 
    df.to_excel(dir + '/' + ver + '/'+ 'all_site_mismatch_a_term.xlsx') 
    
    
            
      
#タプルのリストから、列を抽出
#[('a', 1), ('b', 2), ('c', 3), ('d', 4)] => (['a', 'b', 'c', 'd'], [1, 2, 3, 4])
def func_list_tuple(samples):
  return [a for a, b in samples], [b for a, b in samples]
      
      
  


if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    
    #,'tau.doshisha.ac.jp','www.sci.hokudai.ac.jp'も閲覧不可のため除いた
    
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','ufcpp.net','univ-juken.com',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp',
                    'www.momoyama-usagi.com','yorikuwa.com']
    
    
    input_name = ['kosen_biseki1']
    
    ver = '0526'
    limit = '1'

    main(list_sitename,input_name,ver,limit)