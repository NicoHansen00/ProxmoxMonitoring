import json
from pathlib import Path

incfilename="increment.json"
setfilename="setting.json"

class store:
    def increment():
        data: dict
        with open(Path(__file__).parent / incfilename, mode="r", encoding="utf-8") as read_file:
            data = json.load(read_file)
            if data["current"] < data["min"] or data["current"] > data["max"]:
                data["current"] = data["min"]
            else:
                data["current"] = data["current"] + data["increment"]

        with open(incfilename, mode="w", encoding="utf-8") as write_file:        
            json.dump(data, write_file) 
        return int(data["current"])
    
    def mqttbrokerinfo():
        with open(Path(__file__).parent / setfilename, mode="r", encoding="utf-8") as read_file:
            return dict(json.load(read_file))
    