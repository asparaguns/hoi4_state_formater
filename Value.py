from Editor import Editor
class Value:
	#state
	stateInfomationList = Editor().loadList("stateInfomationList")
	stateBuildingsList = Editor().loadList("stateBuildingsList")
	resourceList = Editor().loadList("resourceList")
	stateInfomation = stateInfomationList + ["add_extra_state_shared_building_slots", "set_demilitarized_zone", "local_supplies"] + stateBuildingsList + resourceList
	#history
	historyList = ["add_core_of", "add_claim_by"]
	historyInfomation = ["id", "tag", "type"]
	#procince
	provinceBuildingsList = Editor().loadList("provinceBuildingsList")
	provinceInfomation = ["id", "province", "victory_point"] + provinceBuildingsList