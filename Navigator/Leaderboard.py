from pymongo.mongo_client import MongoClient
import os,dns,certifi,base64
from cryptography.fernet import Fernet
import Settings as settings

# CONNECT TO LEADERBOARD CLIENT
def getLeaderboardClient():
    if settings.connectToLeaderboard:
        # START CONNECTION
        try:
            database = MongoClient((Fernet(base64.b64decode(os.getenv('DBKEY'))).decrypt(os.getenv('DBTOKEN'))).decode(), connectTimeoutMS=3000, socketTimeoutMS=3000, tlsCAFile=certifi.where())
            settings.debug("Connected to leaderboard database")
            return database
        except:
            settings.debug("Could not connect to leaderboard database. Scores will not be uploaded") # Debug
            settings.connectToLeaderboard = False
            return None
    else: return None


# GET LEADERBOARD FROM DATABASE
def getLeaders():
    if settings.connectToLeaderboard:
        try:
            database = getLeaderboardClient()
            collection = database["navigator"]["leaderboard"]
            leaders = list(collection.find().sort('longestRun', -1).limit(settings.leaderboardSize))
            settings.debug("Refreshed leaderboard") # Debug
            database.close()
            settings.debug("Disconnected from leaderboard client") # Debug
            leaderBoard = []
            for leaderIndex in range(len(leaders)):
                leader = leaders[leaderIndex]
                leaderBoard.append( {'id': leader['_id'], 'name':leader['name'], 'time':leader['longestRun'], 'score':leader['highScore']} )
            return leaderBoard
        except:
            settings.debug("Could not get leaderboard") # Debug
            settings.connectToLeaderboard = False
            return None
    else: return None


# UPLOAD RECORDS TO LEADERBOARD
def uploadRecords(records,userName):
    if settings.connectToLeaderboard and not settings.devMode:
        database = getLeaderboardClient()

        # UPLOAD RECORDS
        try:
            collection = database["navigator"]["leaderboard"]
            uploadData = {'_id':records['id'], 'name':userName, 'highScore': records['highScore'], 'longestRun':records['longestRun']} # Data for upload

            # Check if already exists in leaderboard
            settings.debug("Checking for previous records on leaderboard") # Debug
            data = collection.find_one({'_id':records['id']}) # Previous record
            repeat = collection.find_one({'name':userName}) # Repeat usernames

            repeatFound = False
            if repeat is not None:
                if (data is None) or ( (data is not None) and (repeat != data or repeat['_id'] != data['_id']) ) :
                    if records['longestRun'] < repeat['longestRun']: repeatFound = True

            if not repeatFound and data is not None:
                settings.debug("Records found") # Debug
                longestRun = data.get('longestRun')
                highScore = data.get('highScore')

                if (uploadData['highScore'] > highScore or uploadData['longestRun'] > longestRun) and (uploadData['longestRun'] > 0):
                    uploadData['highScore'] = max(highScore,uploadData['highScore'])
                    uploadData['longestRun'] = max(longestRun,uploadData['longestRun'])
                    settings.debug("Updating leaderboard records") # Debug
                    collection.update_one({'_id': records['id']}, {'$set': uploadData}, upsert=True)
                    settings.debug("Successfully updated scores in database") # Debug
                else: settings.debug("Skipped leaderboard update, scores unchanged") # Debug

            else: # Insert new data
                if repeatFound: settings.debug("Repeat username found on leaderboard")
                else:
                    settings.debug("Adding record to leaderboard") # Debug
                    collection.insert_one(uploadData)
                    settings.debug("Successfully inserted high score in database") # Debug

            database.close()
            settings.debug("Disconnected from leaderboard database") # Debug

        except:
            settings.debug("Failed to upload records to database") # Debug
            settings.connectToLeaderboard = False
            return