from net.readers.interface_reader import InterfaceReader

class MetadataReader():
    def __init__(self, metadata_dict={}, interface_dict={}) -> None:
        self.metadata_dict = metadata_dict
        self.interface_dict = interface_dict
        self.result = {}

    # get mac address of the management interface which is the ID of the device
    def get_mac(self):
        iface_reader = InterfaceReader(self.interface_dict)
        iface_reader.read()
        for interface in iface_reader.result:
            if interface["NAME"] == "eth0":
                return interface["MACADDR"]

    # get mac address of the management interface which is the ID of the device
    def get_loopback_address(self):
        iface_reader = InterfaceReader(self.interface_dict)
        iface_reader.read()
        for interface in iface_reader.result:
            if interface["NAME"] == "lo":
                return interface["IPADDR"]
    
    def __str__(self) -> str:
        return f'MetadataReader = {vars(self)}'

    def read(self):
        self.result["HOSTNAME"] = self.metadata_dict["system"]["state"]["hostname"]
        self.result["MAIN_ADDRESS"] = self.get_loopback_address() 
        self.result["MAC"] = self.get_mac()
        self.result["TYPE"] = "ROUTER"
        self.result["PLATFORM"] = "OcNOS"

