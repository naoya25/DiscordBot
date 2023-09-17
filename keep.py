from flask import Flask, request, Response
from flask_httpauth import HTTPBasicAuth
from threading import Thread
import os
from get_ranking import getRecentData
from dotenv import load_dotenv
load_dotenv()

app = Flask('')
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
    if username in os.getenv('LOGINID') and password == os.getenv('LOGINPASSWORD'):
        return username

@app.route('/')
def main():
    return "Bot is alive"

@app.route('/download_csv')
@auth.login_required
def download_csv():
    guildid = request.args.get('guildid')
    posts = getRecentData(guildid=guildid)
    csv_data = 'id,guildid,channelid,userid,body,positive,neutral,negative,created_at\n'
    csv_data += "\n".join([",".join(map(str, row)) for row in posts])
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=sentiment.csv"}
    )

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()
