import nbtlib
import itemData
import update
import globalStorage
import reporter
class UpdateError(Exception):
    def __init__(self,ecode,message) -> None:
        self.ecode = ecode
        self.message = message
        self.codemap = {
            "01":"Too long nbt path",
            "02":"Not supported nbt",
            "03":"Not supported in latest Minecraft version",
            "04":"Not supported type",
            "05":"Not supported type in latest Minecraft version",
        }
    def __str__(self) -> str:
        if self.ecode in self.codemap:
            errmsg = self.codemap[self.ecode]
            return f"{errmsg}:{self.message}"
        else:
            raise ValueError("Not a usable error-code")
itemTags = [    #标记游戏中带有的NBT标签，此标签外的NBT标签会被认定为custom_data
        "Enchantments",
        "display",
        "AttributeModifiers",
        #"CanPlaceOn",
        #"CanDestroy",
        "BlockEntityTag",
        #"BlockStateTag",
        #"Unbreakable",
        #"SkullOwner",
        #"HideFlags",
        #"generation",
        #"Damage",
        #"CustomModelData",
        "StoredEnchantments",
        #"Glowing",
        #"Health",
        #"Invulnerable",
        #"NoAI",
        #"NoGravity",
        #"Silent",
        #"BucketVariantTag",
        #"Age",
        #"HuntingCooldown",
        #"Variant",
        "Decorations",
        "Trim",
        #"instrument",
        #"Potion",
        #"CustomPotionColor",
        "custom_potion_effects",
        "effects",
        "pages",
        "filtered_pages",
        #"author",
        #"filtered_title",
        #"resolved",
        #"title",
        "DebugProperty",
        "Explosion",
        "Fireworks",
        #"LodestoneDimension",
        "LodestonePos",
        #"LodestoneTracked",
        #"RepairCost",
        "EntityTag",
        "Items",
        #"Charged",
        "ChargedProjectiles",
        #"map"
    ]

global Tags
Tags = {
    "item":{
        "CanPlaceOn":"\"$FLAG$\"",
        "CanDestroy":"\"$FLAG$\"",
        "Enchantments":[
            {
                "id":"$FLAG$",
                "lvl":1
            }
        ],
        "StoredEnchantments":[{
            "id":"$FLAG$",
            "lvl":1
        }],
        "display":{
            "Name":"$FLAG$"
        },
        "AttributeModifiers":[
            {
                "Name":"$FLAG$"
            }   
        ],
        "BlockEntityTag":{
            "note_block_sound":"$FLAG$"
        },
        "Decorations":[
            {"id":'$FLAG$',
             "type":26,
             "x":114.0,
             "z":514.0,
             "rot":0.0
            }
            ],
        "Trim":{
            "material":"$FLAG$",
            "pattern":"bitch"
        },
        "custom_potion_effects":[
            {
                'id':"$FLAG$"
            }
        ],
        "effects":[
            {
                "id":"$FLAG$"
            }
        ],
        "pages":[
            "$FLAG$"
        ],
        "filtered_pages":{
            "0":"$FLAG$"
        },
        "DebugProperty":{
            "\"minecraft:dirt\"":"$FLAG$"
        },
        "Explosion":{
            "Colors":"$FLAG$"
        },
        "Fireworks":{
            "Flight":"$FLAG$"
        },
        "LodestonePos":{
            "X":"$FLAG$",
            "Y":0,
            "Z":0
        },
        "EntityTag":{
            "id":"$FLAG$"
        },
        "Items":[
            {
                "Slot":0,
                "id":"$FLAG$"
            }
        ],
        "ChargedProjectiles":[
            {
                "Slot":0,
                "id":"$FLAG$"  
            }
        ],
        "$NOTINOBJ$":"$FLAG$",
        "ItemTagProcess":{
            "-1":[
                "BlockEntityData",
                "Trim",
                "DebugProperty",
                "Explosion",
                "Fireworks",
                "LodestonePos",
                "EntityTag",
                "BlockEntityTag"
            ],
            "-1+off":[
                "AttributeModifiers",
                "custom_potion_effects",
                "effects",
                "pages"
            ],
            "-1+replace":[
                "Items",
                "ChargedProjectiles"
            ]
        },
        "NOT_SUPPORTED":{
            "display":{
                "Name":"$FLAG$"
            }, 
            "filtered_pages":{
                "0":"$FLAG$"
            },  
            "author":"$FLAG$",
            "filtered_title":"$FLAG$",
            "resolved":"$FLAG$",
            "title":"$FLAG$",
        }
    },
    "entity":{

    }
}

def find_flag_path(data, path='',match='$FLAG$'):

    # 如果当前键名等于match，返回当前路径
    if isinstance(data, dict) and match in data:
        return path
    
    # 如果当前值是match，返回当前路径
    if data == match:
        return path
    

    # 如果当前值是字典，递归遍历其键值对
    if isinstance(data, dict):
        for key, value in data.items():
            new_path = find_flag_path(value, path + '.' + str(key) if path else str(key))
            if new_path:
                return new_path
    
    # 如果当前值是列表，递归遍历其元素
    elif isinstance(data, list):
        for index, item in enumerate(data):
            new_path = find_flag_path(item, path + '[' + str(index) + ']' if path else '[' + str(index) + ']')
            if new_path:
                return new_path
    
    # 如果没有找到"FLAG"，返回None
    return None


def tag_to_dict(tag):
    if isinstance(tag, nbtlib.tag.Compound):
        # 如果标签是化合物类型，则递归转换每个子标签
        return {key: tag_to_dict(value) for key, value in tag.items()}
    elif isinstance(tag, nbtlib.tag.List):
        # 如果标签是列表类型，则递归转换列表中的每个元素
        return [tag_to_dict(item) for item in tag]
    elif isinstance(tag, nbtlib.tag.ByteArray):
        # 字节数组可能需要特殊处理，这里直接返回其值
        return tag.unpack()
    elif isinstance(tag, nbtlib.tag.IntArray):
        # 整型数组同样返回其值
        return list(tag)
    elif isinstance(tag, nbtlib.tag.String):
        # 字符串类型直接返回其值
        return tag.unpack()
    # 对于其他类型，直接返回其值
    return tag


def DictToNBTString(data):  
    if isinstance(data, dict):   
        pairs = ["{}:{}".format(key, DictToNBTString(value)) for key, value in data.items()]  
        return "{{{}}}".format(", ".join(pairs))  
    elif isinstance(data, list):    
        items = [DictToNBTString(item) for item in data]  
        return "[{}]".format(", ".join(items))  
    elif isinstance(data, (str, int, float, bool)):  
        # 基本类型转换为字符串  
        if isinstance(data, str):  
            # 为了简化，这里只使用引号  
            return '"{}"'.format(data)  
        else:  
            return str(data)  
    else:  
        raise ValueError("Unsupported type for conversion to NBT-like string: {}".format(type(data)))  

def ItemNBTPath(raw=None,type="none"):
    if raw == None:
        return ""
    else:
        catch = False
        nodes = itemData.getNBTList(raw,".")
        pointer = 0
        belist = nodes.copy()
        for i in nodes:
            if catch == True:   #放在检查是否进入nbt标签前
                if "[" in i:
                    indexi = "[" + i.split("[",1)[1]
                    i = i.split("[",1)[0]
                else:
                    indexi = ""
                thisTag = i
                if thisTag in Tags["item"]["NOT_SUPPORTED"]:
                    raise UpdateError("02","At '" + raw +"' ")
                if itemData.itemTags.count(i) >= 1 and pointer + 1 == lenNodes:
                    if i == "Enchantments" or i == "StoredEnchantments" or i == "Charged":
                        raise UpdateError("03","At '" + raw +"' ")
                    if i in Tags["item"]:
                        getNBT = "{" + i + ":" + DictToNBTString(Tags["item"][i]) + "}"
                    else:
                        getNBT = "{" + i + ":" + DictToNBTString(Tags["item"]["$NOTINOBJ$"]) + "}"
                    if i == "ChargedProjectiles":
                        itemData.charged["Charged"] = True
                    getNBT = update.item_stack(getNBT,":","{}")     #更新版本
                    temp = nbtlib.parse_nbt(getNBT)     #解析新版本数据
                    temp = tag_to_dict(temp)        #将解析后的数据转化为字典
                    path = find_flag_path(temp,match="$FLAG$")      #寻址
                    path = itemData.getNBTList(path,".")        #格式化地址
                    nodes.extend(path)
                    break
                elif itemData.itemTags.count(i) == 0:
                    nodes.insert(pointer,"custom_data")
                    nodes.extend(msc_nodes)
                    break
                elif pointer == lenNodes:
                    reporter.reporter.Error(f"Update nbt path error:Path is too long,at'{raw}',at{globalStorage.thisFile}",logp="NBTPath",path=globalStorage.thisFile)
                    raise UpdateError("01","At '" + raw +"' ")
                    #print("[Error]at '" + raw +"' :Path Is Too Long(ERR1)")
                    #return "Fail"
                 
            if i == "tag":
                catch = True
                nodes[pointer] = "components"
                lenNodes = len(nodes)
                belist = nodes[:pointer]
                msc_nodes = nodes[pointer+1:]
                nodes = nodes[:pointer+1]
            pointer += 1
        if type == "entity" or type == "block":
            print("Not fully processed, at: " + raw)
        if i in Tags["item"]["ItemTagProcess"]["-1"]:
            nodes = nodes[:-1]
        if i in Tags["item"]["ItemTagProcess"]["-1+off"]:
            nodes = nodes[:-1]
            nodes[-1] = nodes[-1].split("[",1)[0]
        if i in Tags["item"]["ItemTagProcess"]["-1+replace"]:
            nodes = nodes[:-1]
            nodes[-1] = nodes[-1].split("[",1)[0]
            nodes[-1] += indexi
        result = ""
        for i in nodes:
            result += i + "."
        result = result[:-1]
        return result
    
if __name__ == "__main__":
    print(ItemNBTPath("Items[0].tag.CanDestroy","entity"))
# em = {}
# for i,s in a,a.items():
#     em[i] = s
# print(em)