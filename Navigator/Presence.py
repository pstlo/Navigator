import os,pypresence,base64,asyncio,time
from cryptography.fernet import Fernet
import Settings as settings


# ASYNCHRONOUSLY UPDATE DISCORD PRESENCE
async def getPresence(presence):
    try:
        await asyncio.wait_for(presence.connect(),timeout = 0.5)
        await presence.update(details='Playing Navigator', state='Navigating the depths of space', large_image='background', small_image = 'icon', buttons=[{'label': 'Play Navigator', 'url': 'https://pstlo.github.io/navigator'}],start=int(time.time()))
        settings.debug("Discord presence connected") # Debug
    except: settings.debug("Discord presence timed out, likely due to multiple launches in a short duration") # Debug


def start():
    if settings.showPresence:
        try:
            presence = pypresence.AioPresence((Fernet(base64.b64decode(os.getenv('DCKEY'))).decrypt(os.getenv('DCTOKEN'))).decode())
            settings.debug("Loading Discord presence") # Debug
            asyncio.run(getPresence(presence))
            return presence
        except:
            settings.debug("Continuing without Discord presence") # Debug
            return None
            
            
            