import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import numpy as np

# 한글 설정
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)


# cctv.csv파일 가공
def setting_cctv_file(_cctv_table):
    _cctv_table = _cctv_table.dropna()  # 값을 가지고 있지 않은 데이터 삭제

    _cctv_table.to_csv("./서울시 자치구 목적별 CCTV 설치 현황_가공.csv", encoding="cp949", mode='w', index=True)


# accident.csv파일 가공
def setting_accident_file(_accident_table):
    _accident_table = _accident_table.drop(_accident_table.index[0])  # 필요없는 행 삭제
    _accident_table = _accident_table.dropna()  # 값을 가지고 있지 않은 데이터 삭제
    _accident_table.sort_values(by='지역', inplace=True)  # 지역을 기준으로 오름차순
    _accident_table['어린이보호구역내 어린이 교통사고 발생건수'] = np.where(_accident_table['어린이보호구역내 어린이 교통사고 발생건수'] == '-', 0,
                                                         _accident_table['어린이보호구역내 어린이 교통사고 발생건수'])  # 데이터 값'-'을 '0'으로 수정

    _accident_table.to_csv("./서울시 어린이 교통사고 현황_가공.csv", encoding="cp949", mode='w', index=True)


# cctv_modify.csv파일과 accident_modify.csv파일 병합
def setting_merge_file():
    cctv_filename_modify = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황_가공.csv'
    cctv_table_modify = pd.read_csv(cctv_filename_modify, encoding='CP949', header=0, engine='python')
    accident_filename_modify = 'C:/kse/서울시 어린이 교통사고 현황_가공.csv'
    accident_table_modify = pd.read_csv(accident_filename_modify, encoding='CP949', header=0, engine='python')

    merge_table = pd.concat([cctv_table_modify['기관명'], cctv_table_modify['어린이 보호'],
                             accident_table_modify['어린이보호구역내 어린이 교통사고 발생건수']], axis=1)  # 데이터 병합
    merge_table.rename(columns={"어린이 보호": "어린이 보호 cctv수"}, inplace=1)  # 컬럼명 수정
    merge_table['cctv수 범위'] = merge_table['어린이 보호 cctv수'].apply(cctv_category)  # 새로운 컬럼 추가후 값 저장

    merge_table.to_csv("./서울시 어린이 교통사고 발생건수와 어린이 보호 cctv수.csv", encoding="cp949", mode='w', index=False)
    return merge_table


# cctv 개수 범위 지정
def cctv_category(x):
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


# cctv 설치 수와 어린이 교통사고 발생건수 분석
def setting_analysis_file(_merged_table):
    myData = []

    cctv_category_unique_value = sorted(_merged_table['cctv수 범위'].unique())  # cctv범위의 고유값을 오름차순으로 정렬 / 출력값 : [0,1,2,3,4,5]

    for i in cctv_category_unique_value:
        myData_j = []
        for j in range(1):
            totalSum = _merged_table['어린이보호구역내 어린이 교통사고 발생건수'][_merged_table['cctv수 범위'] == i].sum()  # cctv범위가 i(= 0~5)일때 해당 지역의 교통사고 발생건수 총합
            totalCount = _merged_table['어린이 보호 cctv수'][_merged_table['cctv수 범위'] == i].count()  # cctv범위가 i(= 0~5)일때 범위내 지역수
            totalAverage = round(totalSum / totalCount, 1)  # cctv범위내 교통사고 발생건수 평균
            myData_j.append(totalSum)
            myData_j.append(totalCount)
            myData_j.append(totalAverage)
        myData.append(myData_j)

    myData_table = pd.DataFrame(myData, columns=('범위내 어린이 교통사고 발생건수 총합 '
                                                 , '범위내 지역수', '범위내 어린이 교통사고 발생건수 평균'))
    category = ['100미만', '100이상 200미만', '200이상 300미만', '300이상 400미만', '400이상 500미만', '500이상']
    myData_table["범위"] = category  # '범위' 컬럼 추가

    myData_table.to_csv("./Result.csv", encoding="cp949", mode='w', index=True)
    return myData_table


# 시각화
def draw_graph(_result):
    sns.pointplot(x="범위", y="범위내 어린이 교통사고 발생건수 평균", data=_result)  # 점선 그래프로 시각화
    plt.title("2018년도 어린이 보호 cctv 수에 따른 어린이 교통사고 발생건수")
    plt.show()


# 메인함수
if __name__ == '__main__':
    cctv_filename = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황.csv'
    cctv_table = pd.read_csv(cctv_filename, encoding='CP949', header=0, engine='python')
    accident_filename = 'C:/kse/서울시 어린이 교통사고 현황.csv'
    accident_table = pd.read_csv(accident_filename, encoding='CP949', header=0, engine='python')

    setting_cctv_file(cctv_table)  # 목적별 cctv 설치수에 관련된 파일 가공
    setting_accident_file(accident_table)  # 어린이 교통사고 현황에 관련된 파일 가공

    result = setting_analysis_file(setting_merge_file())  # 가공된 두 파일을 병합 후 분석
    draw_graph(result)
