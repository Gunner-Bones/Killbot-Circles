# Killbot-Circles

A Discord bot used for integration into the [Pointercrate](https://pointercrate.com/) website, providing many features and tools used for
Discord users who use Pointercrate. This bot is used in the [Official Demons List Public Server](https://discord.gg/M7bDDQf), and if you
would like to use the official bot this code runs on, you can [invite the bot](https://discordapp.com/oauth2/authorize?client_id=501942021615779850&scope=bot).

## Getting Started

This bot runs off a [Python 3.7](https://www.python.org/downloads/) script with required libraries. 

### Prerequisites

Applications required to run and test the bot:
* A Python 3.7 IDE - [Here is one I use](https://www.jetbrains.com/pycharm/)
* [Discord](https://discordapp.com/)

### Installing

Once you have the `pcbot.py` script and the required TXT files, create another TXT file in the same directory and name it `pass.txt`. 
Directly paste your own bot's client secret into that TXT file for the bot to use 
(Visit the [Discord Developers](https://discordapp.com/developers) dashboard on making your own bot). 

The Discord Rewrite API is required to run the script. [This](https://discordpy.readthedocs.io/en/rewrite/intro.html#installing) outlines how to install the rewrite API for Python 3.

Once you have installed the rewrite, and set your Python IDE to use the version of Python 3 that contains the rewrite, run `pcbot.py` to run the bot.

If you are experiencing a `CERTIFICATE_VERIFY_FAILED` error, note that some versions of the Discord API simply do not work on OSX.

### Testing

It is recommended you create a testing Discord bot for testing new changes of code as so no errors or harmful bugs could affect your main
Discord bot. Simply create a new Discord bot in the [Developer Dashboard](https://discordapp.com/developers) and set the bot's secret
accordingly in your `pass.txt`.
