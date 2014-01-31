import requests
from Tkinter import *

class Application(Frame):
    def __init__(self, master=None):
        self.myListA = list()
        self.myListB = list()
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def getToken(self):
        req = requests.post("https://foundation.iplantcollaborative.org/auth-v1/", auth=(self.username, self.password))
        token = req.json()["result"]["token"]
        return token

    def makeListFromResult(self, json, item="path"):
        listFromResult = list()
        for i in range(len(json["result"])):
            lenItem = len(json["result"][i][item])
            listFromResult.append(json["result"][i][item][1:lenItem])
        return listFromResult

    def connect(self):
        self.username = self.userName.get()
        self.password = self.passWord.get()
        self.token = self.getToken()
        thisRequest = requests.get("https://foundation.iplantcollaborative.org/io-v1/io/list/" + 
            self.enterFolder.get(), auth=(self.username, self.password)).json()
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
        self.myListB = list()
        self.listBoxB.delete(0, END)
        myListAlen = float(len(self.myListA))
        count = 0.0
        for item in self.myListA:
            count += 1.0
            print str((count/myListAlen)*100) + " Percent Complete"
            #self.percent["text"] = str((count/myListAlen)*100) + "%"
            thisRequest = requests.get("https://foundation.iplantcollaborative.org/io-v1/io/list/" + item, 
                auth=(self.username, self.password)).json()
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
        count = 0.0
        myListBlen = float(len(self.myListB))
        for each in self.myListB:
            count += 1.0
            print str((count/myListBlen)*100) + " Percent Complete"
            #self.percent["text"] = str((count/myListBlen)*100) + "%"
            fileName = self.getFileName(each)
            newFilePath = moveFolder + "/" + fileName
           #print newFilePath
            thisRequest = requests.put(url="https://foundation.iplantcollaborative.org/io-v1/io/" + each, 
                auth=(self.username, self.password), data={"action":"move", "newPath":newFilePath})
            thisRequest = thisRequest.json()
            print "Move:" + thisRequest["status"]
            self.log.insert(END, "Move:" + thisRequest['status'])
            #print self.deleteYesNo.get()
        if self.deleteYesNo.get()==1:
            for each in self.myListA:
                thisRequest = requests.delete(url="https://foundation.iplantcollaborative.org/io-v1/io/" + each, 
                    auth=(self.username, self.password))
                thisRequest = thisRequest.json()
                try:
                    print "Delete:" + thisRequest["status"]
                    self.log.insert(END, "Delete:" + thisRequest["status"])
                except:
                    pass

    def containA(self):
        thisStr = self.containStrA.get()
        namesToKeep = list()
        for each in self.myListA:
            if thisStr in each:
                namesToKeep.append(each)
        self.myListA = namesToKeep
        self.listBoxA.delete(0, END)
        for each in self.myListA:
            self.listBoxA.insert(END, each)

    def containB(self):
        thisStr = self.containStrB.get()
        namesToKeep = list()
        for each in self.myListB:
            if thisStr in each:
                namesToKeep.append(each)
        self.myListB = namesToKeep
        self.listBoxB.delete(0, END)
        for each in self.myListB:
            self.listBoxB.insert(END, each)

    def createWidgets(self):

        self.scrollbarA = Scrollbar(self, orient=VERTICAL)
        self.scrollbarA.grid(row=0, column=2)

        self.listBoxA = Listbox(self, selectmode=EXTENDED)
        self.listBoxA.config(height=25, width=50)
        self.listBoxA.grid(row=0, column=0, columnspan=2)

        ## Attach scrollbars
        self.listBoxA.config(yscrollcommand=self.scrollbarA.set)
        self.scrollbarA.config(command=self.listBoxA.yview)


root = Tk()
root.wm_title('Aggregate')
app = Application(master=root)
app.mainloop()
root.destroy()