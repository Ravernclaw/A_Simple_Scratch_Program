# !/usr/bin/env python
# -*-coding:utf-8-*-
#-*-coding:GBK -*-
import urllib.request
import requests
from bs4 import BeautifulSoup
import pandas as pd

search = str(input('Please input the keywords:'))#关键词
titles = []#keywords you wanna search for
time = []
m = 0
for i in range(1, 103): #The pages you wanna search
	url = "http://data.people.com.cn/rmrb/s?qs=" + '''{"cds":[{"cdr":"AND","cds":[{"fld":"title","cdr":"OR","hlt":"true","vlr":"OR","val":"''' +search+ '''"},{"fld":"subTitle","cdr":"OR","hlt":"true","vlr":"OR","val":"''' +search+ '''"},{"fld":"introTitle","cdr":"OR","hlt":"true","vlr":"OR","val":"''' +search+ '''"}]}],"obs":[{"fld":"dataTime","drt":"DESC"}]}&tr=A&ss=1&pageNo='''+str(i)+'''&pageSize=20'''
	print("url:",url)
	headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
	r = requests.get(url, timeout=30, headers=headers)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	# print(r.text)
	root = BeautifulSoup(r.text, "html.parser")
	table = root.find(attrs={"class": "sreach_div"})
	# print(table)
	rows = table.find_all(attrs={"class": "sreach_li"})
	j = 0
	for row in rows:
		m = m+1
		j = j+1
		mark = row.find_all('a')[0]
		#print(mark)
		print("Save", m, "piece news:",mark.get_text()) 
		record = [mark.get_text(),]
		titles.append(mark.get_text())
		columns = row.find_all('div')
		for col in columns: #iterate colums
			record.append(col.get_text().strip().replace('\n', '').replace('\r', '').replace('\t', ''))
		# print(record)
		time.append(record[1].split("第")[0])
		file = open("./data/"+str(record[1])+".txt", 'w', encoding='UTF-8')
		file.write(str(','.join(record)))
		file.close()

if __name__=="__main__":
	print(titles)
	print(time)
	df1 = pd.DataFrame(data=titles)
	df2 = pd.DataFrame(data=time)
	df = pd.concat([df1, df2], axis=1)
	print(df)
	df.to_csv('./data/titles.csv', encoding='utf_8_sig')
	print('finished')
