summon minecraft:zombie ~ ~ ~ {ArmorItems:[{id:"minecraft:golden_boots",count:1b},{id:"minecraft:golden_leggings",count:1b},{id:"minecraft:golden_chestplate",count:1b},{id:"minecraft:knowledge_book",count:1b,components:{custom_model_data:20102}}],ArmorDropChances:[0.0f,0.0f,0.0f,0.0f],Tags:["not_spawn_in_lemon"],HandDropChances:[0.0f,0.0f],HandItems:[{count:1b,id:"minecraft:golden_sword"}],Attributes:[{Name:"generic.armor",Base:10d}]} 
data modify entity @s DeathLootTable set value "minecraft:empty" 
tp @s ~ 1024 ~ 
kill @s 
