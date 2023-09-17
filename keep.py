from flask import Flask, request, Response
from threading import Thread
from get_ranking import getRecentData

app = Flask('')

@app.route('/')
def main():
    return "Bot is alive"

@app.route('/download_csv')
def download_csv():
    guildid = request.args.get('guildid')
    posts = getRecentData(guildid=guildid)
    csv_data = 'id,guildid,channelid,userid,body,positive,neutral,negative,created_at\n'
    csv_data += "\n".join([",".join(map(str, row)) for row in posts])
    return Response(
        csv_data,
        mimetype="text/csv",
        headers={"Content-disposition": "attachment; filename=data.csv"}
    )

def run():
  app.run(host='0.0.0.0', port=8080)

def keep_alive():
  server = Thread(target=run)
  server.start()
