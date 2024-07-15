# 데이터프레임 만들기

import pandas as pd


1. 딕셔너리로 만들기

dic = { 'name' : [ 'a', 'b', 'c'] , 'age' : [10 , 15, 17] , 'sex' : ['f', 'm', 'f'] }
DF = pd.DataFrame(dic)
print(DF)

  name  age
0    a   10
1    b   15
2    c   17


2. 리스트로 만들기

a=['name', 'age', 'sex']
b=['a',10,'f']
c=['b',15,'m']
d=['c',17,'f']

list = [b,c,d]
Df = pd.DataFrame(list, columns = a)
print(Df)


# 데이터 프레임 행, 열 갯수 확인하기
print(Df.shape)       # (3,3)


# 데이터 프레임 컬럼명 가져오기
print(Df.columns)     # Index(['name', 'age', 'sex'], dtype='object')


# 특정 컬럼 데이터 가져오기
print(Df['name'])

0    a
1    b
2    c
Name: name, dtype: object



# 특정 행 가져오기 (head, tail, .loc)

print(Df.head(1))  #첫번째

print(Df.tail(1))  #마지막

print(DF.loc[3])   #세번째


# info , describe
print(Df.info())

<class 'pandas.core.frame.DataFrame'>
RangeIndex: 3 entries, 0 to 2
Data columns (total 3 columns):
 #   Column  Non-Null Count  Dtype 
---  ------  --------------  ----- 
 0   name    3 non-null      object
 1   age     3 non-null      int64 
 2   sex     3 non-null      object
dtypes: int64(1), object(2)
memory usage: 204.0+ bytes
None


print(Df.describe)  # 숫자데이터에 대한 통계수치들

             age
count   3.000000
mean   14.000000
std     3.605551
min    10.000000
25%    12.500000
50%    15.000000
75%    16.000000
max    17.000000
