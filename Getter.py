import re

class Getter:
	def __init__(self, code):
		self.code = code
	
	def getValue(self, pattern):
		self.pattern = pattern + "\s*=\s*\"?(\w+)\"?"
		match = re.search(self.pattern, self.code)
		return match.group(1) if match else None
	
	def getValueList(self, pattern):
		self.pattern = pattern + "\s*=\s*(\w+)"
		match = re.findall(self.pattern, self.code)
		return match if match else None
	
	def getDebugCore(self):
		self.pattern = "(\w+)\s*=\s*{\s*debug_core\s*=\s*yes\s*}"
		match = re.findall(self.pattern, self.code)
		return match if match else None
	
	def getStateArray(self):
		self.pattern = r"add_to_array\s*=\s*{[^}]*\b(.{3})\.pfk_state_array_(\d+)\s*=\s*THIS\s*}"
		match = re.findall(self.pattern, self.code)
		return dict(match) if match else None
	
	def getProvinces(self):
		self.pattern = r"provinces\s*=\s*{([^{}]*)}"
		match = re.findall(r'\b\d+\b', re.search(self.pattern, self.code).group(1))
		return match if match else None
	
	def getProvinceBuildings(self, building):
		buildingFlag = False
		provinceFlag = False
		province = {}
		for t in self.code.split("\n"):
			if(re.search(r"buildings", t)):
				buildingFlag = True
			if(buildingFlag):
				if(re.findall(r"(\d+)\s*=", t)):
					key = re.search(r"(\d+)\s*=", t).group(1)
					provinceFlag = True
				
				if(provinceFlag):
					a = re.findall(r"(\w+)\s*=\s*\d+", t)
					if(a == [building]):
						value = re.search(r"\s*=\s*(\d+)", t)
						province[key] = value.group(1)
				elif(provinceFlag and "}" in t):
					provinceFlag = False
				elif(not provinceFlag and "}" in t):
					buildingFlag = False
		return province
	def getVictoryPoints(self):
		pattern = r'victory_points\s*=\s*{((?:\s*\d+\s*)+)}'
		match = re.findall(pattern, self.code)
		return match if match else None