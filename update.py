import itemData
import entityData
import NBTPath
import globalStorage
import reporter

def init():
    global commands_in_file
    commands_in_file = {}

def commandInit(inp_command = ""):
    '''
    返回一个sid\n
    在commands_in_file字典里通过commands_in_file[sid]访问命令信息\n
    sid.raw:原命令\n
    sid.cut:分段后的命令\n
    sid.type:命令类型\n
    '''
    global commands_in_file
    inp_command = inp_command.lstrip()
    command = itemData.getNBTList(inp_command," ")#精准拆分命令
    if inp_command != "" and inp_command != None:
        if command[0] == "give":
            command_type = "give"
        elif command[0] == "item":
            command_type = "item"
        elif command[0] == "loot":
            command_type = "loot"
        elif command[0] == "execute":
            command_type = "execute"
        elif command[0] == "clear":
            command_type = "clear"
        elif command[0] == "summon":
            command_type = "summon"
        elif command[0] == "#":
            command_type = "pass"
        else:
            command_type = "common"
        sid = itemData.randomPropertyName(8)
        commands_in_file[sid] = {}
        commands_in_file[sid]["raw"] = inp_command
        commands_in_file[sid]["cut"] = command
        commands_in_file[sid]["type"] = command_type
        return sid
    else:
        reporter.reporter.Error(f"Command init error,at'{inp_command}',at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
        return "Fail"

def exec_ccmd(cmd = None):
    if cmd == None:
        return ""
    else:
        sid = commandInit(cmd)
        commandType = commands_in_file[sid]["type"]
        if commandType == "give":
            return give(sid)
        elif commandType == "item":
            return item(sid)
        elif commandType == "loot":
            return loot(sid)
        elif commandType == "execute":
            return execute(sid)
        elif commandType == "clear":
            return clear(sid)
        elif commandType == "summon":
            return summon(sid)
        elif commandType == "common":
            return common_command(sid)
        elif commandType == "pass":
            return commands_in_file[sid]["raw"]

def item_stack(item_nbt = None,connectletter = "=",wrapper = "[]"):
    '''
    将nbt转换为物品堆叠组件
    Example:
        item_stack("{Unbreakable:1b}")
    '''
    if item_nbt == None:
        return ""
    else:
        item_nbt = itemData.format_nbt(item_nbt)
        nbts = itemData.getNBTList(item_nbt[1:-1])
        sd = wrapper[0]
        cd = "custom_data={"

        for i in nbts:      #筛选HideFlags
            handle = i.split(":",1)
            if handle[0] == "HideFlags":
                itemData.hideFlags(int(handle[1]))

        for i in nbts:
            handle = i.split(":",1)
            ret = itemData.updateNBT(handle[0],handle[1],connect=connectletter)
            if ret == "customNBT":
                cd += i + ","
            elif ret == "addin":
                pass
            else:
                if ret != None:
                    sd += ret + ","

        last = itemData.done(connect=connectletter)#将done()返回值格式化
        if last != "":
            last = last + ","

        cd = cd[:-1] + "},"
        if cd == "custom_data=},":
            cd = ""
        sd = (sd + cd + last)[:-1] + wrapper[1]
        if sd == wrapper[1]:
            sd = wrapper
        return sd
#————————————————————————————————————————————————————————————————————————————————————————————————————
def give(sid = None):
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]
            if cmd[2].count("{") != 0:
                item = cmd[2][:cmd[2].index("{")]   #get item name (minecraft:xxx/xxx)
                if item.count("minecraft:") == 0:
                    item = "minecraft:" + item
                nbt = cmd[2][cmd[2].index("{"):]    #get nbt ({Unbreakable:1b})

                output = item_stack(nbt)

                cmd[1] = entityData.target_selector(cmd[1])

                if len(cmd) == 4:
                    return cmd[0] + " " + cmd[1] + " " + item + output + " " + cmd[3]
                else:
                    return cmd[0] + " " + cmd[1] + " " + item + output
            else:
                if len(cmd) == 4:
                    return cmd[0] + " " + cmd[1] + " " + cmd[2] + " " + cmd[3]
                else:
                    return cmd[0] + " " + cmd[1] + " " + cmd[2]
        except:
            reporter.reporter.Error(f"Update command 'give' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#——————————————————————————————————————————————————————————————————————————————————————————————————

def item(sid = None):
    '''
    数据结构:
        item modify (block <POS>[不考虑]  |entity <TARGET>) ... \n
        item replace ...
            with <ITEM>(转换) <COUNT>\n
            from (block <POS>[不考虑]  |entity <TARGET>)
    sid为字符串，是一个commandInit返回的sid
    Example:item("aA15Bc2D")
    '''

    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]

            if cmd[1] == "modify":      #当是item modify时
                if cmd[2] == "entity":
                    cmd[3] = entityData.target_selector(cmd[3])

            else:       #item replace
                if cmd[2] == "with":

                    item = cmd[3].split("{",1)[0]       #获取item的id
                    if item.count("minecraft:") == 0:
                        item = "minecraft:" + item

                    nbt = cmd[3][cmd[3].index("{"):]     #获取nbt
                    ret = item_stack(nbt)
                    item = item + ret
                    cmd[3] = item
                else:       #item replace from
                    if cmd[3] == "entity":
                        cmd[4] = entityData.target_selector(cmd[4])
            
            output = ""
            for i in cmd:
                output += i + " "
            return output
        except:
            reporter.reporter.Error(f"Update command 'item' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#——————————————————————————————————————————————————————————————————————————————————————————————————

def loot(sid = None):
    '''
    命令结构：
    loot <来源> <目标>\n
    来源:

     
    '''
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]

            target = ""
            to = ""
            if cmd[1] == "give":
                target += "give " + entityData.target_selector(cmd[2])
                to = cmd[3:]
            elif cmd[1] == "insert":
                target += "insert " + cmd[2] + " " + cmd[3] + " " + cmd[4]
                to = cmd[5:]
            elif cmd[1] == "spawn":
                target += "spawn " + cmd[2] + " " + cmd[3] + " " + cmd[4]
                to = cmd[5:]

            elif cmd[1] == "replace":
                target += "relpace "
                if cmd[2] == "block":
                    target += "block " + cmd[3] + " " + cmd[4] + " " + cmd[5] + " " + cmd[6]
                    try:
                        int(cmd[7])
                        has_count = True
                    except:
                        has_count = False
                    if has_count == True:
                        target += " " + cmd[7]
                        to = cmd[8:]
                    else:
                        to = cmd[7:]
                elif cmd[2] == "entity":
                    target += "entity " + entityData.target_selector(cmd[3]) + cmd[4]
                    try:
                        int(cmd[5])
                        has_count = True
                    except:
                        has_count = False
                    if has_count == True:
                        target += " " + cmd[5]
                        to = cmd[6:]
                    else:
                        to = cmd[5:]
            #print(to)
            #目标
            op2 = ""
            if to[0] == "loot":
                op2 += "loot " + to[1]
            elif to[0] == "kill":
                op2 += "kill " + entityData.target_selector(to[1])
            elif to[0] == "fish":
                op2 += "fish " + to[1] + " " + to[2] + " " + to[3] + " " + to[4]
                if len(to) == 6:
                    if to[5] == "mainhand" or to[5] == "offhand":
                        op2 += " " + to[5]
                    else:
                        handle_item = to[5].split("{",1)[0]
                        tag = "{" + to[5].split("{",1)[1]
                        tag = item_stack(tag)
                        op2 += " " + handle_item + tag
            elif to[0] == "mine":
                op2 += "mine " + to[1] + " " + to[2] + " " + to[3]
                if len(to) == 5:
                    if to[4] == "mainhand" or to[4] == "offhand":
                        op2 += " " + to[4]
                    else:
                        handle_item = to[4].split("{",1)[0]
                        tag = "{" + to[4].split("{",1)[1]
                        tag = item_stack(tag)
                        op2 += " " + handle_item + tag
            return target + " " + op2
        except:
            reporter.reporter.Error(f"Update command 'loot' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#———————————————————————————————————————————————————————————————————————————————————————————————————
def clear(sid = None):
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]
            cmd[1] = entityData.target_selector(cmd[1])
            handle_item = cmd[2].split("{",1)[0]
            tag = "{" + cmd[2].split("{",1)[1]
            tag = item_stack(tag)
            cmd[2] = handle_item + tag
            result = ""
            for i in cmd:
                result += i + " " 
            return result
        except:
            reporter.reporter.Error(f"Update command 'clear' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#———————————————————————————————————————————————————————————————————————————————————————————————————
def attribute(sid = None):
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]
            cmd[1] = entityData.target_selector(cmd[1])
            if len(cmd) == 9:
                if cmd[8] == "add":
                    cmd[8] = "add_value"
                elif cmd[8] == "multiply":
                    cmd[8] = "add_multiplied_total"
                elif cmd[8] == "multiply_base":
                    cmd[8] = "add_multiplied_base"
            result = ""
            for i in cmd:
                result += i + " " 
            return result
        except:
            reporter.reporter.Error(f"Update command 'attribute' error,,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail" 
#————————————————————————————————————————————————————————————————————————————————————————————————————
def common_command(sid = None):
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]
            pos = 0
            for i in cmd:
                if i[-1] == "]" and i [0] != "[":
                    cmd[pos] = entityData.target_selector(i)
                pos += 1
            result = ""
            for i in cmd:
                result += i + " " 
            return result
        except:
            reporter.reporter.Error(f"Update command 'common_command' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#————————————————————————————————————————————————————————————————————————————————————————————————————
def execute(sid = None):
    if sid == None:
        return ""
    else:
        try:
            twice_command = "None"
            cmd = commands_in_file[sid]["cut"]
            pointer = 1
            loopTime = 0
            not_finished = True
            while not_finished == True and pointer < len(cmd):
                loopTime += 1
                try:
                    handle = cmd[pointer]
                except:
                    not_finished = False
                    runCommands = cmd[pointer + 1:]
                    executeParts = cmd[:pointer + 1]
                if handle == "align" or handle == "anchored" or handle == "in" or handle == "on":
                    pointer += 2
                elif handle == "as" or handle == "at":
                    cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                    pointer += 2
                elif handle == "facing":
                    if cmd[pointer + 1] == "entity":
                        cmd[pointer + 2] == entityData.target_selector(cmd[pointer + 2])
                    pointer += 4
                elif handle == "positioned":
                    if cmd[pointer + 1] == "over":
                        pointer += 3
                    elif cmd[pointer + 1] == "as":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                        pointer += 3
                    else:
                        pointer += 4
                elif handle == "rotated":
                    if cmd[pointer + 1] == "as":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                    pointer += 3
                elif handle == "if" or handle == "unless":
                    twice_command = "if"
                    pointer += 1
                elif handle == "store":
                    twice_command = "store"
                    pointer += 2
                elif handle == "biome":
                    pointer += 5
                    twice_command == "None"
                elif handle == "block":
                    if twice_command == "if":
                        pointer += 5
                        twice_command = "None"
                    elif twice_command == "store":
                        cmd[pointer + 4] = NBTPath.ItemNBTPath(cmd[pointer + 4],"block")
                        pointer += 7
                        twice_command = "None"
                elif handle == "blocks":
                    pointer += 11
                    twice_command == "None"
                elif handle == "data":
                    if cmd[pointer + 1] == "block":
                        cmd[pointer + 5] = NBTPath.ItemNBTPath(cmd[pointer + 5],"block")
                        pointer += 6
                    elif cmd[pointer + 1] == "entity":
                        cmd[pointer + 2] = entityData.target_selector(cmd[pointer + 2])
                        cmd[pointer + 3] = NBTPath.ItemNBTPath(cmd[pointer + 3],"entity")
                        pointer += 4
                    else:
                        cmd[pointer + 2] = entityData.target_selector(cmd[pointer + 2])
                        pointer += 4
                    twice_command == "None"
                elif handle == "entity":
                    if twice_command == "if":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                        twice_command = "None"
                        pointer += 2
                    elif twice_command == "store":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                        cmd[pointer + 2] = NBTPath.ItemNBTPath(cmd[pointer + 2],"entity")
                        twice_command = "None"
                        pointer += 5
                elif handle == "loaded":
                    pointer += 4
                    twice_command == "None"
                elif handle == "score":
                    if twice_command == "if":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                        if cmd[pointer + 3] == "matches":
                            pointer += 5
                        else:
                            cmd[pointer + 4] = entityData.target_selector(cmd[pointer + 4])
                            pointer += 6
                        twice_command = "None"
                    elif twice_command == "store":
                        cmd[pointer + 1] = entityData.target_selector(cmd[pointer + 1])
                        pointer += 3
                        twice_command = "None"
                elif handle == "bossbar":
                    pointer += 3
                    twice_command == "None"
                elif handle == "storage":
                    pointer += 5
                    twice_command == "None"
                elif handle == "dimension" or handle == "function" or handle == "predicate":
                    pointer += 2
                    twice_command == "None"
                elif handle == "run" or pointer >= len(cmd):
                    not_finished = False
                if loopTime >= 100000:
                    reporter.reporter.Error(f"Update command 'execute' error,command is too long,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
                    return "Fail"
            runCommands = cmd[pointer + 1:]
            executeParts = cmd[:pointer + 1]
            executePart = ""
            for i in executeParts:
                executePart += i + " "
            runCommand = ""
            for i in runCommands:
                runCommand += i + " "
            if runCommand != "":
                runCommand = exec_ccmd(runCommand)
            result = executePart + runCommand
            return result
                    
        except:
            reporter.reporter.Error(f"Update command 'execute' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#————————————————————————————————————————————————————————————————————————————————————————————————————
def summon(sid = None):
    if sid == None:
        return ""
    else:
        try:
            cmd = commands_in_file[sid]["cut"]
            cmd[1] = entityData.target_selector(cmd[1])
            if len(cmd) == 6:
                cmd[5] = entityData.updateEntityNBT(cmd[5])
            out = ""
            for i in cmd:
                out += i + " "
            return out
        except:
            reporter.reporter.Error(f"Update command 'summon' error,at{globalStorage.thisFile}",logp="update",path=globalStorage.thisFile)
            return "Fail"
#————————————————————————————————————————————————————————————————————————————————————————————————————
init()
if __name__ == "__main__":
    #itemData.hideFlags(255)
    #print(itemData.HideFlags)
    print(item_stack("{Unbreakable:0b}"))
    #sida = commandInit("give @s minecraft:enchanted_book{StoredEnchantments:[{lvl:3s,id:'minecraft:fortune'}]}")
    #commandInit("give @e diamond_sword{Enchantments:[{id:'minecraft:sharpness',lvl:2s},{id:'minecraft:looting',lvl:4s}],color:1A} 1")
    #commandInit("give @e diamond_sword{display:{Name:\"wps\"}}")
    #print(give(sida))

    # sid = commandInit("item modify entity @e[nbt={item:{Count:65,id:'test'}}]")
    # sid2 = commandInit("item replace from entity @e[nbt={item:{Count:65,id:'test'}}]")
    # print(item(sid))
    # print(item(sid2))
    #sid = commandInit("loot replace block ~ ~ ~ container.11 1 mine 11 45 14 diamond{Unbreakable:1b}")
    #sid = commandInit("clear @e[nbt={item:{id:'dirt',Count:1b}}] diamond{Unbreakable:1b} 1")
    #sid = commandInit("attribute @e[nbt={item:{id:'dirt',Count:1b}}] <attribute> base set 123")
    #print(common_command(sid))
    #sid = commandInit("execute if entity @s[nbt={item:{Count:15b,id:'minecraft:grass_block'}}] run give @s diamond{Unbreakable:1b} 1")
    #print(exec_ccmd("summon creeper ~ ~ ~ {item:{id:'glass',Count:114514b}}"))
    #print(exec_ccmd("execute if data entity @s Items[0].tag.Unbreakable run say 1"))