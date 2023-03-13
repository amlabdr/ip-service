import json
from config.config import Config
from net.reader import Reader

def run():
    config = Config()
    result = {}
    reader = Reader() 
    reader.read(config)
    result = reader.result 
    json_data = json.dumps(result,indent=2)
    with open("/tmp/result.json", 'w') as json_file:
        json_file.write(json_data)
        json_file.close()
    print("Done")

if __name__ == '__main__':
    run()


