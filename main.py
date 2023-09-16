import discord
import os
import asyncio
import datetime
from keep import keep_alive
from model import record_text_sentiment
from dotenv import load_dotenv
load_dotenv()

class MyClient(discord.Client):
    async def send_ranking(self):
        await self.wait_until_ready()
        while not self.is_closed():
            now = datetime.datetime.now()
            print(now)
            if now.weekday() == 6 and now.hour == 12:
                channel = self.get_channel(int(os.getenv('CHANNELID')))
                await channel.send('日曜日だよ〜')
            await asyncio.sleep(60*60)

    async def on_ready(self):
        print(f'ログインしました: {self.user}')
        self.loop.create_task(self.send_ranking())

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


client.run(os.getenv('TOKEN'))
