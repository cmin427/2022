from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import math 
import pandas as pd 
import ast
import re
from collections import Counter

# 전처리 관련 함수들
# 전처리 관련 함수들
# 전처리 관련 함수들
# 전처리 관련 함수들

nan_value = float("NaN")

def cleanText(readData):    #특수 문자 제거
    text = re.sub('[-=+#/\?:^$.@*\"※~&%ㆍ!』\\‘|\(\)\[\]\<\>`\…》]', ',', readData)
    return text

def isNaN(num):   # 전처리 에 사용됨 
    return num != num

def list_to_dict(result,key,list_):  # 전처리 에 사용됨 
  if len(list_) > 0:
    k = ','.join(list_)
    result[key] = k
    return result
  else:
    return result

def ingre_to_counter(df):  # 전처리 에 사용됨 
  raw_ingre_list = []
  for rows in df.raw_ingre:
    raw_ingre_list += rows
  count_list = Counter(raw_ingre_list)
  count_list = list(count_list) 
  return count_list

def check_ingre(ingre_list):    # 전처리 에 사용됨 
  word_kimchi = ['김치','겉절이','깍두기']
  word_vegi = ['아보카도', '빈', '아스파', '파', '키위', '새싹', '양퍄', '연근','마늘', '대파', '쪽파', '고추', '전분', '파채', '사과', '배', '스위트콘', '잔파', '쑥갓','양파','배추','파프리카','두릅','호박','샐러리', '잎', '피망','감자','당근',
               '숙주','상추','부추','시금치','청경채','더덕','토마토','오이','무','수수','미나리','줄기','고수','주키니','고사리','달래','시래기','우엉','브로','채소','야채','냉이','머위','도라지','나물','고구마','케일','가지','곰취','두부','유부',
               '피팡', '딸기', '베리', '건포도','샬롯','곶감', '밤', '비트', '호바', '쑥','죽순','색각','우거지','오렌지','샐러드','셀러리','대추','페페','로즈',',인삼','봄동','콩물','콩국','완두','얼갈이','바나나','멜론','수박','고구맛','당귀','포도',
               '모과','감귤','돌산갓','인삼','알타리','복숭아','자몽','석류','귤','참외','감말랭','율','케이퍼','적근대','자두','홍시']
  word_sea = ['해삼', '멸지','명란','새우','바자락','고등어','꼴뚜','전복','소라','뱅어','세우' , '조개', '합','멸치','북어','우렁','다시마','연어','꼬막','오징어','낙지','참치','게','어묵','문어','오뎅','바지락','김','해물','꾸미','실치','갈치',
              '골뱅이','명태','이리','크래','맛살','미역','진미','굴','관자','가리비','홍합','쥐포','크레미','중하', '대하', '아귀', '감태','해산물','지리','날치','창란','창난','쉬림','디포리','가다랑','솔치','황태','가쯔','가쓰오','가츠오','다시팩',
              '삼치','장어','동태','오만둥이','간재미','꽁치','우럭','밴딩','전어', '광어', '먹태', '민어', '놀래미', '시사모', '가스오부시', '랍스타', '어포', '홍어']
  word_meat = ['돈채','고기','대패','다리','영계','갈비','살','육','돼지','닭','소고기','고깃','삼겹','오리','차돌','치킨','족발','심','떡갈비','돈까스','삽겹','한우','곱창','막창','대창','미트','오돌뼈','양지','소꼬리','스테이크','함박']
  word_cap = ['버섯','느타리','새송이','팽이','양송이','표고']
  word_ham = ['캔','리챔', '돈가스', '피클', '산적', '동그랑','햄','소시지','소세지','스팸','베이컨','만두','비엔나','순대','런천','후랑크','핫도그','교자','핫바','곤약','묵','짜왕','진짬','너겟','믹스','사골','크래미','크레미']
  word_egg = ['계란','계랸','달걀','흰자','노른자','메추리알','메츄리알','수란','초란','반숙', '후라이','유정란']
  word_rice = ['백미','흑미', '일미', '누룽지','쌀','밥','햇반','떡','떢','빵','또띠','라이스','씨리얼', '시리얼', '귀리', '현미','치아바타','잡곡','력분','카스테라','로투스','오트밀']
  word_noo = ['소바','면','국수','우동','잡채','파스타','푸실리']
  word_milk = ['버터','우유','크림','치즈','연유','치츠','모짜', '렐라', '졸라','플레인','요거트','요구','두유']
  word_nut = ['아몬드', '땅콩','견과','넛','잣','넉맷','호두']
  word_favor = ['마요', '식초', '케첩', '생강', '솔트', '땡초', '떙초', '식초', '매실', '요리당', '생강', '미향', '조청', '드레싱', '버진', '춘장', '케챂', '와인', '소주', '맛술', '청주', '정종', '연두', '간잔', '겨자', '청양', '수금', '포도주', 
                '유자청', '조미료','진간', '큐민', '월계수', '쯔유', '캐쳡', '소소', '설당', '과실', '다진', '젓갈', '소다', '이신', '짜장','설턍','섵탕','케찹', '케챱', '캐찹', '캐챱', '올리고당', '페퍼', '레몬', '까나리', '염', '양념', '고주창', 
                '고춧', '꿀', '참기름', '들기름', '매식액', '머스', '라임','소스','카레', '설탕', '소금', '후추', '바질', '가루', '미림', '미원', '다시다', 'msg', 'MSG', '액젓', '깨', '꺠', '쌈장', '된장', '간장', '고추장', '물엿', '매실청', '두반장', 
                '메실청', '원당', '와사비', '즙','메실','실액','강장','장조림국물','꼬추','타임','조리술','요리술','향신','조정','청국','사이다','허브','올리브','식용유','식요','다싯','카놀','포도씨','우스터','인삼주','후주','메이플','기름',
                '올라고','산초','황두','앤초','성탕','마가린','시즈','복분','복문','케쳡','식용류','캐첩','후룻','해바라','섬초','까놀','요리유','흑임','해바라기','맥주','할라','시럽','낫또','후춧','오일','홍초','민트','커리','오미자청','계피','슈가',
                '초코', '누텔라', '바닐라', '오레오', '제티', '몽쉘', '초콜릿', '죠리퐁','코코아', '카라멜', '요리엿', '초장', '홀스래디쉬', '발사믹', '앙금', '녹차', '백련초', '커피','럼주']
  kimchi_list = []
  vegi_list = []
  sea_list = []
  meat_list = []
  cap_list = []
  ham_list = []
  noo_list = []
  milk_list = []
  rice_list = []
  egg_list = []
  nut_list = []
  favor_list = []
  etc_list = []
  result_dict = {}
  k = 0
  for ingre in ingre_list:
    k = 0
    if k == 0:
      for c in word_favor:
        if c in ingre:
          favor_list.append(ingre)
          k = 1
          break
    if k == 0:
      for v in word_kimchi:
        if v in ingre:
          kimchi_list.append(ingre)
          k = 1
          break
    if k == 0:
      for v in word_vegi:
        if v in ingre:
          vegi_list.append(ingre)
          k = 1
          break
    if k == 0:
      for s in word_sea:
        if s in ingre:
          sea_list.append(ingre)
          k = 1
          break
    if k == 0:
      for m in word_meat:
        if m in ingre:
          meat_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_cap:
        if c in ingre:
          cap_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_ham:
        if c in ingre:
          ham_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_noo:
        if c in ingre:
          noo_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_milk:
        if c in ingre:
          milk_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_rice:
        if c in ingre:
          rice_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_egg:
        if c in ingre:
          egg_list.append(ingre)
          k = 1
          break
    if k == 0:
      for c in word_nut:
        if c in ingre:
          nut_list.append(ingre)
          k = 1
          break
    if k == 0:
      etc_list.append(ingre)

  result_dict = list_to_dict(result_dict,'김치류',kimchi_list)
  result_dict = list_to_dict(result_dict,'채소류',vegi_list)
  result_dict = list_to_dict(result_dict,'해산물',sea_list)
  result_dict = list_to_dict(result_dict,'육류',meat_list)
  result_dict = list_to_dict(result_dict,'버섯류',cap_list)
  result_dict = list_to_dict(result_dict,'조리가공품류',ham_list)
  result_dict = list_to_dict(result_dict,'면류',noo_list)
  result_dict = list_to_dict(result_dict,'유제품',milk_list)
  result_dict = list_to_dict(result_dict,'곡물전분류',rice_list)
  result_dict = list_to_dict(result_dict,'난류',egg_list)
  result_dict = list_to_dict(result_dict,'견과류',nut_list)
  result_dict = list_to_dict(result_dict,'조미료',favor_list)
  result_dict = list_to_dict(result_dict,'기타',etc_list)
  # print(etc_list)
  return result_dict