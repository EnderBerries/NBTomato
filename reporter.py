import os
import time
import zipfile
import json

class Reporter:
    def __init__(self) -> None:
        self.ShowDetailedInfo = True
    def init(self,path = None) -> None:#必须手动执行
        if path == None:
            self.path = os.getcwd() + "\\Output Reporter"
        else:
            self.path = path
        self.bakeupPath = self.path + "\\Backup"
        self.latestPath = self.path + "\\latest.log"
        self.errorList = []
        self.warnList = []
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        if not os.path.exists(self.bakeupPath):
            os.makedirs(self.bakeupPath)
        if os.path.exists(self.latestPath):
            try:
                f = open(self.latestPath,"r")
                line = f.readline()
                logtime = line.split("[",1)[1]
                logtime = logtime.split("]",1)[0]
                zip = zipfile.ZipFile(self.bakeupPath + "\\" + logtime + ".zip","w",zipfile.ZIP_DEFLATED)
                zip.write(self.latestPath,arcname="latest.log")
            except:
                pass
        self.latest = open(self.latestPath,"w")
        self.latest.write("@Log time at["+time.strftime("%Y-%m-%d %H-%M-%S") + "]\n")

    def log(self,loginfo = "None",logat = "Main",logtype = "INFO",logwrapper = "[]"):
        logtime = logwrapper[0] + time.strftime("%H-%M-%S") + logwrapper[1]
        logInfo = logwrapper[0] + logat + "/" + logtype + logwrapper[1] + ": " + loginfo
        if self.ShowDetailedInfo == False and logtype != "Warn" and logtype != "Error":#简化时不显示Info
            self.latest.write(logtime+logInfo+"\n")
            print(logtime+logInfo)

    def warn(self,warnInfo="",logp="Main",path=""):
        self.log(warnInfo,logat=logp,logtype="Warn")
        self.warnList.append(path)

    def Error(self,errorInfo="",logp="Main",path=""):
        self.log(errorInfo,logat=logp,logtype="Error")
        self.errorList.append(path)

    def done(self):
        self.log("Report Output at: '%s' , '%s'"%(self.path+"\\ErrorReport.json",self.path+"\\WarningReport.json"))
        self.log("Stopping!")
        self.latest.close()
        with open(self.path+"\\ErrorReport.json","w") as err:
            err.write(json.dumps(self.errorList,indent=4))
            err.close()
        with open(self.path+"\\WarningReport.json","w") as warn:
            warn.write(json.dumps(self.warnList,indent=4))
            warn.close()

reporter = Reporter()
if __name__ == "__main__":
    report = Reporter()
    report.init()
    report.log("test1,At...")
    report.log("test2,At...")
    report.warn("At ...",path="C:/item.json")
    report.Error("At ...",path="C:/item.json")
    report.done()