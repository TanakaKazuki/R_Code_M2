#R_DATA_M2/For_yogo_bunpu/.のテキストデータをもとに、
#各分野ごとの重複のない出現用語を調べる
#1章（数列と級数）
#1.1 〜　2.4節
#2章（微分法）
#3.1　〜　7.5節
#3章（積分法）
#8.1　〜　10.3節

import re
import csv
from pathlib import Path
from lxml import html
import os
import datetime as dt

list_one = ['数列', '項', '初項', '一般項','数列', '初項', '等差数列', '一般項', '公差', '和','数列', '初項', '等比数列',
            '一般項', '公比', '和','数列', '初項', '等差数列', '和', '総和',
            'シグマ', 'シグマ記号', '累乗', '部分分数分解', '部分分数',
            '数列', '無限数列', '無限大', '収束', '極限値', '発散', '正の無限大', '負の無限大', '振動', '等比数列', '公比', '極限',
            '数列', '無限級数', '級数', '第n部分和', '部分和', '和', '収束', '発散', 
            '初項', '公比', '等比数列', '無限等比級数', '等比級数', '循環小数', '既約分数',
            '数列', '公差', '等差数列', '漸化式','数列', '漸化式', '数学的帰納法']


list_two = ['関数', '極限', '収束', '極限値', '発散',
            '関数', '右側極限値', '左側極限値', '片側極限値', 
            '極限値', '数直線', '区間', '閉区間', '開区間', '連続',
            '関数', '変化量', '平均変化率', '接線', '接点', '極限値', '微分可能', '連続性', '連続', '微分係数',
            '関数', '微分可能', '微分係数', '導関数', '微分', '数学的帰納法', '定数倍', '和', '差',
            '合成関数', '導関数', '微分', '積', '導関数',
            '接線の方程式', '接線', '傾き','導関数', '単調増加', '単調減少', '増減表', '増減', 
            '極値', '極小', '極小値', '極大', '極大値', '必要条件',
            '2回微分可能', '二回微分可能', '第二次導関数', '第2次導関数', '関数', '凹凸', 
            '下に凸', '上に凸', '変曲点', '必要条件', '増減', '極値',
            '関数', '最大値', '最小値', '定義域','関数', '商', '導関数', '分数関数', 'x^n',
            '逆関数', '合成関数', '無理関数','対数関数', '導関数', '自然対数の底', '自然対数'
            '対数微分法', 'x^α', '指数関数', '導関数', 'e^x',
            '正弦関数', '極限', '三角関数', '導関数', '極限値',
            '逆正弦関数', 'アークサイン', '逆余弦関数', 'アークコサイン', '逆正接関数', 'アークタンジェント', '逆三角関数', '導関数',
            '不定形', '平均値の定理', 'コーシー', 'ロピタル', '極限','関数', '増減', '変曲点', 'ロピタル', '増減表',
            '関数', '最大値', '最小値', '増減表','接線', '微分', '変化量', '近似',
            '速度', '加速度', '平均速度', '上昇速度', '変化率']


list_three = ['定積分', '積分可能', '積分', '下端', '上端', '積分変数', '被積分関数', '速さ', 
              '原始関数', '微分積分学の基本定理', '三角関数','不定積分', '積分定数', '積分', '被積分関数',
              '線形性', '加法性', '面積', '定積分', '三角関数','定積分', '置換積分法', '置換積分', '積分', '三角関数',
              '部分積分法', '部分積分', '定積分', '積分', '三角関数',
              '偶関数', '奇関数', 'sin^nx', 'cos^nx', '定積分', '積分', '三角関数',
              '曲線', '面積', '直線', '積分', '三角関数','体積', '立体', '回転体', '積分', '三角関数',
              '速度', '位置', '導関数', '加速度', '積分', '三角関数',
              '不定積分', '微分積分学の基本定理', '線形性', '積分', '三角関数',
              '不定積分', '置換積分法', '置換積分', '合成関数', '分数関数', '有理関数', '積分',
              '三角関数', '部分分数分解', '部分分数',
              '不定積分', '部分積分法', '部分積分', '逆正弦関数', '積分', '三角関数', '対数関数', '逆三角関数', '指数関数', '逆正弦関数', 
              'アークサイン', '逆余弦関数', 'アークコサイン', '逆正接関数', 'アークタンジェント']

#各章ごとの用語の重複を無くす
list_one = list(set(list_one))
list_two = list(set(list_two))
list_three = list(set(list_three))

list_one_only = list(set(list_one)-set(list_two))
list_one_only = list(set(list_one_only)-set(list_three))


list_two_only = list(set(list_two)-set(list_one))
list_two_only = list(set(list_two_only)-set(list_three))

list_three_only = list(set(list_three)-set(list_one))
list_three_only = list(set(list_three_only)-set(list_two))

print('1章')
print(list_one)
print(len(list_one))
print('2章')
print(list_two)
print(len(list_two))
print('3章')
print(list_three)
print(len(list_three))

########################################
#例として、「ももやま」と「よりくわ」の各章の出現用語を把握
momoyama_1 = ['極限', '無限大','数学的帰納法', '漸化式']
momoyama_2 = ['関数', '発散','関数', '極限','関数', '極限','関数', '連続','接線', '微分可能', '関数',
              '連続性', '関数', '連続', '微分可能','関数', '微分可能', '微分', '導関数',
              '微分', '積', '導関数','接線', '接線の方程式','導関数', '関数', '逆関数',
              '合成関数', '関数', '商','導関数','導関数','逆三角関数', '逆正弦関数', '逆余弦関数', '逆正接関数',
              '逆三角関数','増減表', '関数', '変曲点', '増減','増減表', '関数']
momoyama_3 = ['面積', '不定積分', '積分', '定積分','積分', '定積分','積分', '定積分','面積', '積分', '曲線',
              '体積', '積分','不定積分', '積分','積分', '三角関数','不定積分', '積分','部分分数分解', '部分分数', '積分',
              '置換積分', '積分','積分', '三角関数','三角関数', '逆余弦関数', '逆三角関数', '積分', '逆正接関数', '逆正弦関数',
              '不定積分', '積分','積分', '部分積分','積分', '部分積分']

yorikuwa_1 = ['数列', '一般項', '項','数列', '一般項', '項','数列', '一般項', '項','等差数列', '数列', '一般項', '公差',
              '等差数列', '数列','和', '等差数列', '数列','和', '等差数列', '数列','和', '等差数列', '数列', '一般項',
              '公比', '数列', '等比数列', '一般項','数列', '等比数列','和', '数列', '等比数列','和', '数列', '等比数列',
              '和', '数列', '等比数列', '一般項','シグマ', 'シグマ記号','部分分数分解', '和', '数列', '部分分数',
              '和', '数列','和', '数列', 'シグマ記号', '等差数列', 'シグマ', '累乗','数列', '収束', '発散',
              '極限', '数列','極限', '数列','極限', '等比数列', '数列','数列', '収束', '極限', '等比数列', '発散',
              '無限級数', '級数','等比級数', '級数', '無限等比級数','数列', '無限等比級数', '級数', '収束',
              '等比級数', '無限級数', '等比数列', '発散','等差数列', '漸化式', '数列','数学的帰納法', '漸化式', '数列']

yorikuwa_2 = ['関数', '極限','関数', '極限','関数', '極限','関数', '極限','関数', '極限','関数', '極限','極限値', '極限',
               '関数', '極限','極限値', '関数', '極限','関数','平均変化率','微分係数','平均変化率', '極限値', '微分係数',
               '接線', '関数','関数', '導関数','微分','関数', '微分','関数', '微分', '微分係数', '導関数',
               '合成関数', '微分', '積','微分','微分', '積', '導関数','接線', '接線の方程式','接線', '傾き',
               '接線', '傾き', '接線の方程式','増減表', '極値', '増減', '導関数','極値', '関数', '増減',
               '最小値', '関数', '最大値','無理関数', '関数', '分数関数','関数', '導関数','対数関数','対数関数','導関数',
               '対数微分法','指数関数','指数関数', '対数微分法','導関数','三角関数','三角関数','極限値', '極限', '導関数',
               '導関数','極限', '不定形','極限', '不定形','極限', '不定形','増減表', '関数', '増減','関数',
               '増減表', '関数', '増減','増減表', '関数', '増減','最小値', '関数', '最大値','最小値', '関数', '最大値', '増減表']

yorikuwa_3 = ['積分', '定積分','積分', '定積分','定積分', '積分', '三角関数','積分', '定積分','積分', '定積分',
              '面積', '積分', '定積分','定積分', '不定積分', '積分', '三角関数',
              '置換積分', '積分', '定積分', '置換積分法','三角関数', '置換積分', '積分', '置換積分法', '定積分',
              '三角関数', '置換積分', '積分', '置換積分法', '定積分','積分', '定積分',
              '積分', '定積分', '部分積分法', '部分積分','三角関数', '積分', '部分積分法', '部分積分', '定積分',
              '積分', '定積分','奇関数', '積分', '定積分', '偶関数','奇関数', '三角関数', '偶関数', '積分', '定積分',
              '積分', '定積分','面積', '積分','面積', '積分','面積', '積分','不定積分', '積分','積分','不定積分', '積分', '三角関数',
              '不定積分', '積分','合成関数', '積分','置換積分', '積分', '置換積分法','置換積分', '積分', '置換積分法',
              '積分', '分数関数','不定積分', '三角関数', '置換積分', '合成関数', '積分', '分数関数', '置換積分法',
              '積分', '三角関数','積分', '三角関数','不定積分', '積分','積分', '部分積分法', '部分積分',
              '不定積分', '三角関数', '指数関数', '積分', '部分積分法', '部分積分','不定積分', '積分']

momoyama_1 = list(set(momoyama_1))
momoyama_1 = list(set(momoyama_1)&set(list_one))
momoyama_2 = list(set(momoyama_2))
momoyama_2 = list(set(momoyama_2)&set(list_two))
momoyama_3 = list(set(momoyama_3))
momoyama_3 = list(set(momoyama_3)&set(list_three))



yorikuwa_1 = list(set(yorikuwa_1))
yorikuwa_1 = list(set(yorikuwa_1)&set(list_one))
yorikuwa_2 = list(set(yorikuwa_2))
yorikuwa_2 = list(set(yorikuwa_2)&set(list_two))
yorikuwa_3 = list(set(yorikuwa_3))
yorikuwa_3 = list(set(yorikuwa_3)&set(list_three))

print('momoyama1')
print(momoyama_1)
print(len(momoyama_1))
print("yorikuwa1")
print(yorikuwa_1)
print(len(yorikuwa_1))


print('momoyama2')
print(momoyama_2)
print(len(momoyama_2))
print("yorikuwa2")
print(yorikuwa_2)
print(len(yorikuwa_2))

print('momoyama3')
print(momoyama_3)
print(len(momoyama_3))
print("yorikuwa3")
print(yorikuwa_3)
print(len(yorikuwa_3))

only_momoyama1 = list(set(momoyama_1)-set(yorikuwa_1))
print('only_momoyama1')
print(only_momoyama1)
print(len(only_momoyama1))

only_yorikuwa1 = list(set(yorikuwa_1)-set(momoyama_1))
print('only_yorikuwa1')
print(only_yorikuwa1)
print(len(only_yorikuwa1))

only_momoyama2 = list(set(momoyama_2)-set(yorikuwa_2))
print('only_momoyama2')
print(only_momoyama2)
print(len(only_momoyama2))

only_yorikuwa2 = list(set(yorikuwa_2)-set(momoyama_2))
print('only_yorikuwa2')
print(only_yorikuwa2)
print(len(only_yorikuwa2))

only_momoyama3 = list(set(momoyama_3)-set(yorikuwa_3))
print('only_momoyama3')
print(only_momoyama3)
print(len(only_momoyama3))

only_yorikuwa3 = list(set(yorikuwa_3)-set(momoyama_3))
print('only_yorikuwa3')
print(only_yorikuwa3)
print(len(only_yorikuwa3))