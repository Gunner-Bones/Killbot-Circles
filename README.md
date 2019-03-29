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
