import pandas as pd

a = pd.DataFrame()#{"aaa":[9,8,7,6,5,4,3,2,1],'bbb':[1,2,3,4,5,6,7,8,9]}
b = pd.DataFrame({'ccc':[1,2,3,4,5,6,7,8,9]})
c = pd.DataFrame({"aaa":[9,8,7,6,5,4,3,2,1],'bbb':[1,2,3,4,5,6,7,8,9]})#
# c = pd.merge(a,b,'left')
# d = pd.merge(b,a,'left')

a = pd.concat([a,c,b],1)
# a = pd.merge(a,c,'right',left_index=True,right_index=True)
a.columns = ['a','b','c']
print(a)
# print(d)