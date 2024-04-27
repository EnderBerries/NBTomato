import json
import update
import NBTPath
import reporter
import globalStorage

# reporter.reporter.init() #DEBUG
# globalStorage.init()
# globalStorage.thisFile = "1bc"

def imp(itemModifier = None):
    if "function" in itemModifier:#只判断一轮
        if itemModifier["function"] == "copy_nbt":#新版本不再支持以前的copy_nbt(现在以custom_data为根标签)
            reporter.reporter.Error("Not supported type in latest Minecraft version,at "+globalStorage.thisFile,path=globalStorage.thisFile,logp="jsonFiles")
            raise NBTPath.UpdateError("05")
            # for i in itemModifier["ops"]:
            #     i["source"] = NBTPath.ItemNBTPath(i["source"])
            #     i["target"] = NBTPath.ItemNBTPath(i["target"])
        elif itemModifier["function"] == "set_nbt":
            itemModifier["function"] = "set_components"
            itemModifier["components"] = update.item_stack(itemModifier["tag"])
            del(itemModifier["tag"])
        
        elif itemModifier["function"] == "set_attributes":
            pointer = 0
            try:
                for i in itemModifier["modifiers"]:
                    if i["operation"] == "addition":
                        itemModifier["modifiers"][pointer]["operation"] = "add_value"
                    if i["operation"] == "multiply_base":
                        itemModifier["modifiers"][pointer]["operation"] = "add_multiplied_base"
                    if i["operation"] == "multiply_total":
                        itemModifier["modifiers"][pointer]["operation"] = "add_multiplied_total"
                    pointer += 1
            except KeyError as err:
                reporter.reporter.Error("Wrong item-modifier format,at "+globalStorage.thisFile+f"\n    {err}",path=globalStorage.thisFile,logp="jsonFiles")
                raise KeyError(err)
    
    return itemModifier


def item_modifier(filePath = None,dictinp="{}",mode="w"):
    if filePath == None:
        pass
    else:
        if mode == "w":
            with open(filePath,'r') as f:
                itemModifier = json.load(f)
                f.close()
        else:
            itemModifier = dictinp

        if isinstance(itemModifier,dict):
            itemModifier = imp(itemModifier)
        else:#list
            tlst = []
            for s in itemModifier:
                tlst.append(imp(s))
            itemModifier = tlst.copy()

        if mode == "w":
            with open(filePath,'w') as f:
                f.write(json.dumps(itemModifier,indent=4))
                f.close()
        else:
            return itemModifier

def loot_table(filePath = None):
    if filePath == None:
        pass
    else:
        with open(filePath,'r') as f:
            lootTable = json.load(f)
            f.close()
        if "functions" in lootTable:
            lootTable["functions"] = item_modifier(dictinp=lootTable["functions"],mode="r")
        if "pools" in lootTable:
            jsonpointer = 0
            for s in lootTable["pools"]:
                if "functions" in s:
                    lootTable["pools"][jsonpointer]["functions"] = item_modifier(dictinp=lootTable["pools"][jsonpointer]["functions"] ,mode="r")
                    entriespointer = 0
                    if "entries" in s:
                        for s2 in lootTable["pools"][jsonpointer]["entries"]:
                            if "functions" in s2:
                                lootTable["pools"][jsonpointer]["entries"][entriespointer]["functions"] = item_modifier(dictinp=lootTable["pools"][jsonpointer]["entries"][entriespointer]["functions"] ,mode="r")
                            entriespointer += 1
                jsonpointer += 1


item_modifier(r"C:\Users\65961\Desktop\Python\datapack_update24w09a\s.json")
# reporter.reporter.Error("Not supported type,at "+globalStorage.thisFile,path=globalStorage.thisFile,logp="jsonFiles")
#reporter.reporter.done()
