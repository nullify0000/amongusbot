import discord
from discord.ext import commands

# ServerEvents Settings
bot_status = '.help | made by nullify'
welcome_channel_id = 754787831263526924

class ServerEvents(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status=discord.Status.dnd, activity=discord.Game(bot_status))
        print(f'[+] Updated bot status: {bot_status}')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = self.client.get_channel(welcome_channel_id)
        if channel:
            # Create embed object
            embed = discord.Embed(title=member.name, description=f'Welcome to {channel.guild.name}, \nwe hope you enjoy your stay!', color=discord.Color.green())
            embed.set_footer(text=channel.guild.name, icon_url=member.guild.icon_url)
            embed.set_thumbnail(url=member.avatar_url)
            #embed.timestamp = datetime.datetime.utcnow()

            # Send embed object
            await channel.send(embed=embed)


def setup(client):
    client.add_cog(ServerEvents(client))