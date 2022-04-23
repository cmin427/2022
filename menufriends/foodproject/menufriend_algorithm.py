from other_functions_2 import mf_1500_function,mf_33000_function,find_ingre
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import pandas as pd
import numpy as np
import math
####my branch
def adjust_history(input_value):
  if type(input_value)==type('1'):
    list_ = input_value.split(',')
  elif type(input_value) == type(1):
    list_ = [input_value]
  else:
    list_ = input_value[:]
  list_ = [int(item) for item in list_]
  new_list = []
  for it in list_:
    if it != -1:
      new_list.append(it)  
  return new_list[-1:-4:-1]
  
def adjust_user(user_info): 
  user_info[1] = adjust_history(user_info[1])
  weight_by_date = [0.01,     0.1,    0.7]
  user = [[[100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100, 0]], [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 100]]]
  if len(user_info[1]) <= 0:
    return user
  base_order_dict = {'견과류': 0, '곡물전분류': 1, '기타': 2, '김치류': 3, '난류': 4, '면류': 5, '버섯류': 6, '유제품': 7, '육류': 8, '조리가공품류': 9, '조미료': 10, '채소류': 11, '해산물': 12}
  for pre_menu,weight in zip(user_info[1],weight_by_date):
    pre_menu_ingre = find_ingre(pre_menu)
    for ingre in pre_menu_ingre:
      k = base_order_dict[ingre]
      user[k][0][k] *= weight
  return user

def cal_cosine(df,ingre_col,user,user_info):  
  # ingre_col : 재료 컬럼 
  # user_info : dict형태인 사용자의 재료별 선호도
  tfidf_vec = TfidfVectorizer()
  tfidf_matrix = tfidf_vec.fit_transform(ingre_col)
  df_frame = pd.DataFrame(data=df.title)
  for idx, cat in enumerate(user_info[0]):
    cosine_sim = linear_kernel(user[idx], tfidf_matrix) 
    a = (cosine_sim[0])
    df_frame[f'{cat}'] = a
    # indices = pd.Series(df.index, index=df.index)
    # top_list = recommend(df, indices, cosine_sim, 7)
    
  df_frame['곡물전분류'] = df_frame['곡물전분류'].apply(lambda x: user_info[0]['곡물전분류'] ** float(x) )
  df_frame['김치류'] = df_frame['김치류'].apply(lambda x: user_info[0]['김치류'] ** float(x) )
  df_frame['난류'] = df_frame['난류'].apply(lambda x: user_info[0]['난류'] ** float(x) )
  df_frame['면류'] = df_frame['면류'].apply(lambda x: user_info[0]['면류'] ** float(x) )
  df_frame['버섯류'] = df_frame['버섯류'].apply(lambda x: user_info[0]['버섯류'] ** float(x) )
  df_frame['유제품'] = df_frame['유제품'].apply(lambda x: user_info[0]['유제품'] ** float(x) )
  df_frame['육류'] = df_frame['육류'].apply(lambda x: user_info[0]['육류'] ** float(x) )
  df_frame['조리가공품류'] = df_frame['조리가공품류'].apply(lambda x: user_info[0]['조리가공품류'] ** float(x) )
  df_frame['채소류'] = df_frame['채소류'].apply(lambda x: user_info[0]['채소류'] ** float(x) )
  df_frame['해산물'] = df_frame['해산물'].apply(lambda x: user_info[0]['해산물'] ** float(x) )
  df_frame_1 = df_frame.iloc[:,1:]
  df_frame_1['result'] = df_frame['곡물전분류'] * df_frame['김치류'] * df_frame['난류'] * df_frame['면류'] * df_frame['버섯류'] * df_frame['유제품'] * df_frame['육류'] * df_frame['조리가공품류'] * df_frame['채소류'] * df_frame['해산물'] 
  return df_frame_1.result

def cosine_result(df, user_info, is_1500):  
  user = adjust_user(user_info)
  if is_1500 == 1:  # mf_1500 
    a = cal_cosine(df,df.main_ingredients,user,user_info)
    b = cal_cosine(df,df.ingredients,user,user_info)
    result = a * 0.7 + b * 0.3            # 주재료 0.7 부재료 0.3
  else:  # mf_33000
    a = cal_cosine(df,df.raw_ingre_sep,user,user_info)
    result = a
  result = result.sort_values(ascending=False).index.tolist()
  return result

def mf_main(is_1500,user_info,head,n): # 위에서 head 번째 부터 n개
  file_name = 'mfd.csv'
  file_path = 'C:\\Users\\min\Desktop\\min-git\\menufriend\\foodproject\\' + file_name
  # file_path = './mfd.csv'
  if is_1500 == 1:  #1500이면 1 
    df = mf_1500_function(file_path)
  elif is_1500 == 0: # 33000이면 0
    df = mf_33000_function(file_path)
  result = cosine_result(df,user_info,is_1500)
  result = result[head-1:head+n-1]
  result_menu = []
  print_result_menu = []
  for idx in result:
    result_menu.append(idx)
  # a = (df.loc[idx,'title'])
  # print_result_menu.append([idx,a])
  # print(print_result_menu)
  return result_menu

# user_1 = [{'견과류': 1, '곡물전분류':1, '기타': 1, '김치류': 1, '난류': 1, '면류': 1, '버섯류': 1, 
# '유제품': 1, '육류': 1, '조리가공품류': 1, '조미료': 1, '채소류': 1, '해산물': 1},[2580,87,29874]]  # 최근에 먹은것부터 
# print(f'최근 먹은 메뉴 index:{user_1[1]}:, 추천 메뉴 index',mf_main(1,user_1,1,5))
# user_2 = [{'견과류': 1, '곡물전분류':1, '기타': 1, '김치류': 1, '난류': 1, '면류': 1, '버섯류': 1, 
# '유제품': 1, '육류': 3, '조리가공품류': 1, '조미료': 1, '채소류': 3, '해산물': 1},'1'] # 
# print(f'mf_33000:{user_2[1]}',mf_main(0,user_2,1,10))

# user_0 , tfidf_mat = adjust_user
# print(user0,tfidf_mat)

