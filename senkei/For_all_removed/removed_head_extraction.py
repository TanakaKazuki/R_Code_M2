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
        ver = '0511'
        dir2 = 'removed_'+ver+'/'
        
        df = pd.read_csv(dir + dir2 + 'removed_correspondence_list_'+sitename+'.csv',header=None)
        
        fname = df[0]
        furl = df[1]
        
        for i in range(len(fname)):
            filename = fname[i]
            fileurl = furl[i]
            
            # (1/8) HTML ファイルを指定します
            print(sitename)
            
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

                print(f'(デバッグ) {h_tag.tag}: {h_text}')

                # 見出しタグと同じ階層にあったテキストを入れるリスト
                contents = []

                # 見出しの次のタグを取得
                next_tag = h_tag.getnext()

                # 次のタグがなくなるまでループ
                # while next_tag is not None:
                #     # タグが見出しだったらブレーク
                #     if RE_H_MATCH(next_tag.tag):
                #         print(f'(デバッグ) 次の見出しタグ {next_tag.tag} が見つかった。')
                #         print(f'(デバッグ) while ブレーク\n')
                #         break

                #     # タグのテキストを取得
                #     text = next_tag.text_content()

                #     # 空でなければリストに追加
                #     if text:
                #         contents.append(text)

                #     print(f'(デバッグ) {next_tag.tag}: {text}')

                #     # さらに次のタグを取得してループする
                #     next_tag = next_tag.getnext()
                # else:
                #     # 同じ階層のタグをたどり尽くして、次のタグが無かった場合。
                #     print(f'(デバッグ) 次のタグが無かった。 {next_tag}')

                # # リストを連結してひとつの文字列にします
                # contents = '|'.join(contents)

                # リストに追加
                #texts.append([fileurl ,h_tag.tag, h_text, contents])
                texts.append([fileurl ,h_tag.tag, h_text])

            # (8/8) テキストを CSV に保存します
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
    
    

import pandas as pd

if __name__ == "__main__":
    """読み込むファイル名の指定"""
    #path
    # df = pd.read_csv('/Users/kazuki/Desktop/research/data_Research_M2/R_Data_M2/kaiseki/html_data/correspondence_list_yorikuwa.com.csv',header=None)
    # filename = df[0]
    # fileurl = df[1]
    
    
    
    #'racco.mikeneko.jp','www.maroon.dti.ne.jp',を除いた22サイト
    list_sitename = ['ai-trend.jp','atarimae.biz','jfor.net','k-san.link',
                 'linear-algebra.com','linky-juku.com','manabitimes.jp','math-fun.net',
                 'math-juken.com','math-note.xyz','mathwords.net','oguemon.com','opencourse.doshisha.ac.jp',
                 'ramenhuhu.com','risalc.info','takun-physics.net',
                 'tau.doshisha.ac.jp','univ-study.net','w3e.kanazawa-it.ac.jp',
                 'www.geisya.or.jp','www.headboost.jp','www.momoyama-usagi']
    
    

    main(list_sitename)

