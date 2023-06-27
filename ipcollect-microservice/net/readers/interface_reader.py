from utils.common import get_value
from utils.common import expand_range_string

class InterfaceReader():
    def __init__(self, input_dict={}) -> None:
        self.input_dict = input_dict
        self.result = []

    def get_interface_name(self, interface_dict={}):
        return get_value(interface_dict, ["name"], "")

    def get_interface_admin_status(self, interface_dict={}):
        return get_value(interface_dict, ["state", "admin-status"], "")

    def get_interface_operational_status(self, interface_dict={}):
        return get_value(interface_dict, ["state", "oper-status"], "")

    def get_interface_index(self, interface_dict={}, keys =[]):
        if keys == []:
            return get_value(interface_dict, ["state","ifindex"], "")
        return get_value(interface_dict, keys, "")

    def get_interface_mtu(self, interface_dict={}):
        return get_value(interface_dict, ["state","mtu"], "")

    def get_interface_speed(self, interface_dict={}):
        result = get_value(interface_dict, ["ethernet", "state", "negotiated-port-speed"], "")
        return result.split('_')[-1]

    def get_interface_mac(self, interface_dict={}):
        return get_value(interface_dict, ["ethernet", "state", "hw-mac-address"], "")

    def get_interface_vlan_mode(self, interface_dict={}):
        return get_value(interface_dict, ["ethernet", "switched-vlan", "state", "interface-mode"], "None")

    def get_interface_vlans(self, interface_dict={}, interface_vlan_mode='None'):
        if interface_vlan_mode == 'TRUNK':
            result=[]
            tmp_result = get_value(interface_dict, ["ethernet", "switched-vlan", "state", "trunk-vlans"], "1")
            #contiguous ranges
            if isinstance(tmp_result, list):
                for element in tmp_result:
                    tmp_element = expand_range_string(element)
                    result.extend(tmp_element)
                return result
            elif isinstance(tmp_result, str):
                return expand_range_string(tmp_result)
        elif interface_vlan_mode == 'ACCESS':
            result = [get_value(interface_dict, ["ethernet", "switched-vlan", "state", "access-vlan"], "1")]
        return result 

    def get_interface_native_vlan(self, interface_dict={}):
        return get_value(interface_dict, ["ethernet", "switched-vlan", "state", "native-vlan"], "1")
    
    def get_interface_ipv4(self, interface_dict={}):
        if isinstance(get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address"]),list):
            return get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", 0, "ip"], "") + "/" + get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", 0, "config", "prefix-length"], "")
        elif isinstance(get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address"]),dict):
            return get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", "ip"], "") + "/" + get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", "config", "prefix-length"], "")
        return ""

    def get_vlan_interface_ipv4(self, interface_dict={}):
        if isinstance(get_value(interface_dict, ["ipv4", "addresses", "address"]),dict):
            return get_value(interface_dict, ["ipv4", "addresses", "address", "config", "ip"], "") + "/" + get_value(interface_dict, ["ipv4", "addresses", "address", "config", "prefix-length"], "")
        return ""

    def get_interface_type(self, interface_dict={}):
        if "vlan" in interface_dict["name"]:
            return "Vlan"
        if get_value(interface_dict, ["ethernet", "switched-vlan", "state", "interface-mode"], ""):
            return "Bridge"
        if "lo" in interface_dict["name"]:
            return "Loopback"
        return "Other" 

    def read(self):
        for interface in self.input_dict["interfaces"]["interface"]:
            result = {}
            if interface["name"] != "vlan1":
                result["INDEX"] = self.get_interface_index(interface)
                result["NAME"] = self.get_interface_name(interface)
                result["ADMIN_STATUS"] = self.get_interface_admin_status(interface)
                result["OPERATIONAL_STATUS"] = self.get_interface_operational_status(interface)
                result["MTU"] = self.get_interface_mtu(interface)
                result["SPEED"] = self.get_interface_speed(interface)
                result["MACADDR"] = self.get_interface_mac(interface)
                result["IPADDR"] = self.get_interface_ipv4(interface)
                result["TYPE"] = self.get_interface_type(interface)
                result["VLAN_MODE"] = self.get_interface_vlan_mode(interface)
                if result["VLAN_MODE"] != "None":
                    result["VLANS"] = self.get_interface_vlans(interface, result["VLAN_MODE"])
                if result["VLAN_MODE"] == "TRUNK":
                    result["NATIVE_VLAN"] = self.get_interface_native_vlan(interface)
                self.result.append(result)
            else:
                for subinterface in interface["subinterfaces"]["subinterface"]:
                    result = {}
                    result["INDEX"] = self.get_interface_index(subinterface, ["index"])
                    result["NAME"] = "vlan"+result["INDEX"] 
                    result["ADMIN_STATUS"] = self.get_interface_admin_status(subinterface)
                    result["OPERATIONAL_STATUS"] = self.get_interface_operational_status(subinterface)
                    result["MTU"] = "" 
                    result["SPEED"] = ""
                    result["MACADDR"] = "" 
                    result["IPADDR"] = self.get_vlan_interface_ipv4(subinterface)
                    result["TYPE"] = "Vlan"
                    result["VLAN"] = result["INDEX"]
                    self.result.append(result)

            
