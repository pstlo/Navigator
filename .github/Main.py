# Run Navigator from PYD file
import os,sys,random,math,platform,json,base64,time,pypresence,asyncio
from cryptography.fernet import Fernet
from dotenv import load_dotenv
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
import pygame
sys.path.append('.')
import Navigator
if __name__ == "__main__": Navigator.gameLoop()

