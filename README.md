# ModLogBot
A bot for posting mod logs into a subreddit.

# Requirements
* Python 3.4
* PRAW
* simpleconfigparser

# Installation
Run the command:

    pip install -r requirements.txt

Linux users may need to use sudo. The program may also be "pip3" instead of "pip" depending on your distribution.

# Edit The Settings File Before Running The Bot
Set the limit to how many entries you want detected. Set the subreddit where you want the logs posted. Set the subreddit you want to get the logs from. Finally, set the username and password for the reddit account you want to use to do this.

# Run The Bot
Navigate to the installation directory and run the command:

    python publicmodlog.py

The command might need "python3" instead of "python" depending on your Linux distribution.
