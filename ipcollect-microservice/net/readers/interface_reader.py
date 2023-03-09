from net.reader import Reader

class InterfaceReader(Reader):
    def __init__(self, input_dict={}) -> None:
        self.input_dict = input_dict
        self.result = []

    def get_interface_name(self, interface_dict={}):
        return super().get_value(interface_dict, ["name"], "")

    def get_interface_admin_status(self, interface_dict={}):
        return super().get_value(interface_dict, ["state", "admin-status"], "")

    def get_interface_operational_status(self, interface_dict={}):
        return super().get_value(interface_dict, ["state", "oper-status"], "")

    def get_interface_index(self, interface_dict={}, keys =[]):
        if keys == []:
            return super().get_value(interface_dict, ["state","ifindex"], "")
        return super().get_value(interface_dict, keys, "")

    def get_interface_mtu(self, interface_dict={}):
        return super().get_value(interface_dict, ["state","mtu"], "")

    def get_interface_speed(self, interface_dict={}):
        return super().get_value(interface_dict, ["ethernet", "state", "negotiated-port-speed"], "")

    def get_interface_mac(self, interface_dict={}):
        return super().get_value(interface_dict, ["ethernet", "state", "hw-mac-address"], "")

    def get_interface_ipv4(self, interface_dict={}):
        if isinstance(super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address"]),list):
            return super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", 0, "ip"], "") + "/" + super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", 0, "config", "prefix-length"], "")
        elif isinstance(super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address"]),dict):
            return super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", "ip"], "") + "/" + super().get_value(interface_dict, ["subinterfaces", "subinterface", "ipv4", "addresses", "address", "config", "prefix-length"], "")
        return ""

    def get_vlan_interface_ipv4(self, interface_dict={}):
        if isinstance(super().get_value(interface_dict, ["ipv4", "addresses", "address"]),dict):
            return super().get_value(interface_dict, ["ipv4", "addresses", "address", "config", "ip"], "") + "/" + super().get_value(interface_dict, ["ipv4", "addresses", "address", "config", "prefix-length"], "")
        return ""

    def get_interface_type(self, interface_dict={}):
        if "vlan" in interface_dict["name"]:
            return "Vlan"
        if super().get_value(interface_dict, ["ethernet", "switched-vlan", "state", "interface-mode"], ""):
            return "Bridge"
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
                    self.result.append(result)

            
