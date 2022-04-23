# 실행 커맨드: $ python txt2csv.py (txt파일명) (아이디 값(빠른게 1, 늦은게2)) {(시작 프레임) (끝 프레임) (클래스번호)} {반복2} {반복3}
# 실행 커맨드 예시 : $ python txt2csv.py teakowndo1-1 2 5 23 3 -> (teakowndo1-1.txt파일을 읽어서 늦은ID가 공격자이고 5~23프레임을 3번(머리 공격)으로 라벨링csv로 저장)
import sys
import pandas as pd

args = sys.argv[1:]

if (len(args)) % 3 != 2:
    print('input error')
    sys.exit()

count = len(args) // 3

data_path = 'C:\\Users\\min\\Desktop\\project\\A-free\\data\\' # 각자 path 변경 필요

txt_file_name = data_path + 'txt\\' + args[0] + '.txt' # 각자 path 변경 필요

# txt파일 Dataframe으로 읽어오기
df = pd.read_csv(txt_file_name, sep = ' ', header=None)
# print(df)

if int(args[1]) == 1:
    new_df = df.iloc[:, 0:36]
    new_df['36'] = 0
    for j in range(count):
        start_frame = int(args[j*3 + 2])
        end_frame = int(args[j*3 + 3])
        label_num = int(args[j*3 + 4])
        for i in range(start_frame-1, end_frame):
            new_df.iloc[i, new_df.columns.get_loc('36')] = label_num
elif int(args[1]) == 2:
    new_df = df.iloc[:, 36:72]
    new_df['72'] = 0
    for j in range(count):
        start_frame = int(args[j*3 + 2])
        end_frame = int(args[j*3 + 3])
        label_num = int(args[j*3 + 4])
        for i in range(start_frame-1, end_frame):
            new_df.iloc[i, new_df.columns.get_loc('72')] = label_num
# print(new_df)

# Dataframe을 csv 파일로 저장
csv_file_name = data_path + 'csv\\' + args[0] + '.csv' # 각자 path 변경 필요
new_df.to_csv(csv_file_name, index=False, header=False, float_format='%.2f')

print('csv 변환 및 labeling 완료')