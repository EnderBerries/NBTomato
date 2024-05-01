'''
You can add your own localized translation in this file\n
The following is a detailed explanation of the parameters:\n
    <Lang>:Your language code (if multiple packages have duplicate language codes, these localized translations may overlap with each other)\n
    <pack>:Your language name
    <translation>:Content to be translated

Here is English Comparison Table:

    Lang="en_us"
    translation={
        "en_us":{
            "trans.pack.name":"English(US)",
            "trans.finished_change_language":"Successfully set the language",
            "trans.main.get_mcmeta_path":"Please enter the \"pack.mcmeta\" file path:",
        }
    }

After you complete the translation,You should use "python -m" to compile your program into ".pyc" file\n
Then, place your ".pyc" file in the folder "Languages" and remove the key "Languages" from "settings.json"\n
Finally,run "NBTomato.py",then you should see your language in the menu
'''


#Fill the things below
Lang="<Lang>"
translation={
    "en_us":{
        "trans.pack.name":"<pack>",
        "trans.finished_change_language":"<translation>",
        "trans.main.get_mcmeta_path":"<translation>",
    }
}