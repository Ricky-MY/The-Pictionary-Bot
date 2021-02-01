# Pictionary

## Table of Contents
* 1. [General Info](#general-info)
* 2. [Bot Explanation](#explanation)
* 3. [Installation](#installation)

### General Info
This extremely simplified repository contains all files required to maintain the Pictionary mini-game bot for discord authored using the discord.py library. This is a recreation of the worlds renowned mini-game we all love(pictionary) into discord. A game instance can be started on a server basis. Custom prefixes has also been implemented.

### Explanation 
**=** A pictionary game is started when the lobby-making command is called, every participant is required to **prove** their **activity**. This, as of the latest update, is recoginized as replying `ready`. If any of the participants **fail** to prove activity within `30` seconds, the game will consequently fail to start.

**=** After **every** participant have proven their activity, the game will begin after 5 seconds. Chat will be **disabled** until the first drawing is submitted.

**=** A member is then chosen to submit a drawing of a random theme. You can draw the theme on literally anything, you candraw it on a piece of paper, take a picture and DM the bot, you can draw the picture on MS paint and send the bot, literally anything!. If they **fail** to submit the picture within a time frame of `60 seconds`, they will recieve a deduction and the game will continue onto another person in queue. 

**=** If however the member **successfully** submitted the drawing, the other participants will have a timeframe of `70 seconds` to guess.

**=** The first person to correctly answer will recieve a few points.

**=** This process is repeated through every member and every rounds.

### How to run this project?
To run this project, install it locally by following these steps:

* 1. Install the discord.py module

You can get the library directly from PyPI:
```
python3 -m pip install -U discord.py
```
If you are using Windows, then the following should be used instead:
```
py -3 -m pip install -U discord.py
```

* 2. Install the menus extension of the discord.py module
```
py -3 -m pip install -U git+https://github.com/Rapptz/discord-ext-menus
```
If you don't have git, make sure to install it before the menus extension.

* 3. Navigate to the THIS_MY_TOKEN_HEHE.txt file

Insert the token of your bot instance into the text file.

* 4. There are no more dependencies, run the bot instance and have fun. 

