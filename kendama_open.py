import pandas as pd
import random

class Table:
    def create():
        df = pd.DataFrame(columns=[['name', 'surname', 'points', 'maxPoints']])
        return df 
    
    def show(tableLink=0):
        if tableLink == 0:
            return Table.create()
        else:
            df = pd.read_csv(tableLink)
            return df
        
    def addPlayer(tableName, playerDataArray):
        userInput = {}
        for c in tableName.columns:
            if tableName.columns.get_loc(c) < 2:
                userInput.update({c:playerDataArray[tableName.columns.get_loc(c)]})
            elif tableName.columns.get_loc(c) == 2: userInput.update({c:0})
            elif tableName.columns.get_loc(c) == 3: userInput.update({c:3})
                
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