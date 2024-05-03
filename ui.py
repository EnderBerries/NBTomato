'''
临时使用tui
'''
import globalStorage
import os

class tui:
    def __init__(self):
        self.reg={
            "main":[
                "trans.ui.menu",
                "trans.ui.menu.settings",
                "trans.ui.menu.update",
                "trans.ui.menu.exit"
            ],
            "settings":[
                "trans.ui.menu",
                "trans.ui.menu.settings.languages",
                "trans.ui.menu.settings.show_detailed_info",
                "trans.ui.menu.settings.back"
            ],
            "show_detailed_info":[
                "trans.ui.menu",
                "trans.ui.on",
                "trans.ui.off",
                "trans.ui.menu.settings.back"
            ],
            "allows":{
                "main":["1","2","3"],
                "settings":["1","2","3"],
                "show_detailed_info":["1","2","3"],
            },
            "exec":{
                "main":[
                    "self.settings()",
                    "self.update()",
                    "self.exit_()"
                ],
                "settings":[
                    "globalStorage.ChangeLanguage()",
                    "self.show_detailed_info()",
                    "pass"
                ],
                "show_detailed_info":[
                    "globalStorage.SetConfig('ShowDetailedInfo',True)",
                    "globalStorage.SetConfig('ShowDetailedInfo',False)",
                    "pass"
                ]
            }
        }
        #debug
        #globalStorage.init()

    def AcceptCheck(self,accept,value):
        if value in accept:
            return True
        else:
            return False

    def menu(self,menu):
        allow = False
        while not allow:
            for i in self.reg[menu]:
                print(globalStorage.GetTranslation(i))
            self.choose = input(globalStorage.GetTranslation("trans.ui.input"))
            allow = self.AcceptCheck(self.reg["allows"][menu],self.choose) 
            if not allow:
                input(globalStorage.GetTranslation("trans.ui.not_allow"))  
            os.system("cls")
        exec(self.reg["exec"][menu][int(self.choose)-1])

    def main(self):
        self.menu("main")
     
    def settings(self):
        self.menu("settings")
        if self.choose != self.reg["allows"]["settings"][-1]:
            self.settings()
        else:
            self.main()#返回

    def update(self):
        import NBTomato
        NBTomato.main()

    def exit_(self):
        print(globalStorage.GetTranslation("trans.exit"))
        exit()

    def show_detailed_info(self):
        self.menu("show_detailed_info")
        if self.choose != self.reg["allows"]["show_detailed_info"][-1]:
            print(globalStorage.GetTranslation("trans.ui.saved"))
        else:
            print(globalStorage.GetTranslation("trans.ui.not_saved"))
        self.settings()

if __name__ == "__main__":
    a = tui()
    a.main()