import pandas as pd

a=['name', 'age', 'sex']
b=['a',10,'f']
c=['b',15,'m']
d=['c',17,'f']

list = [b,c,d]

data= pd.DataFrame(list, columns = a)



# .iloc[]   ~ > .loc과 달리 i (=index) 인덱싱을 통해 일부 행, 컬럼을 불러올 수 있음


data.iloc[0:2] // 첫번째 ~ 두번째 행 가져오기


data.iloc[[0,2]] // 첫번째, 세번째 행 가져오기


data.iloc[:,1] // 두번째 컬럼만 가져오기
