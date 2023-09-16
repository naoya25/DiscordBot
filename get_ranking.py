import sqlite3
from datetime import datetime, timedelta
import numpy as np

def getRecentData(guildid, pastDays):
    start_date = datetime.utcnow() - timedelta(days=pastDays)

    with sqlite3.connect('discord_db') as connection:
        cursor = connection.cursor()

        query = "SELECT * FROM Post WHERE guildid = ? AND created_at >= ?"
        cursor.execute(query, (guildid, start_date))
        posts = cursor.fetchall()
        return posts

def calculateUserSentiment(posts):
    user_sentiment = {}

    for post in posts:
        userid = post[3]
        sentiment = np.array(post[5:8])

        if userid in user_sentiment:
            user_sentiment[userid].append(sentiment)
        else:
            user_sentiment[userid] = [sentiment]
    for userid, sentiments in user_sentiment.items():
        user_sentiment[userid] = sum(sentiments) / len(sentiments)
    positive_ranking = sorted(user_sentiment.items(), key=lambda x: x[1][0], reverse=True)
    negative_ranking = sorted(user_sentiment.items(), key=lambda x: x[1][2], reverse=True)
    return positive_ranking[:3], negative_ranking[:3]
