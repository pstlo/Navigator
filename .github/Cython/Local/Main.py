# Run Navigator from PYD file on local machine ( replace the parent directory's "main.py" file )
import os,sys,random,math,platform,json,base64,time,pypresence,asyncio,dns,certifi
from cryptography.fernet import Fernet
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
sys.path.append('.')
import Navigator
if __name__ == "__main__": Navigator.gameLoop()

