import update
while True:
    sid = update.commandInit(input(">>>"))
    commandtype = update.commands_in_file[sid]["type"]
    if commandtype == "give":
        print(update.give(sid))

# import itemData
# while True:
#     print(itemData.format_nbt(input(">>>")))