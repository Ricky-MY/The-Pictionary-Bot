# Pictionary

[![HitCount](http://hits.dwyl.com/Ricky-MY/The-Pictionary-Bot.svg)](http://hits.dwyl.com/Ricky-MY/The-Pictionary-Bot)

## Table of Contents
* 1. [General Info](#general-info)
* 2. [Trace Tables](#trace-tables)
* 3. [Bot Explanation](#wordy-explanation)
* 4. [Installation](#how-can-i-run-this-project)

### General Info
This GitHub repository contains all files required to maintain the Pictionary mini-game bot for discord authored using the discord.py library. This is a recreation of the worlds renowned mini-game we all love, that is pictionary, into discord. A game instance can be started on a channel basis. Custom prefixes has also been implemented.

Started: 1/10/2020

### Trace Tables
~~~
          +--------------+           +-------------+           +-----------------+    +-------------------------------+
 start -> |              |---------->|    Create   |---------->|  Update         | <--| - on_raw_reaction + a checker |
          |   Lobbying   |           |  Attendance |           |  attendance list|    +-------------------------------+
  end  <- |              |<----------|   List      |<----------|  on user input  |                                  
          +--------------+           +-------------+  takedown +-----------------+                                  
                                                                        |
                                                                        | - all users responded
                                                                        V
                                                               +--------------+
                                                       +------>|    Get       | 
                                                       |       |  Drawing     |
                                                       |       +--------------+
                        +--------------+               |              |
              end  <----|  build and   |<--------------+              |
                        |output scores |      ^        |              V
                        +--------------+      |        |        +-------------+    +------------------+
                                              |        |        |  Create or  |--->|  on_message to   |     
                            after all members |        +--------|  update     |<---| recieve answers  |
                       .----------------------+                 | check list  |    +------------------+  
                                                                +-------------+ 
~~~
### Wordy Explanation 
**1.** When a lobby is initiated**(start_game command used)**, every participant is required to **prove** their **activity**. This, as of the latest update, is recoginized as reacting to the lobby message with 🖌️. If any of the participants **fail** to prove activity within `30` seconds, the game will consequently fail to start. Players can also vote for take-down using the emoji TAKEDOWN.

**2.** After **every** participant have proven their activity, the game will begin after 5 seconds. Chat will be **disabled** until the first drawing is submitted.

**3.** A member is then chosen to submit a drawing of a random theme. You can draw the theme on literally anything, you candraw it on a piece of paper, take a picture and DM the bot, you can draw the picture on MS paint and send the bot, literally anything!. If they **fail** to submit the picture within a time frame of `60 seconds`, they will recieve a deduction and the game will continue onto another person in queue.

**4.** If however the member **successfully** submitted the drawing, the other participants will have a timeframe of `70 seconds` to guess.

**5.** All players who are able to answer correctly gets the points, the faster the more points.

**6.** This process is repeated through every member and every rounds.

### How can I run this project?
To run this project, install it locally by following these steps:

* 1. Install the discord.py module (USE PYTHON 3.8 OR ABOVE)

You can get the library directly from PyPI:
On macOS:
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

* 3. Setup dotenv for token feeding

a. Install python-dotenv
macOS:
```
python3 -m pip install python-dotenv
```
Windows:
```
py -3 -m pip install python-dotenv
```
b. Create a `.env` file in the root directory
This must be in the same directory as `__main__.py`

d. Insert in your token
~~~
TOKEN="YOUR_TOKEN"
~~~

**That is all you need to run this project. If you want to try out a pre-hosted bot, please navigate to this website https://top.gg/bot/768442873561481216** 

