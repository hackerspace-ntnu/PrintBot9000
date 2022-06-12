# PrintBot9000 - The Hackerspace Meme Printer

Currently, a simple script to print a random meme from a subreddit of choice is provided. This can be run with a crontab or something to print a meme at regular intervals. 

To set up, you need to create a Reddit application. Go to [https://www.reddit.com/prefs/apps](https://www.reddit.com/prefs/apps), and create a "script". Set redirect URL to `http://localhost:8080`. You need the client ID and the secret. Modify the config object on the top of `redditpostprinter.py` with your values. 

The connected thermal printer needs to be set as default, and needs to be set up to support CUPS. Use this guide: [Networked Thermal Printer using Raspberry Pi and CUPS](https://learn.adafruit.com/networked-thermal-printer-using-cups-and-raspberry-pi/connect-and-configure-printer)

Note that the code has not been tested, and may explode. 
