import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import numpy as np

# 1) 한글 설정
## font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
> font_manager의 FontProperties에 폰트 경로를 전달하여 폰트 이름을 얻어옴
## rc('font', family=font_name)
> rc를 통해 폰트를 설정


# 2) def setting_cctv_file(_cctv_table):
> cctv.csv파일 가공
## _cctv_table = _cctv_table.dropna()
> 전달 받은 csv파일 데이터 중 값을 가지고 있지 않은 데이터 삭제
## _cctv_table.to_csv("./서울시 자치구 목적별 CCTV 설치 현황_가공.csv", encoding="cp949", mode='w', index=True)
> 변경 된 데이터 파일을 다른이름의 csv파일(='서울시 자치구 목적별 CCTV 설치 현황_가공')로 저장

# 3) def setting_accident_file(_accident_table):
> accident.csv파일 가공
## _accident_table = _accident_table.drop(_accident_table.index[0])
> 필요없는 행(='합계') 삭제
## _accident_table = _accident_table.dropna()
> 전달 받은 csv파일 데이터 중 값을 가지고 있지 않은 데이터 삭제
## _accident_table.sort_values(by='지역', inplace=True)
> '지역'을 기준으로 오름차순 정렬
## _accident_table['어린이보호구역내 어린이 교통사고 발생건수'] = np.where(_accident_table['어린이보호구역내 어린이 교통사고 발생건수'] == '-', 0,_accident_table['어린이보호구역내 어린이 교통사고 발생건수'])
> '어린이보호구역내 어린이 교통사고 발생건수'의 데이터 값이 '-'이면 '0'으로 수정
## _accident_table.to_csv("./서울시 어린이 교통사고 현황_가공.csv", encoding="cp949", mode='w', index=True)
> 변경 된 데이터 파일을 다른이름의 csv파일(='서울시 어린이 교통사고 현황_가공')로 저장


# 4) def setting_merge_file():
> ctv_modify.csv파일과 accident_modify.csv파일 병합
## cctv_filename_modify = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황_가공.csv'
> 읽어올 csv파일 경로 정의
## cctv_table_modify = pd.read_csv(cctv_filename_modify, encoding='CP949', header=0, engine='python')
> 해당 csv파일(='서울시 자치구 목적별 CCTV 설치 현황_가공') 읽어옴
## accident_filename_modify = 'C:/kse/서울시 어린이 교통사고 현황_가공.csv'
> 읽어올 csv파일 경로 정의
## accident_table_modify = pd.read_csv(accident_filename_modify, encoding='CP949', header=0, engine='python')
> 해당 csv파일(='서울시 어린이 교통사고 현황_가공') 읽어옴

## merge_table = pd.concat([cctv_table_modify['기관명'], cctv_table_modify['어린이 보호'],accident_table_modify['어린이보호구역내 어린이 교통사고 발생건수']], axis=1)
> 두 개의 csv파일에서 필요한 데이터만 추출하여 오른쪽방향으로(axis=1) 합병
## merge_table.rename(columns={"어린이 보호": "어린이 보호 cctv수"}, inplace=1)
> 컬럼명을 '어린이 보호'에서 '어린이 보호 cctv수'로 수정
merge_table['cctv수 범위'] = merge_table['어린이 보호 cctv수'].apply(cctv_category)
> 새로운 컬럼(='cctv수 범위') 추가후 값 cctv_category()함수로부터의 반환값을 저장

## merge_table.to_csv("./서울시 어린이 교통사고 발생건수와 어린이 보호 cctv수.csv", encoding="cp949", mode='w', index=False)
> 합병 된 데이터 파일을 다른이름의 csv파일(='서울시 어린이 교통사고 발생건수와 어린이 보호 cctv수')로 저장
## return merge_table
> 합병 된 데이터(='merge_table')을 반환


# 5) def cctv_category(x):
> cctv 개수 범위 지정
##
    if x < 100:
        return 0
    elif x < 200:
        return 1
    elif x < 300:
        return 2
    elif x < 400:
        return 3
    elif x < 500:
        return 4
    else:
        return 5
> 전달 받은 데이터 값이 100미만이면 0을, 200미만이면 1을, 300미만이면 2를, 400미만이면 3을, 500미만이면 4를, 500이상이면 5를 반환


# 6) def setting_analysis_file(_merged_table):
> cctv 설치 수와 어린이 교통사고 발생건수 분석
## myData = []
> 이차원 배열을 사용하기 위해, '행'부분 데이터를 담을 배열(='myData') 선언

## cctv_category_unique_value = sorted(_merged_table['cctv수 범위'].unique())
> cctv범위의 고유값(= 0,1,2,3,4,5)을 오름차순으로 정렬

## for i in cctv_category_unique_value:
> cctv범위의 고유값만큼 for 반복문 실행
## myData_j = []
> 이차원 배열을 사용하기 위해, '열'부분 데이터를 담을 배열(='myData_j') 선언
## for j in range(2):
> range()범위(=3) 만큼 반복문 실행
## totalSum = _merged_table['어린이보호구역내 어린이 교통사고 발생건수'][_merged_table['cctv수 범위'] == i].sum()
> cctv범위 값이 i(= 0~5)일때 해당 지역의 어린이 교통사고 발생건수 총합
## totalCount = _merged_table['어린이 보호 cctv수'][_merged_table['cctv수 범위'] == i].count()
> cctv범위 값이 i(= 0~5)일때 범위내 지역수
## totalAverage = round(totalSum / totalCount, 1)
> cctv범위내 어린이 교통사고 발생건수 평균
## myData_j.append(totalSum)
> 0열에 totalSum 값 추가
## myData_j.append(totalCount)
> 1열에 totalCount 값 추가
## myData_j.append(totalAverage)
> 2열에 totalAverage 값 추가
## myData.append(myData_j)
> 하나의 행(totalSum,totalCount,totalAverage) 추가
## myData_table = pd.DataFrame(myData, columns=('범위내 어린이 교통사고 발생건수 총합 ' , '범위내 지역수', '범위내 어린이 교통사고 발생건수 평균'))
> 생성된 myData_table 데이터 파일을 csv파일로 저장
## category = ['100미만', '100이상 200미만', '200이상 300미만', '300이상 400미만', '400이상 500미만', '500이상']
> 필요한 컬럼(='category')를 정의
## myData_table["범위"] = category
> '범위'라는 컬럼명으로 category데이터 추가

## myData_table.to_csv("./Result.csv", encoding="cp949", mode='w', index=True)
> 생성 된 데이터 파일을 다른이름의 csv파일(='Result')로 저장
## return myData_table
> 생성 된 데이터(='myData_table') 반환

# 7) def draw_graph(_result):
> 그래프로 시각화
## sns.pointplot(x="범위", y="어린이 교통사고 발생건수 평균", data=_result)
> x축이 '범위', y축이 '어린이 교통사고 발생건수 평균'인 점선 그래프로 시각화
## plt.title("2018년도 어린이 보호 cctv 수에 따른 어린이 교통사고 발생건수")
> 그래프 제목 설정
## plt.show()
> 그래프 


# 8) if __name__ == '__main__':
> 메인함수
## cctv_filename = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황.csv'
> 읽어올 csv파일 경로 정의
## cctv_table = pd.read_csv(cctv_filename, encoding='CP949', header=0, engine='python')
> 해당 csv파일(='서울시 자치구 목적별 CCTV 설치 현황') 읽어옴
## accident_filename = 'C:/kse/서울시 어린이 교통사고 현황.csv'
> 읽어올 csv파일 경로 정의
## accident_table = pd.read_csv(accident_filename, encoding='CP949', header=0, engine='python')
> 해당 csv파일(='서울시 어린이 교통사고 현황') 읽어옴

## setting_cctv_file(cctv_table)
> '목적별 cctv 설치수'에 관련된 파일 가공
## setting_accident_file(accident_table)
> '어린이 교통사고 현황'에 관련된 파일 가공

## result = setting_analysis_file(setting_merge_file())
> 가공된 두 파일을 병합 후 분석
## draw_graph(result)
> 그래프로 시각화
