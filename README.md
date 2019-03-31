# Killbot-Circles

A Discord bot used for integration into the [Pointercrate](https://pointercrate.com/) website, providing many features and tools used for
[Discord](https://discordapp.com/) users who use Pointercrate. This bot is used in the [Official Demons List Public Server](https://discord.gg/M7bDDQf), and if you
would like to use the official bot this code runs on, you can [invite the bot](https://discordapp.com/oauth2/authorize?client_id=501942021615779850&scope=bot).

## Getting Started

This bot runs off a [Python 3.7](https://www.python.org/downloads/) script with required libraries. The Discord rewrite API requires
at least Python 3.6, and it's always best to use the latest version of Python.

### Prerequisites

Applications required to run and test the bot:
* A Python 3.7 IDE - [Here is one I use](https://www.jetbrains.com/pycharm/). An IDE is not required, but it will immensely help the coding process.
* [Discord](https://discordapp.com/)

### Discord Bot Setup

You'll need to create your own Discord Bot for testing, so you can control where this bot can activate and who can use the bot on Discord. This can all be done on [Discord](https://discordapp.com/) and the [Discord Developers](https://discordapp.com/developers) dashboard. 

If you have not done so already, create a [Discord](https://discordapp.com/) account, and then on Discord click Add a Server. Choose Create, name your server and then create. If you already have a server you want to use, you don't have to create a new one, as long as you are either the owner or have administrative privelages of that server.

To create a Discord Bot, go on the [Discord Developers](https://discordapp.com/developers) dasboard and login with your Discord account. On the Applications tab, click New Application and name your bot. To turn your application to a bot user, go to the application's Bot tab, and click Add Bot. With your newly created bot, underneath the name it'll give you the bot's Client Token. This will be used for the code to run the discord bot. To add your discord bot to your server, go to the bot's OAuth2 tab. For basic permissions, click the 'bot' checkbox, which will generate a link below. In that link's page, choose the server you want to add the bot to, and click Add. If you go back to your Discord server, you should see your bot has joined it.

### Installing

To get a copy of the Killbot Circles code, clone the repository. Download the ZIP of the repository by finding the *Clone or Download* button on the [repository page](https://github.com/Gunner-Bones/Killbot-Circles), and extract the ZIP file. This will include `pcbot.py`, which is the main bot script, and a lot of TXT files that contain data for the bot to use.

To be able to use this code with your Discord bot, create a TXT file in the same directory as `pcbot.py` and name it `pass.txt`. In that TXT file, directly paste your Discord bot's Client Token (where to find that is explained in the **Discord Bot Setup** section).

The Discord Rewrite API is required to run the script. [This](https://discordpy.readthedocs.io/en/rewrite/intro.html#installing) outlines how to install the rewrite API for Python 3.

Once you have installed the rewrite, and set your Python IDE to use the version of Python 3 that contains the rewrite, run `pcbot.py` to run the bot.

### Testing

Once you have the Discord bot set up correctly in Discord and with your files, run `pcbot.py` to run the bot. If the script does not error, and the bot user in your Discord goes online, then the script is running properly.

## Deployment

To keep the bot running 24/7, you'll need to host it on a server. A cheap method I use for keeping the bot online is running an [Amazon EC2](https://aws.amazon.com/ec2/) server. They offer a free 1-year tier for a basic server, which should be more than enough to run a couple of Discord bots.
You'll need to SSH into your server to transfer files. [Cyberduck](https://cyberduck.io/) is a great SSH application.
You'll also need to see a command-line terminal so you can execute commands in your server and turn on the bot. [Putty](https://www.putty.org/) is a good tool for this (Putty is also built in to Cyberduck).

Once you have transfered all the appropriate files, open Putty so you can install Python 3 and dependency libraries. You can install Python and the libraries using the `pip install` command.

### Linux Usage

Assuming Python 3 has been installed, this repository already comes with two Linux executables you can use to run the bot. `run.sh` runs the bot normally, displaying the Python console in your terminal. This is used for testing purposes to make sure the bot runs fine in the server. `nrun.sh` runs the bot in Nohup, which allows it to run continuously, even when you disconnect from the server. The Python console does not display in this mode.

To run one of these scripts, type
```
./run.sh
```
```
./nrun.sh
```

Here are some other basic Linux commands if you're unfamiliar with the terminal:
```
cd directory
```
* Change your current directory to a different location. This matters for running files as you should be in the same directory as the executable when you run it. If you are already in a directory with a folder, you don't have to type out the folder's full address, but you can type `cd folder`. If you want to go up a directory, type `cd ..`
```
ls
```
* Lists all files and folders in your current directory
```
ps aux | grep python
```
* Shows all running Python processes. This is used to show all bots running and can be used if you want to terminate a bot. To terminate a bot, after running this command find the Process ID of the bot, and type `kill process_id`.
```
nano file.extension
```
* Opens up a simple text editor for editing files. This editor isn't as clean to use than a normal text editor, so it's not recommended using unless you really need to quickly edit something in the server without having to retransfer files. Note that if you use `nano` and specify a file that doesn't exist, it will create a file instead. For example, you could type `nano pass.txt` if you forgot to put that in and it will create the file and open the new text file in the editor.

## Built with

* [Python 3.7](https://www.python.org/downloads/)
* [Discord.py Rewrite](https://discordpy.readthedocs.io/en/rewrite/intro.html#installing) - Discord's Python API
* AWS Linux

## Authors
* **GunnerBones**
* **yevnyra**
* **PoisoN**
