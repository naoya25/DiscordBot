from transformers import pipeline
import sqlite3


def record_text_sentiment(guildid, channelid, userid, body, created_at):
    nlp = pipeline(
        model="lxyuan/distilbert-base-multilingual-cased-sentiments-student",
        return_all_scores=True)
    negaposi_list = [nlp(body)[0][i]['score'] for i in range(3)]

    try:
        with sqlite3.connect('discord_db') as connection:
            cursor = connection.cursor()
            cursor.execute("""
                    CREATE TABLE IF NOT EXISTS Post (
                        id INTEGER PRIMARY KEY,
                        guildid INTEGER,
                        channelid INTEGER,
                        userid INTEGER,
                        body STRING,
                        positive REAL,
                        neutral REAL,
                        negative REAL,
                        created_at TIMESTAMP
                    )
                    """)

            insert_query = """
                    INSERT INTO Post (guildid, channelid, userid, body, created_at, positive, neutral, negative)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """
            cursor.execute(insert_query,
                            [guildid, channelid, userid, body, created_at] +
                            negaposi_list)
    except sqlite3.Error as e:
        print('DBのエラー: ', e)

    return negaposi_list
