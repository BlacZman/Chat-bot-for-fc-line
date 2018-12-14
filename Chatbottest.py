#!/usr/bin python3
from fbchat import Client, log
from fbchat.models import *
import apiai
import json
import http.client as user
from cook import Cook
from credit import Account
from datetime import datetime, date, timedelta


class Somchai(Client):
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "e56b12694ce64293bb32e7d5103a6a41"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = "de"
        self.request.session_id = "ggwp"


    def WeatherConnector(self, obj):
        """
        Time forecast are 1:00, 4:00, 7:00, 10:00, 13:00, 16:00, 19:00, 22:00.
        Format date sent by Apiai are xxxx-xx-xx(10), xx:xx:xx(8), xxxx-xx-xx/xxxx-xx-xx(21), xx:xx:xx/xx:xx:xx(17),
        xxxx-xx-xxTxx:xx:xxZ, xxxx-xx-xxTxx:xx:xxZ/xxxx-xx-xxTxx:xx:xxZ
        check length of the date
        """
        receivedDate = obj['result']['parameters']['date-time']
        location = ""
        try:
            location = obj['result']['parameters']['address']['business-name']
        except:
            print("No 'business-name' key in data!")
            try:
                location = obj['result']['parameters']['address']['city']
            except:
                print("No 'subadmin-area' key in data!")
                try:
                    location = obj['result']['parameters']['address']['subadmin-area']
                except:
                    try:
                        location = obj['result']['parameters']['thai-address']
                    except:
                        print("No 'thai-address' key in data!")
                    finally:
                        if location == "" or location == None:
                            location = "Bangkok"


        print(location)

        timeNow = datetime.now()
        deltaT = timedelta(days=0)
        if len(receivedDate) == 10:
            objTime = datetime.strptime(receivedDate, '%Y-%m-%d')
            deltaT = objTime - timeNow.replace(hour=0,minute=0,second=0, microsecond=0)

        elif len(receivedDate) == 21:
            date1 = receivedDate[0:10]
            date2 = receivedDate[11:22]
            # check if base case is current time
            objTime1 = datetime.strptime(date1, '%Y-%m-%d')
            #if timeNow - objTime1 >= timedelta(days=1):
            #    return 1
            objTime2 = datetime.strptime(date2, '%Y-%m-%d')
            deltaT = objTime2 - objTime1
            timeModify = timeNow + deltaT

        elif len(receivedDate) == 17:
            date1 = receivedDate[0:8]
            date2 = receivedDate[9:17]
            objTime1 = datetime.strptime(date1, '%H:%M:%S')
            objTime2 = datetime.strptime(date2, '%H:%M:%S')
            if objTime2 > objTime1:
                objTime2 = objTime2.replace(year=timeNow.year, month=timeNow.month, day=timeNow.day)
            else:
                nextday = timeNow.day + 1
                objTime2 = objTime2.replace(year=timeNow.year, month=timeNow.month, day=nextday)

            objTime1 = objTime1.replace(year=timeNow.year, month=timeNow.month, day=timeNow.day)
            timeNow = timeNow.replace(microsecond=0)
            # check if base case is current time
            #if timeNow - objTime1  >= timedelta(seconds=2):
            #    return 1

            deltaT = objTime2 - objTime1
            timeModify = timeNow + deltaT

        elif receivedDate == '':
            receivedDate = timeNow
            deltaT = timedelta(days=0)


        print(deltaT)

        if deltaT >= timedelta(days=0) and deltaT <= timedelta(days=5):
            conn = user.HTTPSConnection('api.openweathermap.org', timeout=10)
            if deltaT == timedelta(days=0):
                conn.request("GET", "/data/2.5/weather?q={}&appid=%s&units=metric".format(location) % Account.APIcode)
            else:
                conn.request("GET", "/data/2.5/forecast?q={}&appid=%s&units=metric".format(location) % Account.APIcode)
            responseWeather = conn.getresponse()
            weatherObj = json.load(responseWeather)
            codeStatus = int(weatherObj['cod'])
            if codeStatus == 200:
                print(weatherObj)
                timeNow = datetime.now()
                try:
                    for x in weatherObj['list']:
                        dataTime = datetime.strptime(x['dt_txt'], '%Y-%m-%d %H:%M:%S')
                        if dataTime - timeNow > deltaT:
                            if obj['result']['action'] == 'weather':
                                return [x['weather'][0]['description'],location,dataTime]
                            else:
                                return [x['main']['temp'],location,dataTime]

                except:
                    print("Error occur or it's not forecast")
                if obj['result']['action'] == 'weather':
                    return [weatherObj['weather'][0]['description'],location,"Today"]
                else:
                    return [weatherObj['main']['temp'],location,"Today"]
            elif codeStatus == 404:
                print("Cannot find the city")
            conn.close()

        else:
            return 1


    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        self.markAsRead(author_id) # mark read message
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type)) # log message incoming
        self.apiaiCon()  # use ai function
        msgtext = message_object.text # read message
        log.info(msgtext) # log message
        if author_id != self.uid and thread_type == ThreadType.USER:
            self.request.query = msgtext # throw message to dialogflow
            response = self.request.getresponse() # receive response from server
            obj = json.load(response) # decode json to array
            log.info(obj) # log object from server
            Action = obj['result']['action'] # access to action of bot
            reply = obj['result']['fulfillment']['speech'] # access to reply bot
            if Action == "weather" or Action == "weather.temperature":
                Result = self.WeatherConnector(obj)
                if Result == 1:
                    self.send(Message(text="Sorry, \nwe cannot collect data from the past or forecast more than 5 days"),
                              thread_id=thread_id, thread_type=thread_type)
                    self.markAsDelivered(author_id, thread_id)
                else:
                    if Action == "weather":
                        self.send(Message(text="There are {} in {} {}!!".format(Result[0], Result[1], Result[2])),
                                  thread_id=thread_id, thread_type=thread_type)
                        self.markAsDelivered(author_id, thread_id)
                    else:
                        self.send(Message(text="{} temperature is {} Celsius in {}!".format(Result[2], Result[0], Result[1])),
                                  thread_id=thread_id, thread_type=thread_type)
                        self.markAsDelivered(author_id, thread_id)
            else:
                ckas = Cook()# Create Cook object
                try:
                    newAc = obj['result']['action']
                except:
                    newAc = 
                if newAc == "cook.list.all" or newAc == "cook.list.custom" or newAc == "cook.list.default":
                    linkCk = ckas.start(reply,author_id)
                else:
                    linkCk = ckas.start(msgtext,author_id)
                if linkCk == 1:
                    log.info("=====>" + author_id)
                    self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                    self.markAsDelivered(author_id, thread_id)
                else:
                    log.info(linkCk)
                    self.send(Message(text=linkCk), thread_id=thread_id, thread_type=thread_type)
                    self.markAsDelivered(author_id, thread_id)

        elif author_id == self.uid and msgtext == "bot_shutdown":
            self.send(Message(text="Bot shutting down"), thread_id=thread_id, thread_type=thread_type)
            self.markAsDelivered(author_id, thread_id)
            self.logout()


Bot1 = Somchai(Account.email, Account.password)
Bot1.listen()