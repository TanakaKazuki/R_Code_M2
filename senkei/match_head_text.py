import re
import csv
from pathlib import Path
from lxml import html
import os
import MeCab
import pandas as pd
import ast

def main(list_sitename,list_textname,limit,delete_term):
  #各テキスト
  for i in range(len(list_textname)):
    text_name = list_textname[i]
    df_text = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+text_name+'.csv')
    
    #df_text[0]節番号
    #df_text[1]節名
    #df_text[2]節内出現用語
    
    #各節内出現用語をMecabで分割し、ページ内出現用語の表記と合わせる
    column_setu_mecab = []
    for setu in range(len(df_text['term'])):
      setu_term = df_text['term'][setu].split('/')
      setu_term_mecab = get_nouns(setu_term)
      column_setu_mecab.append(setu_term_mecab)
      
    df_text['term_mecab'] = column_setu_mecab
    df_text.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+text_name+'_mecab.csv',sep=',',index=None) 
    df_text.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+text_name+'_mecab.xlsx') 

        
      
    
    #各ウェブサイト
    for site_num in range(len(list_sitename)):
      site_name = list_sitename[site_num]
      
      column_setu_num = [] #節番号
      column_setu_name = [] #節名
      column_match_page = [] #マッチしたページ
      column_match_term = [] #マッチした用語
      column_match_url = [] #マッチしたページのURL
      column_setu_term = [] #節内出現用語
      column_match_page_term = [] #マッチしたページ見出し内用語
      
      #テキスト内の各節
      for setu_num in range(len(df_text['setu_num'])):
        setu_term = df_text['term_mecab'][setu_num]
        #print(setu_term)
        setu_name = df_text['setu_name'][setu_num]
        setu_number = df_text['setu_num'][setu_num]
        #print(setu_name)
      
        
        #サイト内全ページの見出し出現用語
        df_site = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/head_data_site/'+site_name+'_header_term.csv')
        #id,URL,タイトル,タイトル・見出し出現用語,タイトル・見出し出現用語数
        
        #csv形式によりstr型になってしまったリストをlist型に戻す
        df_site['タイトル・見出し出現用語'] = [ast.literal_eval(d) for d in df_site['タイトル・見出し出現用語']]
        df_site['タイトル内単語'] = [ast.literal_eval(d) for d in df_site['タイトル内単語']]
        df_site['見出し内単語'] = [ast.literal_eval(d) for d in df_site['見出し内単語']]
        
        #各ページ
        for page in range(len(df_site['タイトル'])):
          #各ページ内　タイトル・見出し出現用語
          page_term = df_site['タイトル・見出し出現用語'][page]
          
          
          page_name = df_site['タイトル'][page]
          page_url = df_site['URL'][page]
             
          
          setu_page_and = check_match_yogo(page_term,setu_term)
          setu_page_and = term_delete(delete_term,setu_page_and)
          
          
          if(setu_page_and and len(setu_page_and) >= int(limit)):
            print('setu_page_and',setu_page_and)
            print('setu_term',setu_term)
            print('page_term',page_term)
            
            print('setu_page_and',setu_page_and)
            print('setu_name',setu_name)
            print('setu_term',setu_term)
            print('page_name',page_name)
            print('page_term',page_term)
            
            column_setu_num.append(setu_number)
            column_setu_name.append(setu_name)
            column_setu_term.append(setu_term)
            column_match_page.append(page_name)
            column_match_term.append(list(setu_page_and))
            column_match_url.append(page_url)
            column_match_page_term.append(page_term)
            
        
        df_output = pd.DataFrame({'節番号':column_setu_num,'節名':column_setu_name,'マッチページ':column_match_page,'マッチページURL':column_match_url,'マッチ用語':column_match_term,'節内出現用語':column_setu_term,'マッチページ見出し用語':column_match_page_term})
        df_output.to_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/text_match/'+text_name+'/'+text_name+''+site_name+'_'+limit+'.csv',sep=',',index=None) 
        df_output.to_excel('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/text_match/'+text_name+'/'+text_name+''+site_name+'_'+limit+'.xlsx') 
        

#見出し内出現用語　と　テキスト内出現用語 から不用語を除く
def term_delete(delete_term,match_term):
  for r in delete_term:
    #一致語があり、かつその中に不用語があるなら
    if match_term and r in match_term:
      match_term = match_term.remove(r)
  return match_term
  
  
#各ページ内出現用語と各節内出現用語の、一致用語を返す
def check_match_yogo(page_term,setu_term):
  # print('page_term',page_term)
  # print('setu_term',setu_term)
  set_page_term = set(page_term)
  set_setu_term = set(setu_term)
  
  
  match_term = list(set_page_term & set_setu_term)
  # print('set_page_term',set_page_term)
  # print('set_setu_term',set_setu_term)
  # print('match_term',match_term)
  
  
  return match_term
  

def get_nouns(sentence_list):

    nounAndPronoun = []
    for i in range(len(sentence_list)):  
        mecab = MeCab.Tagger ('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
        text = sentence_list[i]
        result = mecab.parse(text)
        #print(result)
        lines = result.split('\n')
        
        for line in lines:
            feature = line.split('\t')
            if len(feature) == 2:
                info = feature[1].split(',')
                hinshi = info[0]
                if hinshi in ('名詞', '固有名詞'):
                    nounAndPronoun.append(info[6])
    
    nounAndPronoun = list(set(nounAndPronoun))
                    
    return nounAndPronoun
  


if __name__ == "__main__":    
    list_sitename =['ai-trend.jp','atarimae.biz','iwata-system-support.com','jfor.net','k-san.link',
                    'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net','math-juken.com',
                    'math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
                    'ramenhuhu.com','risalc.info','sun.ac.jp','takun-physics.net','tau.doshisha.ac.jp',
                    'univ-study.net','w3e.kanazawa-it.ac.jp','www.geisya.or.jp','www.headboost.jp',
                    'www.momoyama-usagi']
    
    
    #sitename ='yorikuwa.com'
    
    list_textname = []
    #df_text = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/textbook/'+textname+'.csv',header=None)

    delete_term = ['法','性','定理','定義','関数','*']
    #テキスト内用語とページ見出し内用語の、一致用語数の閾値
    limit = '2'
    
    main(list_sitename,list_textname,limit,delete_term)