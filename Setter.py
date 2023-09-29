from Value import Value
from Getter import Getter

class Setter(Value):
	def __init__(self, codes):
		self.codes = Getter(codes)
	
	def setStateData(self):
		allStatesInfomation = []
		temp = {}
		for state in self.stateInfomation:
			temp[state] = self.codes.getValue(state)
		allStatesInfomation.append(temp)
		return allStatesInfomation
	
	def setHistoryData(self):
		allHistoriesInfomation = []
		temp = {}
		if self.codes.getValueList("owner") != None:
			temp["id"] = self.codes.getValue("id")
			temp["tag"] = self.codes.getValueList("owner")[0]
			temp["type"] = "owner"
		allHistoriesInfomation.append(temp)
		for effect in self.historyList:
			if self.codes.getValueList(effect) != None:
				for tag in self.codes.getValueList(effect):
					temp = {}
					temp["id"] = self.codes.getValue("id")
					temp["tag"] = tag
					temp["type"] = effect
					allHistoriesInfomation.append(temp)
		if self.codes.getDebugCore() != None:
			for debugCore in self.codes.getDebugCore():
				temp = {}
				temp["id"] = self.codes.getValue("id")
				temp["tag"] = debugCore
				temp["type"] = "add_debug_core_PREV"
				allHistoriesInfomation.append(temp)
		return allHistoriesInfomation
	def setStateArrayData(self):
		allStateArrayData = []
		if self.codes.getStateArray() != None:
			for key, value in self.codes.getStateArray().items():
				temp = {}
				temp["id"] = self.codes.getValue("id")
				temp["tag"] = key
				temp["type"] = value
				allStateArrayData.append(temp)
		return allStateArrayData
	def setProvinceData(self):
		allProvincesInfomation = []
		provinceBuildings = {}
		victoryPoints = {}
		if self.codes.getVictoryPoints() != None:
			for victoryPoint in self.codes.getVictoryPoints():
				victoryPoints[victoryPoint.split()[0]] = int(float(victoryPoint.split()[1]))
		
		for building in self.provinceBuildingsList:
			if self.codes.getProvinceBuildings(building) != "":
				provinceBuildings[building] = self.codes.getProvinceBuildings(building)
			
		for province in self.codes.getProvinces():
			temp = {}
			temp["id"] = self.codes.getValue("id")
			temp["province"] = province
			temp["victory_point"] = victoryPoints[province] if province in victoryPoints else None
			for building in self.provinceBuildingsList:
				temp[building] = provinceBuildings[building][province] if province in provinceBuildings[building] else None
			allProvincesInfomation.append(temp)
		return allProvincesInfomation