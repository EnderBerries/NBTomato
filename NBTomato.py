import os
import reporter
import itemData
import blockEntityData
import entityData
import jsonFiles
import NBTPath
import update
import globalStorage

reporter.reporter.init()
globalStorage.init()
#C:\Users\65961\Desktop\Python\datapack_update24w09a
report = ()
#总进度:
all_ex = [
    #"item",
    #"execute"
    #"give"
    #"#",
    #"其他命令"
    #"loot",
    #"attribute",
    "data",
    #"summon",
    "战利品表谓词",
    "战利品表",
    "配方",
]

data = {
    "paths":{
        "functions":"data\\$namespace$\\functions",
        "advancements":"data\\$namespace$\\advancements",
        "lootTables":"data\\$namespace$\\loot_tables",
        "predicates":"data\\$namespace$\\predicates",
        "itemModifiers":"data\\$namespace$\\item_modifiers",
        "feature":"data\\$namespace$\\worldgen\\configured_feature",
        "placedFeature":"data\\$namespace$\\worldgen\\placed_feature",
        "recipes":"data\\$namespace$\\worldgen\\biome"
    },
    "functions":[],
    "FilePaths":{}
}

mcmetaPath = input(globalStorage.GetTranslation("trans.main.get_mcmeta_path"))


#mcmetaPath = r"D:\mc\PCL\.minecraft\saves\PortalTestA\datapacks\Darkplace\pack.mcmeta"
dataPath = os.path.dirname(mcmetaPath)
namespaces = os.listdir(os.path.join(dataPath,"data"))#获取命名空间



def get_files(getpath = str,Namespace = str,Item_name = str):
    '''
    获取getpath文件夹内的全部文件路径，并将其存入data["FilePaths"][namespace][<item_name>]中
    '''
    #print(getpath)
    for i in os.walk(getpath):
        if i[2] != []:
            for s in i[2]:
                data["FilePaths"][Namespace][Item_name].append(os.path.join(i[0],s))
    return "SUCCESS"

def get_data():
    for namespace in namespaces:
        data["FilePaths"][namespace] = {}
        #存储要更改的文件
        if os.path.exists(os.path.join(dataPath,data["paths"]["functions"]).replace("$namespace$",namespace)):      data["FilePaths"][namespace]["functions"] = [];      get_files(os.path.join(dataPath,data["paths"]["functions"]).replace("$namespace$",namespace),namespace,"functions")#判断是否存在functions文件夹，有则储存
        if os.path.exists(os.path.join(dataPath,data["paths"]["itemModifiers"]).replace("$namespace$",namespace)):      data["FilePaths"][namespace]["item_modifiers"] = []      ;get_files(os.path.join(dataPath,data["paths"]["itemModifiers"]).replace("$namespace$",namespace),namespace,"item_modifiers")#判断是否存在modifiers文件夹，有则储存
        if os.path.exists(os.path.join(dataPath,data["paths"]["lootTables"]).replace("$namespace$",namespace)):      data["FilePaths"][namespace]["loot_tables"] = []     ;get_files(os.path.join(dataPath,data["paths"]["lootTables"]).replace("$namespace$",namespace),namespace,"loot_tables")#判断是否存在loot_tables文件夹，有则储存

def OneFileReadAndWrite(FilePath,FileType):
    if FileType == "FUNCTION":
        functionsRem = []
        functionsOut = []
        try:
            reporter.reporter.log(f"Updating Function:{FilePath}")
            with open(FilePath, "r" ,encoding="utf-8") as f:
                globalStorage.thisFile = FilePath   #暴露当前文件地址

                functionsRem = f.readlines()

                listpointer = 0
                for i in functionsRem:
                    functionsRem[listpointer] = functionsRem[listpointer].rstrip()
                    listpointer += 1
                
                for functionGet in functionsRem:#进行版本更新
                    ret = update.exec_ccmd(functionGet)
                    functionsOut.append(ret)
                
                f.close()

            with open(FilePath, "w" ,encoding="utf-8") as f:#覆盖写入升级后的函数
                for function in functionsOut:
                    f.write(function+"\n")
                f.close()
        except:
            pass
    
    elif FileType == "ITEMMODIFIER":
        reporter.reporter.log(f"Updating ItemModifier:'{FilePath}'")
        try:
            jsonFiles.item_modifier(FilePath)
        except:
            pass

    elif FileType == "LOOTTABLE":
        reporter.reporter.log(f"Updating LootTable:'{FilePath}'")
        try:
            jsonFiles.loot_table(FilePath)
        except:
            pass

# for namespace in namespaces:
#     for i in data["FilePaths"][namespace]:
#         with open(i,"r",encoding="utf-8") as f:
#             globalStorage.thisFile = i
#             wr = f.read()
#             print(wr+"\n")
#             f.close()

# def debug(funcPath,arg):
#     ''
#     exec(funcPath+arg)

# debug("reporter.reporter.init","()")
# debug("reporter.reporter.log","('Info2')")

# inpfile = input(">>>")
# OneFileReadAndWrite(inpfile,"LOOTTABLE")
# reporter.reporter.done()

if __name__ == "__main__":
    #get_files("<YOUR pack.mcmeta>")
    get_data()
    for i in namespaces:
        reporter.reporter.log(f"Updateing namespace '{i}'")

        reporter.reporter.log(f">Task:Update functions in namespace '{i}'")
        if "functions" in data["FilePaths"][i]:
            for s in data["FilePaths"][i]["functions"]:
                OneFileReadAndWrite(s,"FUNCTION")
        else:
            reporter.reporter.log(f">Not found functions in namespace '{i}'")

        reporter.reporter.log(f">Task:Update item-modifiers in namespace '{i}'")
        if "item_modifiers" in data["FilePaths"][i]:
            for s in data["FilePaths"][i]["item_modifiers"]:
                OneFileReadAndWrite(s,"ITEMMODIFIER")
        else:
            reporter.reporter.log(f">Not found item-modifiers in namespace '{i}'")
   
        reporter.reporter.log(f">Task:Update loot-tables in namespace '{i}'")
        if "loot_tables" in data["FilePaths"][i]:
            for s in data["FilePaths"][i]["loot_tables"]:
                OneFileReadAndWrite(s,"LOOTTABLE")
        else:
            reporter.reporter.log(f">Not found loot-tables in namespace '{i}'")