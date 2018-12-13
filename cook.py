import json
from operator import itemgetter
from copy import deepcopy
"""
list of command:
cook [method] --> access to cooking method

[method]:
    help --> list all cook command in detail
    list [cmd] --> if [cmd] is 'None' then default
                    default -list all default recipe,
                    custom  -list all custom recipe,
                    all     -list all recipe,

    list [name] [ingredient/procedure] --> [name] -name of recipe
                                           **[ingredient/procedure] -ingredient/procedure in recipe
                                           **if there is None then show all ingredient and procedure

    add [name] [ingredient/procedure] [info1,info2, ...]--> add custom recipe for 'each' user
                    [name] --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe
                    [ingredient/procedure] ***OPTIONAL***--> add infomation to one of them
                    [info1,info2, ...] ***OPTIONAL***--> infomation about recipe
                    *CANNOT have whitespace in infomation* **ONLY IN [in1,in 2,in3] FORMATION**

    edit [name] [ingredient/procedure] [number] [new info]--> edit custom recipe for 'each' user
                    [name] --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe
                    [ingredient/procedure] --> add infomation to one of them
                    [number] -->  0 is append
                                1-n is number represent position in database

    del, delete [name] [ingredient/procedure] [number] --> delete custom recipe using name
                    [name] --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe
                    [ingredient/procedure] ***OPTIONAL*** -->
                    [number] --> 1-n is number represent position in database

    ver --> show version of the cooking(for what?)

======================================================
***********use when text condition is right***********
**********DID NOT SUPPORT THAI LANGUAGE YET***********
======================================================
"""
class Cook:
    def start(self, text, id):
        try:
            self.token = text.split(' ')
        except:
            return "Error in splitting the text"
        self.id = int(id)
        if self.token[0] != "cook":
            return 1
        else:
            print(self.id)
            self.checkIDinDatabase()
            return self.checkCommand()



    def checkCommand(self):
        length = len(self.token)
        if length == 1: # only 'cook'
            if self.token[0] == "cook":
                return "type 'cook help' for more information"
            else:
                return 1

        elif length == 2:
            if self.token[1] == "list": # Command 'cook list'
                txt = self.recipeCus(1)
                listofall = ""
                for x in txt:
                    listofall += "- " + x['name'] + "\n"
                return listofall

            elif self.token[1] == "ver" or self.token[1] == "version":
                txt = self.recipeCus(0)
                return txt

            elif self.token[1] == "help": # Command 'cook help'
                return self.helpCommand()

        else:
            # Command 'cook list default/custom/all/[name](only)'
            if self.token[1] == 'list':
                if self.token[2] == 'default':
                    txt = self.recipeCus(1)
                    listofall = ""
                    for x in txt:
                        listofall += "- " + x['name'] + "\n"
                    return listofall
                elif self.token[2] == 'custom':
                    txt = self.recipeCus(2, id=self.id)
                    listofall = ""
                    for x in txt:
                        listofall += "- " + x['name'] + "\n"
                    return listofall
                elif self.token[2] == 'all':
                    txt = self.recipeCus(1)
                    listofall = "=================\n**System recipe**\n"
                    for x in txt:
                        listofall += "- " + x['name'] + "\n"
                    txt = self.recipeCus(2, id=self.id)
                    listofall += "=================\n**User recipe**\n"
                    for x in txt:
                        listofall += "- " + x['name'] + "\n"
                    listofall += "=================\n"
                    return listofall
                elif length == 3:
                    txt = self.recipeCus(3, id=self.id)
                    for x in txt[0]:
                        listofall = "**System recipe**\n*" + self.token[2] + "*\n=============\n**Ingredient**\n"
                        if x['name'] == self.token[2]:
                            for n in x['ingredient']:
                                listofall += '- ' + n + '\n'
                            listofall += "=============\n**Procedure**\n"
                            for n in x['procedure']:
                                listofall += '- ' + n + '\n'
                            return listofall
                    for x in txt[1]:
                        listofall = "**User recipe**\n*" + self.token[2] + "*\n=============\n**Ingredient**\n"
                        if x['name'] == self.token[2]:
                            for n in x['ingredient']:
                                listofall += '- ' + n + '\n'
                            listofall += "=============\n**Procedure**\n"
                            for n in x['procedure']:
                                listofall += '- ' + n + '\n'
                            return listofall
                    fallback = "{} is not found on database!\n".format(self.token[2])
                    for x in txt[0]:
                        if x['name'].find(self.token[2]) != -1:
                            fallback += "Did you mean {}?\n".format(x['name'])
                    for x in txt[1]:
                        if x['name'].find(self.token[2]) != -1:
                            fallback += "Did you mean {}?\n".format(x['name'])
                    return fallback
                elif length == 4:
                    txt = self.recipeCus(3, id=self.id)
                    if self.token[3] == 'in' or self.token[3] == 'ingredient':
                        for x in txt[0]:
                            listofall = "**System recipe**\n*" + self.token[2] + "*\n=============\n**Ingredient**\n"
                            if x['name'] == self.token[2]:
                                for n in x['ingredient']:
                                    listofall += '- ' + n + '\n'
                                return listofall
                        for x in txt[1]:
                            listofall = "**User recipe**\n*" + self.token[2] + "*\n=============\n**Ingredient**\n"
                            if x['name'] == self.token[2]:
                                for n in x['ingredient']:
                                    listofall += '- ' + n + '\n'
                                return listofall
                        fallback = "{} is not found on database!\n".format(self.token[2])
                        for x in txt[0]:
                            if x['name'].find(self.token[2]) != -1:
                                fallback += "Did you mean {}?\n".format(x['name'])
                        for x in txt[1]:
                            if x['name'].find(self.token[2]) != -1:
                                fallback += "Did you mean {}?\n".format(x['name'])
                        return fallback
                    if self.token[3] == 'pr' or self.token[3] == 'procedure':
                        for x in txt[0]:
                            listofall = "**System recipe**\n*" + self.token[2] + "*\n=============\n**Procedure**\n"
                        if x['name'] == self.token[2]:
                            for n in x['procedure']:
                                listofall += '- ' + n + '\n'
                            return listofall
                        for x in txt[1]:
                            listofall = "**User recipe**\n*" + self.token[2] + "*\n=============\n**Procedure**\n"
                            if x['name'] == self.token[2]:
                                for n in x['procedure']:
                                    listofall += '- ' + n + '\n'
                                return listofall
                        fallback = "{} is not found on database!\n".format(self.token[2])
                        for x in txt[0]:
                            if x['name'].find(self.token[2]) != -1:
                                fallback += "Did you mean {}?\n".format(x['name'])
                        for x in txt[1]:
                            if x['name'].find(self.token[2]) != -1:
                                fallback += "Did you mean {}?\n".format(x['name'])
                        return fallback

            # Command 'cook del/delete [name] ***OPTIONAL[ingredient/procedure] [number]***'
            elif self.token[1] == "add" or self.token[1] == "delete":
                return self.writeCus(0,0)
            elif self.token[1] == "edit":
                return self.writeCus(1,0)
            elif self.token[1] == "del" or self.token[1] == "delete":
                return self.writeCus(2,0)
            else:
                return "No command to be found"



    def checkIDinDatabase(self):
        with open("cookAssistant.json", "r+") as files:
            txt = json.load(files)
            for x in txt["storage"]:
                if x["id"] == self.id:
                    return 0
            
            arr = {"id": self.id, "recipe-custom": []}
            txt["storage"].append(arr)
            files.seek(0)
            json.dump(txt,files,indent=4)
            files.truncate()
            files.close()
        return 0



    def writeCus(self, mode, devmode):
        with open("cookAssistant.json","r+") as files:
            txt = json.load(files)
            if devmode == 1:
                if mode == 0: # add mode
                    arr = {'name':'', 'ingredient':[], 'procedure':[]}
                    txtin = input("Enter the name of recipe : ")
                    for x in txt['recipe-default']:
                        if x['name'] == txtin:
                            print("Add failed(System detected another name in database)")
                            files.close()
                            return 0

                    arr['name'] = txtin
                    limit = 1
                    while limit == 1:
                        txtin = input("Enter the ingredient of the recipe or exit input 1 : ")
                        if txtin == '1':
                            limit = 0
                        else:
                            arr['ingredient'].append(txtin)

                    limit = 1
                    while limit:
                        txtin = input("Enter the procedure of the recipe or exit input 1 : ")
                        if txtin == '1':
                            limit = 0 
                        else:
                            arr['procedure'].append(txtin)

                    print("Are you sure you want to put this?")
                    print("'name':{}".format(arr['name']))
                    print("'ingredient':{}".format(arr['ingredient']))
                    print("'procedure':{}".format(arr['procedure']))
                    txtin = input("yes(1) or no(0)")
                    while txtin != 'yes' and txtin != '1' and txtin != 'no' and txtin != '0':
                        txtin = input("yes(1) or no(0) : ")
                    if txtin == 'yes' or txtin == '1':
                        txt['recipe-default'].append(arr)
                        files.seek(0)
                        json.dump(txt,files,indent=4)
                        files.truncate()
                        files.close()
                        return 1
                    elif txtin == 'no' or txtin == '0':
                        print("Add failed(by user)")
                        files.close()
                        return 0

                elif mode == 1: # edit mode
                    for x in txt['recipe-default']:
                        print(x['name'])
                    name = input("Enter the name of recipe you want to edit : ")
                    limit = 0
                    for x in txt['recipe-default']:
                        if x['name'] == name:
                            limit = 1
                    if limit != 0:
                        txtin = input("Enter which one to edit. ingredient(1), procedure(2) : ")
                        if txtin == '1':
                            txtin = input("Enter which ingredient to edit. append(-1) index(1 to n) : ")
                            if txtin == '-1':
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        edited = input("Enter the information about ingredient or 1 to exit : ")
                                        while edited != '1':
                                            x['ingredient'].append(edited)
                                            edited = input("Enter the information about ingredient or 1 to exit : ")
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Edit successful")
                                return 1
                            else:
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        edited = input("Enter the information about ingredient : ")
                                        x['ingredient'][int(txtin)-1] = edited
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Edit successful")
                                return 1
                        elif txtin == '2':
                            txtin = input("Enter which procedure to edit. append(-1) index(1 to n) : ")
                            if txtin == '-1':
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        edited = input("Enter the information about procedure or 1 to exit : ")
                                        while edited != '1':
                                            x['procedure'].append(edited)
                                            edited = input("Enter the information about procedure or 1 to exit : ")
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Edit successful")
                                return 1
                            else:
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        edited = input("Enter the information about procedure : ")
                                        x['procedure'][int(txtin)-1] = edited
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Edit successful")
                                return 1
                    else:
                        print("Edit failed(Cannot find the recipe in database)")
                        return 0


                elif mode == 2: # delete mode
                    for x in txt['recipe-default']:
                        print(x['name'])
                    name = input("Enter the name of recipe you want to delete : ")
                    limit = 0
                    for x in txt['recipe-default']:
                        if x['name'] == name:
                            limit = 1
                    if limit != 0:
                        txtin = input("Enter which one to delete. All(0), ingredient(1), procedure(2) : ")
                        if txtin == '0':
                            i = 0
                            for x in txt['recipe-default']:
                                if x['name'] == name:
                                    txt['recipe-default'].pop(i)
                                i += 1
                            files.seek(0)
                            json.dump(txt,files,indent=4)
                            files.truncate()
                            files.close()
                            print("Delete successful")
                            return 1
                        elif txtin == '1':
                            txtin = input("Enter which ingredient to delete. All(-1) or index(1 to n) : ")
                            if txtin == '-1':
                                for x in txt['recipe-default']:        
                                    if x['name'] == name:
                                        x['ingredient'].clear()
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Delete successful")
                                return 1
                            else:
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        x['ingredient'].pop(int(txtin)-1)
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Delete successful")
                                return 1
                        elif txtin == '2':
                            txtin = input("Enter which procedure to delete. All(-1) or index(1 to n) : ")
                            if txtin == '-1':
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        x['procedure'].clear()
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Delete successful")
                                return 1
                            else:
                                for x in txt['recipe-default']:
                                    if x['name'] == name:
                                        x['procedure'].pop(int(txtin)-1)
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                print("Delete successful")
                                return 1
                    else:
                        print("Delete failed(Cannot find the name of recipe)")
                        return 0
            else:
                try:
                    self.token[2]
                except:
                    return "Syntax error: Empty [name] string!"
                if mode == 0: # Add mode | cook add [name] [ingredient/procedure] [info1,info2, ...]
                    for x in txt['storage']:
                        if x['id'] == self.id:
                            for y in x['recipe-custom']:
                                if y['name'] == self.token[2]:
                                    return "There is {} in database!\nYou need to edit database".format(self.token[2])
                    arr = {'name': self.token[2], 'ingredient': [], 'procedure': []}
                    try:
                        self.token[3]
                        if self.token[3] == 'ingredient':
                            try:
                                self.token[4]
                                nwToken = self.mergeInfo().split(',')
                                for x in nwToken:
                                    arr['ingredient'].append(x)
                                i=0
                                for x in txt['storage']:
                                    if x['id'] == self.id:
                                        txt['storage'][i].append(arr)
                                    i+=1
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                return "Adding {} to database. Success!".format(self.token[2])
                            except:
                                i=0
                                for x in txt['storage']:
                                    if x['id'] == self.id:
                                        txt['storage'][i]['recipe-custom'].append(arr)
                                    i+=1
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                return "Syntax warning: Empty infomation\nEmpty '{}' is created".format(self.token[2])
                            
                            
                        elif self.token[3] == 'procedure':
                            try:
                                self.token[4]
                                nwToken = self.mergeInfo().split(',')
                                for x in nwToken:
                                    arr['procedure'].append(x)
                                i=0
                                for x in txt['storage']:
                                    if x['id'] == self.id:
                                        txt['storage'][i]['recipe-custom'].append(arr)
                                    i+=1
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                return "Adding {} to database. Success!".format(self.token[2])
                            except:
                                i=0
                                for x in txt['storage']:
                                    if x['id'] == self.id:
                                        txt['storage'][i]['recipe-custom'].append(arr)
                                    i+=1
                                files.seek(0)
                                json.dump(txt,files,indent=4)
                                files.truncate()
                                files.close()
                                return "Syntax warning: Empty infomation\nEmpty '{}' is created".format(self.token[2])
                    except:
                        i=0
                        for x in txt['storage']:
                            if x['id'] == self.id:
                                txt['storage'][i]['recipe-custom'].append(arr)
                            i+=1
                        files.seek(0)
                        json.dump(txt,files,indent=4)
                        files.truncate()
                        files.close()
                        return "Syntax warning: Empty [ingredient/procedure]\nEmpty '{}' is created".format(self.token[2])

                elif mode == 1: # Edit mode |cook edit [name] [ingredient/procedure] [number] [new info]
                    for x in txt['storage']:
                        if x['id'] == self.id:
                            for y in x['recipe-custom']:
                                if self.token[2] == y['name']:
                                    if self.token[3] == 'ingredient':
                                        try:
                                            self.token[4]
                                            if self.token[4] == '0':
                                                try:
                                                    self.token[5]
                                                    merge = self.mergeInfo()
                                                    y['ingredient'].append(merge)
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Edit success"
                                                except:
                                                    return "Syntax error: Empty [info] string!"
                                            else:
                                                try:
                                                    self.token[5]
                                                    merge = self.mergeInfo()
                                                    y['ingredient'][int(self.token[4])-1] = merge
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Edit success"
                                                except:
                                                    return "Syntax error: Empty [info] string!"
                                        except:
                                            return "Syntax Error: Empty [number] string!"
                                    elif self.token[3] == 'procedure':
                                        try:
                                            self.token[4]
                                            if self.token[4] == '0':
                                                try:
                                                    self.token[5]
                                                    merge = self.mergeInfo()
                                                    y['procedure'].append(merge)
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Edit success"
                                                except:
                                                    return "Syntax error: Empty [info] string!"
                                            else:
                                                try:
                                                    self.token[5]
                                                    merge = self.mergeInfo()
                                                    y['procedure'][int(self.token[4])-1] = merge
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Edit success"
                                                except:
                                                    return "Syntax error: Empty [info] string!"
                                        except:
                                            return "Syntax Error: Empty [number] string!"
                                    else:
                                        return "Syntax Error in {}".format(self.token[3])

                    return "Cannot find {} in database!".format(self.token[2])

                elif mode == 2: # Delete mode | cook del/delete [name] [ingredient/procedure] [number]
                    for x in txt['storage']:
                        if x['id'] == self.id:
                            i=0
                            for y in x['recipe-custom']:
                                if y['name'] == self.token[2]:
                                    try:
                                        self.token[3]
                                        if self.token[3] == 'ingredient':
                                            try:
                                                self.token[4]
                                                if int(self.token[4]) <= 0:
                                                    return "[number] is less than 1"
                                                else:
                                                    y['ingredient'].pop(int(self.token[4])-1)
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Delete ingredient in {} success".format(self.token[2])
                                            except:
                                                return "Syntax Error: Empty [number] string!"
                                        elif self.token[3] == 'procedure':
                                            try:
                                                self.token[4]
                                                if int(self.token[4]) <= 0:
                                                    return "[number] is less than 1"
                                                else:
                                                    y['procedure'].pop(int(self.token[4])-1)
                                                    files.seek(0)
                                                    json.dump(txt,files,indent=4)
                                                    files.truncate()
                                                    files.close()
                                                    return "Delete procedure in {} success".format(self.token[2])
                                            except:
                                                return "Syntax Error: Empty [number] string!"
                                        else:
                                            return "Syntax Error in {}".format(self.token[3])
                                    except:
                                        x['recipe-custom'].pop(i)
                                        files.seek(0)
                                        json.dump(txt,files,indent=4)
                                        files.truncate()
                                        files.close()
                                        return "Delete {} and related data success".format(self.token[2])
                                i+=1

                    return "Cannot find {} in database!".format(self.token[2])



    def showInDevMode(self):
        with open("cookAssistant.json") as files:
            txt = json.load(files)
            sortedtxt = self.sortItem(txt['recipe-default'], "name", False)
            for x in sortedtxt:
                print(x['name'])
            into = input("Enter the name to find the ingredient and procedure or 1 to exit : ")
            while into != "1":
                for x in sortedtxt:
                    if x['name'] == into:
                        print("**Ingredient**")
                        i=1
                        for y in x['ingredient']:
                            print("{}- {}".format(i,y))
                            i+=1
                        print("**Procedure**")
                        i=1
                        for y in x['procedure']:
                            print("{}- {}".format(i,y))
                            i+=1
                            
                into = input("Enter the name to find the ingredient and procedure or 1 to exit : ") 
            


    def recipeCus(self, mode, **kwargs):
        with open("cookAssistant.json") as files:
            txt = json.load(files)
            if mode == 0: # version
                return "Cooking Assistant version: " + txt['V']
            elif mode == 1: # list default
                sortedItem = self.sortItem(txt["recipe-default"], "name", False)
                return sortedItem
            elif mode == 2: # list custom
                for key, value in kwargs.items():
                    if key == 'id':
                        for x in txt['storage']:
                            if x['id'] == value:
                                sortedItem = self.sortItem(x["recipe-custom"], "name", False)
                                return sortedItem
            elif mode == 3: # find mode
                sortedItem1 = self.sortItem(txt["recipe-default"], "name", False)
                sortedItem2 = ""
                for key, value in kwargs.items():
                    if key == 'id':
                        for x in txt['storage']:
                            if x['id'] == value:
                                sortedItem2 = self.sortItem(x["recipe-custom"], "name", False)
                allarray = [sortedItem1, sortedItem2]
                return allarray



    def sortItem(self, item, keysorter, desc=False):
        dummy = deepcopy(item)
        srt_dum = sorted(item, key = itemgetter(keysorter), reverse=desc)
        return srt_dum



    def mergeInfo(self):
        merger = ''
        if self.token[1] == 'add':
            i=0
            for x in self.token:
                if i >= 4:
                    merger += x + ' '
                i+=1
            lol = len(merger)
            merger = merger[0:lol-1]
            print("info : {}".format(merger))
            return merger
        elif self.token[1] == 'edit':
            i=0
            for x in self.token:
                if i >= 5:
                    merger += x + ' '
                i+=1
            lol = len(merger)
            merger = merger[0:lol-1]
            print("info : {}".format(merger))
            return merger
        else:
            return None



    def helpCommand(self):
        return "list of command:\n*cook [method]* --> access to cooking method\n\n*[method]*:\n*help* --> list all cook command in detail\n*list [cmd]* --> if [cmd] is 'None' then default\n*default* -list all default recipe,\n*custom*  -list all custom recipe,\n*all*     -list all recipe\n\n*list [name] [ingredient/procedure]* --> *[name]* -name of recipe\n**[ingredient/procedure]* -ingredient/procedure in recipe\n**if there is None then show all ingredient and procedure\n\n*add [name] [ingredient/procedure]* [info1,info2, ...]*--> add custom recipe for 'each' user\n*[name]* --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe\n*[ingredient/procedure]* ***OPTIONAL***--> add infomation to one of them\n*[info1,info2, ...]* ***OPTIONAL***--> infomation about recipe\n*CANNOT have whitespace in infomation* **ONLY IN [in1,in 2,in3] FORMATION**\n\n*edit [name] [ingredient/procedure]* *[number] [new info]*--> edit custom recipe for 'each' user\n*[name]* --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe\n*[ingredient/procedure]* --> add infomation to one of them\n*[number]* -->  0 is append\n-->1-n is number represent position in database\n\n*del, delete [name] [ingredient/procedure] [number]* --> delete custom recipe using name]\n*[name]* --> ***MUST BE NO WHITESPACE IN [name]*** name of recipe\n*[ingredient/procedure]* ***OPTIONAL*** -->\n*[number]* --> 1-n is number represent position in database\n\n*ver* --> show version of the cooking(for what?)"
