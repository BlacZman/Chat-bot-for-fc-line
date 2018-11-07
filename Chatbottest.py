from fbchat import Client, log
from fbchat.models import *
import apiai
import json
import http.client as user
from credit import Account
from datetime import datetime,date,timedelta


class Somchai(Client):
    def apiaiCon(self):
        self.CLIENT_ACCESS_TOKEN = "e56b12694ce64293bb32e7d5103a6a41"
        self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
        self.request = self.ai.text_request()
        self.request.lang = "de"
        self.request.session_id = "ggwp"

    def WeatherConnector(self, receivedDate, location):
        """
        Time forecast are 1:00, 4:00, 7:00, 10:00, 13:00, 16:00, 19:00, 22:00.
        Format date sent by Apiai are xxxx-xx-xx(10), xx:xx:xx(8), xxxx-xx-xx/xxxx-xx-xx(21), xx:xx:xx/xx:xx:xx(17),
        xxxx-xx-xxTxx:xx:xxZ, xxxx-xx-xxTxx:xx:xxZ/xxxx-xx-xxTxx:xx:xxZ
        check length of the date
        """
        timeNow = datetime.now()
        forecastTime = timeNow.replace(hour=1,minute=0,second=0, microsecond=0)

        if len(receivedDate) == 10:
            objTime = datetime.strptime(receivedDate, '%Y-%m-%d')
            deltaT = objTime - timeNow.replace(hour=0,minute=0,second=0, microsecond=0)

        elif len(receivedDate) == 21:
            date1 = receivedDate[0:10]
            date2 = receivedDate[11:22]
            #check if base case is current time
            objTime1 = datetime.strptime(date1, '%Y-%m-%d')
            if timeNow - objTime1 >= timedelta(days=1):
                return 1
            objTime2 = datetime.strptime(date2, '%Y-%m-%d')
            deltaT = objTime2 - objTime1
            timeModify = timeNow + deltaT
            timeModify = timeNow.timestamp()

        #elif len(receivedDate) == 21:


        elif receivedDate == '':
            receivedDate = timeNowq
            deltaT = timedelta(days=0)

        print(deltaT)

        if deltaT >= timedelta(days=0) and deltaT <= timedelta(days=5):
            conn = user.HTTPSConnection('api.openweathermap.org', timeout=10)
            if deltaT == timedelta(days=0):
                conn.request("GET", "/data/2.5/weather?q={}&appid=%s&units=metric".format(location) % (Account.APIcode))
            else:
                conn.request("GET", "/data/2.5/forecast?q={}&appid=%s&units=metric".format(location) % (Account.APIcode))
            responseWeather = conn.getresponse()
            weatherObj = json.load(responseWeather)
            codeStatus = int(weatherObj['cod'])
            if codeStatus == 200:
                print(weatherObj)
            elif codeStatus == 404:
                pass
            conn.close()

        else:
            return 1


    def onMessage(self, author_id=None, message_object=None, thread_id=None, thread_type=ThreadType.USER, **kwargs):
        self.markAsRead(author_id)
        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))
        self.apiaiCon()
        msgtext = message_object.text
        print(msgtext)
        self.request.query = msgtext
        response = self.request.getresponse()
        obj = json.load(response)
        print(obj)
        Location = "Bangkok"
        Action = obj['result']['action']
        reply = obj['result']['fulfillment']['speech']
        if author_id != self.uid:
            if Action == "weather" or Action == "weather.temperature":
                dateInWeather = obj['result']['parameters']['date-time']
                try:
                    Location = obj['result']['parameters']['address']['business-name']
                except:
                    print("No 'business-name' key in data!")
                    try:
                        Location = obj['result']['parameters']['address']['city']
                    except:
                        print("No 'city' key in data!")
                        Location = "Bangkok"
                print(Location)
                Result = self.WeatherConnector(dateInWeather, Location)
                print(Location)
                if Result == 1:
                    self.send(Message(text="Sorry, we cannot collect data from the past or forecast more than 5 days"), thread_id=thread_id, thread_type=thread_type)
                    self.markAsDelivered(author_id, thread_id)

            else:
                self.send(Message(text=reply), thread_id=thread_id, thread_type=thread_type)
                self.markAsDelivered(author_id, thread_id)

        elif author_id == self.uid and msgtext == "bot_shutdown":
            self.send(Message(text="Bot shutting down"), thread_id=thread_id, thread_type=thread_type)
            self.markAsDelivered(author_id, thread_id)
            self.logout()


Bot1 = Somchai(Account.email, Account.password)
Bot1.listen()
