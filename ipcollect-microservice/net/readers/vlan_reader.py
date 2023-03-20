import json
from utils.common import get_value

class VlanReader():
    def __init__(self, input_dict={}) -> None:
        self.input_dict = input_dict
        self.result = []

    def get_vlan_name(self, vlan_dict={}):
        return get_value(vlan_dict, ["state", "name"], "")

    def get_vlan_id(self, vlan_dict={}):
        return get_value(vlan_dict, ["state", "vlan-id"], "")

    def get_vlan_members(self, vlan_dict={}):
        result = []
        members = get_value(vlan_dict, ["members", "member"], "")
        if isinstance(members, list):
            for member in members:
                result.append(get_value(member, ["state", "interface"], ""))
        elif isinstance(members, dict):
            result.append(get_value(members, ["state", "interface"]))
        return result
    
    def read(self):
        vlans = self.input_dict["network-instances"]["network-instance"]["vlans"]["vlan"]
        if isinstance(vlans, list):
            for vlan in vlans:
                result = {}
                result["NAME"] = self.get_vlan_name(vlan)
                result["VID"] = self.get_vlan_id(vlan)
                result["BRIDGE_GROUP"] = "1"
                self.result.append(result)
        elif isinstance(vlans, dict):
            result = {}
            result["NAME"] = self.get_vlan_name(vlans)
            result["VID"] = self.get_vlan_id(vlans)
            result["BRIDGE_GROUP"] = "1"
            self.result.append(result)
        #add default vlan which is no returned by netconf
        self.result.append({
                          "NAME": "default_vlan",
                          "VID": "1",
                          "BRIDGE_GROUP": "1"
                      })


