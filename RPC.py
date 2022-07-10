# Astral - A VSRG (Vertical Scrolling Rhythm Game) developed in Python3.
# This program can be found on GitHub: https://github.com/RenderingByte/Astral
# This file serves as the host for the Discord RPC for Astral.

# Imports
import Globals
import threading
import time
from pypresence import Presence
    
# RPC Configuration
class Config():
    def __init__(self, details_text, current_details_text):
        self.details_text = details_text
        self.current_details_text = current_details_text

config = Config("Astral Is Loading", "")

def Handle(RPC):
    """
        Automatically manage and update the user's RPC.
        Based on Config class (or config object).
        
        :param RPC: The RPC Object
    """
    
    while Globals.program.isRunning:
        
        # Only update if state has changed.
        if config.current_details_text != config.details_text:
            
            RPC.update(
                large_image="icon",
                large_text="Clicking Notes To The Music",
                details=config.details_text,
                start=int(time.time())
            )
            
            config.current_details_text = config.details_text
        
        # Minimum time between updates is 15 Seconds.
        time.sleep(15)

# Only run if the user wants Discord RPC Enabled.
if Globals.options.options["enablerpc"]:

    # Attempt to establish a connection to Discord.
    try:
        
        RPC = Presence("994801218486550598")
        RPC.connect()
        print("\033[92mDiscord RPC Connected.")
        
        # RPC Thread
        threading.Thread(target=Handle, args=(RPC,)).start()
        
    except:
        
        print("\033[91mDiscord RPC Connection Failed.")