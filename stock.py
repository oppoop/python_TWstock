"""

-----外資與投信買賣超-----
-----對個股成交比例-----

"""

import datetime
import time
import requests
from bs4 import BeautifulSoup
import csv #載入csv套件
import pandas as pd #載入pandas 取名為pd
import io
date=str(datetime.date.today())# 取今天的日期
date=date.replace("-", "")#去除日期"-"的符號
#date='20211001'

"""
下面網址為證交所每日收盤行情 不含權證
"""
url="https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date="+date+"&type=ALLBUT0999"
page=requests.get(url) # 取得當天收盤行情資料
use_text=page.text.splitlines() #page 資料分成一行一行處理
"""
用for迴圈 找出要的資料位址起始 initial_point : i
"""
for i,text in enumerate(use_text):
        if text == '"證券代號","證券名稱","成交股數","成交筆數","成交金額","開盤價","最高價","最低價","收盤價","漲跌(+/-)","漲跌價差","最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量","本益比",':
            initial_point = i
            break
"""
1.將資料轉成dataframe格式
"""
df = pd.read_csv(io.StringIO(''.join([text[:-1] + '\n' for text in use_text[initial_point:]])))
df['證券代號'] = df['證券代號'].str.replace('=','')#刪除 證券代號欄位的=符號
df['證券代號'] = df['證券代號'].str.replace('"','')#刪除 證券代號欄位的"符號
"""
1.將成交股數rename:成交張數，並且轉換為int
2.刪除不需要的欄位 :"最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量"

"""
df['成交股數'] = df['成交股數'].str.replace(',','').astype(int)
df=df.rename(columns={'成交股數':'成交張數'})
df["成交張數"]=(df["成交張數"]/1000).astype(int)
drop_columns=["最後揭示買價","最後揭示買量","最後揭示賣價","最後揭示賣量"]
df=df.drop(columns=drop_columns)

for i in range(len(df["開盤價"])):
    if df["開盤價"][i]=="--":
        df=df.drop(index=i)
    

"""
1.刪除成交張數為0的股票
2.將所有欄位轉換為格式化
"""
# for i,data in enumerate(df["開盤價"]):
#     if data=="--":
#         df=df.drop(index=i)
df['開盤價']=df['開盤價'].str.replace(',','').astype(float)
df['收盤價']=df['收盤價'].str.replace(',','').astype(float)
df['最高價']=df['最高價'].str.replace(',','').astype(float)
df['最低價']=df['最低價'].str.replace(',','').astype(float)
df['成交筆數']=df['成交筆數'].str.replace(',','').astype(int)
df['成交金額']=df['成交金額'].str.replace(',','').astype(float)# 有問題要注意 
df['本益比']=df['本益比'].str.replace(',','').astype(float)

#--------------------------------------------------------------------------

import datetime
import time
import requests
from bs4 import BeautifulSoup
import csv #載入csv套件
import pandas as pd #載入pandas 取名為pd
import datetime
import io
"""
下面網址為證交所每日三大法人買賣超日報 不含權證
"""
url_1="https://www.twse.com.tw/fund/T86?response=csv&date="+date+"&selectType=ALLBUT0999"

page_1=requests.get(url_1) # 取得當天收盤行情資料
use_text_1=page_1.text.splitlines() #page 資料分行處理
"""
用for迴圈 找出要的資料位址起始 initial_point : i
"""
start_str='"證券代號","證券名稱","外陸資買進股數(不含外資自營商)","外陸資賣出股數(不含外資自營商)","外陸資買賣超股數(不含外資自營商)","外資自營商買進股數","外資自營商賣出股數","外資自營商買賣超股數","投信買進股數","投信賣出股數","投信買賣超股數","自營商買賣超股數","自營商買進股數(自行買賣)","自營商賣出股數(自行買賣)","自營商買賣超股數(自行買賣)","自營商買進股數(避險)","自營商賣出股數(避險)","自營商買賣超股數(避險)","三大法人買賣超股數",'
for i,text in enumerate(use_text_1):
        if text == start_str:
            initial_point = i
            break
df_1 = pd.read_csv(io.StringIO(''.join([text[:-1] + '\n' for text in use_text_1[initial_point:]])))
df_1['證券代號'] = df_1['證券代號'].str.replace('=','')#刪除 證券代號欄位的=符號
df_1['證券代號'] = df_1['證券代號'].str.replace('"','')#刪除 證券代號欄位的"符號
df_1=df_1.dropna()
drop_columns_1=["外陸資買進股數(不含外資自營商)","外陸資賣出股數(不含外資自營商)","外資自營商買進股數",
                "外資自營商賣出股數","投信買進股數","投信賣出股數","外資自營商買賣超股數",
                "自營商買賣超股數","自營商買進股數(自行買賣)","自營商賣出股數(自行買賣)",
                "自營商買進股數(避險)","自營商賣出股數(避險)"]
df_1=df_1.drop(columns=drop_columns_1)

df_1["投信買賣超股數"]=df_1["投信買賣超股數"].str.replace(',','').astype(int)
df_1["外陸資買賣超股數(不含外資自營商)"]=df_1["外陸資買賣超股數(不含外資自營商)"].str.replace(',','').astype(int)
df_1["自營商買賣超股數(自行買賣)"]=df_1["自營商買賣超股數(自行買賣)"].str.replace(',','').astype(int)
df_1["自營商買賣超股數(避險)"]=df_1["自營商買賣超股數(避險)"].str.replace(',','').astype(int)
df_1["三大法人買賣超股數"]=df_1["三大法人買賣超股數"].str.replace(',','').astype(int)
rename_columns_1=["證券代號","證券名稱","外資買賣超張數","投信買賣超張數",
                  "自營商買賣超張數","自營商(避險)買賣超張數","三大法人買賣超張數"]
df_1.columns=rename_columns_1
df_1["外資買賣超張數"]=round(df_1["外資買賣超張數"]/1000)# 買賣超股數 轉換成張數 四捨五入
df_1["投信買賣超張數"]=round(df_1["投信買賣超張數"]/1000)# 買賣超股數 轉換成張數 四捨五入
df_1["自營商買賣超張數"]=round(df_1["自營商買賣超張數"]/1000)# 買賣超股數 轉換成張數 四捨五入
df_1["自營商(避險)買賣超張數"]=round(df_1["自營商(避險)買賣超張數"]/1000)# 買賣超股數 轉換成張數 四捨五入
df_1["三大法人買賣超張數"]=round(df_1["三大法人買賣超張數"]/1000)# 買賣超股數 轉換成張數 四捨五入



df_final=pd.merge(df_1,df, left_on="證券代號",right_on="證券代號")
df_final=df_final.rename(columns={"證券名稱_x":"證券名稱"})
df_final=df_final.drop(columns=["證券名稱_y"])

a=df_final["外資買賣超張數"]/df_final["成交張數"] # a:外資買賣超占成交張數比例
a=round(a,2) #取小數點第二位
df_final.insert(1,column="外資買超占比",value=a)

b=df_final["投信買賣超張數"]/df_final["成交張數"] # a:外資買賣超占成交張數比例
b=round(b,2) #取小數點第二位
df_final.insert(1,column="投信買超占比",value=b)
"""
--------------------------------------------------------------------
籌碼分析: 外資買超比:10%以上 & 成交張數大於5000張
"""
mask=((df_final["外資買超占比"]>0.1) & (df_final["成交張數"]>5000))
print(date+" 籌碼分析: 外資買超比:10%以上 & 成交張數大於5000張")
df2=df_final[mask].head(50)
df2=df2[['證券代號','證券名稱','外資買超占比']]
df2=df2.sort_values('外資買超占比',ascending=False)

te1=''  #回覆文字檔1
for i in df2.values:
    for ii in i:
        te1=te1+"  "+str(ii)
    te1=te1+'\n'
print(te1)
print("------------------------------------------------------------")
"""
--------------------------------------------------------------------
籌碼分析: 投信買超比:5%以上 & 成交張數大於3000張
"""
mask_1=((df_final["投信買超占比"]>0.05) & (df_final["成交張數"]>3000))
print(date+" 籌碼分析: 投信買超比:5%以上 & 成交張數大於3000張")
df3=df_final[mask_1].head(50)
df3=df3[['證券代號','證券名稱','投信買超占比']]
df3=df3.sort_values('投信買超占比',ascending=False)

te2=''  #回覆文字檔2
for i in df3.values:
    for ii in i:
        te2=te2+"  "+str(ii)
    te2=te2+'\n'
print(te2)
print("------------------------------------------------------------")
#---------------------------------------------------------------------
"""
--------------------------------------------------------------------
籌碼分析: 外資"賣"超比:20%以上 & 成交張數大於5000張
"""
mask_2=((df_final["外資買超占比"]<-0.2) & (df_final["成交張數"]>5000))
print(date+" 籌碼分析: 外資<賣>超比:30%以上 & 成交張數大於5000張")
df4=df_final[mask_2].head(20)
df4=df4[['證券代號','證券名稱','外資買超占比']]
df4=df4.sort_values('外資買超占比')

te1=''  #回覆文字檔1
for i in df4.values:
    for ii in i:
        te1=te1+"  "+str(ii)
    te1=te1+'\n'
print(te1)
print("------------------------------------------------------------")
"""
--------------------------------------------------------------------
籌碼分析: 投信賣超比:5%以上 & 成交張數大於3000張
"""
mask_3=((df_final["投信買超占比"]<-0.05) & (df_final["成交張數"]>3000))
print("籌碼分析: 投信<賣>超比:0.05%以上 & 成交張數大於3000張")
df5=df_final[mask_3].head(50)
df5=df5[['證券代號','證券名稱','投信買超占比']]
df5=df5.sort_values('投信買超占比')

te2=''  #回覆文字檔2
for i in df5.values:
    for ii in i:
        te2=te2+"  "+str(ii)
    te2=te2+'\n'
print(te2)
print("------------------------------------------------------------")

# mask=df_final["證券代號"]=="5425"
# print(df_final[mask])

# a=df_final.groupby("證券代號")
# b=a.get_group("5425")


















    





























