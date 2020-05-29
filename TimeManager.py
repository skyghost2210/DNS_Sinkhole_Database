import urllib.request, urllib.parse, urllib.error
import json
import datetime


class TimeManager:
    def __init__(self, dateBegin):
        self.APITimeURL = "http://worldtimeapi.org/api/timezone/Asia/Ho_Chi_Minh"
        self.lastUpdateTimeFile = "Saved/LAST_TIME_UPDATE.txt"
        #Check if user want to specify time
        if dateBegin is not None:
            self.time = dateBegin
        else:
            self.time = self.get_time_from_file()
            if self.time is None:
                print('Begin date: None (Download all Mode)')

    def get_time_from_file(self):
        try:
            fileData = open(self.lastUpdateTimeFile,"r")
            return fileData.read()
        except:
            print("TIME FILE NOT FOUND")
            return None
        fileData.close()

    #Get API Time to save
    def get_server_time(self):
        try:
            raw_time_data = urllib.request.urlopen(self.APITimeURL)
            time_data = json.load(raw_time_data)
            return str(time_data['datetime'])
        #If time server is down
        except:
            print("WARNING: TIME SERVER IS DOWN. GET LOCAL TIME")
            return str(datetime.datetime.now().astimezone().isoformat())
        
    #Write the updated time to a txt file
    def write_time_to_file(self):
        fileOpen = open(self.lastUpdateTimeFile,'w+')
        fileOpen.write(str(self.get_server_time()))
        fileOpen.close()