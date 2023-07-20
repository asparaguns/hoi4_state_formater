import re
from Value import Value
from Editor import Editor

class Writer(Value):
	def __init__(self, id):
		self.id = id
		self.statesData = list(filter(lambda item : item['id'] == id, Editor().loadCSV("state")))[0]
		self.historyData = list(filter(lambda item : item['id'] == id, Editor().loadCSV("history")))
		self.provincesData = list(filter(lambda item : item['id'] == id, Editor().loadCSV("province")))
		self.projectFKikanData = list(filter(lambda item : item['id'] == id, Editor().loadCSV("projectFKikan")))
		
	def writeAll(self):
		codeList = []
		codeList.append("state = {")
		codeList += self.writeState()
		codeList.append("}")
		print(self.id)
		return codeList
		
	def writeState(self):
		codeList = []
		for effect in self.stateInfomationList:
			if self.statesData[effect] != "":
				codeList.append(effect + " = " + str(self.statesData[effect]))
				if effect == "id":
					codeList.append("name = \"STATE_{}\"".format(str(self.statesData[effect])))
		resourceNum = sum([1 for resource in self.resourceList if self.statesData[resource] != ""])
		codeList.append("")
		if(resourceNum == 1):
			for resource in self.resourceList:
				if(self.statesData[resource] != ""):
						codeList.append("resources = {{\t{0} = {1}\t}}".format(resource, self.statesData[resource]))
						codeList.append("")
						break
		elif(resourceNum > 1):
			codeList.append("resources = {")
			for resource in self.resourceList:
				if(self.statesData[resource] != ""):
					codeList.append("\t{0} = {1}".format(resource, self.statesData[resource]))
			codeList.append("}")
			codeList.append("")
			
		codeList.append("history = {")
		codeList += self.writeHistory()
		codeList.append("}")
		codeList.append("")
		codeList.append("provinces = {")
		
		provinceId = ""
		for province in self.provincesData:
			provinceId += "\t"
			provinceId += str(province["province"])
		codeList.append(provinceId)
		codeList.append("}")
		if self.statesData["local_supplies"] != "":
			codeList.append("local_supplies = " + str(float(self.statesData["local_supplies"])))
		return ['\t' + str(value) for value in codeList]
	def writeHistory(self):
		codeList = []
		codeList1 = []
		codeList2 = []
		code = ""
		ownerTagFlag = False
		for history in self.historyData:
			if history["type"] == "owner":
				ownerTag = history["tag"]
				codeList += ["owner = " + history['tag']]
		for effect in self.historyList:
			for history in self.historyData:
				if effect == history["type"]:
					if history["tag"] != "":
						if history["tag"] == ownerTag:	ownerTagFlag = True
						else:	codeList1.append(history["tag"])
			if ownerTagFlag:
				codeList1 = [ownerTag] + codeList1
				ownerTagFlag = False
			codeList += [effect + " = " + str(value) for value in codeList1]
			codeList1 = []
		for history in self.historyData:
			if history["type"] == "debug_core":
				if history["tag"] != "":
					if history["tag"] == ownerTag:	code = history["tag"]
					else:	codeList2.append(history["tag"])
		if code != "":	codeList2 = [code] + codeList2
		codeList += [str(value) + " = {\tdebug_core = yes\t}" for value in codeList2]
		codeList.append("buildings = {")
		codeList += self.writeBuildings()
		codeList.append("}")
		for province in self.provincesData:
			if province["victory_point"] != "":
				code = "victory_points = {\t"
				code += str(province["province"]) + "\t"
				code += str(province["victory_point"])
				code += "\t}"
				codeList.append(code)
		for history in self.projectFKikanData:
			if history["tag"] != "":
				codeList.append("add_to_array = {{\t{}.pfk_state_array_{} = THIS\t}}".format(history["tag"], str(history["type"])))
		if self.statesData["add_extra_state_shared_building_slots"] != "":
			codeList.append("add_extra_state_shared_building_slots = " + str(self.statesData["add_extra_state_shared_building_slots"]))
		if self.statesData["set_demilitarized_zone"] != "":
			codeList.append("set_demilitarized_zone = " + str(self.statesData["set_demilitarized_zone"]))
		return ['\t' + str(value) for value in codeList]
	def writeBuildings(self):
		codeList = []
		for building in self.stateBuildingsList:
			if self.statesData[building] != "":
				codeList.append(building + " = " + str(self.statesData[building]))
		for building in self.provinceBuildingsList:
			for province in self.provincesData:
				if province[building] != "":
					code = str(province["province"]) + " = {\t"
					code += building + " = " + str(province[building])
					code += "\t}"
					codeList.append(code)
		return ['\t' + str(value) for value in codeList]