import os
import Pokemon_Image_Brightness_Finder as imageBrightness
import requests

folderPath = '/home/mark/Adams_Dev_Test/Pokemon-Terminal/pokemonterminal/Images/HQ_Images/'
# folderPath = '/home/adam/Pokemon_Images/Pokemon/assets/HQ_Images/'

list = os.listdir(folderPath)
list.sort()

open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info.txt', 'w').close()
open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log.txt', 'w').close()
# open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'w').close()
# open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log_Temp.txt', 'w').close()

# pkmnTypeVariants = open('/home/mark/Adams_Dev_Test/Pokemon_Mega_And_Regional_Type_Variations.py').read().split()
pkmnNameLog = open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log.txt').read().split()
# pkmnTypeVariants = open('/home/adam/Pokemon_Images/Adams_Tests/Pokemon_Mega_And_Regional_Type_Variations.py').read().split()
# pkmnNameLog = open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log.txt').read().split()

testCount = 0

for fileName in list:    
    pokemonDexNo = fileName[:4]
    pokemonDexNo = int(pokemonDexNo)
    pokemonDexNoFixed = ("{:04d}".format(pokemonDexNo))
    pokemonName = "Burmy-Plant"
    # pokemonName = fileName[5:-4]
    pokemonNameFixed = pokemonName.replace('_', '-').replace("'", "").replace('.', '-')

    pkmnTypeList = ''
    pkmnAbilityList = ''
    pkmnHiddenAbilityList = ''

    try:
        pkmnSearchVariable = requests.get("https://pokeapi.co/api/v2/pokemon/" + pokemonNameFixed)

        pkmnNameVariable = pkmnSearchVariable.json()['name'].title()
        pkmnTypesVariable = pkmnSearchVariable.json()['types']
        pkmnAbilitiesVariable = pkmnSearchVariable.json()['abilities']


        for item in pkmnTypesVariable:
            pkmnTypeList = pkmnTypeList + '\t' + (item['type']['name']).title()
            print(pkmnTypeList)

        
        for item in pkmnAbilitiesVariable:
            if not item['is_hidden']:
                pkmnAbilityList = pkmnAbilityList + '\t' + (item['ability']['name']).title()
                print(pkmnAbilityList)

        for item in pkmnAbilitiesVariable:
            if item['is_hidden']:
                pkmnHiddenAbilityList = (item['ability']['name']).title()
                print(pkmnHiddenAbilityList)

        

    except:
        pkmnSearchVariableBackup = requests.get("https://pokeapi.co/api/v2/pokemon-form/" + pokemonNameFixed)
        pkmnURLVariable = pkmnSearchVariableBackup.json()['pokemon']
        pkmnURL = (pkmnAbilitiesVariable['url'])

        print(pkmnURL)

        pkmnNameVariable = pkmnSearchVariable.json()['name'].title()

        pkmnAbilitiesVariable = pkmnURL(item['abilities'])

        print(pkmnAbilitiesVariable)


        for item in pkmnTypesVariable:
            pkmnTypeList = pkmnTypeList + '\t' + (item['type']['name']).title()
            print(pkmnTypeList)


        pkmnAbilitiesVariable = pkmnSearchVariable.json()['pokemon']

        pkmnAbilityList = (pkmnAbilitiesVariable['url']).title()

        print(pkmnAbilityList)

        for item in pkmnTypesVariableBackup:
            pkmnTypeList = pkmnTypeList + '\t' + (item['type']['name']).title()
            print(pkmnTypeList)

        for item in pkmnAbilitiesVariable:
            if not item['is_hidden']:
                pkmnAbilityList = pkmnAbilityList + '\t' + (item['ability']['name']).title()
                print(pkmnAbilityList)

        for item in pkmnAbilitiesVariable:
            if item['is_hidden']:
                pkmnHiddenAbilityList = (item['ability']['name']).title()
                print(pkmnHiddenAbilityList)


    with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info.txt', 'a') as compiledCsv:
    # with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Temp.txt', 'a') as compiledCsv:
        compiledCsv.write(str(pokemonDexNoFixed) + '\t' + pokemonName.title() + '\t' + str(imageBrightness.pokemonImageBrightnessFinder(folderPath, fileName)) + '\t' + pkmnTypeList + '\t' + pkmnAbilityList + '\t' + pkmnHiddenAbilityList + '\n')
    with open('/home/mark/Adams_Dev_Test/Pokemon_Compiled_Info_Log.txt', 'a') as infoLog:
    # with open('/home/adam/Pokemon_Images/Pokemon_Compiled_Info_Log_Temp.txt', 'a') as infoLog:
        infoLog.write(fileName + '\n')
    
    # except:
    #     print('test' + pokemonNameFixed)
