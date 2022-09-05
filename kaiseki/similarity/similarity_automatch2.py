#閾値2語の自動マッチング結果をもとに、
# 各サイトごとの類似度（コサイン類似度、内積、ユークリッド距離）を求める
#

#各章ごとの類似度（コサイン類似度、内積、ユークリッド距離）を求める

from cmath import nan
import re
import csv
from pathlib import Path
from turtle import dot
from lxml import html
import os
import MeCab
import pandas as pd
import numpy as np
import ast
import datetime as dt

def main(list_sitename,input_name):
  df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/Aggregation_data/Aggregation_0526/Aggregation_match_kosen_biseki1_0526_2.csv')
  
  cos_sim_list_list = []
  sec1_cos_sim_list_list = []
  sec2_cos_sim_list_list = []
  sec3_cos_sim_list_list = []
  sec4_cos_sim_list_list = []
  sec5_cos_sim_list_list = []
  sec6_cos_sim_list_list = []
  sec7_cos_sim_list_list = []
  sec8_cos_sim_list_list = []
  sec9_cos_sim_list_list = []
  sec10_cos_sim_list_list = []
  
  dot_list_list = []
  sec1_dot_list_list = []
  sec2_dot_list_list = []
  sec3_dot_list_list = []
  sec4_dot_list_list = []
  sec5_dot_list_list = []
  sec6_dot_list_list = []
  sec7_dot_list_list = []
  sec8_dot_list_list = []
  sec9_dot_list_list = []
  sec10_dot_list_list = []
  
  euclidean_list_list = []
  sec1_euclidean_list_list = []
  sec2_euclidean_list_list = []
  sec3_euclidean_list_list = []
  sec4_euclidean_list_list = []
  sec5_euclidean_list_list = []
  sec6_euclidean_list_list = []
  sec7_euclidean_list_list = []
  sec8_euclidean_list_list = []
  sec9_euclidean_list_list = []
  sec10_euclidean_list_list = []
  
  
  for i in range(len(list_sitename)):
    site_name_1 = list_sitename[i]
    #print(df[site_name_1])
    
    #テキスト全体のマッチ傾向
    match_num_site_name_1 = df[site_name_1]
    cos_sim_list = []
    dot_list = []
    euclidean_list = []
    
    #テキストの1章のマッチ傾向
    #print(df[df['節番号'].isin([1.1, 1.2,1.3,1.4])][site_name_1])
    sec1_match_num_site_name_1 = df[df['節番号'].isin([1.1,1.2,1.3,1.4])][site_name_1]
    sec1_cos_sim_list = []
    sec1_dot_list = []
    sec1_euclidean_list = []
    #print(sec1_match_num_site_name_1)
    #テキストの2章のマッチ傾向
    sec2_match_num_site_name_1 = df[df['節番号'].isin([2.1,2.2,2.3,2.4])][site_name_1]
    sec2_cos_sim_list = []
    sec2_dot_list = []
    sec2_euclidean_list = []
    #テキストの3章のマッチ傾向
    sec3_match_num_site_name_1 = df[df['節番号'].isin([3.1,3.2])][site_name_1]
    sec3_cos_sim_list = []
    sec3_dot_list = []
    sec3_euclidean_list = []
    #テキストの4章のマッチ傾向
    sec4_match_num_site_name_1 = df[df['節番号'].isin([4.1,4.2,4.3])][site_name_1]
    sec4_cos_sim_list = []
    sec4_dot_list = []
    sec4_euclidean_list = []
    #テキストの5章のマッチ傾向
    sec5_match_num_site_name_1 = df[df['節番号'].isin([5.1,5.2,5.3,5.4])][site_name_1]
    sec5_cos_sim_list = []
    sec5_dot_list = []
    sec5_euclidean_list = []
    #テキストの6章のマッチ傾向
    sec6_match_num_site_name_1 = df[df['節番号'].isin([6.1,6.2,6.3,6.4,6.5])][site_name_1]
    sec6_cos_sim_list = []
    sec6_dot_list = []
    sec6_euclidean_list = []
    #テキストの7章のマッチ傾向
    sec7_match_num_site_name_1 = df[df['節番号'].isin([7.1,7.2,7.3,7.4,7.5])][site_name_1]
    sec7_cos_sim_list = []
    sec7_dot_list = []
    sec7_euclidean_list = []
    #テキストの8章のマッチ傾向
    sec8_match_num_site_name_1 = df[df['節番号'].isin([8.1,8.2,8.3,8.4,8.5])][site_name_1]
    sec8_cos_sim_list = []
    sec8_dot_list = []
    sec8_euclidean_list = []
    #テキストの9章のマッチ傾向
    sec9_match_num_site_name_1 = df[df['節番号'].isin([9.1,9.2,9.3])][site_name_1]
    sec9_cos_sim_list = []
    sec9_dot_list = []
    sec9_euclidean_list = []
    #テキストの10章のマッチ傾向
    sec10_match_num_site_name_1 = df[df['節番号'].isin([10.1,10.2,10.3])][site_name_1]
    sec10_cos_sim_list = []
    sec10_dot_list = []
    sec10_euclidean_list = []
    
    
    
    
    
    #各サイトから見た各サイトとのコサイン類似度
    for j in range(len(list_sitename)):
      site_name_2 = list_sitename[j]
      
      #テキスト全体のマッチ傾向
      match_num_site_name_2 = df[site_name_2]
      cos_sim_list.append(cos_sim(match_num_site_name_1,match_num_site_name_2))  
      dot_list.append(sum(match_num_site_name_1 * match_num_site_name_2))
      euclidean_list.append(np.linalg.norm(match_num_site_name_1-match_num_site_name_2))
      
      #テキストの1章のマッチ傾向
      sec1_match_num_site_name_2 = df[df['節番号'].isin([1.1,1.2,1.3,1.4])][site_name_2]
      sec1_cos_sim_list.append(cos_sim(sec1_match_num_site_name_1,sec1_match_num_site_name_2))
      sec1_dot_list.append(sum(sec1_match_num_site_name_1 * sec1_match_num_site_name_2))
      sec1_euclidean_list.append(np.linalg.norm(sec1_match_num_site_name_1 - sec1_match_num_site_name_2))
      #テキストの2章のマッチ傾向
      sec2_match_num_site_name_2 = df[df['節番号'].isin([2.1,2.2,2.3,2.4])][site_name_2]
      sec2_cos_sim_list.append(cos_sim(sec2_match_num_site_name_1,sec2_match_num_site_name_2))
      sec2_dot_list.append(sum(sec2_match_num_site_name_1 * sec2_match_num_site_name_2))
      sec2_euclidean_list.append(np.linalg.norm(sec2_match_num_site_name_1 - sec2_match_num_site_name_2))
      
      
      #テキストの3章のマッチ傾向
      sec3_match_num_site_name_2 = df[df['節番号'].isin([3.1,3.2])][site_name_2]
      sec3_cos_sim_list.append(cos_sim(sec3_match_num_site_name_1,sec3_match_num_site_name_2))
      sec3_dot_list.append(sum(sec3_match_num_site_name_1 * sec3_match_num_site_name_2))
      sec3_euclidean_list.append(np.linalg.norm(sec3_match_num_site_name_1 - sec3_match_num_site_name_2))
      
      #テキストの4章のマッチ傾向
      sec4_match_num_site_name_2 = df[df['節番号'].isin([4.1,4.2,4.3])][site_name_2]
      sec4_cos_sim_list.append(cos_sim(sec4_match_num_site_name_1,sec4_match_num_site_name_2))
      sec4_dot_list.append(sum(sec4_match_num_site_name_1 * sec4_match_num_site_name_2))
      sec4_euclidean_list.append(np.linalg.norm(sec4_match_num_site_name_1 - sec4_match_num_site_name_2))
      
      #テキストの5章のマッチ傾向
      sec5_match_num_site_name_2 = df[df['節番号'].isin([5.1,5.2,5.3,5.4])][site_name_2]
      sec5_cos_sim_list.append(cos_sim(sec5_match_num_site_name_1,sec5_match_num_site_name_2))
      sec5_dot_list.append(sum(sec5_match_num_site_name_1 * sec5_match_num_site_name_2))
      sec5_euclidean_list.append(np.linalg.norm(sec5_match_num_site_name_1 - sec5_match_num_site_name_2))
      
      #テキストの6章のマッチ傾向
      sec6_match_num_site_name_2 = df[df['節番号'].isin([6.1,6.2,6.3,6.4,6.5])][site_name_2]
      sec6_cos_sim_list.append(cos_sim(sec6_match_num_site_name_1,sec6_match_num_site_name_2))
      sec6_dot_list.append(sum(sec6_match_num_site_name_1 * sec6_match_num_site_name_2))
      sec6_euclidean_list.append(np.linalg.norm(sec6_match_num_site_name_1 - sec6_match_num_site_name_2))
      #テキストの7章のマッチ傾向
      sec7_match_num_site_name_2 = df[df['節番号'].isin([7.1,7.2,7.3,7.4,7.5])][site_name_2]
      sec7_cos_sim_list.append(cos_sim(sec7_match_num_site_name_1,sec7_match_num_site_name_2))
      sec7_dot_list.append(sum(sec7_match_num_site_name_1 * sec7_match_num_site_name_2))
      sec7_euclidean_list.append(np.linalg.norm(sec7_match_num_site_name_1 - sec7_match_num_site_name_2))
      #テキストの8章のマッチ傾向
      sec8_match_num_site_name_2 = df[df['節番号'].isin([8.1,8.2,8.3,8.4,8.5])][site_name_2]
      sec8_cos_sim_list.append(cos_sim(sec8_match_num_site_name_1,sec8_match_num_site_name_2))
      sec8_dot_list.append(sum(sec8_match_num_site_name_1 * sec8_match_num_site_name_2))
      sec8_euclidean_list.append(np.linalg.norm(sec8_match_num_site_name_1 - sec8_match_num_site_name_2))
      #テキストの9章のマッチ傾向
      sec9_match_num_site_name_2 = df[df['節番号'].isin([9.1,9.2,9.3])][site_name_2]
      sec9_cos_sim_list.append(cos_sim(sec9_match_num_site_name_1,sec9_match_num_site_name_2))
      sec9_dot_list.append(sum(sec9_match_num_site_name_1 * sec9_match_num_site_name_2))
      sec9_euclidean_list.append(np.linalg.norm(sec9_match_num_site_name_1 - sec9_match_num_site_name_2))
      #テキストの10章のマッチ傾向
      sec10_match_num_site_name_2 = df[df['節番号'].isin([10.1,10.2,10.3])][site_name_2]
      sec10_cos_sim_list.append(cos_sim(sec10_match_num_site_name_1,sec10_match_num_site_name_2))
      sec10_dot_list.append(sum(sec10_match_num_site_name_1 * sec10_match_num_site_name_2))
      sec10_euclidean_list.append(np.linalg.norm(sec10_match_num_site_name_1 - sec10_match_num_site_name_2))
      
      
    
    cos_sim_list_list.append(cos_sim_list)
    sec1_cos_sim_list_list.append(sec1_cos_sim_list)
    sec2_cos_sim_list_list.append(sec2_cos_sim_list)
    sec3_cos_sim_list_list.append(sec3_cos_sim_list)
    sec4_cos_sim_list_list.append(sec4_cos_sim_list)
    sec5_cos_sim_list_list.append(sec5_cos_sim_list)
    sec6_cos_sim_list_list.append(sec6_cos_sim_list)
    sec7_cos_sim_list_list.append(sec7_cos_sim_list)
    sec8_cos_sim_list_list.append(sec8_cos_sim_list)
    sec9_cos_sim_list_list.append(sec9_cos_sim_list)
    sec10_cos_sim_list_list.append(sec10_cos_sim_list)
    
    dot_list_list.append(dot_list)
    sec1_dot_list_list.append(sec1_dot_list)
    sec2_dot_list_list.append(sec2_dot_list)
    sec3_dot_list_list.append(sec3_dot_list)
    sec4_dot_list_list.append(sec4_dot_list)
    sec5_dot_list_list.append(sec5_dot_list)
    sec6_dot_list_list.append(sec6_dot_list)
    sec7_dot_list_list.append(sec7_dot_list)
    sec8_dot_list_list.append(sec8_dot_list)
    sec9_dot_list_list.append(sec9_dot_list)
    sec10_dot_list_list.append(sec10_dot_list)
    
    euclidean_list_list.append(euclidean_list)
    sec1_euclidean_list_list.append(sec1_euclidean_list)
    sec2_euclidean_list_list.append(sec2_euclidean_list)
    sec3_euclidean_list_list.append(sec3_euclidean_list)
    sec4_euclidean_list_list.append(sec4_euclidean_list)
    sec5_euclidean_list_list.append(sec5_euclidean_list)
    sec6_euclidean_list_list.append(sec6_euclidean_list)
    sec7_euclidean_list_list.append(sec7_euclidean_list)
    sec8_euclidean_list_list.append(sec8_euclidean_list)
    sec9_euclidean_list_list.append(sec9_euclidean_list)
    sec10_euclidean_list_list.append(sec10_euclidean_list)
    

  #類似度（ユークリッド距離）
  df_euclidean = pd.DataFrame(euclidean_list_list, columns = list_sitename)
  df_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_euclidean.to_csv(dir + '/' + 'euclidean_match.csv',index=None) 
  df_euclidean.to_excel(dir + '/' + 'euclidean_match.xlsx' ) 
  
  df_sec1_euclidean = pd.DataFrame(sec1_euclidean_list_list, columns = list_sitename)
  df_sec1_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec1_euclidean.to_csv(dir + '/' + 'sec1_euclidean_match.csv',index=None) 
  df_sec1_euclidean.to_excel(dir + '/' + 'sec1_euclidean_match.xlsx' ) 
  
  df_sec2_euclidean = pd.DataFrame(sec2_euclidean_list_list, columns = list_sitename)
  df_sec2_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec2_euclidean.to_csv(dir + '/' + 'sec2_euclidean_match.csv',index=None) 
  df_sec2_euclidean.to_excel(dir + '/' + 'sec2_euclidean_match.xlsx' ) 
  
  df_sec3_euclidean = pd.DataFrame(sec3_euclidean_list_list, columns = list_sitename)
  df_sec3_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec3_euclidean.to_csv(dir + '/' + 'sec3_euclidean_match.csv',index=None) 
  df_sec3_euclidean.to_excel(dir + '/' + 'sec3_euclidean_match.xlsx' ) 
  
  df_sec4_euclidean = pd.DataFrame(sec4_euclidean_list_list, columns = list_sitename)
  df_sec4_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec4_euclidean.to_csv(dir + '/' + 'sec4_euclidean_match.csv',index=None) 
  df_sec4_euclidean.to_excel(dir + '/' + 'sec4_euclidean_match.xlsx' ) 
  
  df_sec5_euclidean = pd.DataFrame(sec5_euclidean_list_list, columns = list_sitename)
  df_sec5_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec5_euclidean.to_csv(dir + '/' + 'sec5_euclidean_match.csv',index=None) 
  df_sec5_euclidean.to_excel(dir + '/' + 'sec5_euclidean_match.xlsx' ) 
  
  df_sec6_euclidean = pd.DataFrame(sec6_euclidean_list_list, columns = list_sitename)
  df_sec6_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec6_euclidean.to_csv(dir + '/' + 'sec6_euclidean_match.csv',index=None) 
  df_sec6_euclidean.to_excel(dir + '/' + 'sec6_euclidean_match.xlsx' ) 
  
  
  df_sec7_euclidean = pd.DataFrame(sec7_euclidean_list_list, columns = list_sitename)
  df_sec7_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec7_euclidean.to_csv(dir + '/' + 'sec7_euclidean_match.csv',index=None) 
  df_sec7_euclidean.to_excel(dir + '/' + 'sec7_euclidean_match.xlsx' ) 
  
  df_sec8_euclidean = pd.DataFrame(sec8_euclidean_list_list, columns = list_sitename)
  df_sec8_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec8_euclidean.to_csv(dir + '/' + 'sec8_euclidean_match.csv',index=None) 
  df_sec8_euclidean.to_excel(dir + '/' + 'sec8_euclidean_match.xlsx' ) 
  
  df_sec9_euclidean = pd.DataFrame(sec9_euclidean_list_list, columns = list_sitename)
  df_sec9_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec9_euclidean.to_csv(dir + '/' + 'sec9_euclidean_match.csv',index=None) 
  df_sec9_euclidean.to_excel(dir + '/' + 'sec9_euclidean_match.xlsx' ) 
  
  df_sec10_euclidean = pd.DataFrame(sec10_euclidean_list_list, columns = list_sitename)
  df_sec10_euclidean.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/euclidean'
  df_sec10_euclidean.to_csv(dir + '/' + 'sec10_euclidean_match.csv',index=None) 
  df_sec10_euclidean.to_excel(dir + '/' + 'sec10_euclidean_match.xlsx' ) 
  
  
  #類似度（内積）
  df_dot = pd.DataFrame(dot_list_list, columns = list_sitename)
  df_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_dot.to_csv(dir + '/' + 'dot_match.csv',index=None) 
  df_dot.to_excel(dir + '/' + 'dot_match.xlsx' ) 
  
  df_sec1_dot = pd.DataFrame(sec1_dot_list_list, columns = list_sitename)
  df_sec1_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec1_dot.to_csv(dir + '/' + 'sec1_dot_match.csv',index=None) 
  df_sec1_dot.to_excel(dir + '/' + 'sec1_dot_match.xlsx' ) 
  
  df_sec2_dot = pd.DataFrame(sec2_dot_list_list, columns = list_sitename)
  df_sec2_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec2_dot.to_csv(dir + '/' + 'sec2_dot_match.csv',index=None) 
  df_sec2_dot.to_excel(dir + '/' + 'sec2_dot_match.xlsx' ) 
  
  df_sec3_dot = pd.DataFrame(sec3_dot_list_list, columns = list_sitename)
  df_sec3_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec3_dot.to_csv(dir + '/' + 'sec3_dot_match.csv',index=None) 
  df_sec3_dot.to_excel(dir + '/' + 'sec3_dot_match.xlsx' ) 
  
  
  df_sec4_dot = pd.DataFrame(sec4_dot_list_list, columns = list_sitename)
  df_sec4_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec4_dot.to_csv(dir + '/' + 'sec4_dot_match.csv',index=None) 
  df_sec4_dot.to_excel(dir + '/' + 'sec4_dot_match.xlsx' ) 
  
  df_sec5_dot = pd.DataFrame(sec5_dot_list_list, columns = list_sitename)
  df_sec5_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec5_dot.to_csv(dir + '/' + 'sec5_dot_match.csv',index=None) 
  df_sec5_dot.to_excel(dir + '/' + 'sec5_dot_match.xlsx' ) 
  
  df_sec6_dot = pd.DataFrame(sec6_dot_list_list, columns = list_sitename)
  df_sec6_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec6_dot.to_csv(dir + '/' + 'sec6_dot_match.csv',index=None) 
  df_sec6_dot.to_excel(dir + '/' + 'sec6_dot_match.xlsx' ) 
  
  df_sec7_dot = pd.DataFrame(sec7_dot_list_list, columns = list_sitename)
  df_sec7_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec7_dot.to_csv(dir + '/' + 'sec7_dot_match.csv',index=None) 
  df_sec7_dot.to_excel(dir + '/' + 'sec7_dot_match.xlsx' ) 
  
  df_sec8_dot = pd.DataFrame(sec8_dot_list_list, columns = list_sitename)
  df_sec8_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec8_dot.to_csv(dir + '/' + 'sec8_dot_match.csv',index=None) 
  df_sec8_dot.to_excel(dir + '/' + 'sec8_dot_match.xlsx' ) 
  
  
  df_sec9_dot = pd.DataFrame(sec9_dot_list_list, columns = list_sitename)
  df_sec9_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec9_dot.to_csv(dir + '/' + 'sec9_dot_match.csv',index=None) 
  df_sec9_dot.to_excel(dir + '/' + 'sec9_dot_match.xlsx' ) 
  
  df_sec10_dot = pd.DataFrame(sec10_dot_list_list, columns = list_sitename)
  df_sec10_dot.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/dot'
  df_sec10_dot.to_csv(dir + '/' + 'sec10_dot_match.csv',index=None) 
  df_sec10_dot.to_excel(dir + '/' + 'sec10_dot_match.xlsx' ) 
  
  #テキスト全体の類似度
  df_cos_sim = pd.DataFrame(cos_sim_list_list, columns = list_sitename)
  df_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_cos_sim.to_csv(dir + '/' + 'cos_sim_match.csv',index=None) 
  df_cos_sim.to_excel(dir + '/' + 'cos_sim_match.xlsx' ) 
  
  #テキストの1章の類似度
  df_sec1_cos_sim = pd.DataFrame(sec1_cos_sim_list_list, columns = list_sitename)
  df_sec1_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec1_cos_sim.to_csv(dir + '/' + 'sec1_cos_sim_match.csv',index=None) 
  df_sec1_cos_sim.to_excel(dir + '/' + 'sec1_cos_sim_match.xlsx' ) 
  
  df_sec2_cos_sim = pd.DataFrame(sec2_cos_sim_list_list, columns = list_sitename)
  df_sec2_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec2_cos_sim.to_csv(dir + '/' + 'sec2_cos_sim_match.csv',index=None) 
  df_sec2_cos_sim.to_excel(dir + '/' + 'sec2_cos_sim_match.xlsx' ) 
  
  
  df_sec3_cos_sim = pd.DataFrame(sec3_cos_sim_list_list, columns = list_sitename)
  df_sec3_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec3_cos_sim.to_csv(dir + '/' + 'sec3_cos_sim_match.csv',index=None) 
  df_sec3_cos_sim.to_excel(dir + '/' + 'sec3_cos_sim_match.xlsx' ) 
  
  df_sec4_cos_sim = pd.DataFrame(sec4_cos_sim_list_list, columns = list_sitename)
  df_sec4_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec4_cos_sim.to_csv(dir + '/' + 'sec4_cos_sim_match.csv',index=None) 
  df_sec4_cos_sim.to_excel(dir + '/' + 'sec4_cos_sim_match.xlsx' ) 
  
  df_sec5_cos_sim = pd.DataFrame(sec5_cos_sim_list_list, columns = list_sitename)
  df_sec5_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec5_cos_sim.to_csv(dir + '/' + 'sec5_cos_sim_match.csv',index=None) 
  df_sec5_cos_sim.to_excel(dir + '/' + 'sec5_cos_sim_match.xlsx' ) 
  
  df_sec6_cos_sim = pd.DataFrame(sec5_cos_sim_list_list, columns = list_sitename)
  df_sec6_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec6_cos_sim.to_csv(dir + '/' + 'sec6_cos_sim_match.csv',index=None) 
  df_sec6_cos_sim.to_excel(dir + '/' + 'sec6_cos_sim_match.xlsx' ) 
  
  
  df_sec7_cos_sim = pd.DataFrame(sec7_cos_sim_list_list, columns = list_sitename)
  df_sec7_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec7_cos_sim.to_csv(dir + '/' + 'sec7_cos_sim_match.csv',index=None) 
  df_sec7_cos_sim.to_excel(dir + '/' + 'sec7_cos_sim_match.xlsx' ) 
  
  df_sec8_cos_sim = pd.DataFrame(sec8_cos_sim_list_list, columns = list_sitename)
  df_sec8_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec8_cos_sim.to_csv(dir + '/' + 'sec8_cos_sim_match.csv',index=None) 
  df_sec8_cos_sim.to_excel(dir + '/' + 'sec8_cos_sim_match.xlsx' ) 
  
  
  df_sec9_cos_sim = pd.DataFrame(sec9_cos_sim_list_list, columns = list_sitename)
  df_sec9_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec9_cos_sim.to_csv(dir + '/' + 'sec9_cos_sim_match.csv',index=None) 
  df_sec9_cos_sim.to_excel(dir + '/' + 'sec9_cos_sim_match.xlsx' ) 
  
  df_sec10_cos_sim = pd.DataFrame(sec7_cos_sim_list_list, columns = list_sitename)
  df_sec10_cos_sim.insert(loc = 0,column='サイト名',value=list_sitename)
  dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/similarity/match/cos_sim'
  df_sec10_cos_sim.to_csv(dir + '/' + 'sec10_cos_sim_match.csv',index=None) 
  df_sec10_cos_sim.to_excel(dir + '/' + 'sec10_cos_sim_match.xlsx' ) 





  
#コサイン類似度
def cos_sim(v1, v2):
    if(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) == np.nan):
      print(print(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2)) ))
    
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))    



if __name__ == "__main__":
    """読み込むファイル名の指定"""
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    #現在閲覧できなかった#'www.sci.hokudai.ac.jp','tau.doshisha.ac.jp'を除いた20サイト
    list_sitename =['atarimae.biz','batapara.com','eman-physics.net','examist.jp','fromhimuka.com',
                    'hiraocafe.com','hooktail.sub.jp','manabitimes.jp','math-fun.net',
                    'opencourse.doshisha.ac.jp','math-juken.com','ramenhuhu.com',
                    'rikeilabo.com','ufcpp.net','univ-juken.com',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp',
                    'www.momoyama-usagi.com','yorikuwa.com']
    
    
    input_name = ['correspondence_list','removed_correspondence_list']
    # df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_yorikuwa.com.csv',header=None)
    # filename = df[0]
    # fileurl = df[1]
    # print(filename.head(50))
    # print(fileurl.head(50))

    main(list_sitename,input_name)
