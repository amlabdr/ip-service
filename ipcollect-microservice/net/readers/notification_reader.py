from utils.common import get_value

class NotificationReader():
    def __init__(self, target_node='', notification_dict={}) -> None:
        self.target_node = target_node
        self.notification_dict = notification_dict
        self.result = {}

    def get_interface_status_notification(self):
        result = {}
        result['eventClass'] = self.notification_dict['eventClass']
        if result['eventClass'] == 'state':
            if 'interface-link-state-change-notification' in self.notification_dict.keys():
                result['interface-name'] = get_value(self.notification_dict, 
                                                     ['interface-link-state-change-notification','name'],
                                                     '')
                result['oper-status'] = get_value(self.notification_dict, 
                                                  ['interface-link-state-change-notification','oper-status'],
                                                  '')
            else:
               result = {}
        else:
           result = {}
        return result


    def __str__(self) -> str:
        return f'NotificationReader = {vars(self)}'

    def read(self):
        result = self.get_interface_status_notification()
        self.result["resourceName"] = self.target_node + '/' + str(get_value(result, ['interface-name']))
        self.result["resourceStatus"] = str.upper(str(get_value(result,['oper-status'])))
        self.result["resourceType"] = 'LTP' 

