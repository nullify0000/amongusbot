import discord
from discord.ext import commands

# MessageEvents Settings
banned_words = [ "nigg", "cheat", "hack" ]
admins_exempt = False
ban_giftcards = True

class MessageEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message):

        # Banned words
        for banned_word in banned_words:
            if (banned_word in message.content and (not message.author.guild_permissions.administrator or not admins_exempt)):
                await message.delete()
                await message.channel.send(f'{message.author.mention}, you have been warned for using bad language. :rage:')
                print(f'{message.author.name} sent a banned word in their message ({message.content})')

        # Gift cards
        if (ban_giftcards):
            if ("discord.gift" in message.content):
                await message.delete()
                await message.channel.send(f'{message.author.mention}, please don\'t send gift cards in this channel.')
                print(f'{message.author.name} sent a gift card ({message.content})')

def setup(client):
    client.add_cog(MessageEvents(client))