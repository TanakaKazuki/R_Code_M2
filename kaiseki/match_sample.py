#各ページ内出現用語と各節内出現用語の、一致用語を返す
def check_match_yogo(page_term,setu_term):
  set_page_term = set(page_term)
  set_setu_term = set(setu_term)
  
  match_term = list(set_page_term & set_setu_term)
  
  return match_term



page_term = [['出現用語','出現', '和'],['出現用語', '和']]
setu_term = ['出現','和']
for i in range(len(page_term)):
  match_term = check_match_yogo(page_term[i],setu_term)
  print(match_term)