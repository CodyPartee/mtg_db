################IMPORTS################
import requests
import os
import json
################IMPORTS END################

################CONSTANTS################
scryfallDataUrl = 'https://data.scryfall.io/oracle-cards/oracle-cards-20251229100302.json'
localFileName = 'card_data.json'
rarities = ['common','uncommon','rare','mythic','land']
formats = ['standard','commander','modern','all']
filePath = os.path.join('.\\', localFileName)
maxCards = 100
################CONSTANTS END################

################STATE VARIABLES################
cardSets = []
setCardCount = {}
fileCardCount = 0
jsonDump = []
dataStandard = {}
dataCommander = {}
dataModern = {}
dataAll = {}
metaData = {}
metaData['standard'] = {}
metaData['commander'] = {}
metaData['modern'] = {}
metaData['all'] = {}
################STATE VARIABLES END################

for rarity in rarities:
    dataStandard[rarity] = []
    dataCommander[rarity] = []
    dataModern[rarity] = []
    dataAll[rarity] = []
    metaData['standard'][rarity] = 0
    metaData['commander'][rarity] = 0
    metaData['modern'][rarity] = 0
    metaData['all'][rarity] = 0

if not os.path.exists(filePath):
    try:
        with requests.get(scryfallDataUrl, stream=True) as r:
            r.raise_for_status()
            with open(filePath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded '{localFileName}' to '{'.\\'}' successfully!")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

try:
    with open(filePath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        totalCardCount = len(data)
            
        for format in formats:
            if not os.path.exists(f'.\\{format}'):
                os.mkdir(f'.\\{format}')
            if os.path.exists(f'.\\{format}'):
                if not os.path.exists(f'.\\{format}\\common'):
                    os.mkdir(f'.\\{format}\\common')
                if not os.path.exists(f'.\\{format}\\uncommon'):
                    os.mkdir(f'.\\{format}\\uncommon')
                if not os.path.exists(f'.\\{format}\\rare'):
                    os.mkdir(f'.\\{format}\\rare')
                if not os.path.exists(f'.\\{format}\\mythic'):
                    os.mkdir(f'.\\{format}\\mythic')
                if not os.path.exists(f'.\\{format}\\land'):
                    os.mkdir(f'.\\{format}\\land')

        for rarity in rarities:
            fileCardCount = 0
            fileCount = 1
            for card in data:
                cardObject = {}
                if (card['rarity'] == rarity) or (rarity == 'land' and 'land' in card['type_line'].lower()):

                    cardName = card['name']
                    cardRarity = card['rarity']
                    cardSet = card['set']
                    cardStandardLegal = card['legalities']['standard'].lower()
                    cardCommanderLegal = card['legalities']['commander'].lower()
                    cardModernLegal = card['legalities']['modern'].lower()
                    cardType = card['type_line']
                    cardFront = ''
                    cardBack = ''

                    try:
                        cardImageFront = card['image_uris']['normal'].split('?')[0]
                        cardImageBack = ''
                    except:
                        cardImageFront = card['card_faces'][0]['image_uris']['normal'].split('?')[0]
                        cardImageBack = card['card_faces'][1]['image_uris']['normal'].split('?')[0]

                    if cardStandardLegal == 'legal':
                        dataStandard[rarity].append(dict(cardName = card['name'], cardSet = card['set'], cardType = card['type_line'],
                                            cardFront = cardImageFront, cardBack = cardImageBack))
                        
                    if cardCommanderLegal == 'legal':
                        dataCommander[rarity].append(dict(cardName = card['name'], cardSet = card['set'], cardType = card['type_line'],
                                            cardFront = cardImageFront, cardBack = cardImageBack))
                        
                    if cardModernLegal == 'legal':
                        dataModern[rarity].append(dict(cardName = card['name'], cardSet = card['set'], cardType = card['type_line'],
                                            cardFront = cardImageFront, cardBack = cardImageBack))
                    
                    dataAll[rarity].append(dict(cardName = card['name'], cardSet = card['set'], cardType = card['type_line'],
                                         cardFront = cardImageFront,cardBack = cardImageBack))
                    fileCardCount += 1
            
            fileCount = 1
            cardStorage = []
            for rarity in dataStandard:
                for card in dataStandard[rarity]:
                    cardStorage.append(card)
                    if len(cardStorage) == maxCards:
                        with open(f'.\\standard\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                            cardStorage = []
                        fileCount += 1
                if len(cardStorage) > 0:
                    with open(f'.\\standard\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                metaData['standard'][rarity] = fileCount
                fileCount = 1
                cardStorage = []

            for rarity in dataCommander:
                for card in dataCommander[rarity]:
                    cardStorage.append(card)
                    if len(cardStorage) == maxCards:
                        with open(f'.\\commander\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                            cardStorage = []
                        fileCount += 1
                if len(cardStorage) > 0:
                    with open(f'.\\commander\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                metaData['commander'][rarity] = fileCount
                fileCount = 1
                cardStorage = []
            
            for rarity in dataModern:
                for card in dataModern[rarity]:
                    cardStorage.append(card)
                    if len(cardStorage) == maxCards:
                        with open(f'.\\modern\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                            cardStorage = []
                        fileCount += 1
                if len(cardStorage) > 0:
                    with open(f'.\\modern\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                metaData['modern'][rarity] = fileCount
                fileCount = 1
                cardStorage = []
            
            for rarity in dataAll:
                for card in dataAll[rarity]:
                    cardStorage.append(card)
                    if len(cardStorage) == maxCards:
                        with open(f'.\\all\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                            cardStorage = []
                        fileCount += 1
                if len(cardStorage) > 0:
                    with open(f'.\\all\\{rarity}\\{fileCount}.json', 'w') as metaOutput:
                            json.dump(cardStorage, metaOutput, indent=4)
                metaData['all'][rarity] = fileCount
                fileCount = 1
                cardStorage = []

            with open(f'.\\meta_data.json', 'w') as metaOutput:
                json.dump(metaData, metaOutput, indent=4)

except Exception as e:
    pass