import requests

class Request:
    def __init__(self):
        pass

    def postRequest(self,url, filename,token=""):
        filedata = {'filedata': (filename, open(filename, 'rb'))}
        hed = {'Authorization': 'Bearer ' + token}
        response = requests.post(url, files=filedata,headers=hed)
        return response.text

    def postRequestJson(self,url,data):
        response = requests.post(url, json=data)
        return response
    
    def getRequest(self, url,token =""):
        hed = {'Authorization': 'Bearer ' + token}
        response = requests.get(url, headers=hed)
        return response.text