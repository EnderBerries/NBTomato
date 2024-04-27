'''
此模块用于升级包含实体数据的NBT标签
如:Passengers;ArmorItems
'''
import itemData
import blockEntityData

def init():
    global specialEntityTag
    model = [         #挨个划勾，用来标记(给我看)
        #"Passengers",
        #"ArmorItems",
        #"body_armor_item",
        #"HandItems",
        #"Inventory",
        #"Items",
        #"SaddleItem",
        #"Offers",
        #"item",
        #"SpawnData",
        #"SpawnPotentials",
        #"TileEntityData",
        #"FireworksItem",
        #"SelectedItem",
        #"EnderItems",
        #"ShoulderEntityLeft",
        #"ShoulderEntityRight"
    ]
    specialEntityTag = [
        "Passengers",
        "ArmorItems",
        "body_armor_item",
        "HandItems",
        "Inventory",
        "Items",
        "SaddleItem",       #这是鞍
        "Offers",
        "item",
        "SpawnData",
        "SpawnPotentials",
        "TileEntityData",
        "FireworksItem",#
        "SelectedItem",
        "EnderItems",
        "ShoulderEntityLeft",
        "ShoulderEntityRight"
    ]

def updateEntityNBT(tag = None):
    if tag == None:
        return "Fail"
    else:
        gotTags = itemData.getNBTList(tag[1:-1])
        output = "{"
        for handle in gotTags:
            handle = handle.split(":",1)
            if specialEntityTag.count(handle[0]) >= 1:
#————————————————————————————————————————————————————————————————————————————
                #print(handle)
                if handle[0] == "item" or handle[0] == "FireworksItem" or handle[0] == "body_armor_item" or handle[0] == "SaddleItem" or handle[0] == "SelectedItem":         #对item、body_armor_item、SaddleItem与FireworksItem的升级(键后直接跟物品共通标签)
                    #print(handle[1])
                    handle[1] = itemData.itemStorageTagOld(handle[1])
                    if handle[1] == "Fail":
                        return "Fail"
                    else:
                        output += handle[0] + ":" + handle[1] + ","

                elif handle[0] == "ArmorItems" or handle[0] == "HandItems" or handle[0] == "Inventory" or handle[0] == "Items" or handle[0] == "EnderItems":         #对ArmorItems、Items、Inventory和HandItems的升级(反正都是一个源码)(键后跟包含多个物品共通标签的列表)
                    final = "["
                    handle_nbt = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_nbt:
                        i = itemData.itemStorageTagOld(i)
                        if i == "Fail":
                            return "Fail"
                        else:
                            final += i + ","
                    output += handle[0] + ":" + final[:-1] + "],"
                
                elif handle[0] == "Offers":         #村民交易选项
                    offers = "Offers:{"
                    handle_nbt = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_nbt:
                        handle_part = i.split(":",1)
                        if handle_part[0] == "Recipes":
                            RecipesList = itemData.getNBTList(handle_part[1][1:-1])
                            recipes = "Recipes:["
                            for s in RecipesList:
                                holdRecipe = itemData.getNBTList(s[1:-1])
                                heldRecipe = "{"
                                for t in holdRecipe:
                                    handle_nbt_inRecipe = t.split(":",1)
                                    if handle_nbt_inRecipe[0] == "buy" or handle_nbt_inRecipe[0] == "buyB" or handle_nbt_inRecipe[0] == "sell":
                                        ret = itemData.itemStorageTagOld(handle_nbt_inRecipe[1])
                                        heldRecipe += handle_nbt_inRecipe[0] + ":" + ret + ","
                                    else:
                                        heldRecipe += t + ","
                                heldRecipe = heldRecipe[:-1] + "}"
                                recipes += heldRecipe + ","
                            recipes = recipes[:-1] + "]"
                    offers += recipes + "},"
                    output += offers
                    
                elif handle[0] == "SpawnData":      #刷怪笼表现方式1
                    spawnData = "SpawnData:{"
                    handle_nbt = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_nbt:
                        handle_part = i.split(":",1)
                        if handle_part[0] == "entity":
                            ret = updateEntityNBT(handle_part[1])
                            spawnData += "entity:" + ret + ","
                        elif handle_part[0] == "custom_spawn_rules":
                            spawnData += i + ","
                    spawnData = spawnData[:-1] + "},"
                    output += spawnData
                
                elif handle[0] == "SpawnPotentials":    #刷怪笼2
                    spawnPotentials = "SpawnPotentials:["
                    handle_nbt2 = itemData.getNBTList(handle[1][1:-1])
                    for s in handle_nbt2:
                        handled = "{"
                        handle_part2 = itemData.getNBTList(s[1:-1])
                        for t in handle_part2:
                            gotnbt = t.split(":",1)
                            if gotnbt[0] == "weight":
                                handled += t + ","
                            elif gotnbt[0] == "data":
                                spawnData = "data:{"
                                handle_nbt = itemData.getNBTList(gotnbt[1][1:-1])
                                for i in handle_nbt:
                                    handle_part = i.split(":",1)
                                    if handle_part[0] == "entity":
                                        ret = updateEntityNBT(handle_part[1])
                                        spawnData += "entity:" + ret + ","
                                    elif handle_part[0] == "custom_spawn_rules":
                                        spawnData += i + ","
                                spawnData = spawnData[:-1] + "},"
                                handled += spawnData
                        handled = handled[:-1] + "},"
                        spawnPotentials += handled
                    spawnPotentials = spawnPotentials[:-1] + "],"
                    output += spawnPotentials

                elif handle[0] == "Passengers":     #关于乘客。可以无限堆叠所以很麻烦
                    passsengers = "Passengers:["
                    handle_part = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_part:
                        ret = updateEntityNBT(i)
                        passsengers += ret + ","
                    passsengers = passsengers[:-1] + "],"
                    output += passsengers

                elif handle[0] == "ShoulderEntityLeft" or handle[0] == "ShoulderEntityRight":   #玩家肩上的实体(只能显示为鹦鹉)
                    shoulder = handle[0] + ":"
                    ret = updateEntityNBT(handle[1])
                    output += shoulder + ret + ","

                elif handle[0] == "TileEntityData":         #妈的，这个恶心死，又要写一个升级方块实体的:(
                    ret = blockEntityData.updateBlockEntityNBT(handle[1])
                    output += "TileEntityData:" + ret + ","
#————————————————————————————————————————————————————————————————————————————
            else:
                output += handle[0] + ":" + handle[1] + ","
                

        output = output[:-1] + "}"
        return output
def target_selector(target = None):
    '''
    更新目标选择器
    主要是实体的NBT标签
    标准使用：
        target_selector("<ENTITYNAME>[nbt=<NBT>,<key>=<VALUE>,...]")
    Example:
        target_selector("@e[limit=1]")
    '''
    if target == None:
        return None
    else:
        try:
            playername = target.split("[",1)[0]
            if len(target.split("[",1)) >= 2:
                target = "[" + target.split("[",1)[1]
                target = itemData.format_nbt(target,frontm="[",backm="]")
                targetSelector = "["
                targets = itemData.getNBTList(target[1:-1])
                for i in targets:
                    handle_target = i.split("=",1)
                    if handle_target[0] == "nbt":
                        ret = updateEntityNBT(handle_target[1])
                        targetSelector += handle_target[0] + "=" + ret + ","
                    else:
                        targetSelector += i + ","
                if targetSelector == "[":
                    targetSelector = playername + targetSelector + "]"
                    return targetSelector
                else:
                    targetSelector = playername + targetSelector[:-1] + "]"
                    return targetSelector
            else:
                return playername
        except ValueError:
            return "Fail"
init()
if __name__ == "__main__":
    #print(updateEntityNBT("{TileEntityData:{id:'minecraft:grass',item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}}}}"))
    print(updateEntityNBT("{ShoulderEntityRight:{id:'minecraft:creeper',item:{Count:1b,id:'dirt'}}}"))
    #print(target_selector("EnderBerries[level=1,limit=2,nbt={item:{Count:1b,id:test}}]"))
#print(updateEntityNBT("{item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}},id:'minecraft:creeper'}"))
#print(updateEntityNBT("{Inventory:[{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255,asa:2}},{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,asa:4}},{},{}]}"))
#print(updateEntityNBT("{Offers:{Recipes:[{buy:{id:'minecraft:test',Count:12b},sell:{id:'minecraft:test2',Count:24b},xp:2,uses:0}],os:1}}"))
#print(updateEntityNBT("{SpawnData:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper',item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}}}}}"))
#print(updateEntityNBT("{SpawnPotentials:[{data:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper',item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}}}},weight:22},{data:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper'}},weight:22}]}"))
#print(updateEntityNBT("{id:'ant',Passengers:[{id:'bat',Passengers:[{id:'cat',item:{Count:13b,id:'minecraft:dirt',tag:{Unbreakable:1b}}},{id:'car'}]}]}"))