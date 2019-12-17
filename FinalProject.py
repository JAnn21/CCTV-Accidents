import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import font_manager, rc
import numpy as np

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)



def setting_cctv_file(_cctv_table):
    _cctv_table = _cctv_table.dropna()

    _cctv_table.to_csv("./서울시 자치구 목적별 CCTV 설치 현황_가공.csv", encoding="cp949", mode='w', index=True)


# accident.csv파일 가공
def setting_accident_file(_accident_table):
    _accident_table = _accident_table.drop(_accident_table.index[0])
    _accident_table = _accident_table.dropna()
    _accident_table.sort_values(by='지역', inplace=True)
    _accident_table['어린이보호구역내 어린이 교통사고 발생건수'] = np.where(_accident_table['어린이보호구역내 어린이 교통사고 발생건수'] == '-', 0,
                                                         _accident_table['어린이보호구역내 어린이 교통사고 발생건수'])

    _accident_table.to_csv("./서울시 어린이 교통사고 현황_가공.csv", encoding="cp949", mode='w', index=True)



def setting_merge_file():
    cctv_filename_modify = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황_가공.csv'
    cctv_table_modify = pd.read_csv(cctv_filename_modify, encoding='CP949', header=0, engine='python')
    accident_filename_modify = 'C:/kse/서울시 어린이 교통사고 현황_가공.csv'
    accident_table_modify = pd.read_csv(accident_filename_modify, encoding='CP949', header=0, engine='python')

    merge_table = pd.concat([cctv_table_modify['기관명'], cctv_table_modify['어린이 보호'],
                             accident_table_modify['어린이보호구역내 어린이 교통사고 발생건수']], axis=1)
    merge_table.rename(columns={"어린이 보호": "어린이 보호 cctv수"}, inplace=1)
    merge_table['cctv수 범위'] = merge_table['어린이 보호 cctv수'].apply(cctv_category)

    merge_table.to_csv("./서울시 어린이 교통사고 발생건수와 어린이 보호 cctv수.csv", encoding="cp949", mode='w', index=False)
    return merge_table



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



def setting_analysis_file(_merged_table):
    myData = []

    cctv_category_unique_value = sorted(_merged_table['cctv수 범위'].unique())

    for i in cctv_category_unique_value:
        myData_j = []
        for j in range(1):
            totalSum = _merged_table['어린이보호구역내 어린이 교통사고 발생건수'][_merged_table['cctv수 범위'] == i].sum()
            totalCount = _merged_table['어린이 보호 cctv수'][_merged_table['cctv수 범위'] == i].count()
            totalAverage = round(totalSum / totalCount, 1)
            myData_j.append(totalSum)
            myData_j.append(totalCount)
            myData_j.append(totalAverage)
        myData.append(myData_j)

    myData_table = pd.DataFrame(myData, columns=('범위내 어린이 교통사고 발생건수 총합 '
                                                 , '범위내 지역수', '범위내 어린이 교통사고 발생건수 평균'))
    category = ['100미만', '100이상 200미만', '200이상 300미만', '300이상 400미만', '400이상 500미만', '500이상']
    myData_table["범위"] = category

    myData_table.to_csv("./Result.csv", encoding="cp949", mode='w', index=True)
    return myData_table



def draw_graph(_result):
    sns.pointplot(x="범위", y="범위내 어린이 교통사고 발생건수 평균", data=_result)
    plt.title("2018년도 어린이 보호 cctv 수에 따른 어린이 교통사고 발생건수")
    plt.show()



if __name__ == '__main__':
    cctv_filename = 'C:/kse/서울시 자치구 목적별 CCTV 설치 현황.csv'
    cctv_table = pd.read_csv(cctv_filename, encoding='CP949', header=0, engine='python')
    accident_filename = 'C:/kse/서울시 어린이 교통사고 현황.csv'
    accident_table = pd.read_csv(accident_filename, encoding='CP949', header=0, engine='python')

    setting_cctv_file(cctv_table)
    setting_accident_file(accident_table)

    result = setting_analysis_file(setting_merge_file())
    draw_graph(result)
