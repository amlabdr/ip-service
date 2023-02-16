from config.config import Config
from controller.controller_service import Controller_service
from network.network_config import Network_config

def run():
    cfg = Config()
    Ctl_service = Controller_service(config = cfg)
    network_config = Network_config()
    network_config.get_topology(cfg)
    Ctl_service.run_http_server(network_config,cfg=cfg)

if __name__ == '__main__':
    run()