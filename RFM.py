# -*- coding: utf-8 -*-
"""
Author: Dolly Chen
RFM 分析模型
"""
import pandas as pd
import datetime
import glob
import re

df=pd.read_excel('superstore.xlsx',sheet_name='2018')
df['Order Date'] = pd.to_datetime(df['Order Date'],errors='coerce')
df['購買日期_今日相差天數'] = pd.to_datetime('2018-11-10')-df['Order Date']
df['購買日期_今日相差天數']= df['購買日期_今日相差天數'].dt.days
newdf = df[['購買日期_今日相差天數','Order ID','Sales','Customer ID']].dropna()
newdf['Sales'] = newdf['Sales'].astype(str)
newdf['Sales'] = newdf['Sales'].apply(lambda x:x if re.match(r'\d+.\d+',x) else 0).apply(float)
df_RFM = newdf.groupby('Customer ID',as_index=False).agg({'購買日期_今日相差天數':min,'Order ID':'count','Sales':sum})
df_RFM['購買日期_今日相差天數'] = df_RFM['購買日期_今日相差天數'].apply(lambda x:abs(x))
df_RFM.columns = ['Customer ID','R','F','M']
### 判斷R是否大於等於平均
df_RFM.loc[df_RFM['R'] >= df_RFM['R'].mean(), 'R_S']=1
df_RFM.loc[df_RFM['R'] <df_RFM['R'].mean(), 'R_S']=2
### 判斷F, M是否大於等於平均, F&M的值越大越好
df_RFM.loc[df_RFM['F'] <= df_RFM['F'].mean(), 'F_S']=1
df_RFM.loc[df_RFM['F'] >df_RFM['F'].mean(), 'F_S']=2
df_RFM.loc[df_RFM['M'] <= df_RFM['M'].mean(), 'M_S']=1
df_RFM.loc[df_RFM['M'] >df_RFM['M'].mean(), 'M_S']=2
df_RFM['RFM'] = 100*df_RFM['R_S']+10*df_RFM['F_S']+df_RFM['M_S']
## 定義RFM分數和客戶類型
RFM_type=pd.DataFrame( data={'RFM':[111,112,121,122,211,212,221,222],
              'type':['潛在客戶','挽留客戶','一般保持客戶','重點保持客戶',
                      '一般發展客戶','重點發展客戶','一般價值客戶','高價值客戶']})
df_RFM1=df_RFM.merge(RFM_type, how='left',on='RFM')
## 把顧客類型欄位merge到前資料
df_new=pd.merge(df, df_RFM1.drop(columns=['R','F','M','R_S','F_S','M_S']), on='Customer ID', how='inner')
# df_new.to_excel('superstore_cutomeradd.xlsx', index=False)
display(df_new)


