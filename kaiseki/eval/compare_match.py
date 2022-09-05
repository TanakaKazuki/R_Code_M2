#2022/05/26
#text_matchの結果をもとに、
#hand_matchの結果と、各節ごとにどの程度マッチしているか確認
import csv
from pathlib import Path
import os
from re import A, match
import site
import pandas as pd
import numpy as np
import datetime as dt


#####①出力想定（人手マッチの評価）#####
# 節番号　節名　マッチページ　　マッチページURL　補足 自動マッチ結果   マッチ用語
# 1.1   aa    aaaaaa    　　　aaaa          --    ○ 　　　　　　　aaaa


#####②出力想定（人手マッチのカバー率の一覧）#####
#サイト名　人手マッチページ組数　自動マッチ成功数　自動マッチ失敗数  自動マッチカバー率　自動マッチ総ページ組数    Precision　　 人手総ページ数（ページの種類）　　自動マッチ総ページ数（ページの種類）
# aaa        10                5             5               50%　　　　　　　　 50             　　　5/50　　　　　　　5                            30



def main(list_site,list_textname,limit,ver):
  
  for i in range(len(list_textname)):
    textname = list_textname[i]
    #出力想定②用
    column_sitename = []
    column_handmatch_num = []
    column_match_success_num = []
    column_match_failure_num = []
    column_match_cover_per = []
    column_match_all_num = []
    column_precison = []
    
    column_handmatch_kind = []
    column_match_kind = []
    
    for j in range(len(list_site)):
      sitename = list_site[j]
      
      column_sitename.append(sitename)
      
      #人手マッチング結果の読み込み
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/hand_match/'+'0616'
      df_handmatch_sub = pd.read_csv(dir+'/'+'handmatch_'+textname+'_'+sitename+'.csv')
      print(df_handmatch_sub)
      df_handmatch_sub = df_handmatch_sub[df_handmatch_sub['評価（1:節内記述と対応,2:節内に関する内容だが非対応）']==1]
      
      df_handmatch = df_handmatch_sub.reset_index()
      print(df_handmatch)
      #自動マッチング結果の読み込み
      dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/For_all_removed/text_match/kosen_biseki1'
      df_match = pd.read_csv(dir+'/0628/'+textname+'_'+sitename+'_'+limit+'_0628.csv')
      
      df_handmatch['自動マッチ結果'] = np.nan
      df_handmatch['マッチ用語'] = np.nan
      
      df_handmatch_eval = check_match(df_handmatch,df_match,textname,sitename)
      
      column_handmatch_num.append(len(df_handmatch_eval['節番号']))
      success_bool = (df_handmatch_eval['自動マッチ結果'] =='○')
      column_match_success_num.append(success_bool.sum())
      failure_bool = (df_handmatch_eval['自動マッチ結果'] =='×')
      column_match_failure_num.append(failure_bool.sum())
      
      cover_per = success_bool.sum()/len(df_handmatch_eval['節番号'])
      column_match_cover_per.append(cover_per)
      
      column_match_all_num.append(len(df_match['節番号']))
      
      precision = success_bool.sum() /len(df_match['節番号'])
      column_precison.append(precision)
      
      #手動マッチのページ種類
      handmatch_kind = len(df_handmatch['マッチページURL'].unique())
      column_handmatch_kind.append(handmatch_kind)
      
      #自動マッチのページ種類
      match_kind = len(df_match['マッチページURL'].unique())
      column_match_kind.append(match_kind)
      

    #手動マッチページのうち、何ページが自動マッチ成功し、何ページが失敗したか確認
    df_output = pd.DataFrame({'サイト名':column_sitename,'人手マッチページ組数':column_handmatch_num,'自動マッチ成功数':column_match_success_num,'自動マッチ失敗数':column_match_failure_num,'自動マッチカバー率':column_match_cover_per,'自動マッチ総ページ組数':column_match_all_num,'Precision':column_precison,'人手総ページ数（ページの種類）':column_handmatch_kind,'自動総ページ数（ページの種類）':column_match_kind})
    dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/eval/'+ver
    df_output.to_csv(dir+'/'+'eval_aggregation_match_'+limit+'.csv',sep=',',index=None) 
    df_output.to_excel(dir+'/'+'eval_aggregation_match_'+limit+'.xlsx') 
        
      

#各節の手動マッチページが、自動マッチング結果にあるか確認      
def check_match(df_handmatch,df_match,textname,sitename):
  for i in range(len(df_handmatch['節番号'])):
    hand_match_setu = df_handmatch['節番号'][i]
    hand_match_URL = df_handmatch['マッチページURL'][i]
    for j in range(len(df_match['節番号'])):
      if (df_match['節番号'][j]==hand_match_setu)and(df_match['マッチページURL'][j]==hand_match_URL):
        df_handmatch['自動マッチ結果'][i] = '○'
        df_handmatch['マッチ用語'][i] = df_match['マッチ用語'][j]
        #print(df_match['節番号'][j])
        #print(df_match['マッチページ'][j])
        break
      df_handmatch['自動マッチ結果'][i] = '×'
      
  
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/eval/'   
  df_handmatch.to_csv(dir+'/'+ver+'/'+'eval_handmatch_'+textname+'_'+sitename+'_'+limit+'.csv',sep=',',index=None) 
  df_handmatch.to_excel(dir+'/'+ver+'/'+'eval_handmatch_'+textname+'_'+sitename+'_'+limit+'.xlsx') 
      
  return df_handmatch

if __name__ == "__main__":    
    
    #'tau.doshisha.ac.jp'
    #'www.sci.hokudai.ac.jp' は手動マッチしていないため、
    #リストから除外
    list_handmatch_site =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','ufcpp.net','univ-juken.com',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp',
                    'www.momoyama-usagi.com','yorikuwa.com']
    
    list_textname = ['kosen_biseki1']
    limit = '2'
    ver = '0628'
  
    main(list_handmatch_site,list_textname,limit,ver)