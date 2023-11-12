# For github action
import os,sys,random,math,platform,json,base64,time,pypresence,asyncio,dns,certifi
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
import Navigator
if __name__ == "__main__": Navigator.game.gameLoop()

