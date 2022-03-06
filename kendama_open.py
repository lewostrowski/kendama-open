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
        dfN = df.loc[df['Level'] == level]
        if type(year) == int: 
            yearInput = f'year{year}'
            dfN = dfN[['Level', 'Number', yearInput]]

        if len(dfN.columns) == 3:
            pick = random.randint(0,len(dfN))
            dfN = dfN.loc[dfN.index == pick]
            pickedTrick = dfN.to_dict('records')
            return pickedTrick

class Ken:
    def addPoint(tableLink, pIndex):
        df = Table.show(tableLink)
        df.loc[df.index == pIndex, 'points'] += 1
        return df

    def removePoint(tableLink, pIndex):
        df = Table.show(tableLink)
        df.loc[df.index == pIndex, 'points'] -= 1
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


class Dev:
    def returnPlayerDict():
        playersDict = {
        'Jack': {
            'skills': 3,
            'freq': 9
        },
        'Mike': {
            'skills': 5,
            'freq': 8
        },
        'Anna': {
            'skills': 3,
            'freq': 5
        },
        'Braian': {
            'skills': 5,
            'freq': 5
        },
        'Jessica': {
            'skills': 4,
            'freq': 7
        },
        'Sonia': {
            'skills': 6,
            'freq': 3
        }
        }
        return playersDict

    def devFreq(playersDict):
        for p in playersDict:
            playerFreq = playersDict[p].get('freq')
            playerFreq = playerFreq * random.randint(1,6)
            playersDict[p].update({'gameFreq': playerFreq})
        return playersDict

    def devSkill(playersDict, randomFacto=True):
        for p in playersDict:
            playerSkill = playersDict[p].get('skills')
            playerSkill = playerSkill * random.randint(1,5)
            if randomFacto == True: playerSkill += random.randint(-5,5)
            playersDict[p].update({'gameSkills': playerSkill})
        return playersDict

    def devGame(playersDict, pArray=[]):
        if len(pArray) == 0:
            pDict = Dev.devFreq(playersDict)
            pDict = Dev.devSkill(playersDict)
            gamePopulation = random.randint(2,len(pDict)) 

            pFreq = []
            for p in pDict: pFreq.append(pDict[p].get('gameFreq'))
            while len(pFreq) > gamePopulation: pFreq.pop(pFreq.index(min(pFreq)))

            game = {
                'name': [],
                'winner': [],
                'points': []
            } 

            for p in pDict: 
                if pDict[p].get('gameFreq') in pFreq: game['name'].append(p)

        elif len(pArray) > 1:
            pDict = Dev.devSkill(playersDict)

            game = {
                'name': pArray,
                'winner': [],
                'points': []
            } 

        pSkill = []
        for p in game['name']: pSkill.append(pDict[p].get('gameSkills'))
        for p in game['name']: 
            if pDict[p].get('gameSkills') == max(pSkill) and game['winner'].count(True) == 0: game['winner'].append(True)
            else: game['winner'].append(False)

        for p in game['name']:
            pIndex = game['name'].index(p)
            if game['winner'][pIndex] == True: game['points'].append(random.randint(0,2))
            else: game['points'].append(3)

        return game

    def devSession(maxRounds=6):
        gameRounds = random.randint(1,maxRounds)
        game = Dev.devGame(playersDict)

        game.update({'gameUID': 0})
        dfN = pd.DataFrame.from_dict(game)

        roundsLeft = gameRounds-1
        if gameRounds > 1:
            while roundsLeft != 0:
                nextGame = Dev.devGame(playersDict, pArray=game['name'])
                nextGame.update({'gameUID': roundsLeft})
                dfNext = pd.DataFrame.from_dict(nextGame)
                dfN = pd.concat([dfN, dfNext])
                roundsLeft -= 1

        masterUID = uuid.uuid4().time
        dfN['masterUID'] = masterUID
        return dfN

    def devGenerateTable(sessionNumber=20):
        n = 1
        df = Dev.devSession()
        while n < sessionNumber:
            dfT = Dev.devSession()
            df = pd.concat([df, dfT])
            n += 1
        for n in df['masterUID']:
            dfN = df.loc[df['masterUID'] == n]
            dfCount = dfN['gameUID'].nunique()
            df.loc[df['masterUID'] == n, 'finGames'] = dfCount
        df['finGames'] = df['finGames'].astype(int)
        df.to_csv('csv/playerModel.csv', index=False)