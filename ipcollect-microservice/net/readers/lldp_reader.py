from net.reader import Reader

class LldpReader(Reader):
    def __init__(self, input_dict={}) -> None:
        self.input_dict = input_dict
        self.result = []

    def get_lldp_local_port(self, interface_dict={}):
        return super().get_value(interface_dict, ["name"], "")

    def get_lldp_remote_port(self, interface_dict={}):
        return super().get_value(interface_dict, ["neighbors", "neighbor", "state", "port-id"], "")

    def get_lldp_neighbor_id(self, interface_dict={}):
        return super().get_value(interface_dict, ["neighbors", "neighbor", "state", "chassis-id"], "")

    def read(self):
        for interface in self.input_dict["lldp"]["interfaces"]["interface"]:
            result = {}
            result["LOCALPORT"] = self.get_lldp_local_port(interface)
            result["REMOTEPORT"] = self.get_lldp_remote_port(interface)
            result["REMOTEDEVICE"] = self.get_lldp_neighbor_id(interface)
            if result["REMOTEDEVICE"] != "":
                self.result.append(result)


