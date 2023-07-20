import os
from Value import Value
from Editor import Editor
from Setter import Setter
from Writer import Writer

path = "./states/"
folderfile = os.listdir(path)
stateCSV = []
historyCSV = []
provinceCSV = []
pfkCSV = []
for fileName in folderfile:
	filePath = path + fileName
	code = Editor().loadFile(filePath)
	
	stateCSV += Setter(code).setStateData()
	historyCSV += Setter(code).setHistoryData()
	provinceCSV += Setter(code).setProvinceData()
	pfkCSV += Setter(code).setStateArrayData()
	
Editor().writeCSV("state", Value().stateInfomation, stateCSV)
Editor().writeCSV("history", Value().historyInfomation, historyCSV)
Editor().writeCSV("province", Value().provinceInfomation, provinceCSV)
Editor().writeCSV("projectFKikan", Value().historyInfomation, pfkCSV)
Editor().defaultSortCSV()

for fileName in folderfile:
	filePath = path + fileName
	with open(filePath, 'w') as file:
		file.write("\n".join(Writer(int(Editor().getStateId(fileName))).writeAll()))