"""
用于升级物品NBT数据。
配方等NBT不由此模块负责
"""
import random
import entityData
import globalStorage
import reporter
modulev = "0.0.2.2"
updatev = "Minecraft-Snapshot-24w10a"
updateb = "Minecraft-Snapshot-24w08a"
def moduleVersion():
    return "itemData module version:" + modulev +"\nyour datapack will update to:" + updatev
def randomPropertyName(long = 8):
    '''生成玩家的头的properties中随机name'''
    a = ""
    try:
        for i in range(long):
            a += "ABCDEFabcdef123456"[random.randint(0,17)]
        return a
    except:
        return "FFF000"

special_items_model1 = '{Count:*,id:*,tag:*}'
special_items_model2 = '{Count:*,id:*}'

def getGlobals():
    tempPath = "globalData.p"
    with open(tempPath,"r") as g:
        i = g.read()
        return(i.split("\n"))

def getNBTList(inp,find = ","):
    '''
    用于拆分NBT
    '''
    global NBTList
    NBTList = []
    mlist = []
    fk,hk,pos,bm,sm,lastpos,fm,tm = 0,0,0,0,0,0,0,0
    laststr = ""
    for i in inp:
        pos += 1
        if i == "{":
            hk += 1
        elif i == "}":
            hk -= 1
        elif i == "[":
            fk += 1
        elif i == "]":
             fk -= 1
        elif i == "'":
            sm += 1
            if laststr != "\\" :mlist.append("'")
        elif i == '"':
            bm += 1
            if laststr != "\\" :mlist.append('"')
        elif i == find and fk == 0 and hk == 0:
            if len(mlist) == 0:
                NBTList.append(inp[lastpos:pos-1])
                lastpos = pos 
            elif len(mlist) >= 2 and mlist[0] == mlist[-1]:
                mlist.clear()
                NBTList.append(inp[lastpos:pos-1])
                lastpos = pos 
        laststr = i
    if len(inp[lastpos:]) != 0 == 0:
        mlist.clear()
        NBTList.append(inp[lastpos:])
    return NBTList

def format_nbt(inp,frontm="{",backm="}"):
    '''
    用来格式化nbt字符串(去除不必要的空格)
    '''
    curly_brackets = 0
    nbtlist = []
    mlist = []
    while len(inp) != 0 and inp[0] == frontm and inp[-1] == backm:
        inp = inp[1:-1]
        curly_brackets += 1
    sm = 0
    bm = 0
    pos = 0
    lastpos = 0
    outp = ""
    for i in inp:
        pos += 1
        if i == "'":
            sm += 1
            if laststr != "\\" :mlist.append("'")
        elif i == '"':
            bm += 1
            if laststr != "\\" :mlist.append('"')
        elif i == " ":
            if len(mlist) == 0:
                nbtlist.append(inp[lastpos:pos-1])
                lastpos = pos
            elif len(mlist) >= 2 and mlist[0] == mlist[-1]:
                mlist.clear()
                nbtlist.append(inp[lastpos:pos-1])
                lastpos = pos 
        laststr = i
    if len(inp[lastpos:]) != 0 :# == 0 
        nbtlist.append(inp[lastpos:])
    for i in nbtlist:
        outp += i
    return frontm * curly_brackets + outp + backm * curly_brackets
    
def init():
    '''
    导入基本数据，自动执行，无其他实际功能
    '''
    global replace
    global itemTypes
    global bucket_entity
    global block_entity
    global sign
    global banner
    global shulker_box
    global skull
    global bed
    global components
    global itemTags
    global HideFlags
    global base_color
    global container_loot
    global bucket_entity_data
    global bucketnbt
    global maps
    global dec_name
    global dec_rot
    global dec_type
    global dec_x
    global dec_z
    global potion_contents
    global potionnbt
    global writable_book_content
    global writable_booknbt
    global book_filter
    global written_booknbt
    global booktype
    global lodestonenbt
    global firework_star_shapes
    global compass_data
    global charged
    booktype = "writable_book"
    book_filter = {}
    charged = {}
    dec_rot,dec_name,dec_type,dec_x,dec_z = "","","","",""
    container_loot,bucket_entity_data,potion_contents,writable_book_content,compass_data = [],[""],[""],[""],[""]
    HideFlags = "00000000"
    base_color = [
        "white",
        "orange",
        "magenta",
        "light_blue",
        "yellow",
        "lime",
        "pink",
        "gray",
        "light_gray",
        "cyan",
        "purple",
        "blue",
        "brown",
        "green",
        "red",
        "black",
    ]
    replace = {
        "Damage": "damage",
        "RepairCost": "repair_cost",
        "Items": "bundle_contents",
        "map": "map_id",
        "CustomModelData": "custom_model_data",
        "Trim": "trim",
        "effects": "suspicious_stew",
        "Recipes": "recipes",
    }
    bucket_entity = [
        "minecraft:cod_bucket",
        "minecraft:salmon_bucket",
        "minecraft:pufferfish_bucket",
        "minecraft:tropical_fish_bucket",
        "minecraft:axolotl_bucket",
        "minecraft:tadpole_bucket",
    ]
    lodestonenbt = [
        "LodestoneDimension",
        "LodestonePos",
        "LodestoneTracked"
    ]
    bed = [
        "minecraft:white_bed",
        "minecraft:orange_bed",
        "minecraft:magenta_bed",
        "minecraft:light_blue_bed" "minecraft:yellow_bed",
        "minecraft:lime_bed",
        "minecraft:pink_bed",
        "minecraft:gray_bed",
        "minecraft:light_gray_bed",
        "minecraft:cyan_bed",
        "minecraft:purple_bed",
        "minecraft:blue_bed",
        "minecraft:brown_bed",
        "minecraft:green_bed",
        "minecraft:red_bed",
        "minecraft:black_bed",
    ]
    sign = [
        "minecraft:oak_sign",
        "minecraft:spruce_sign",
        "minecraft:birch_sign",
        "minecraft:jungle_sign",
        "minecraft:acacia_sign",
        "minecraft:dark_oak_sign",
        "minecraft:mangrove_sign",
        "minecraft:cherry_sign",
        "minecraft:bamboo_sign",
        "minecraft:crimson_sign",
        "minecraft:warped_sign",
        "minecraft:oak_hanging_sign",
        "minecraft:spruce_hanging_sign",
        "minecraft:birch_hanging_sign",
        "minecraft:jungle_hanging_sign",
        "minecraft:acacia_hanging_sign",
        "minecraft:dark_oak_hanging_sign",
        "minecraft:mangrove_hanging_sign",
        "minecraft:cherry_hanging_sign",
        "minecraft:bamboo_hanging_sign",
        "minecraft:crimson_hanging_sign",
        "minecraft:warped_hanging_sign",
    ]
    banner = [
        "minecraft:white_banner",
        "minecraft:orange_banner",
        "minecraft:magenta_banner",
        "minecraft:light_blue_banner",
        "minecraft:yellow_banner",
        "minecraft:lime_banner",
        "minecraft:pink_banner",
        "minecraft:gray_banner",
        "minecraft:light_gray_banner",
        "minecraft:cyan_banner",
        "minecraft:purple_banner",
        "minecraft:blue_banner",
        "minecraft:brown_banner",
        "minecraft:green_banner",
        "minecraft:red_banner",
        "minecraft:black_banner",
    ]
    shulker_box = [
        "minecraft:shulker_box",
        "minecraft:white_shulker_box",
        "minecraft:orange_shulker_box",
        "minecraft:magenta_shulker_box",
        "minecraft:light_blue_shulker_box",
        "minecraft:yellow_shulker_box",
        "minecraft:lime_shulker_box",
        "minecraft:pink_shulker_box",
        "minecraft:gray_shulker_box",
        "minecraft:light_gray_shulker_box",
        "minecraft:cyan_shulker_box",
        "minecraft:purple_shulker_box",
        "minecraft:blue_shulker_box",
        "minecraft:brown_shulker_box",
        "minecraft:green_shulker_box",
        "minecraft:red_shulker_box",
        "minecraft:black_shulker_box",
    ]
    firework_star_shapes = [
        "small_ball",
        "large_ball",
        "star",
        "creeper",
        "burst"
    ]
    skull = [
        "minecraft:skeleton_skull",
        "minecraft:wither_skeleton_skull",
        "minecraft:zombie_head",
        "minecraft:player_head",
        "minecraft:creeper_head",
        "minecraft:dragon_head",
        "minecraft:piglin_head",
    ]
    block_entity = [
        "minecraft:beehive",
        "minecraft:bee_nest",
        sign,
        banner,
        "minecraft:chest",
        "minecraft:trapped_chest",
        "minecraft:dispenser",
        "minecraft:furnace",
        "minecraft:brewing_stand",
        "minecraft:hopper",
        "minecraft:dropper",
        shulker_box,
        "minecraft:barrel",
        "minecraft:smoker",
        "minecraft:blast_furnace",
        "minecraft:campfire",
        "minecraft:soul_campfire",
        "minecraft:lectern",
        "minecraft:chiseled_bookshelf",
        "minecraft:crafter",
        "minecraft:suspicious_gravel",
        "minecraft:suspicious_sand",
        "minecraft:beacon",
        "minecraft:trial_spawner",
        "minecraft:spawner",
        "minecraft:jukebox",
        "minecraft:enchanting_table",
        "minecraft:ender_chest",
        skull,
        "minecraft:command_block",
        "minecraft:structure_block",
        "minecraft:daylight_detector",
        "minecraft:comparator",
        bed,
        "minecraft:conduit",
        "minecraft:bell",
        "minecraft:sculk_catalyst",
        "minecraft:sculk_sensor",
        "minecraft:calibrated_sculk_sensor",
        "minecraft:sculk_shrieker",
        "minecraft:decorated_pot",
    ]
    maps = [
        "player",
        "frame",
        "red_marker",
        "blue_marker",
        "target_x",
        "target_point",
        "player_off_map",
        "player_off_limits",
        "mansion",
        "monument",
        "banner_white",
        "banner_orange",
        "banner_magenta",
        "banner_light_blue",
        "banner_yellow",
        "banner_lime",
        "banner_pink",
        "banner_gray",
        "banner_light_gray",
        "banner_cyan",
        "banner_purple",
        "banner_blue",
        "banner_brown",
        "banner_green",
        "banner_red",
        "banner_black",
        "red_x",
        "village_desert",
        "village_plains",
        "village_savanna",
        "village_snowy",
        "village_taiga",
        "jungle_temple",
        "swamp_hut",
    ]
    itemTypes = {
        "common_item": 12,
        "minecraft:enchanted_book": 0,
        "minecraft:crossbow": 1,
        "minecraft:bundle": 2,
        "minecraft:map": 3,
        "minecraft:writable_book": 4,
        "minecraft:written_book": 5,
        "bucket_entity": 6,
        "minecraft:compass": 7,
        "minecraft:firework_star": 8,
        "minecraft:firework_rocket": 9,
        "minecraft:player_head": 10,
        "block_entity": 11,
    }
    components = [
        #"minecraft:custom_data",
        #"minecraft:unbreakable",
        #"minecraft:damage",
        #"minecraft:repair_cost",
        #"minecraft:enchantments",
        #"minecraft:stored_enchantments",
        #"minecraft:custom_name",
        #"minecraft:lore",
        #"minecraft:can_break",
        #"minecraft:can_place_on",
        #"minecraft:dyed_color",
        #"minecraft:intangible_projectile",
        #"minecraft:attribute_modifiers",
        #"minecraft:charged_projectiles",
        #"minecraft:bundle_contents",
        #"minecraft:map_color",
        #"minecraft:map_decorations",
        #"minecraft:map_id",
        #"minecraft:custom_model_data",
        #"minecraft:potion_contents",
        #"minecraft:writable_book_contents",
        #"minecraft:written_book_contents",
        #"minecraft:trim",
        #"minecraft:hide_additional_tooltip",
        #"minecraft:suspicious_stew",
        #"minecraft:debug_stick_state",
        #"minecraft:entity_data",
        #"minecraft:bucket_entity_data",
        #"minecraft:instrument",
        #"minecraft:lodestone_tracker",
        #"minecraft:firework_explosion",
        #"minecraft:fireworks",
        #"minecraft:profile",
        #"minecraft:note_block_sound",
        #"minecraft:base_color",
        #"minecraft:banner_patterns",
        #"minecraft:pot_decorations",
        #"minecraft:container",
        #"minecraft:container_loot",
        #"minecraft:lock",
        #"minecraft:block_entity_data",
        #"minecraft:block_state",
        #"minecraft:recipes",
        #"minecraft:bees",
        #"minecraft:enchantment_glint_override",
    ]
    potionnbt=[     #药水独有NBT
        "Potion",
        "CustomPotionColor",
        "custom_potion_effects"
    ]
    writable_booknbt=[
        "pages",
        "filtered_pages"
    ]
    bucketnbt = [       #桶装生物
        "Glowing",
        "Health",
        "Invulnerable",
        "NoAI",
        "NoGravity",
        "Silent",
        "BucketVariantTag",
        "Age",
        "HuntingCooldown",
        "Variant",
    ]
    written_booknbt=[ #这里指成书独有的NBT标签，同时成书与书与笔NBT标签的重合部分已被记录
        "author",
        "filtered_title",
        "generation",
        "resolved",
        "title"
    ]
    itemTags = [    #标记游戏中带有的NBT标签，此标签外的NBT标签会被认定为custom_data
        "Enchantments",
        "display",
        "AttributeModifiers",
        "CanPlaceOn",
        "CanDestroy",
        "BlockEntityTag",
        "BlockStateTag",
        "Unbreakable",
        "SkullOwner",
        "HideFlags",
        "generation",
        "Damage",
        "CustomModelData",
        "StoredEnchantments",
        "Glowing",
        "Health",
        "Invulnerable",
        "NoAI",
        "NoGravity",
        "Silent",
        "BucketVariantTag",
        "Age",
        "HuntingCooldown",
        "Variant",
        "Decorations",
        "Trim",
        "instrument",
        "Potion",
        "CustomPotionColor",
        "custom_potion_effects",
        "effects",
        "pages",
        "filtered_pages",
        "author",
        "filtered_title",
        "generation",
        "resolved",
        "title",
        "DebugProperty",
        "Explosion",
        "Fireworks",
        "LodestoneDimension",
        "LodestonePos",
        "LodestoneTracked",
        "SkullOwner",
        "RepairCost",
        "EntityTag",
        "Items",
        "Charged",
        "ChargedProjectiles",
        "map"
    ]
init()


def done(connect = "="):
    '''
    用于重新组合原来零散的NBT数据
    在同一物品已将全部NBT用于输入转换函数后，获取最后几个组合组件
    connect参数用来调整键与值之间的连接符
        如:
        >>>done(":")
        bucket_entity_data:{...}
            ...
    '''
    global dec_name
    global dec_rot
    global dec_type
    global dec_x
    global dec_z
    global potion_contents
    global container_loot
    global bucket_entity_data
    global booktype
    global book_filter
    global lodestonenbt
    global compass_data
    global charged

    if bucket_entity_data[0] == "" and len(bucket_entity_data) != 1:
        bucket_entity_data.pop(0)

    if compass_data[0] == "" and len(compass_data) != 1:
        compass_data.pop(0)

    if potion_contents[0] == "" and len(potion_contents) != 1:
        potion_contents.pop(0)

    bucket = "bucket_entity_data" + connect + "{"
    potion = "potion_contents" + connect + "{"
    compass = "lodestone_tracker" + connect + "{"

    if booktype == "written_book":#判断是否是成书
        endstring = "],"
        writable_book = "written_book_contents" + connect + "{pages:["
    else:
        endstring = "]},"
        writable_book = "writable_book_contents" + connect + "{pages:["

    for i in bucket_entity_data:
        bucket += i + ","
    bucket = bucket[:-1] + "},"

    for i in potion_contents:
        potion += i + ","
    potion = potion[:-1] + "},"

    for i in compass_data:      #磁石指南针
        handle_nbt = i.split(":",1)
        if handle_nbt[0] == "LodestoneTracked":
            compass += "tracked:" + handle_nbt[1] + ","
    loaded = 0
    for i in compass_data:
        handle_nbt = i.split(":",1)
        if handle_nbt[0] == "LodestonePos":
            if loaded == 0:
                compass += "target:{"
            loaded = 1
            compass += "pos:" + handle_nbt[1] + ","
        elif handle_nbt[0] == "LodestoneDimension":
            if loaded == 0:
                compass += "target:{"
            loaded = 1
            compass += "dimension:" + handle_nbt[1] + ","
    for i in range(loaded + 1):
        if compass_data[0] != "":
            compass = compass[:-1] + "},"
        else:
            compass += "},"

    if book_filter != {}:
        ipos = 0
        for i in book_filter["pages"]:#填充书的页面
            ipos += 1
            temp4 = "{text:" + i
            if str(ipos) in book_filter:
                temp4 += ",filtered:" + book_filter[str(ipos)]
            temp4 += "},"
            writable_book += temp4
        writable_book = writable_book[:-1] + endstring

        if booktype == "written_book":#填充成书数据
            writable_book += "author:" + book_filter["author"] + ","
            if "resolved" in book_filter:
                writable_book += "resolved:" + book_filter["resolved"] + ","
            if "generation" in book_filter:
                writable_book += "generation:" + book_filter["generation"] + ","
            writable_book += "title:{text:" + book_filter["title"] + ","
            if "filtered_title" in book_filter:
                writable_book += "filtered:" + book_filter["filtered_title"] + ","
            writable_book = writable_book[:-1] + "}},"

    chargedRet = ""
    if charged != {}:
        if "Charged" in charged and "ChargedProjectiles" in charged:
            chargedRet = "charged_projectiles" + connect + "["
            handle = getNBTList(charged["ChargedProjectiles"][1:-1])
            for i in handle:
                ret = itemStorageTagOld(i)
                chargedRet += ret + ","
            chargedRet = chargedRet[:-1] + "],"

    if bucket == "bucket_entity_data" + connect + "{},":
        bucket = ""
    if potion == "potion_contents" + connect + "{},":
        potion = ""
    if compass == "lodestone_tracker" + connect + "{},":
        compass = ""
    if book_filter == {}:
        writable_book = ""
    if chargedRet == "charged_projectiles" + connect + "],":
        chargedRet == ""
    if HideFlags[-6] == "1":
        hide_additional_tooltip = "hide_additional_tooltip" + connect + "{},"
    else:
        hide_additional_tooltip = ""
    dec_rot,dec_name,dec_type,dec_x,dec_z = "","","","",""
    container_loot,bucket_entity_data,potion_contents,writable_book_content,compass_data = [],[""],[""],[""],[""]
    charged = {}
    output = (bucket + potion + writable_book + compass + chargedRet + hide_additional_tooltip)[:-1]
    return output

def itemType(item):
    for i in block_entity:
        if isinstance(i, str) and item == i:
            return itemTypes["block_entity"]
        elif isinstance(i, list):
            for s in i:
                if item == s:
                    return itemTypes["block_entity"]
    for i in bucket_entity:
        if item == i:
            return itemTypes["bucket_entity"]
    for i in itemTypes.keys():
        if item == i:
            return itemTypes[i]
    return itemTypes["common_item"]


def replaceNBTName(nbt):
    for i in replace.keys():
        if i == nbt:
            return replace[i]
    return nbt


def hideFlags(num, glo = True):
    '''
    由于HideFlags标签被拆分，该函数应在同一物品所有NBT更新前执行以保证NBT正常转换
    如果glo = False，则不改变当前主物品的隐藏部分，并单独返回局部隐藏部分
    '''
    if glo == True:
        global HideFlags
        HideFlags = str(bin(num))[2:]
        HideFlags = (8 - len(HideFlags)) * "0" + HideFlags
        return HideFlags
    else:
        hs = str(bin(num))[2:]
        hs = (8 - len(hs)) * "0" + hs
        return hs
    # print(HideFlags)


def updateNBT(mode, value, connect = "=" ,hs = None):
    if hs == None:
        hs = HideFlags
    '''
    这是升级NBT的规则,传入一对原NBT
        示例:updateNBT("effects","[{id:'minecraft:poison'}]")
        注意传入的两个参数都是字符串
    返回值共有三种：
        customNBT:玩家自定义的NBT，应存储在custom_data组件中
        addin:表示该NBT参与了组合，最后通过done()获取
        <物品堆叠组件>:已经过升级的数据，直接参与拼接即可
    connect参数用来调整键与值之间的连接符
        如:
        >>>updateNBT("Damage","12",":")
        damage:12
    '''
    global bucketnbt
    global potionnbt
    global written_booknbt
    global writable_booknbt
    global container_loot
    global bucket_entity_data
    global potion_contents
    global writable_book_content
    global book_filter
    global booktype
    global lodestonenbt
    global charged

    try:
        if itemTags.count(mode) == 0:
            return "customNBT"
        
        elif bucketnbt.count(mode) == 1:
            bucket_entity_data.append(mode +":" + value)
            return "addin"
        
        elif lodestonenbt.count(mode) == 1:
            compass_data.append(mode +":" + value)
            return "addin"
        
        elif mode == "Charged":
            if value == "True" or value == "true" or value == "1b":
                charged["Charged"] = True
                return "addin"
            else:
                return "addin"
        
        elif mode == "ChargedProjectiles":
            charged["ChargedProjectiles"] = value
            return "addin"

        elif mode == "HideFlags":
            return "addin"

        elif writable_booknbt.count(mode) == 1:#书与笔与成书共同部分
            #writable_book_content.append(mode +":" + value)
            if mode == "filtered_pages":
                temp = getNBTList(value[1:-1])
                for i in temp:
                    handle_nbt = i.split(":",1)
                    book_filter[handle_nbt[0]] = handle_nbt[1]
            elif mode == "pages":
                handle_nbt = getNBTList(value[1:-1])
                book_filter["pages"] = handle_nbt
            return "addin"
        
        elif written_booknbt.count(mode) == 1:#成书独占
            #writable_book_content.append(mode +":" + value)
            booktype = "written_book"
            if mode == "title":
                book_filter["title"] = value
            elif mode == "author":
                book_filter["author"] = value
            elif mode == "filtered_title":
                book_filter["filtered_title"] = value
            elif mode == "generation":
                book_filter["generation"] = value
            elif mode == "resolved":
                book_filter["resolved"] = value
            return "addin"

        elif potionnbt.count(mode) == 1:
            if mode == "Potion":
                potion_contents.append("potion:" + value)
            elif mode == "CustomPotionColor":
                potion_contents.append("custom_color:" + value)
            elif mode == "custom_potion_effects":
                potion_contents.append("custom_effects:" + value)
            return "addin"

        elif mode == "Damage":                                          #damage
            return "damage" + connect + value
        
        elif mode == "map":
            return "map_id" + connect + value

        elif mode == "DebugProperty":                                          
            return "debug_stick_state" + connect + value

        elif mode == "RepairCost":                                          #repair cost
            return "repair_cost" + connect + value
        
        elif mode == "CustomModelData":                                        
            return "custom_model_data" + connect + value
        
        elif mode == "instrument":                                          #instrument
            return "instrument" + connect +  value
        
        elif mode == "Trim":                                          #Trim
            if hs[-8] == "1":
                temp = value[:-1] + ",show_in_tooltip:False}"
                return "trim" + connect +  temp
            else:
                return "trim" + connect + value
            
        elif mode == "effects":                                          #suspicious stew
            return "suspicious_stew_effects" + connect + value

        elif mode == "Recipes":                                          #recipes
            return "recipes" + connect +  value
        
        elif mode == "Unbreakable" and value == "1b" or value == "True" or value == "true":  # unbreakable
            if hs[-3] == "1":
                return "unbreakable" + connect + "{show_in_tooltip:False}"
            else:
                return "unbreakable" + connect + "{}"
        elif mode == "Unbreakable" and value != "1b" and value != "True" and value != "0b" and value != "False" or value != "false" and value == "true":
            return "unbreakable" + connect + value
            
        elif mode == "Enchantments":                                      #enchantments
            if value == "[]":
                return "enchantment_glint_override" + connect + "true"
            else:
                temp = value[1:-1]
                enchant_list = getNBTList(temp)
                output = ""
                for i in enchant_list:
                    i = getNBTList(i[1:-1])
                    temp_data = {}
                    for s in i:
                        temp2 = s.split(":",1)
                        if temp2[0] == "id":
                            temp_data.update(id=temp2[1])
                        else:
                            temp_data.update(lvl=temp2[1])
                    enchant = temp_data["id"] + ":" + temp_data["lvl"]
                    output += enchant + ","
                output = output[:-1]
                if hs[-1] == "1":
                    return "enchantment_glint_override" + connect + "true,enchantments" + connect + "{show_in_tooltip:False,levels:{" + output + "}}"
                else:
                    return "enchantment_glint_override" + connect + "true,enchantments" + connect + "{levels:{" + output + "}}"
            
        elif mode == "StoredEnchantments":                                #enchanted books
            if value == "":
                return "enchantment_glint_override" + connect + "true"
            else:
                temp = value[1:-1]
                enchant_list = getNBTList(temp)
                output = ""
                for i in enchant_list:
                    i = getNBTList(i[1:-1])
                    temp_data = {}
                    for s in i:
                        temp2 = s.split(":",1)
                        if temp2[0] == "id":
                            temp_data.update(id=temp2[1])
                        else:
                            temp_data.update(lvl=temp2[1])
                    enchant = temp_data["id"] + ":" + temp_data["lvl"]
                    output += enchant + ","
                output = output[:-1]
                if hs[-6] == "1":
                    return (
                        "enchantment_glint_override" + connect + "true,stored_enchantments" + connect + "{show_in_tooltip:False,levels:{" + output + "}}"
                    )
                else:
                    return "enchantment_glint_override" + connect + "true,stored_enchantments" + connect + "{levels:{" + output + "}}"
                
        elif mode == "display":                                             #display
            #print(value)
            temp = value[1:-1]
            NBTList = getNBTList(temp)
            #print(NBTList)
            output = []
            for i in NBTList:
                handle_nbt = i.split(":",1)
                #print(handle_nbt)
                if handle_nbt[0] == "Name":
                    output.append("custom_name" + connect + handle_nbt[1])
                elif handle_nbt[0] == "Lore":
                    output.append("lore" + connect + handle_nbt[1])
                elif handle_nbt[0] == "color":
                    if hs[-7] == "1":
                        output.append("dyed_color" + connect + "{rgb:" + handle_nbt[1] + ",show_in_tooltip:False}")
                    else:
                        output.append("dyed_color" + connect + "{rgb:" + handle_nbt[1] + "}")
                elif handle_nbt[0] == "MapColor":
                    output.append("map_color" + connect + handle_nbt[1])
            strout = ""
            for i in output:
                strout += i + ","
            strout = strout[:-1]
            return strout

        elif mode == "AttributeModifiers":
            temp = value[2:-2]
            temp2 = temp.split("},{")
            #print(NBTlist)
            #print(temp2)
            modifiers  = ""
            for i in temp2:
                NBTList = getNBTList(i)
                #print(NBTList,"############")
                #print(NBTList)
                modifier = "{"
                for s in NBTList:
                    handle_nbt = s.split(":",1)
                    if handle_nbt[0][1:-1] == "UUID" or handle_nbt[0] == "UUID":
                        modifier += "\"uuid\":"+ handle_nbt[1] + ","
                    elif handle_nbt[0][1:-1] == "Operation" or handle_nbt[0] == "Operation":
                        if handle_nbt[1] == "0":
                            modifier += "\"operation\":'add_value',"
                        elif handle_nbt[1] == "1":
                            modifier += "\"operation\":'add_multiplied_base',"
                        elif handle_nbt[1] == "2":
                            modifier += "\"operation\":'add_multiplied_total',"
                    elif handle_nbt[0][1:-1] == "Name" or handle_nbt[0] == "Name":
                        modifier += "\"name\":"+ handle_nbt[1] + ","
                    elif handle_nbt[0][1:-1] == "AttributeName" or handle_nbt[0] == "AttributeName":
                        modifier += "\"type\":"+ handle_nbt[1] + ","
                    elif handle_nbt[0][1:-1] == "Amount" or handle_nbt[0] == "Amount":
                        modifier += "\"amount\":"+ handle_nbt[1] + ","
                    elif handle_nbt[0][1:-1] == "Slot" or handle_nbt[0] == "Slot":
                        modifier += "\"slot\":"+ handle_nbt[1] + ","
                modifier = modifier[:-1] + "}"
                modifiers += modifier + ","
            modifiers = "modifiers:[" + modifiers[:-1] + "]" 
            #print(modifiers)
            if hs[-2] == "1":
                return "attribute_modifiers" + connect + "{show_in_tooltip:False," + modifiers + "}"
            else:
                return "attribute_modifiers" + connect + "{" + modifiers + "}"

        elif mode == "EntityTag":       #What the fuck这是一坨什么答辩
            ret = entityData.updateEntityNBT(value)
            return "entity_data" + connect + ret
            # nbts = getNBTList(value[1:-1])
            # #print(nbts)
            # wrote = ""
            # for i in nbts:
            #     handle_nbt = i.split(":",1)
            #     print(handle_nbt[1])
            #     #if handle_nbt[0] == "Passen"
            #     cutable = 1
            #     while cutable >= 1:
            #         cuttimes = 0
            #         pos = 0
            #         for s in handle_nbt:
            #             if s[0] == "{"and s[-1] == "}":
            #                 cuttimes +=  1
            #                 handle_nbt.pop(pos)
            #                 a = getNBTList(s[1:-1]) 
            #                 temp4 = handle_nbt[pos:]
            #                 handle_nbt = handle_nbt[:pos]
            #                 handle_nbt.append("{")
            #                 handle_nbt.extend(a)
            #                 handle_nbt.append("},")
            #                 handle_nbt.extend(temp4)
            #             elif s[0] == "["and s[-1] == "]":
            #                 cuttimes += 1
            #                 handle_nbt.pop(pos)
            #                 a = getNBTList(s[1:-1]) 
            #                 temp4 = handle_nbt[pos:]
            #                 handle_nbt = handle_nbt[:pos]
            #                 handle_nbt.append("[")
            #                 handle_nbt.extend(a)
            #                 handle_nbt.append("],")
            #                 handle_nbt.extend(temp4)
            #             pos2 = 0
            #             for s in handle_nbt:
            #                 if s.count(":[") >= 1 and s[-1] == "]" or s.count(":{") >= 1 and s[-1] == "}":
            #                     a = handle_nbt.pop(pos2) 
            #                     temp5 = handle_nbt[pos2:]
            #                     handle_nbt = handle_nbt[:pos2]
            #                     a = a.split(":",1)
            #                     a[0] += ":"
            #                     handle_nbt.extend(a)
            #                     handle_nbt.extend(temp5)
            #                 pos2 += 1
            #             pos += 1
            #         if cuttimes == 0:
            #             cutable = 0
            #             out = ""
            #     print(handle_nbt)
            #     for t in handle_nbt[1:]:
            #         out += t
            #     wrote += handle_nbt[0] + ":" + t + ","
            # print(wrote,out)
            # return 0
        
        elif mode == "BlockEntityTag":
            outputlist = "{"
            temp = value[1:-1]
            tags = getNBTList(temp)
            #print(tags)
            for i in tags:
                handle_nbt = i.split(":",1)
            
                if handle_nbt[0] == "note_block_sound":
                    outputlist += "note_block_sound:" + handle_nbt[1] + ","

                elif handle_nbt[0] == "Base":
                    outputlist += "base_color:"+ base_color[int(handle_nbt[1])%16] + ","

                elif handle_nbt[0] == "Patterns":
                    pattern = "{"
                    parts = handle_nbt[1][2:-2].split("},{")
                    for s in parts:
                        handle_part = getNBTList(s)
                        #print(handle_part)
                        for p in handle_part:
                            temp3 = p.split(":",1)
                            if temp3[0] == "Pattern":
                                pattern += "pattern:" + temp3[1] + ","
                            elif temp3[0] == "Color":
                                pattern += "color:" + base_color[int(temp3[1])%16] + ","
                        pattern = pattern[:-1] + "},{"
                    pattern = "[" + pattern[:-2] + "]"
                    outputlist += "banner_patterns:" + pattern + ","
                    
                elif handle_nbt[0] == "sherds":
                    outputlist += "pot_decorations:" + handle_nbt[1] + ","

                elif handle_nbt[0] == "Items":          #我需要新的函数(不用了)
                    final = "container:["
                    items = getNBTList(handle_nbt[1][1:-1])
                    for s in items:
                        anItem = "{item:{"
                        handle_part = getNBTList(s[1:-1])
                        for t in handle_part:
                            get = t.split(":",1)
                            if get[0] == "Slot":
                                if get[1][-1] == "b": slot = get[1][:-1]
                                elif get[1][-1] != "b": slot = get[1]
                                else: return "Fail"
                            else:
                                anItem  += t + ","
                        anItem = anItem[:-1] + "},"
                        anItem += "slot:" + slot + "},"
                        final += anItem
                    final = final[:-1] + "],"
                    outputlist += final


                    #print()
                elif handle_nbt[0] == "Bees":
                    #beeslist = handle_nbt[1][2:-2].split("},{")
                    bees = handle_nbt[1].replace("EntityData:","entity_data:")
                    bees = bees.replace("TicksInHive:","ticks_in_hive:")
                    bees = bees.replace("MinOccupationTicks:","min_ticks_in_hive:")
                    bees = "bees:" + bees
                    outputlist += bees + ","
                    #print(bees)

                elif handle_nbt[0] == "FlowerPos":        #不小心加的(算了加回来吧)
                    poss = getNBTList(handle_nbt[1][1:-1])
                    poslist = "["
                    for i in poss:
                        poslist += i[2:] + ","
                    poslist = poslist[:-1] + "]"
                    outputlist += "flower_pos:" +  poslist + ","

                elif handle_nbt[0] == "Lock":
                    outputlist += "lock:" + handle_nbt[1] + ","
                    #print(handle_nbt[1])
                
                elif handle_nbt[0] == "LootTable":
                    container_loot.append("loot_table:" + handle_nbt[1])

                elif handle_nbt[0] == "LootTableSeed":
                    container_loot.append("seed:" + handle_nbt[1])


            container_loots = "container_loot:{"
            for i in container_loot:
                container_loots += i + ","
            container_loots = container_loots[:-1] + "},"
            if container_loots == 'container_loot:},':
                container_loots = ""
            outputlist += container_loots

            if outputlist[-1] == ",":
                outputlist = outputlist[:-1] + "}"
            else:
                outputlist += "}"
            return "block_entity_data" + connect + outputlist
        
        elif mode == "CanDestroy":
            blocks = value[1:-1].split(",")
            if hs[-4] == "1":
                show = ",show_in_tooltip:False"
            else:
                show = ""
            islist = len(blocks) == 1
            outputlist = ""
            #print(blocks)
            for i in blocks:
                outputlist += i + ","
            outputlist = outputlist[:-1]
            if not islist:
                return "can_break" + connect + "{blocks:[" + outputlist + "]"+ show +"}"
            else:
                return "can_break" + connect + "{blocks:" + outputlist +  show +"}"
            
        elif mode == "CanPlaceOn":
            blocks = value[1:-1].split(",")
            if hs[-5] == "1":
                show = ",show_in_tooltip:False"
            else:
                show = ""
            islist = len(blocks) == 1
            outputlist = ""
            #print(blocks)
            for i in blocks:
                outputlist += i + ","
            outputlist = outputlist[:-1]
            if not islist:
                return "can_place_on" + connect + "{blocks:[" + outputlist + "]"+ show +"}"
            else:
                return "can_place_on" + connect + "{blocks:" + outputlist +  show +"}"
        
        elif mode == "BlockStateTag":
            return "block_state" + connect + value
        
        elif mode == "Decorations":
            global dec_name
            global dec_rot
            global dec_type
            global dec_x
            global dec_z
            map_decorations = "map_decorations" + connect + "{"
            decorations = value[2:-2].split("},{")
            for i in decorations:
                handle_nbt = getNBTList(i)
                for s in handle_nbt:
                    handle_part = s.split(":",1)
                    if handle_part[0] == "id":
                        dec_name = handle_part[1]
                    elif handle_part[0] == "type":
                        dec_type = "type:\"" + maps[int(handle_part[1])] + "\","
                    elif handle_part[0] == "x":
                        dec_x = "x:" + handle_part[1] + ","
                    elif handle_part[0] == "z":
                        dec_z = "z:" + handle_part[1] + ","
                    elif handle_part[0] == "rot": #change "double" to "float"
                        if handle_part[1][-1] != "f":
                            if handle_part[1][-1] == "d": dec_rot = "rotation:" + handle_part[1][:-1] + "f,"
                            else: dec_rot = "rotation:" + handle_part[1] + "f,"
                        else:
                            dec_rot = "rotation:" + handle_part[1] + ","
                map_decorations += (dec_name + ":{" + dec_type + dec_x + dec_z + dec_rot)[:-1] + "},"
                dec_rot,dec_name,dec_type,dec_x,dec_z = "","","","",""
            map_decorations = map_decorations[:-1] + "}"
            return map_decorations
        
        elif mode == "Items":
            Items = "bundle_contents" + connect + "["
            handle = getNBTList(value[1:-1])
            for i in handle:
                ret = itemStorageTagOld(i)
                Items += ret + ","
            Items = Items[:-1] + "]"
            return Items

        elif mode == "Explosion":   #烟火之星,同时烟花火箭也采用此相同逻辑作为爆炸效果
            explosion = "firework_explosion" + connect + "{"
            temp = value[1:-1]
            fstags = getNBTList(temp)
            for i in fstags:
                handle_nbt = i.split(":",1)
                if handle_nbt[0] == "Colors":
                    explosion += "colors:" + handle_nbt[1] + ","
                elif handle_nbt[0] == "FadeColors":
                    explosion += "fade_colors:" + handle_nbt[1] + ","
                elif handle_nbt[0] == "Flicker":
                    explosion += "has_twinkle:" + handle_nbt[1] + ","
                elif handle_nbt[0] == "Trail":
                    explosion += "has_trail:" + handle_nbt[1] + ","
                elif handle_nbt[0] == "Type":
                    explosion += "shape:\"" + firework_star_shapes[int(handle_nbt[1])] + "\","
            explosion = explosion[:-1] + "}"
            return explosion
            
        elif mode == "Fireworks":   #烟花火箭
            firework = "fireworks" + connect + "{"
            temp = value[1:-1]
            fireworktag = getNBTList(temp)
            for i in fireworktag:
                handle_nbt = i.split(":",1)
                if handle_nbt[0] == "Flight":
                    firework += "flight_duration:" + handle_nbt[1] + ","
                elif handle_nbt[0] == "Explosions":
                    firework += "explosions:["
                    explosionsList = handle_nbt[1][2:-2].split("},{")
                    for s in explosionsList:
                        explo = "{"
                        handle_part = getNBTList(s)
                        for t in handle_part:
                            handle = t.split(":",1)
                            if handle[0] == "Colors":
                                explo += "colors:" + handle[1] + ","
                            elif handle[0] == "FadeColors":
                                explo += "fade_colors:" + handle[1] + ","
                            elif handle[0] == "Flicker":
                                explo += "has_twinkle:" + handle[1] + ","
                            elif handle[0] == "Trail":
                                explo += "has_trail:" + handle[1] + ","
                            elif handle[0] == "Type":
                                explo += "shape:\"" + firework_star_shapes[int(handle[1])] + "\","
                        explo = explo[:-1] + "},"
                        firework += explo
                    firework = firework[:-1] + "],"
            firework = firework[:-1] + "}"
            return firework

        elif mode == "SkullOwner":
            if value[0] == "{":#判断是否为符合标签形式
                output = "profile" + connect + "{"
                profile_list = getNBTList(value[1:-1])
                #print(profile_list)
                for i in profile_list:
                    handle_nbt = i.split(":",1)
                    if handle_nbt[0] == "Id":
                        output += "id:" + handle_nbt[1] + ","
                    elif handle_nbt[0] == "Name":
                        output += "name:" + handle_nbt[1] + ","
                    elif handle_nbt[0] == "Properties":
                        output += "properties:["
                        propertys = getNBTList(handle_nbt[1][1:-1].replace("textures:","")[1:-1])
                        for s in propertys:
                            onep = "{"
                            handle_part = getNBTList(s[1:-1])
                            for t in handle_part:
                                temp2 = t.split(":",1)
                                if temp2[0] == "Value":
                                    onep += "value:" + temp2[1] + ","
                                elif temp2[0] == "Signature":
                                    onep += "signature:" + temp2[1] + ","
                            onep += "name:" + randomPropertyName() + ","
                            onep = onep[:-1] + "},"
                            output += onep
                        output = output[:-1] + "],"
                output = output[:-1] + "}"
                return output
            else:               #字符串形式
                return "profile" + connect + value
    except:
        reporter.reporter.Error(f"Update nbt error,at'{mode}:{value}',at{globalStorage.thisFile}",logp="itemData",path=globalStorage.thisFile)
        return "Fail"

def itemStorageTagOld(tag = "{}"):
    '''
    用来升级物品通用存储格式
    输入为字符串，如：
        itemStorageTagOld("{id:'minecraft:diamond',Count:12,tag:{Unbreakable:1b}}")
    返回字符串，如：
        "{id:'minecraft:diamond',count:12,components:{unbreakable:true}}"
    '''
    try:
        output = "{"
        storage = getNBTList(tag[1:-1])
        for i in storage:
            handle_part = i.split(":",1)
            if handle_part[0] == "id":
                output += "id:" + handle_part[1] + ","
            elif handle_part[0] == "Count":
                output += "count:" + handle_part[1] + ","
                try:
                    if handle_part[1][-1] == "b":
                        handle_part[1] = handle_part[1][:-1]
                    if int(handle_part[1]) > 64:
                        print("[Warn]Count>64, at" + tag)
                finally:
                    pass
            elif handle_part[0] == "tag":
                local_hs = "00000000"
                cd = "custom_data:{"
                comp = "components:{"
                nbts = getNBTList(handle_part[1][1:-1])
                for s in nbts:
                    temp = s.split(":",1)
                    if temp[0] == "HideFlags":
                        local_hs = hideFlags(int(temp[1]),False)
                for s in nbts:
                    temp = s.split(":",1)
                    ret = updateNBT(temp[0],temp[1],":",local_hs)
                    if ret == "customNBT":
                        cd += s + ","
                    elif ret == "addin":
                        pass
                    else:
                        comp += ret + ","
                cd = cd[:-1] + "},"
                if cd == "custom_data:},":
                    cd = ""
                comp = (comp + cd + done(":"))[:-1] + "}"
                output += comp + ","
        if output != "{":
            output = output[:-1] + "}"
        else:
            output += "}"
        return output
    except:
        reporter.reporter.Error(f"Update nbt error,at'{tag}',at{globalStorage.thisFile}",logp="itemData",path=globalStorage.thisFile)
        return "Fail"


if __name__ == "__main__":
    hideFlags(255)
    '''
    print(updateNBT("Charged","True"))
    print(updateNBT("ChargedProjectiles","[{id:'minecraft:dirt',Count:1b},{id:'minecraft:grass',Count:1b}]"))
    print(done())
    '''
    #print(updateNBT("Items","[{id:'minecraft:dirt',Count:17},{id:'minecraft:diamond',Count:1b}]") + "," + done())
    print(updateNBT("BlockEntityTag","{id:'minecrat'}",connect=":"))
    #print(updateNBT("StoredEnchantments","[{lvl:3s,id:'minecraft:fortune'}]"))
    #print(updateNBT("BlockEntityTag","{Lock:'asa',LootTable:'minecraft:chests/buried_treasure',LootTableSeed:1145141919810}"))
    # print(updateNBT("EntityTag","{id:\"minecraft:iron_golem\",Health:1f,as:{csa:[{as},{df}]}}"))
#print(itemStorageTagOld("{id:'minecraft:diamond',Count:12,tag:{Unbreakable:1b,RepairCost:12,NoAI:1b,Age:14,HideFlags:1}}"))
#print(randomPropertyName())
#print(updateNBT("SkullOwner","{Id:'[I,12,23,34]',Name:'abc',Properties:{textures:[{Value:\"ABCDEFG\",Signature:\"s\"},{Value:\"HIJKLMN\"}]}}"))

'''
print(updateNBT("LodestoneTracked","1b"))
print(updateNBT("LodestonePos","[I,1,2,3]"))
print(updateNBT("LodestoneDimension","minecraft:overworld"))
print(done())
'''
#print(updateNBT("Fireworks","{Flight:3,Explosions:[{Colors:[1,2,3],FadeColors:[4,5,6],Flicker:1b,Trail:1b,Type:2},{Colors:[1,2,3],FadeColors:[4,5,6],Flicker:0b,Trail:1b,Type:4}]}"))
#print(updateNBT("Explosion","{Colors:[1,2,3],FadeColors:[4,5,6],Flicker:1b,Trail:1b,Type:2}"))
#print(moduleVersion())
#print(updateNBT("DebugProperty","{\"minecraft:grass_block\": \"snowy\"}"))
'''
print(updateNBT("title","'fuck'"))
print(updateNBT("author","'fucku'"))
print(updateNBT("filtered_pages","{1:'c',2:'d'}"))
print(updateNBT("filtered_title","'as'"))
print(updateNBT("pages","['a','b','c']"))
print(done())
'''
# print(updateNBT("Trim","{pattern:'minecraft:silence',material:'minecraft:redstone'}"))
# print(updateNBT("Decorations","[{id:'as',type:26,x:114.0d,z:514.0d,rot:0.0f},{id:'ass',type:27,x:114.0d,z:514.0d,rot:0.0d}]"))
# print(updateNBT("effects","[{id:'minecraft:poison'}]"))
'''
print(updateNBT("Potion","'minecraft:invisibility'"))
print(updateNBT("CustomPotionColor","16711680"))
print(updateNBT("NoAI","1b"))
print(updateNBT("Age","44"))
print(done())
'''
# print(updateNBT("BlockStateTag","{waterlogged:\"true\"}"))
# print(updateNBT("CanPlaceOn","[\"minecraft:dirt\",\"#minecraft:air\"]"))
# print(updateNBT("BlockEntityTag","{Lock:'asa',LootTable:'minecraft:chests/buried_treasure',LootTableSeed:1145141919810}"))
# print(updateNBT("BlockEntityTag","{FlowerPos:{X:1.0,Y:1.0,Z:1.0}}"))
# print(updateNBT("BlockEntityTag","{FlowerPos:{X:1.0,Y:1.0,Z:1.0},Bees:[{EntityData:{id:'minecraft:bee'},MinOccupationTicks:1145,TicksInHive:100},{EntityData:{id:'minecraft:bee'},MinOccupationTicks:1160,TicksInHive:200}]}"))
#print(updateNBT("BlockEntityTag","{Items:[{id:'asd',Count:1b,Slot:2},{id:'oak',Count:13,Slot:4b}]"))
# print(updateNBT("BlockEntityTag","{note_block_sound:'a',Base:2,Patterns:[{Pattern:'minecraft:stripe_top',Color:1},{Pattern:'minecraft:stripe_top',Color:2}],sherds:['arms_up_pottery_sherd','angler_pottery_sherd','danger_pottery_sherd','shelter_pottery_sherd']}"))
# print(updateNBT("AttributeModifiers","[{AttributeName:\"a\",Name:\"a\",Amount:a,Operation:1,UUID:[I;1,2,3,4],Slot:s},{AttributeName:\"a\",Name:\"a\",Amount:a,Operation:2,UUID:[I;1,2,3,4],Slot:s}]"))
# print(updateNBT("display","{Name:{\"text\":\"wps\",\"color\":\"red\"},color:12345678,Lore:['{\"text\": \"蛋糕是个谎言！\"}'],MapColor:12345678}"))
    
# print(itemType("minecraft:barrel"))
# print(updateNBTName("Unbreakable"))
#print(updateNBT("AttributeModifiers","[{\"AttributeName\":\"generic.attack_damage\",\"Name\":\"abc\"}]"))
#print(updateNBT("display","{Name:abs}"))