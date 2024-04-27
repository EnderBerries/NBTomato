'''
此模块用于升级包含方块实体数据的NBT标签
如:Patterns;Items
'''
import itemData
import entityData

def init():
    global specialEntityTag
    model = [         #挨个划勾，用来标记(给我看)
        #"Patterns",
        #"Items",
        #"Bees",
        #"FlowerPos",
        #"item",
        #"Book",     #=item
        #"SpawnData",
        #"SpawnPotentials",
        #"ExtraType",#头的字符串形式
        #"SkullOwner",
        #"spawn_data",
        #"spawn_potentials",
        #"config",     #=item
        #"server_data",
        #"shared_data"
    ]
    specialEntityTag = [
        "Patterns",
        "Items",
        "Bees",
        "FlowerPos",
        "item",
        "Book",     #=item
        "SpawnData",
        "SpawnPotentials",
        "ExtraType",#头
        "SkullOwner",
        "spawn_data",
        "spawn_potentials",
        "config",     #=item
        "server_data",
        "shared_data"
    ]

def updateBlockEntityNBT(tag = None):
    if tag == None:
        return "Fail"
    else:
        gotTags = itemData.getNBTList(tag[1:-1])
        output = "{"
        skullOwner = False

        for handle in gotTags:      #获取玩家的头的格式
            handle = handle.split(":",1)
            if specialEntityTag.count(handle[0]) >= 1:
                if handle[0] == "SkullOwner":
                    skullOwner = True

        for handle in gotTags:
            handle = handle.split(":",1)
            if specialEntityTag.count(handle[0]) >= 1:
#————————————————————————————————————————————————————————————————————————————
                if handle[0] == "item" or handle[0] == "Book" or handle[0] == "SaddleItem":         #对item、body_armor_item、SaddleItem与FireworksItem的升级(键后直接跟物品共通标签)
                    handle[1] = itemData.itemStorageTagOld(handle[1])
                    if handle[1] == "Fail":
                        return "Fail"
                    else:
                        output += handle[0] + ":" + handle[1] + ","

                elif handle[0] == "ArmorItems" or handle[0] == "HandItems" or handle[0] == "Inventory" or handle[0] == "Items":         #对ArmorItems、Items、Inventory和HandItems的升级(反正都是一个源码)(键后跟包含多个物品共通标签的列表)
                    final = "["
                    handle_nbt = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_nbt:
                        i = itemData.itemStorageTagOld(i)
                        if i == "Fail":
                            return "Fail"
                        else:
                            final += i + ","
                    output += handle[0] + ":" + final[:-1] + "],"
                
                elif handle[0] == "SpawnData" or handle[0] == "spawn_data":      #刷怪笼表现方式1
                    spawnData = "SpawnData:{"
                    handle_nbt = itemData.getNBTList(handle[1][1:-1])
                    for i in handle_nbt:
                        handle_part = i.split(":",1)
                        if handle_part[0] == "entity":
                            ret = entityData.updateEntityNBT(handle_part[1])
                            spawnData += "entity:" + ret + ","
                        elif handle_part[0] == "custom_spawn_rules":
                            spawnData += i + ","
                    spawnData = spawnData[:-1] + "},"
                    output += spawnData
                
                elif handle[0] == "SpawnPotentials" or handle[0] == "spawn_potentials":    #刷怪笼2
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
                                        ret = entityData.updateEntityNBT(handle_part[1])
                                        spawnData += "entity:" + ret + ","
                                    elif handle_part[0] == "custom_spawn_rules":
                                        spawnData += i + ","
                                spawnData = spawnData[:-1] + "},"
                                handled += spawnData
                        handled = handled[:-1] + "},"
                        spawnPotentials += handled
                    spawnPotentials = spawnPotentials[:-1] + "],"
                    output += spawnPotentials

                elif handle[0] == "Bees":
                    bees = handle[1].replace("EntityData:","entity_data:")
                    bees = bees.replace("TicksInHive:","ticks_in_hive:")
                    bees = bees.replace("MinOccupationTicks:","min_ticks_in_hive:")
                    bees = "bees:" + bees
                    output += bees + ","

                elif handle[0] == "FlowerPos":        
                    poss = itemData.getNBTList(handle[1][1:-1])
                    poslist = "["
                    for i in poss:
                        poslist += i[2:] + ","
                    poslist = poslist[:-1] + "]"
                    output += "flower_pos:" +  poslist + ","

                elif handle[0] == "Patterns":
                    pattern = "{"
                    parts = handle[1][2:-2].split("},{")
                    for s in parts:
                        handle_part = itemData.getNBTList(s)
                        for p in handle_part:
                            temp3 = p.split(":",1)
                            if temp3[0] == "Pattern":
                                pattern += "pattern:" + temp3[1] + ","
                            elif temp3[0] == "Color":
                                pattern += "color:" + itemData.base_color[int(temp3[1])%16] + ","
                        pattern = pattern[:-1] + "},{"
                    pattern = "[" + pattern[:-2] + "]"
                    output += "patterns:" + pattern + ","
                
                elif handle[0] == "SkullOwner":
                    ret = itemData.updateNBT("SkullOwner",handle[1],connect=":")
                    output += ret + ","

                elif handle[0] == "ExtraType" and skullOwner == False:
                    skullowner = "profile:{name:" + handle[1] + "},"
                    output += skullowner

                elif handle[0] == "ExtraType" and skullOwner == True:
                    pass

                elif handle[0] == "server_data":
                    datas = itemData.getNBTList(handle[1][1:-1])
                    server_data = "server_data:{"
                    for t in datas:
                        getData = t.split(":",1)
                        if getData[0] == "items_to_eject":
                            items_to_eject = "items_to_eject:"
                            final = "["
                            handle_nbt = itemData.getNBTList(getData[1][1:-1])
                            for i in handle_nbt:
                                i = itemData.itemStorageTagOld(i)
                                if i == "Fail":
                                    return "Fail"
                                else:
                                    final += i + ","
                            items_to_eject = items_to_eject + final[:-1] + "],"
                            server_data += items_to_eject
                        else:
                            server_data += t + ","
                    server_data = server_data[:-1] + "},"
                    output += server_data

                elif handle[0] == "shared_data":        #宝库的shared_data,格式等同于config
                    datas = itemData.getNBTList(handle[1][1:-1])
                    shared_data = "shared_data:{"
                    for t in datas:
                        getData = t.split(":",1)
                        if getData[0] == "display_item":
                            ret = itemData.itemStorageTagOld(getData[1])
                            if ret == "Fail":
                                return "Fail"
                            else:
                                ret = "display_item:" + ret + ","
                                shared_data += ret
                        else:
                            shared_data += t + ","
                    shared_data = shared_data[:-1] + "},"
                    output += shared_data

                elif handle[0] == "config":
                    datas = itemData.getNBTList(handle[1][1:-1])
                    config = "config:{"
                    for t in datas:
                        getData = t.split(":",1)
                        if getData[0] == "key_item":
                            ret = itemData.itemStorageTagOld(getData[1])
                            if ret == "Fail":
                                return "Fail"
                            else:
                                ret = "key_item:" + ret + ","
                                config += ret
                        else:
                            config += t + ","
                    config = config[:-1] + "},"
                    output += config
#————————————————————————————————————————————————————————————————————————————
            else:
                output += handle[0] + ":" + handle[1] + ","

        output = output[:-1] + "}"
        return output

init()
if __name__ == "__main__":
    print(updateBlockEntityNBT("{id:'$FLAG$'}"))
#print(updateBlockEntityNBT("{SkullOwner:{Id:'[I,12,23,34]',Name:'abc',Properties:{textures:[{Value:\"ABCDEFG\",Signature:\"s\"},{Value:\"HIJKLMN\"}]}},ExtraType:'EnderBerries'}"))
#print(updateBlockEntityNBT("{Patterns:[{Pattern:'minecraft:stripe_top',Color:1},{Pattern:'minecraft:stripe_top',Color:2}]}"))
#print(updateBlockEntityNBT("{server_data:{activation_range:4,items_to_eject:[{id:'minecraft:diamond',Count:1b},{id:'minecraft:grass',Count:4b}]}}"))
#print(updateBlockEntityNBT("{item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}},id:'minecraft:creeper'}"))
#print(updateBlockEntityNBT("{Inventory:[{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255,asa:2}},{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,asa:4}},{},{}]}"))
#print(updateBlockEntityNBT("{Offers:{Recipes:[{buy:{id:'minecraft:test',Count:12b},sell:{id:'minecraft:test2',Count:24b},xp:2,uses:0}],os:1}}"))
#print(updateBlockEntityNBT("{SpawnData:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper',item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}}}}}"))
#print(updateBlockEntityNBT("{SpawnPotentials:[{data:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper',item:{Count:12,id:\"minecraft:test\",tag:{CustomModelData:1b,Unbreakable:1b,HideFlags:255}}}},weight:22},{data:{custom_spawn_rules:{block_light_limit:0.1,sky_light_limit:0.2},entity:{id:'minecraft:creeper'}},weight:22}]}"))
#print(updateBlockEntityNBT("{id:'ant',Passengers:[{id:'bat',Passengers:[{id:'cat',item:{Count:13b,id:'minecraft:dirt',tag:{Unbreakable:1b}}},{id:'car'}]}]}"))