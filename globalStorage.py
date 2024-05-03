import os
import json
def init():
    try:
        os.makedirs(os.path.join(os.getcwd(),"Languages"))
    except:
        pass
    global thisFile
    global translation
    global langs    #语言列表
    global lang     #选定语言
    global version
    global devVersion
    global config
    config = {}
    version = "0.7.3"
    devVersion = 0
    translation = {}
    langs=[]
    thisFile=""
    ReadCFG()
    LoadAll()
    if "language" not in config:
        SetConfig("language","undefined")
    if langs.count(config["language"]) == 0:
        ChangeLanguage()
    else:
        lang = config["language"]

    if "ShowDetailedInfo" not in config:
        SetConfig("ShowDetailedInfo",False)

def GetTranslation(key):
    if key in translation[lang]:
        return translation[lang][key]
    else:
        return key
    
def LoadTranslationPack(pack):
    global translation
    global langs
    try:
        hpack = __import__(f"Languages.{pack}")
        if not eval(f"hpack.{pack}.Lang") in langs:
            langs.append(eval(f"hpack.{pack}.Lang"))
        translation.update(eval(f"hpack.{pack}.translation"))
    except ImportError:
        print(f"load language pack '{pack}' fail")
# init()
# LoadTranslationPack("zh_cn")

def ChangeLanguage():
    global lang
    while True:
        menudic = {}
        s = 1
        print("Choose a language below:")
        for i in langs:
            print("    ",translation[i]["trans.pack.name"],":",s)
            menudic[s] = i
            s += 1
        choose = input(">>>")
        try:
            choose = int(choose)
            lang = menudic[choose]
            #print(lang)
            input(GetTranslation("trans.finished_change_language"))
            break
        except:
            input("enter something available please")
    SetConfig("language",lang)
    os.system("cls")

def LoadAll():
    a = os.listdir("./Languages")
    for i in a:
        if i[-3:] == ".py":
            LoadTranslationPack(i[:-3])
        elif i[-4:] == ".pyc":
            LoadTranslationPack(i[:-4])

def SetConfig(key,value,add=True):
    global config
    try:
        if add == True:
            config.update(dict([(key,value)]))
        elif add == False:
            del config[key]
        else:
            raise ValueError("Not usable")
        with open("settings.json", "w") as f:
            json.dump(config,f, indent=4)

    except KeyError:
        print('set config fail')

def ReadCFG():
    global config
    if os.path.exists("settings.json"):
        with open("settings.json", "r") as f:
            f = json.load(f)
            config = f
    else:
        with open("settings.json", "w") as f:
            json.dump(config,f, indent=4)