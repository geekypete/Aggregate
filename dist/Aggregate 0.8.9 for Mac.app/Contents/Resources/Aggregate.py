import requests
from Tkinter import *
import tkMessageBox

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

    def printP(self, a, b):
        self.percent = Label(self, text="")
        self.percent.grid(row=0, column=4)
        self.update_idletasks()
        self.percent = Label(self, text=str((a/b)*100)[0:5] + "% \n" + str(int(a)) + "/" + str(int(b)))
        self.percent.grid(row=0, column=4)
        self.update_idletasks()

    def getContents(self):
        self.myListB = list()
        self.listBoxB.delete(0, END)
        myListAlen = float(len(self.myListA))
        count = 0.0
        for item in self.myListA:
            count += 1.0
            print str((count/myListAlen)*100) + " Percent Complete"
            thisRequest = requests.get("https://foundation.iplantcollaborative.org/io-v1/io/list/" + item, 
                auth=(self.username, self.password)).json()
            self.printP(count, myListAlen)
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

    def getFilePath(self, moveFolder):
        numList = list()
        for i in range(len(moveFolder)):
            if moveFolder[i] == "/":
                numList.append(i)
        return moveFolder[0:numList[len(numList)-1]]

    def moveFiles(self):
        moveFolder = self.enterMoveFolder.get()
        req = requests.get("https://foundation.iplantcollaborative.org/io-v1/io/list/" + moveFolder, 
            auth=(self.username, self.password))
        if req.json()["status"] == "error":
            fileName = self.getFileName(moveFolder)
            filePath = self.getFilePath(moveFolder)
            payload = {'action' : 'mkdir', 'dirName' : fileName}
            req = requests.put('https://foundation.iplantcollaborative.org/io-v1/io/' + filePath, 
                auth=(self.username, self.password), data=payload)
            #if req.json()["status"] == "success":
                #self.percent = Label(self, text="Folder Created")
                #self.percent.grid(row=0, column=4)
                #self.update_idletasks()
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
            self.printP(count, myListBlen)
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

        self.logo = Label(self, fg="black", font=100)
        self.logo["text"] = "Aggregate: An Application for iPlant Collaborative"
        self.logo.grid(row=0, column=0, columnspan=3, pady=20)

        self.label1 = Label(self, fg="blue")
        self.label1["text"] = "Username:"
        self.label1.grid(row=1, column=0, sticky=E)

        self.label5 = Label(self, fg="blue")
        self.label5["text"] = "Password:"
        self.label5.grid(row=2, column=0, sticky=E)

        self.label3 = Label(self, fg="blue")
        self.label3["text"] = "Select Folders to View:"
        self.label3.grid(row=4, column=0, columnspan=2)

        self.label4 = Label(self, fg="blue")
        self.label4["text"] = "Select Folders and/or Files to Move:"
        self.label4.grid(row=4, column=3, columnspan=2)

        self.containAButton = Button(self)
        self.containAButton["text"] = "Select All Containing:"
        self.containAButton["command"] = self.containA
        self.containAButton.grid(row=9, column=0, sticky=E)

        self.containStrA = StringVar(self)
        self.containStrAEntry = Entry(self, textvariable=self.containStrA)
        self.containStrAEntry.grid(row=9, column=1, sticky=W)

        self.containBButton = Button(self)
        self.containBButton["text"] = "Select All Containing:"
        self.containBButton["command"] = self.containB
        self.containBButton.grid(row=9, column=3, sticky=E)

        self.containStrB = StringVar(self)
        self.containStrBEntry = Entry(self, textvariable=self.containStrB)
        self.containStrBEntry.grid(row=9, column=4, sticky=W)

        self.connectButton = Button(self)
        self.connectButton["text"] = "View Folders in Directory"
        self.connectButton["command"] = self.connect
        self.connectButton.grid(row=3, column=0, sticky=E)

        #self.quitButton = Button(self)
        #self.quitButton["text"] = "Quit"
        #self.quitButton["command"] = self.quit
        #self.quitButton.grid(row=0, column=5)

        self.userName = StringVar(self)
        self.userName.set("")
        self.userNameEntry = Entry(self, textvariable=self.userName)
        self.userNameEntry.grid(row=1, column=1, sticky=W)

        self.passWord = StringVar(self)
        self.passWord.set("")
        self.passWordEntry = Entry(self, textvariable=self.passWord, show="*")
        self.passWordEntry.grid(row=2, column=1, sticky=W)

        self.enterFolder = StringVar(self)
        self.enterFolder.set("")
        self.enterFolderEntry = Entry(self, textvariable=self.enterFolder)
        self.enterFolderEntry.grid(row=3, column=1, sticky=W)

        self.yScrollBarA = Scrollbar(self, orient=VERTICAL)
        self.yScrollBarA.grid(row=5, column=2, sticky=N+S+W)

        self.xScrollBarA = Scrollbar(self, orient=HORIZONTAL)
        self.xScrollBarA.grid(row=6, column=0, sticky=W+E+N)

        self.listBoxA = Listbox(self, selectmode=EXTENDED)
        self.listBoxA.config(height=25, width=62)
        self.listBoxA.grid(row=5, column=0, columnspan=2, sticky=N+S+E+W)

        ## Attach scrollbars
        self.listBoxA.config(yscrollcommand=self.yScrollBarA.set, xscrollcommand=self.xScrollBarA.set)
        self.yScrollBarA.config(command=self.listBoxA.yview)
        self.xScrollBarA.config(command=self.listBoxA.xview)

        self.selectAButton = Button(self)
        self.selectAButton["text"] = "Select"
        self.selectAButton["command"] = self.selectA
        self.selectAButton.grid(row=10, column=0)

        self.deleteAButton = Button(self)
        self.deleteAButton["text"] = "Delete"
        self.deleteAButton["command"] = self.deleteA
        self.deleteAButton.grid(row=10, column=1)

        self.selectBButton = Button(self)
        self.selectBButton["text"] = "Select"
        self.selectBButton["command"] = self.selectB
        self.selectBButton.grid(row=10, column=3)

        self.deleteBButton = Button(self)
        self.deleteBButton["text"] = "Delete"
        self.deleteBButton["command"] = self.deleteB
        self.deleteBButton.grid(row=10, column=4)

        self.getContentsButton = Button(self)
        self.getContentsButton["text"] = "View Contents of Selected Folders"
        self.getContentsButton["command"] = self.getContents
        self.getContentsButton.grid(row=1, column=3, columnspan=2)

        self.selectFileTypeButton = Button(self)
        self.selectFileTypeButton["text"] = "Select File Type"
        self.selectFileTypeButton["command"] = self.selectFileType
        self.selectFileTypeButton.grid(row=2, column=3, sticky=E)

        self.moveFilesButton = Button(self)
        self.moveFilesButton["text"] = "Move Files"
        self.moveFilesButton["command"] = self.moveFiles
        self.moveFilesButton.grid(row=3, column=3, sticky=E)

        self.enterFileType = StringVar(self)
        self.enterFileType.set("")
        self.enterFileTypeEntry = Entry(self, textvariable=self.enterFileType)
        self.enterFileTypeEntry.grid(row=2, column=4, sticky=W)

        self.enterMoveFolder = StringVar(self)
        self.enterMoveFolder.set("")
        self.enterMoveFolderEntry = Entry(self, textvariable=self.enterMoveFolder)
        self.enterMoveFolderEntry.grid(row=3, column=4, sticky=W)

        self.yScrollBarB = Scrollbar(self, orient=VERTICAL)
        self.yScrollBarB.grid(row=5, column=5, sticky=N+S+W)

        self.xScrollBarB = Scrollbar(self, orient=HORIZONTAL)
        self.xScrollBarB.grid(row=6, column=3, sticky=W+E+N)

        self.listBoxB = Listbox(self, selectmode=EXTENDED)
        self.listBoxB.config(height=25, width=62)
        self.listBoxB.grid(row=5, column=3, columnspan=2)

        ## Attach scrollbars
        self.listBoxB.config(yscrollcommand=self.yScrollBarB.set, xscrollcommand=self.xScrollBarB.set)
        self.yScrollBarB.config(command=self.listBoxB.yview)
        self.xScrollBarB.config(command=self.listBoxB.xview)

        self.log = Listbox(self, selectmode=SINGLE)
        self.log.config(height=25, width=25)
        #self.log.grid(row=6, column=4, columnspan=2)

        self.deleteYesNo = IntVar()
        self.deleteCheck = Checkbutton(self, text="Delete Folders After Moving Files?", var=self.deleteYesNo)
        #self.deleteCheck.grid(row=1, column=2, columnspan=2, padx=5, pady=10)

        self.logLabel = Label(self)
        self.logLabel["text"] = "Log"
        #self.logLabel.grid(row=5, column=4, columnspan=2, padx=5, pady=10)

        self.clearButton = Button(self)
        self.clearButton["text"] = "Clear"
        self.clearButton["command"] = self.clear
        #self.clearButton.grid(row=7, column=4, columnspan=2, padx=5, pady=10)

def ask_quit():
    if tkMessageBox.askokcancel("Quit", "You want to quit now?"):
        root.quit()

root = Tk()
root.wm_title('Aggregate')
app = Application(master=root)
root.protocol("WM_DELETE_WINDOW", ask_quit)
app.mainloop()
root.destroy()