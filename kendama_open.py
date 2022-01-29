import pandas as pd
import random

class Table:
    def create():
        df = pd.DataFrame(columns=[['name', 'surname', 'points', 'word', 'gameUID', 'winGames', 'finGames', 'end']])
        return df 
    
    def show(tableLink=0):
        if tableLink == 0:
            return Table.create()
        else:
            df = pd.read_csv(tableLink)
            return df
        
    def addPlayer(tableName, playerDataArray):
        userInput = {}
        userInput.update({'name':playerDataArray[0]})
        userInput.update({'surname':playerDataArray[1]})
        userInput.update({'points':0})
        userInput.update({'word':'KEN'})
        userInput.update({'gameUID':0})
        userInput.update({'winGames':0})
        userInput.update({'finGames':0})
        userInput.update({'end':False})
        df = pd.DataFrame(userInput, index=[0])
        return df
        
    def removePlayer(tableName, pIndex):
        tableName = tableName.drop(index=int(pIndex))
        return tableName
    
    
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
    
    def resetGame(playerDict, gameUID):
        if type(gameUID) == int: pass
        for p in playerDict:
            p.update({'points':0})
            newVal = p.get('finGames')
            newVal += 1
            p.update({'finGames':newVal})
            print(p.get('end'))
            if p.get('end') == False: 
                newVal = p.get('winGames')
                newVal += 1
                p.update({'winGames':newVal})
            else: p.update({'end':False})
        return playerDict