'''
You can add your own localized translation in this file\n
The following is a detailed explanation of the parameters:\n
    <Lang>:Your language code (if multiple packages have duplicate language codes, these localized translations may overlap with each other)\n
    <pack>:Your language name
    <translation>:Content to be translated

Here is English Comparison Table:

    Lang="en_us"
    translation = {  
        "en_us": {  
            "trans.pack.name": "English (US)",  
            "trans.exit": "Exited",  
            "trans.finished_change_language": "Language successfully set",  
            "trans.main.get_mcmeta_path": "Please enter the path to the pack.mcmeta file:",  
            "trans.ui.input": ">>>",  
            "trans.ui.on": "On: 1",  
            "trans.ui.off": "Off: 2",  
            "trans.ui.menu": "Enter the corresponding code to perform the desired operation",  
            "trans.ui.not_allow": "Please enter an allowed value",  
            "trans.ui.menu.settings": "Settings: 1",  
            "trans.ui.menu.update": "Update data pack: 2",  
            "trans.ui.menu.exit": "Exit: 3",  
            "trans.ui.menu.settings.languages": "Language: 1",  
            "trans.ui.menu.settings.show_detailed_info": "Show detailed information: 2",  
            "trans.ui.menu.settings.back": "Back: 3",  
            "trans.ui.saved": "Saved!",  
            "trans.ui.not_saved": "No changes made!",  
        }  
    }

After you complete the translation,You should use "python -m" to compile your program into ".pyc" file\n
Then, place your ".pyc" file in the folder "Languages" and remove the key "Languages" from "settings.json"\n
Finally,run "NBTomato.py",then you should see your language in the menu
'''


#Fill the things below
Lang="<Lang>"
translation={
    "<Lang>":{
        "trans.pack.name":"<pack>",
        "trans.exit": "<translation>",  
        "trans.finished_change_language": "<translation>",  
        "trans.main.get_mcmeta_path": "<translation>",  
        "trans.ui.input": ">>>",  
        "trans.ui.on": "<translation>",  
        "trans.ui.off": "<translation>",  
        "trans.ui.menu": "<translation>",  
        "trans.ui.not_allow": "<translation>",  
        "trans.ui.menu.settings": "<translation>",  
        "trans.ui.menu.update": "<translation>",  
        "trans.ui.menu.exit": "<translation>",  
        "trans.ui.menu.settings.languages": "<translation>",  
        "trans.ui.menu.settings.show_detailed_info": "<translation>",  
        "trans.ui.menu.settings.back": "<translation>",  
        "trans.ui.saved": "<translation>!",  
        "trans.ui.not_saved": "<translation>", 
    }
}