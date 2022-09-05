#-*- coding: utf-8 -*-
# "見出しを抽出し、csvに出力するプログラム"
#  "correspondenceの１列目の番号番目のtxtファイルを読み込む"

import re
import csv
from pathlib import Path
from lxml import html
import os
import datetime as dt

# 不要なタグを検索する xpath 表現のタプル
REMOVE_TAGS = ('.//style', './/script', './/noscript')

# 見出しタグを検索する xpath 表現
XPATH_H_TAGS = './/h1|.//h2|.//h3|.//h4|.//h5|.//h6'

# 見出しタグを検出するための正規表現
RE_H_MATCH = re.compile('^h[1-6]$').match


    

def main(list_sitename):
    """メイン関数"""
    
    make_derectory(list_sitename)
    
    
    
    for site in range(len(list_sitename)):
        sitename = list_sitename[site]
        dir = '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data_removed/'
        #removed_correspondence_list_のバージョン
        correspondence_ver = '0621'
        dir2 = 'removed_'+correspondence_ver+'/'
        
        
        #0526追加#####################
        XPATH_H_TAGS = decide_xpath_h_tag(sitename)
        #############################
        
        df = pd.read_csv(dir + dir2 + 'removed_correspondence_list_'+sitename+'.csv',header=None)
        
        fname = df[0]
        furl = df[1]
        
        for i in range(len(fname)):
            filename = fname[i]
            fileurl = furl[i]
            
            # (1/8) HTML ファイルを指定します
            
            if os.path.exists('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'.txt'):
                src_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'.txt')
            elif os.path.exists('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'_NotFindTitle.txt'):
                src_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/'+sitename+'./'+filename+'_NotFindTitle.txt')
            
            # (2/8) HTML データを取得します
            with src_file.open('rb') as f:
                html_data = f.read()
            
            # エンコーディングを指定してパーサーを作成
            html_parser = html.HTMLParser(encoding='utf-8')

            
            # (3/8) HTML を解析します
            root = html.fromstring(html_data,parser=html_parser)

            # (4/8) HTML から不要なタグを削除します
            for remove_tag in REMOVE_TAGS:
                for tag in root.findall(remove_tag):
                    tag.drop_tree()

            # (5/8) テキストの入れ物を用意します
            #      (デバッグ用にラベル行も追加)
            texts = []
            texts.append(
            # ['URL','タグ名', 'タグテキスト', 'タグに属するテキスト'])
            ['URL','タグ名', 'タグテキスト'])

            # (6/8) タイトルタグを取得します
            t = root.find('.//title')
            if t is not None:
                text = t.text_content()

                # 空でなければリストに追加
                if text:
                    texts.append([t.tag, text, ''])

                print(f'(デバッグ) {t.tag}: {text}\n')

            # (7/8) 見出しタグを検索します
            for h_tag in root.xpath(XPATH_H_TAGS):
                # 見出しタグのテキストを取得
                h_text = h_tag.text_content()
                
        #######0526修正部分#################
                #atarimae.biz,jfor.net対策
                if h_tag.attrib and sitename in ['atarimae.biz','jfor.net','takun-physics.net']:
                    
                    print('h_tag.class')
                    #print(h_tag.attrib['class'])
                    if h_tag.get('class'):
                        if h_tag.attrib['class']=='post-list-title entry-title':
                            print('continue')
                            continue
                #ramenhuhu対策
                elif h_tag.attrib and sitename=='ramenhuhu.com':
                    print('h_tag.class')
                    print(type(h_tag.attrib))
                    if h_tag.get('class'):
                        if (h_tag.attrib['class']=='heading heading-secondary') or (h_tag.attrib['class']=='heading heading-tertiary'):
                            print('continue')
                            continue
                #k-san.link linear-algebra.com
                elif h_tag.attrib and sitename in ['k-san.link','linear-algebra.com']:
                    print('h_tag.class')
                    print(type(h_tag.attrib))
                    if h_tag.get('class'):
                        if h_tag.attrib['class']=='ttl':
                            print('continue')
                            continue
                
                
                
                
                print(f'(デバッグ) {h_tag.tag}: {h_text}')
                # 見出しタグと同じ階層にあったテキストを入れるリスト
                contents = []
                # 見出しの次のタグを取得
                next_tag = h_tag.getnext()
                texts.append([fileurl ,h_tag.tag, h_text])
        ###################################
        
            # (8/8) テキストを CSV に保存します
            
            ver = '0621'
            
            csv_file = Path(r'/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/For_all_removed/head_data/'+sitename+'_'+ver+'/removed_head_'+filename+'.csv')
            with csv_file.open('w', encoding='utf-8', newline='') as f:
                w = csv.writer(f)
                w.writerows(texts)

        # 以上です
    return

#プログラム実行日のフォルダを作る
def make_derectory(list_sitename):
  dt_now = dt.datetime.now()
 
  #フォルダ名用にyyyymmddの文字列を取得する
  mmdd = dt_now.strftime('%m%d')
 
  #作成するフォルダ名を定義する
  for i in range(len(list_sitename)):
    #directory_name = u'removed_'+list_sitename[i] + mmdd
    directory_name = list_sitename[i]+'_'+ mmdd
    #現在のフォルダパスを取得する(プログラムが実行されているフォルダパス)
    #current_directory = os.path.dirname(os.path.abspath(__file__))
    
    #作成のために確認するフォルダパスを作成する
    create_directory =  '/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/For_all_removed/head_data/' + directory_name
    
    #対象フォルダが存在しない場合
    if(not (os.path.exists(create_directory))):
    
        #フォルダを作成
        os.mkdir(create_directory)
    


#サイトごとに読み込むタグを変更する
def decide_xpath_h_tag(sitename):
    
    h3 = [ 'fromhimuka.com','ufcpp.net','rikeilabo.com','univ-juken.com','univ-study.net']
    
    h2 = ['examist.jp','manabitimes.jp','math-fun.net']
    
    if sitename in h3:
        XPATH_H_TAGS = './/h1|.//h2|.//h3|'

    
    elif sitename in h2:
        XPATH_H_TAGS = './/h1|.//h2|'
    else:
        XPATH_H_TAGS = './/h1|.//h2|.//h3|.//h4|.//h5|.//h6'
    
    return XPATH_H_TAGS


import pandas as pd

if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #path
    # df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/senkei/html_data/correspondence_list_yorikuwa.com.csv',header=None)
    # filename = df[0]
    # fileurl = df[1]
    
    
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp','tau.doshisha.ac.jp',を除いた21サイト
    
    
    list_sitename = ['ai-trend.jp','atarimae.biz','jfor.net','k-san.link',
                 'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net',
                 'math-juken.com','math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
                 'ramenhuhu.com','risalc.info','takun-physics.net',
                 'univ-study.net','w3e.kanazawa-it.ac.jp',
                 'www.geisya.or.jp','www.headboost.jp','www.momoyama-usagi']
    
    #list_sitename =['ramenhuhu.com']

    main(list_sitename)

