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
        record_text_sentiment(message.guild.id, message.channel.id, message.author.id, message.content)

intents = discord.Intents.default()
intents.message_content = True
client = MyClient(intents=intents)

keep_alive()
try:
    client.run(os.environ['TOKEN'])
except:
    os.system("kill")
