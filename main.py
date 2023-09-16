import discord
import os
from keep import keep_alive
from model import record_text_sentiment

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'ログインしました: {self.user}')

    async def on_message(self, message):
        if message.author == self.user:
            return
        negaposi = record_text_sentiment(message.guild.id, message.channel.id, message.author.id, message.content, message.created_at)
        print(f'guildid: {message.guild.id}')
        print(f'channelid: {message.channel.id}')
        print(f'userid: {message.author.id}')
        print(f'body: {message.content}')
        print(f'created_at: {message.created_at}')
        print(f'negaposi: {negaposi}')

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

# keep_alive()
# try:
#     client.run(os.environ['TOKEN'])
# except:
#     os.system("kill")

from dotenv import load_dotenv
load_dotenv()
client.run(os.getenv('TOKEN'))
