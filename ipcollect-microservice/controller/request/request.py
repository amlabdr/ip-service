import time
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
        retry_delay = 10  # Delay in seconds between retry attempts
        while True:
            try:
                response = requests.get(url, headers = head)
                # Process the response
                if response.status_code == 200:
                    # Server is available and responded successfully
                    return response.text
                else:
                    # Server responded with an error status code
                    print("Request failed with status code:", response.status_code)
            except requests.exceptions.RequestException as e:
                # Exception occurred during the request
                print("An error occurred:", e)
            # Wait for the retry delay before attempting the request again
            time.sleep(retry_delay)


