import requests

class Request:
    def __init__(self):
        pass

    def post_request_file(self, url, filename, token = ""):
        filedata = {'filedata': (filename, open(filename, 'rb'))}
        head = {'Authorization': 'Bearer ' + token}
        response = requests.post(url, files = filedata,headers = head)
        return response.text

    def post_request_json(self, url, data, token = ''):
        head = {'Authorization': 'Bearer ' + token}
        response = requests.post(url, json = data, headers = head)
        return response
    
    def get_request(self, url, token = ""):
        head = {'Authorization': 'Bearer ' + token}
        response = requests.get(url, headers = head)
        return response.text
