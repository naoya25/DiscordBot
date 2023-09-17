from flask import Flask, request, Response, render_template
from flask_httpauth import HTTPBasicAuth
from threading import Thread
import os
import requests
from bs4 import BeautifulSoup
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
    response = requests.get('https://forms.gle/HB5CUr9ZZJ2cwWmq7')
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')
    ogp_tags = soup.find_all('meta', attrs={'property': 'og:image'})
    ogp_image_url = ogp_tags[0]['content'] if ogp_tags else 'aaa'
    return render_template('/index.html', image=ogp_image_url)

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
