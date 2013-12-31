import requests
from Tkinter import *

key = "sSZmea1S_5_Rkpv1Od3HcxVh7B0a"
secret = "YiMyZbcjTy2uwEHyg5yME0tF8tEa"
apihost = "https://agave.iplantc.org/"

class Application(Frame):
    def __init__(self, apihost=apihost, master=None):
        self.myListA = list()
        self.myListB = list()
        self.apihost = apihost
        #self.username = username
        #self.password = password
        #self.key = key
        #self.secret = secret
        #self.token = self.getToken("access_token")
        #self.refreshToken = self.getToken("refresh_token")
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def getToken(self, tokenType):
        dataPayload = {"grant_type":"client_credentials","username":self.username,"password":self.password,"scope":"PRODUCTION"}
        headersPayload = {"Content-Type":"application/x-www-form-urlencoded"}
        req = requests.post(apihost + "/token", auth=(self.key, self.secret), data=dataPayload, headers=headersPayload)
        return req.json()[tokenType]

    def get(self, rtype, path):
        rtype = rtype + "/2.0/"
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.get(apihost + rtype + path, headers = headersPayload)
        print headersPayload
        return req.json()

    def post(self, rtype, path, data):
        rtype = rtype + "/2.0/"
        dataPayload = data
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.post(apihost + rtype + path, headers = headersPayload, data=dataPayload)
        return req.json()

    def delete(self, rtype, path):
        rtype = rtype + "/2.0/"
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.delete(apihost + rtype + path, headers = headersPayload)
        return req.json()

    def put(self, rtype, path, data):
        rtype = rtype + "/2.0/"
        dataPayload = data
        headersPayload = {"Authorization":"Bearer " + self.token}
        req = requests.put(apihost + rtype + path, headers = headersPayload, data=dataPayload)
        #print apihost + rtype + path
        return req.json()

    def makeListFromResult(self, json, item="path"):
        listFromResult = list()
        for i in range(len(json["result"])):
            listFromResult.append(json["result"][i][item])
        return listFromResult

    def connect(self):
        self.username = self.userName.get()
        self.password = self.passWord.get()
        self.key = self.userKey.get()
        self.secret = self.userSecret.get()
        self.token = self.getToken("access_token")
        thisRequest = self.get("files", "listings/" + self.enterFolder.get())
        thisRequestList = self.makeListFromResult(thisRequest, "path")
        self.myListA = thisRequestList
        self.listBoxA.delete(0, END)
        for item in thisRequestList:
            self.listBoxA.insert(END, item)

    def selectA(self):    
        namesToKeep = list()
        for each in map(int, self.listBoxA.curselection()):
            namesToKeep.append(self.myListA[each])
        self.listBoxA.delete(0, END)
        self.myListA = namesToKeep
        for item in self.myListA:
            self.listBoxA.insert(END, item)

    def deleteA(self):
        namesToRemove = list()
        for each in map(int, self.listBoxA.curselection()):
            namesToRemove.append(self.myListA[each])
        for each in namesToRemove:
            self.myListA.remove(str(each))
            self.listBoxA.delete(0, END)
        for item in self.myListA:
            self.listBoxA.insert(END, item)

    def selectB(self):    
        namesToKeep = list()
        for each in map(int, self.listBoxB.curselection()):
            namesToKeep.append(self.myListB[each])
        self.listBoxB.delete(0, END)
        self.myListB = namesToKeep
        for item in self.myListB:
            self.listBoxB.insert(END, item)

    def deleteB(self):
        namesToRemove = list()
        for each in map(int, self.listBoxB.curselection()):
            namesToRemove.append(self.myListB[each])
        for each in namesToRemove:
            self.myListB.remove(str(each))
            self.listBoxB.delete(0, END)
        for item in self.myListB:
            self.listBoxB.insert(END, item)  

    def printA(self):
        print self.myListA

    def printB(self):
        print self.myListB

    def getContents(self):
        for item in self.myListA:
            thisRequest = self.get("files", "listings/" + item)
            if thisRequest["status"]=="success":
                print "View:" + thisRequest["status"]
                self.log.insert(END, "View:" + thisRequest["status"])
                thisRequestList = self.makeListFromResult(thisRequest, "path")
                for thing in thisRequestList:
                    self.listBoxB.insert(END, thing)
                    self.myListB.append(thing)
            else:
                self.log.insert(END, "View:" + thisRequest["status"])
                print "View:" + thisRequest["status"]

    def breakFileName(self, fileName):
        fileName = fileName.split(".")
        lenFileName = len(fileName)
        return fileName[lenFileName-1]

    def getFileName(self, filePath):
        filePathList = filePath.split("/")
        lenFilePathList = len(filePathList)
        return filePathList[lenFilePathList-1]

    def clear(self):
        self.log.delete(0, END)

    def selectFileType(self):
        fileType = self.enterFileType.get()
        newMyListB = list()
        for file in self.myListB:
            if self.breakFileName(file) == fileType:
                newMyListB.append(file)
        self.myListB = newMyListB
        self.listBoxB.delete(0, END)
        for each in self.myListB:
            self.listBoxB.insert(END, each)

    def moveFiles(self):
        moveFolder = self.enterMoveFolder.get()
        for each in self.myListB:
            fileName = self.getFileName(each)
            newFilePath = moveFolder + "/" + fileName
            print newFilePath
            thisRequest = requests.put(url="https://foundation.iplantcollaborative.org/io-v1/io/" + each, auth=(self.username, self.password), data={"action":"move", "newPath":newFilePath})
            thisRequest = thisRequest.json()
            print "Move:" + thisRequest["status"]
            self.log.insert(END, "Move:" + thisRequest['status'])
            #print self.deleteYesNo.get()
        if self.deleteYesNo.get()==1:
            for each in self.myListA:
                thisRequest = requests.delete(url="https://foundation.iplantcollaborative.org/io-v1/io/" + each, auth=(self.username, self.password))
                thisRequest = thisRequest.json()
                try:
                    print "Delete:" + thisRequest["status"]
                    self.log.insert(END, "Delete:" + thisRequest["status"])
                except:
                    pass

    def createWidgets(self):
        self.logo = PhotoImage(file="logo.gif")
        self.title = Label(self, image=self.logo)
        self.title.grid(row=0, column=0, columnspan=4, pady=10)

        self.label1 = Label(self)
        self.label1["text"] = "Username:Password"
        self.label1.grid(row=1, column=0, padx=10, pady=10)

        self.label2 = Label(self)
        self.label2["text"] = "Client Key:Client Secret"
        self.label2.grid(row=1, column=1, padx=10, pady=10)

        self.connectButton = Button(self)
        self.connectButton["text"] = "View Folders in Directory"
        self.connectButton["command"] = self.connect
        self.connectButton.grid(row=4, column=0, padx=10, pady=10)

        self.quitButton = Button(self)
        self.quitButton["text"] = "Quit"
        self.quitButton["command"] = self.quit
        self.quitButton.grid(row=0, column=4, columnspan=2, padx=10, pady=10)

        self.userName = StringVar(self)
        self.userName.set("dalanders")
        self.userNameEntry = Entry(self, textvariable=self.userName)
        self.userNameEntry.grid(row=2, column=0, padx=10, pady=10)

        self.passWord = StringVar(self)
        self.passWord.set("Shadow@3876")
        self.passWordEntry = Entry(self, textvariable=self.passWord)
        self.passWordEntry.grid(row=3, column=0, padx=10, pady=10)

        self.userKey = StringVar(self)
        self.userKey.set("sSZmea1S_5_Rkpv1Od3HcxVh7B0a")
        self.userKeyEntry = Entry(self, textvariable=self.userKey)
        self.userKeyEntry.grid(row=2, column=1, padx=10, pady=10)

        self.userSecret = StringVar(self)
        self.userSecret.set("YiMyZbcjTy2uwEHyg5yME0tF8tEa")
        self.userSecretEntry = Entry(self, textvariable=self.userSecret)
        self.userSecretEntry.grid(row=3, column=1, padx=10, pady=10)

        self.enterFolder = StringVar(self)
        self.enterFolder.set("dalanders/analyses")
        self.enterFolderEntry = Entry(self, textvariable=self.enterFolder)
        self.enterFolderEntry.grid(row=4, column=1, padx=10, pady=10)

        self.listBoxA = Listbox(self, selectmode=EXTENDED)
        self.listBoxA.config(height=25, width=50)
        self.listBoxA.grid(row=5, column=0, columnspan=2)

        self.selectAButton = Button(self)
        self.selectAButton["text"] = "Select"
        self.selectAButton["command"] = self.selectA
        self.selectAButton.grid(row=6, column=0, padx=10, pady=10)

        self.deleteAButton = Button(self)
        self.deleteAButton["text"] = "Delete"
        self.deleteAButton["command"] = self.deleteA
        self.deleteAButton.grid(row=6, column=1, padx=10, pady=10)

        self.selectBButton = Button(self)
        self.selectBButton["text"] = "Select"
        self.selectBButton["command"] = self.selectB
        self.selectBButton.grid(row=6, column=2, padx=10, pady=10)

        self.deleteBButton = Button(self)
        self.deleteBButton["text"] = "Delete"
        self.deleteBButton["command"] = self.deleteB
        self.deleteBButton.grid(row=6, column=3, padx=10, pady=10)

        self.getContentsButton = Button(self)
        self.getContentsButton["text"] = "View Contents of Selected Folders"
        self.getContentsButton["command"] = self.getContents
        self.getContentsButton.grid(row=2, column=2, columnspan=2, padx=10, pady=10)

        self.selectFileTypeButton = Button(self)
        self.selectFileTypeButton["text"] = "Select File Type"
        self.selectFileTypeButton["command"] = self.selectFileType
        self.selectFileTypeButton.grid(row=3, column=2, padx=10, pady=10)

        self.moveFilesButton = Button(self)
        self.moveFilesButton["text"] = "Move Files"
        self.moveFilesButton["command"] = self.moveFiles
        self.moveFilesButton.grid(row=4, column=2, padx=10, pady=10)

        self.enterFileType = StringVar(self)
        self.enterFileType.set("raw")
        self.enterFileTypeEntry = Entry(self, textvariable=self.enterFileType)
        self.enterFileTypeEntry.grid(row=3, column=3, padx=10, pady=10)

        self.enterMoveFolder = StringVar(self)
        self.enterMoveFolder.set("dalanders/")
        self.enterMoveFolderEntry = Entry(self, textvariable=self.enterMoveFolder)
        self.enterMoveFolderEntry.grid(row=4, column=3, padx=10, pady=10)

        self.listBoxB = Listbox(self, selectmode=EXTENDED)
        self.listBoxB.config(height=25, width=50)
        self.listBoxB.grid(row=5, column=2, columnspan=2)

        self.log = Listbox(self, selectmode=SINGLE)
        self.log.config(height=25, width=25)
        self.log.grid(row=5, column=4, columnspan=2)

        self.deleteYesNo = IntVar()
        self.deleteCheck = Checkbutton(self, text="Delete Folders After Moving Files?", var=self.deleteYesNo)
        self.deleteCheck.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

        #self.printAButton = Button(self)
        #self.printAButton["text"] = "Print A"
        #self.printAButton["command"] = self.printA
        #self.printAButton.grid(row=1, column=2, padx=10, pady=10)

        #self.printBButton = Button(self)
        #self.printBButton["text"] = "Print B"
        #self.printBButton["command"] = self.printB
        #self.printBButton.grid(row=1, column=3, padx=10, pady=10)

        #self.mkDirButton = Button(self)
        #self.mkDirButton["text"] = "Make Directory"
        #self.mkDirButton["command"] = self.mkDir
        #self.mkDirButton.grid(row=2, column=4, padx=10, pady=10)

        self.logLabel = Label(self)
        self.logLabel["text"] = "Log"
        self.logLabel.grid(row=4, column=4, columnspan=2, padx=10, pady=10)

        self.clearButton = Button(self)
        self.clearButton["text"] = "Clear"
        self.clearButton["command"] = self.clear
        self.clearButton.grid(row=6, column=4, columnspan=2, padx=10, pady=10)

root = Tk()
root.wm_title('Aggregate')
app = Application(master=root)
app.mainloop()
root.destroy()