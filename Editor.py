import csv
import re
import pandas as pd

class Editor:
	def removeComments(self, text):
		return re.sub(r'#.*', '', text)
	def loadFile(self, fileName):
		with open(fileName, 'r', encoding = "utf-8") as file:
			t = file.read()
			return self.removeComments(t)
	def loadCSV(self, fileName):
		with open('csv/' + fileName + '.csv', 'r',encoding = "utf-8") as file:
			return self.convertType(csv.DictReader(file))

	def loadList(self, fileName):
		with open('list/' + fileName + '.txt', 'r', encoding = 'utf-8') as file:
			return file.read().splitlines()
		
	def convertType(self, listType):
		tmpList = []
		for dicType in listType:
			tmp = {}
			for key, value in dicType.items():
				if re.match(r'^[+-]?\d+\.\d+$', value):
					tmp[key] = float(value)
				elif re.match(r'^[+-]?\d+$', value):
					tmp[key] = int(value)
				else:
					tmp[key] = value
			tmpList.append(tmp)
		return tmpList
	def writeCSV(self, fileName, filedeName, data):
		with open('csv/' + fileName + '.csv', 'w', newline='', encoding = 'utf-8') as file:
			writer = csv.DictWriter(file, fieldnames = filedeName)
			writer.writeheader()
			writer.writerows(data)
	def sortCSV(self, filePath, sortKey):
		# CSVファイルを辞書型として読み込み、データをリストとして保持
		with open(filePath, 'r', newline='') as csvfile:
			csvreader = csv.DictReader(csvfile)
			data = list(csvreader)
		# データを指定したキーでソート
		sorted_data = sorted(data, key=lambda x: x[sortKey]) if sortKey == "tag" else sorted(data, key=lambda x: int(x[sortKey]))
		# ソート結果を元のファイルに上書きする
		with open(filePath, 'w', newline='') as csvfile:
			fieldnames = csvreader.fieldnames
			csvwriter = csv.DictWriter(csvfile, fieldnames=fieldnames)
			csvwriter.writeheader()
			csvwriter.writerows(sorted_data)
	def defaultSortCSV(self):
		Editor().sortCSV("csv/state.csv", "id")
		Editor().sortCSV("csv/history.csv", "id")
		Editor().sortCSV("csv/province.csv", "province")
		Editor().sortCSV("csv/province.csv", "id")
		Editor().sortCSV("csv/projectFKikan.csv", "tag")
		Editor().sortCSV("csv/projectFKikan.csv", "type")
		Editor().sortCSV("csv/projectFKikan.csv", "id")
	def getStateId(self, fileName):
		return re.search("\d+", fileName).group()
	def measure_times(self, start, end):	#時間計測
		times = int(end - start)
		elapsed_hour = times // 3600
		elapsed_minute = (times % 3600) // 60
		elapsed_second = (times % 3600 % 60)
		print(str(elapsed_hour).zfill(2) + ":" + str(elapsed_minute).zfill(2) + ":" + str(elapsed_second).zfill(2))