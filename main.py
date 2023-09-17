import discord
import os
import asyncio
import datetime
from keep import keep_alive
from model import record_text_sentiment
from get_ranking import getRecentData, calculateUserSentiment
from dotenv import load_dotenv
load_dotenv()

class MyClient(discord.Client):
    async def send_ranking(self):
        await self.wait_until_ready()
        while not self.is_closed():
            now = datetime.datetime.now()
            if now.weekday() == 6 and now.hour == 12:
                channel = self.get_channel(int(os.getenv('CHANNELID')))
                posts = getRecentData(int(os.getenv('GUILDID')), 7)
                positive_ranking, negative_ranking = calculateUserSentiment(posts)
                text = '今週のモチベランキング\npositive\n'
                text += '\n'.join([f'> {i}. {await self.fetch_user(p[0])}' for i, p in enumerate(positive_ranking)])
                text += '\nnegative\n'
                text += '\n'.join([f'> {i}. {await self.fetch_user(n[0])}' for i, n in enumerate(negative_ranking)])
                await channel.send(text)
            if now.day == 1 and now.hour == 12:
                channel = self.get_channel(int(os.getenv('CHANNELID')))
                posts = getRecentData(int(os.getenv('GUILDID')), 30)
                positive_ranking, negative_ranking = calculateUserSentiment(posts)
                text = '今月のモチベランキング\npositive\n'
                text += '\n'.join([f'> {i}. {await self.fetch_user(p[0])}' for i, p in enumerate(positive_ranking)])
                text += '\nnegative\n'
                text += '\n'.join([f'> {i}. {await self.fetch_user(n[0])}' for i, n in enumerate(negative_ranking)])
                await channel.send(text)
            await asyncio.sleep(60*60)

    async def on_ready(self):
        print(f'ログインしました: {self.user}')
        self.loop.create_task(self.send_ranking())
        await tree.sync()

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
tree = discord.app_commands.CommandTree(client)

@tree.command(name='positive',description='userのpositive数値を返します！')
async def positive(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    userposts = getRecentData(interaction.guild.id, userid=user.id)
    posiscore = sum([i[5] for i in userposts]) / len(userposts)
    text = f'{user.display_name}のpositive度合いは: {round(posiscore*100, 1)}%です！'
    await interaction.followup.send(text, ephemeral=False)

@tree.command(name='negative',description='userのnegative数値を返します！')
async def negative(interaction: discord.Interaction, user: discord.Member):
    await interaction.response.defer()
    userposts = getRecentData(interaction.guild.id, userid=user.id)
    negascore = sum([i[7] for i in userposts]) / len(userposts)
    text = f'{user.display_name}のnegative度合いは: {round(negascore*100, 1)}%です！'
    await interaction.followup.send(text, ephemeral=False)

@tree.command(name='download_sentiment',description='このサーバー全てのネガポジをダウンロードします！')
async def download_csv(interaction: discord.Interaction):
    await interaction.response.defer()
    text = f'以下のリンクからダウンロードしてね！\nhttps://discordbot--onaoya2002.repl.co/download_csv?guildid={interaction.guild.id}'
    await interaction.followup.send(text, ephemeral=False)

keep_alive()
try:
    # client.run(os.environ['TOKEN'])
    client.run(os.getenv('TOKEN'))
except:
    os.system("kill")
