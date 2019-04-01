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

To keep the bot running 24/7, you'll need to host it on a server. A cheap method I use for keeping the bot online is running an [Amazon EC2](https://aws.amazon.com/ec2/) server. They offer a free 1-year tier for a basic server, which should be more than enough to run a couple of Discord bots. If you use the Amazon EC2, make sure to use the AWS Linux.
You'll need to SSH into your server to transfer files. [Cyberduck](https://cyberduck.io/) is a great SSH application.
You'll also need to see a command-line terminal so you can execute commands in your server and turn on the bot. [Putty](https://www.putty.org/) is a good tool for this (Putty is also built in to Cyberduck).

Once you have your server set up and you're SSH'd into it, first you'll need to transfer all the files for Killbot Circles: `pcbot.py`, all the TXT and SH files included in your clone of the repo, and `pass.txt`.

Within the Linux terminal, you'll need to install Python 3.7, as well as the discord rewrite API.
To install Python:
```
sudo yum install python3
```
Once Python is installed, use this command to install the Discord rewrite.
```
sudo pip3.7 install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice]
```

Now that everything is installed correctly, you can now run the bot. Running the bot in Nohup allows it to stay online 24/7, but you won't be able to see the Python logs (they output to a file called `nohup.out`, but it's hard to read). If you don't run it in Nohup, you'll be able to see the Python logs in case the bot errors, but it won't stay online 24/7.
Run the normal script just for testing and seeing logs:
```
./run.sh
```
Run the Nohup script to keep the bot online 24/7:
```
./nrun.sh
```

To stop the bot, find its process ID and terminate it.
Type this to find all running python processes:
```
ps aux | grep python
```
This will show a list of processes. Find the bot's process by checking the last variable in each process, which is the file name. The file name should match `python3.7 pcbot.py`. In that process, remember its process ID: It's the 4-5 digit number second from left. Then type:
```
kill <process ID>
```


To verify if your bot is working correctly, in Discord try typing these commands:
* ??kchelp - If this works, you should get private messages from the bot of a list of commands.
* ??refresh - If this works, the bot will initially say "Manual Refresh Started". After a couple minutes, if it works, it will give results of the refresh.

## Built with

* [Python 3.7](https://www.python.org/downloads/)
* [Discord.py Rewrite](https://discordpy.readthedocs.io/en/rewrite/intro.html#installing) - Discord's Python API
* AWS Linux

## Authors
* **GunnerBones**
* **yevnyra**
* **PoisoN**
