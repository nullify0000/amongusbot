import discord
from discord.ext import commands

class Commands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(brief='Check bot latency, in ms.')
    async def ping(self, ctx):
        await ctx.send(f'Bot is Online and functional with {round(self.client.latency * 1000)}ms.')
        print(f'[-] {ctx.message.author.name} called ping command.')

    @commands.command(brief='Clears a certain amount of messages from current text channel.')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=10):
        if (amount <= 1000):
            await ctx.channel.purge(limit = amount + 1)
        else:
            await ctx.send("Clear between 1-1000 messages.")
        print(f'[-] {ctx.message.author.name} called clear command.')
    
    @commands.command(brief='Clears all messages from current text channel.')
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx):
        await ctx.channel.purge()
        print(f'[-] {ctx.message.author.name} called purge command.')


    @commands.command(brief='Lets people know there\'s a new lobby that\'s been created.')
    @commands.has_role("Hoster")
    async def lfg(self, ctx):

        if (not ctx.message.author.voice):
            await ctx.send("Please connect to a lobby.")
        elif ("lfg" in ctx.channel.name):
            # Create embed object
            embed = discord.Embed(title="Starting new lobby", description=f'A new lobby has been created, \nhosted in {ctx.message.author.voice.channel.name} VC')
            embed.set_footer(text=ctx.message.guild.name, icon_url="https://cdn.discordapp.com/emojis/756921237514616963.png")

            # Send embed object
            await ctx.send(embed=embed)
            await ctx.send("@here")
        else:
            await ctx.send("Wrong channel. Only post in LFG channel.")
        await ctx.message.delete()
        print(f'[-] {ctx.message.author.name} called lfg command.')

    def check_starter(ctx):
        return ctx.message.author.id in lobby_starter_ids 

    # Check for Hoster role, or lobby starter
    @commands.command(brief='Formats Among Us lobby details, and pings everyone in that lobby.', pass_context=True)
    @commands.check_any(commands.has_any_role("Hoster"), commands.check(check_starter))
    async def host(self, ctx, invite = "", region = ""):

        if (not ctx.message.author.voice):
            await ctx.send("Please connect to a lobby.")
        elif ("lobby" in ctx.channel.name):
            if (invite == "" or region == ""):
                await ctx.send( "**Incorrect command use, try using this format**\n```.host CODE REGION```")

            # Create embed object
            embed = discord.Embed(title="New Lobby", description=f'A new server has been created,\nplease join in Among Us')
            embed.set_footer(text=ctx.message.guild.name, icon_url="https://cdn.discordapp.com/emojis/756921237514616963.png")
            embed.add_field(name="Server Code",value=invite)
            embed.add_field(name="Region",value=region)

            # Send embed object
            await ctx.send(embed=embed)
            await ctx.send("@here")
        else:
            await ctx.send("Wrong channel. Only post in lobby channels.")
        await ctx.message.delete()
        print(f'[-] {ctx.message.author.name} called host command.')
    
    @commands.command(brief='Check how many users are on the server')
    async def members(self, ctx):
        await ctx.send(f'{ctx.message.guild.name} currently has **{len(ctx.message.guild.members)} members.**')
        print(f'[-] {ctx.message.author.name} called members command.')

def setup(client):
    client.add_cog(Commands(client))