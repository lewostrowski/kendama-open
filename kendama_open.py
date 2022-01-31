import pandas as pd
import random
from datetime import datetime

class Table:
    def create():
        df = pd.DataFrame(columns=[['name', 'points', 'word', 'gameUID', 'winGames', 'finGames', 'end', 'masterUID']])
        return df 
    
    def show(tableLink=0):
        if tableLink == 0:
            return Table.create()
        else:
            df = pd.read_csv(tableLink)
            return df
        
    def addPlayer(tableName, playerData):
        userInput = {}
        userInput.update({'name':playerData})
        userInput.update({'points':0})
        userInput.update({'word':'KEN'})
        userInput.update({'gameUID':0})
        userInput.update({'winGames':0})
        userInput.update({'finGames':0})
        userInput.update({'end':False})
        userInput.update({'masterUID':0})
        return userInput
        
    def removePlayer(tableName, pIndex):
        tableName = tableName.drop(index=int(pIndex))
        return tableName
    
    def saveToMaster(playerDict):
        saveResults = True
        for p in playerDict:
            if p.get('masterUID') == 0: saveResults = False
    
        if saveResults == True: 
            timeStamp = datetime.now()
            for p in playerDict: p.update({'timeStamp':timeStamp})
            dfN = pd.DataFrame(playerDict)
        else: dfN = False
        return dfN
    
    
class Group:
    def geoProg(tableName):
        geometricalProgression = []
        start = 2
        ratio = 2
        while start <= len(tableName):
            geometricalProgression.append(start)
            start = start * ratio
        return geometricalProgression
    
    def playerArray(tableName, shuffle=True):
        tempArray = []
        for p in tableName.index:
            tempArray.append(tableName.iloc[p].to_numpy())

        playerArray = []
        for container in tempArray:
            player = []
            for x in container:
                player.append(x)
            playerArray.append(player)
        if shuffle == True: playerArray = random.sample(playerArray, k=len(playerArray))
        return playerArray
    
    
class Game:
    def addPoint(tableLink, pIndex):
        df = Table.show(tableLink)
        df.loc[df.index == pIndex, 'points'] += 1
        return df
    
    def removePoint(tableLink, pIndex):
        df = Table.show(tableLink)
        df.loc[df.index == pIndex, 'points'] -= 1
        return df
    
    def checkForWinner(playerDict):
        playerLeft = []
        for p in playerDict:
            if p.get('points') == len(p.get('word')):
                playerLeft.append(playerDict.index(p))
        if len(playerLeft) < len(playerDict)-1 and len(playerDict) > 1: finish = False
        elif len(playerLeft) == len(playerDict)-1  and len(playerDict) > 1: 
            finish = True
        else: finish = False
        return finish
    
    def resetGame(playerDict, masterUID=0, exclude=0):
        hardReset = False  
        
        for p in playerDict:
            if p.get('masterUID') == '0' or masterUID == 0: 
                hardReset = True
            
        if hardReset == False:
            for p in playerDict:
                p.update({'points':0})

                newVal = p.get('finGames')
                newVal += 1
                p.update({'finGames':newVal})

                newVal = p.get('gameUID')
                newVal += 1
                p.update({'gameUID':newVal})

                if p.get('end') == False: 
                    newVal = p.get('winGames')
                    newVal += 1
                    p.update({'winGames':newVal})
                else: p.update({'end':False})
                
        elif hardReset == True:
            for p in playerDict:
                p.update({'points':0})
                p.update({'gameUID':0})
                p.update({'winGames':0})
                p.update({'finGames':0})
                p.update({'end':False})
                p.update({'masterUID':0})
        print(playerDict)
        return playerDict