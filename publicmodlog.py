from os.path import isfile
from socket import timeout
import sqlite3 as db
from sys import exit
from time import sleep
import praw
from praw.errors import *
from requests.exceptions import HTTPError
from simpleconfigparser import simpleconfigparser


if isfile("settings.cfg"):
    config = simpleconfigparser()
    config.read("settings.cfg")
else:
    print("Couldn't find settings file. Exiting...")
    exit(1)

username = config.login.username
password = config.login.password

subreddit = config.main.subreddit
post_to = config.main.post_to
limit = int(config.main.limit)

con = db.connect('already_done.db')
cur = con.cursor()

cur.execute("CREATE TABLE IF NOT EXISTS entries(id TEXT)")

client = praw.Reddit(user_agent='public mod logger by /u/SirNeon')

while True:
    try:
        client.login(username, password, disable_warning=True)
        break
    except (InvalidUser, InvalidUserPass) as e:
        print(e)
        exit(1)
    except (HTTPError, timeout) as e:
        print(e)
        continue

while True:
    while True:
        try:
            mod_log = client.get_subreddit(subreddit).get_mod_log(limit=limit)
            break
        except (HTTPError, timeout) as e:
            print(e)
            continue

    for i, log_entry in enumerate(mod_log):
        print("Doing entry {} / {}...\r".format(i+1, limit))
        try:
            action = log_entry.action
            entry_id = log_entry.id
            details = log_entry.details
            mod = log_entry.mod
            target_author = log_entry.target_author
            target_fullname = log_entry.target_fullname
            target_permalink = log_entry.target_permalink
        except AttributeError:
            continue

        cur.execute("SELECT id FROM entries WHERE id=?", (entry_id,))

        if cur.fetchone() is None:
            cur.execute("INSERT INTO entries VALUES(?)", (entry_id,))
            con.commit()
            title = entry_id
            text = "Action: {}\n\n".format(action)
            text += "Moderator: [{0}](https://www.reddit.com/user/{0})\n\n".format(mod)
            if target_author != "":
                text += "Target User: [{0}](https://www.reddit.com/user/{0})\n\n".format(target_author)
            if target_permalink is not None:
                text += "Target Permalink: [https://www.reddit.com{0}](https://www.reddit.com{0})\n\n".format(target_permalink)

            if details != '':
                text += "Details: {}\n\n".format(details)

            if((action == 'removecomment') | (action == 'approvecomment')):
                comment = client.get_info(thing_id=target_fullname)
                text += "#Comment Body\n\n---\n\n{}".format(comment.body)

            while True:
                try:
                    mod_log_subreddit = client.get_subreddit(post_to)
                    mod_log_subreddit.submit(title=title, text=text)
                    break
                except (HTTPError, timeout) as e:
                    continue

        else:
            print("No new posts found. Sleeping for 60s...\r")
            sleep(60)
            break
