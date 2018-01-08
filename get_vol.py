#处理从wind下载的数据，目前仅读取xls文件并提取收盘价，然后按不同周期窗口计算波动率
#不进行年化处理，每年交易周期个数可自行设置

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# cd D:\hs300

def get_vola(data_source,period='W-FRI'):
	hy=pd.read_excel(data_source)#源数据为wind下载的xls数据，数据名称例子603799.sh.xls
	hy.set_index('日期',inplace=True)
	hyc=hy[['收盘价(元)']].copy()
	hyc.dropna(inplace=True)
	#hyc.plot()
	#定义波动率窗口
	if period[0]=='D':
		wd=240
	elif period[0]=='W':
		wd=52
	else:
		wd=12
	try:
		hycw=hyc.resample(period).last()
		hycw['logret']=np.log(hycw['收盘价(元)']/hycw['收盘价(元)'].shift(1))
		hycw.dropna(inplace=True)
		hycw['vola']=hycw['logret'].rolling(window=wd).std()
	except ValueError as e:
		print(e)
	return hycw[['vola']].copy()

