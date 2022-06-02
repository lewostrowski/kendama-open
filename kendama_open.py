import pandas as pd
import random
from datetime import datetime

class Table:
    def create():
        df = pd.DataFrame(columns=[['name', 'points', 'gamesWon']])
        return df

    def show(tableLink=0):
        if tableLink == 0:
            return Table.create()
        else:
            df = pd.read_csv(tableLink)
            return df

    def createGameControl(controlLink):
        defaultControl = {
            'masterUID': [0],
            'word': ['ken'],
            'turnControl': [False],
            'gameUID': [0],
            'winner':[False],
            'winnerPoints': [0],
            'timeStamp': [0]
        }
        dfControl = pd.DataFrame.from_dict(defaultControl)
        dfControl.to_csv(controlLink, index=False)
        return dfControl

    def readGameControl(controlLink):
        df = pd.read_csv(controlLink)
        return df

    def addPlayer(tableName, playerData):
        userInput = {}
        userInput.update({'name':playerData})
        userInput.update({'points':0})
        userInput.update({'gamesWon':0})
        return userInput

    def removePlayer(tableName, pIndex):
        tableName = tableName.drop(index=int(pIndex))
        return tableName

    def saveToMaster(tableName, gameControl):
        saveResults = True
        workUID = 0
        for i in gameControl['masterUID']:
            masterUID = gameControl.loc[gameControl['masterUID'] == i].values[0][0]
            workUID = masterUID
            if masterUID == 0: saveResults = False

        if saveResults == True:
            masterGame = {
                'masterUID': [],
                'timeStamp': [],
                'word': [],
                'gameUID': [],
                'name': [],
                'points': [],
                'winner': []
            }

            for gameUID in gameControl['gameUID']:
                for p in tableName['name']:
                    name = tableName.loc[tableName['name'] == p].values[0][0]
                    gameUID = gameControl.loc[gameControl['gameUID'] == gameUID].values[0][3]
                    word = gameControl.loc[gameControl['gameUID'] == gameUID].values[0][1]
                    timeStamp = gameControl.loc[gameControl['gameUID'] == gameUID].values[0][6]
                    winner = gameControl.loc[gameControl['gameUID'] == gameUID].values[0][4]
                    winnerPoints = gameControl.loc[gameControl['gameUID'] == gameUID].values[0][5]

                    masterGame['name'].append(name)
                    masterGame['gameUID'].append(gameUID)
                    masterGame['masterUID'].append(workUID)
                    masterGame['word'].append(word)
                    masterGame['timeStamp'].append(timeStamp)
                    if name == winner: 
                        masterGame['winner'].append(True)
                        masterGame['points'].append(winnerPoints)
                    else:
                        masterGame['winner'].append(False)
                        masterGame['points'].append(3)

            masterGame = pd.DataFrame(masterGame)
            masterGame.to_csv('csv/masterTable.csv', mode='a', index=False, header=False)

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

class RandomTricks:
    def readTable(tableLink):
        df = pd.read_csv(tableLink)
        return df

    def pickTrick(tableLink, level, year):
        df = RandomTricks.readTable(tableLink)
        dfR = pd.DataFrame()
        for y in year:
            dfN = df.loc[df['year'] == int(y)]
            dfR = pd.concat([dfR, dfN])
        dfRR = pd.DataFrame()
        for l in level:
            dfN = dfR.loc[df['level'] == int(l)]
            dfRR = pd.concat([dfRR, dfN])
        dfRR = dfRR.reset_index(drop=True)
        pick = random.randint(0,len(dfRR)-1)
        dfN = dfRR.loc[dfRR.index == pick]
        trickLink = dfN['name'].values
        trickName = trickLink[0]
        trickName = trickName.replace('   ', '')
        trickName = trickName.replace('  ', '')
        trickName = trickName.replace(',', '')
        trickName = trickName.replace(' ', '+')
        dfN['ytLink'] = trickName
        pickedTrick = dfN.to_dict('records')
        return pickedTrick

class Ken:
    def addPoint(tableLink, pIndex):
        df = Table.show(tableLink)
        df.loc[df.index == pIndex, 'points'] += 1
        return df

    def removePoint(tableLink, pIndex):
        df = Table.show(tableLink)
        zeroCheck = df.loc[df.index == pIndex]
        zeroCheck = zeroCheck['points'].values
        if zeroCheck > 0: df.loc[df.index == pIndex, 'points'] -= 1
        return df

    def checkForWinner(playerDict, gameControl):
        playerLeft = []
        for p in playerDict:
            if p.get('points') == len(gameControl[0].get('word')):
                playerLeft.append(playerDict.index(p))
        if len(playerLeft) < len(playerDict)-1 and len(playerDict) > 1: finish = False
        elif len(playerLeft) == len(playerDict)-1  and len(playerDict) > 1:
            finish = True
        else: finish = False
        return finish

    def resetGame(playerDict, gameControl, controlLink, nextGame=True):
        hardReset = False

        for p in playerDict:
            if (gameControl[-1].get('masterUID') == 0) and nextGame == False:
                hardReset = True

        if hardReset == False: 
            for p in playerDict:
                if p.get('points') < len(gameControl[-1].get('word')):
                   winnerName = p.get('name')
                   winnerPoints = p.get('points')
                   gamesWon = p.get('gamesWon') + 1
                   p.update({'gamesWon':gamesWon})
                   p.update({'points':0})
                else: 
                    p.update({'points':0})

            gameUID = gameControl[-1].get('gameUID') + 1
            
            timeStamp = datetime.now()
            timeStamp = timeStamp.strftime('%Y-%m-%d %H:%M')

            saveGame = {
                'masterUID':gameControl[-1].get('masterUID'),
                'word':gameControl[-1].get('word'),
                'turnControl':gameControl[-1].get('turnControl'),
                'gameUID':gameUID,
                'winner': winnerName,
                'winnerPoints': int(winnerPoints),
                'timeStamp': timeStamp
            }

            gameControl.append(saveGame)
            if gameControl[0].get('winner') == False: gameControl.pop(0)

            df = pd.DataFrame(gameControl)
            df.to_csv(controlLink, index=False)

        elif hardReset == True:
            for p in playerDict:
                p.update({'points':0})
                p.update({'masterUID':0})
                p.update({'winner':False})
        return playerDict

class Stats:
    def filterByDate(tableLink, startDate=0, startTime='00:00', endDate=0, endTime='23:59'):
        df = Table.show(tableLink)
        if startDate == 0: startDate = df['timestamp'].values[0]
        if endDate == 0: endDate = df['timestamp'].values[-1]
        df['timestamp'] = pd.to_datetime(df['timestamp'], yearfirst=True)
        df = df.loc[(df['timestamp'] >= f'{startDate} {startTime}') & (df['timestamp'] <= f'{endDate} {endTime}')]
        return df

    def overallWinner(tableLink):
        df = Table.show(tableLink)
        df = df.loc[df['winner'] == True]
        dfN = df[['name', 'winner']].groupby('name').count().sort_values('winner', ascending=False)
        dfDict = dfN.to_dict()
        return dfDict

    def timeWinner(tableLink, startDate=0, startTime='00:00', endDate=0, endTime='23:59'):
        df = Table.show(tableLink)
        dfFilter = Stats.filterByDate(df, startDate, startTime, endDate, endTime)
        dfDict = Stats.overallWinner(dfFilter)
        return dfDict

    def filterByName(df, playerName):
        dfM = df.loc[df['name'] == playerName]
        dfMap = set(dfM['masterUID'])
        df = df.loc[df['masterUID'].isin(dfMap)]
        dfDict = df.to_dict('records')
        return dfDict