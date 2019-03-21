# -*- coding: utf-8 -*-
import praw
import config
import time
import psycopg2
import re
from random import randint
from linereader import copen

def bot_login():
    print("Logging in...")
    r =    praw.Reddit(username = config.reddit_username,
        password = config.reddit_password,
        client_id = config.client_id,
        client_secret = config.client_secret,
        user_agent = "WannabeQuadrilingual's Brozzer Bilal Bot v0.1")
    print("Logged in")
    return r


def run_bot(r,comments_already_replied):
    takbirList = ['takbir','takbeer','tekbir','تكبير']
    taqiyaList = ['taqiyya','taqqiyya','taqiya','taqqiya']
    jazakallahList = ['jazakallah','jazakillah','jazakumullah']
        
    footer = "\n^Subscribe ^: ^[r/MuslimLounge](https://www.reddit.com/r/MuslimLounge/) ^|| ^[SourceCode](https://github.com/WannabeQuadrilingual/BrozzerAbdullahBot) ^|| ^Contact ^[u/WannabeQuadrilingual](https://www.reddit.com/user/WannabeQuadrilingual/) ^to ^report ^issues"

#    footer = "\nAdvertisement - r/MuslimLounge a sub for casual conversations\n\n^[AboutMe](https://www.reddit.com/user/BrozzerBilalBot/comments/96zex2/about_me/) ^|| ^[SourceCode](https://github.com/GibreelAbdullah/RedditBot) ^|| ^Contact ^WannabeQuadrilingual ^to ^report ^any ^issue"
    comment_stream = r.subreddit('Izlam').stream.comments(pause_after=-1)
    submission_stream = r.subreddit('Izlam').stream.submissions(pause_after=-1)
    while True:
        for comment in comment_stream:
            if (comment is None):
                break
            comment_text = comment.body.lower()
            reply_comment = ""
            if comment.id not in comments_already_replied:
                # searchObj = re.search( r'\b(l+)(o+)(l+)\b', comment.body, re.I)
                if("good bot" in comment_text and comment.parent().author == r.user.me()):
                        print ("Found good bot in " + comment.id)
                        reply_comment = "Good Human. " + get_random_dua() + "\n\n"
                if("bad bot" in comment_text and comment.parent().author == r.user.me()):
                	print ("Found bad bot in " + comment.id)
                	reply_comment = reply_comment + "[Behave yourself!](https://i.ytimg.com/vi/oL15on_OyBA/hqdefault.jpg)\n\n"
                if any(takbir in comment_text for takbir in takbirList):
                    print ("Found Takbir in " + comment.id)
                    reply_comment = reply_comment + "#الله اكبر  ALLAHU AKBAR!!!!\n\n"
                if any(taqiya in comment_text for taqiya in taqiyaList) and not comment.author == r.user.me() :
                    print ("Found Taqiya in " + comment.id)
                    reply_comment = reply_comment + "This brozzer/sizter is using taqqiya, 100% true taqqiya master\n\n"
                if ("staff gorilla" in comment_text):
                    print ("Found staff gorilla in " +comment.id)
                    reply_comment = reply_comment + "[You called me?](https://imgur.com/T60vscc)\n\n"
                if any(jazakallah in comment_text for jazakallah in jazakallahList) and comment.parent().author == r.user.me():
                    print ("Found jazakallah in " + comment.id)
                    reply_comment = reply_comment + "وأنتم فجزاكم الله خيرا Wa antum, fa jazakumullahu khairan\n\n"
                if reply_comment!="":
                    print ("Replying to comment : " + comment.body)
                    print(reply_comment)
                    reply_comment = reply_comment + footer
                    comment.reply(reply_comment)
                    comments_already_replied.append(comment.id)
                    add_to_already_replied(comment.id)
        for submission in submission_stream:
            if(submission is None):
                break
            submission_text = submission.title.lower() + "------\n" + submission.selftext.lower()
            reply_comment = ""
            if submission.id not in comments_already_replied:
                if any(taqiya in submission_text for taqiya in taqiyaList):
                    print("Taqiya in Post : " + submission.id)
                    reply_comment = "Sniff, sniff... I smell Taqiya\n\n"
                if any(takbir in submission_text for takbir in takbirList):
                    print ("Found Takbir in " + submission.id)
                    reply_comment = reply_comment + "#الله اكبر  ALLAHU AKBAR!!!!\n\n"
                if ("staff gorilla" in submission_text):
                    print ("Found staff gorilla in " +submission.id)
                    reply_comment = reply_comment + "[You called me?](https://imgur.com/T60vscc)\n\n"
                if reply_comment!="":
                    print ("Replying to comment : " + submission.id)
                    print(reply_comment)
                    reply_comment = reply_comment + footer
                    submission.reply(reply_comment)
                    comments_already_replied.append(submission.id)
                    add_to_already_replied(submission.id)


def get_random_dua():
    openfile = copen("dua.txt")
    lines = openfile.count('\n') + 1
    dua = openfile.getline(randint(1,lines))
    return dua

def get_already_replied_to():
    conn = connect_to_db()         
    cur = conn.cursor()
    cur.execute("SELECT comment_id FROM already_replied")
    row = cur.fetchone()
    saved_comments = []
    while row is not None:
        # print("row : "+ row[0])
        saved_comments.append(row[0])
        row = cur.fetchone()
    cur.close()
    # print (saved_comments)
    return saved_comments

def add_to_already_replied(comment_id):
    conn = connect_to_db()         
    cur = conn.cursor()
    cur.execute("insert into already_replied (comment_id) values ('"+comment_id+"')")
    conn.commit()
    cur.close()
    
def connect_to_db():
    conn = None
    try:
        conn = psycopg2.connect(database = config.database, host = config.host, user = config.database_user, password = config.database_password)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

r = bot_login()
comments_already_replied = get_already_replied_to()
while True:
    run_bot(r,comments_already_replied)
