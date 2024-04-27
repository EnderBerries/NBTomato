def init():
    global thisFile
    global translation
    thisFile=""
    translation={
        "zh_cn":{
            "trans.main.get_mcmeta_path":"请输入pack.mcmeta文件路径：",
        }
    }

def GetTranslation(language,key):
    if key in translation[language]:
        return translation[language][key]
    else:
        return key